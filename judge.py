# coding: utf-8
import os
import openai
import argparse
from tqdm import tqdm
from main import Chatbot, check_exist


class Judgebot(Chatbot):
    """
    Chatbot for factual statements error judgment.
    """

    def __init__(self, data_path, save_path, model, assist_model):
        super().__init__(data_path, save_path, model)
        self.assist_model = assist_model  # judge model
        self.frequency = 1000  # save frequency
        self.max_retry = 20  # max retry times
        
    def get_judge_lst(self, facts, context):
        """
        Get judge list from the assist model's response.
        """
        if len(facts) == 0: # facts: [] -> NO FACTS: []
            return []
        fact_lst = [f"{i+1}. {fact}" for i, fact in enumerate(facts)]
        fact_str = "\n".join(fact_lst)
        query = f"{context}Context: <statements>:\n{fact_str}\nResponse:\n"
        ret = 0
        while True:
            ret += 1
            if ret >= self.max_retry:  # undetected: [unknown]
                raise ValueError("unknown facts: \n" + fact_str)
                print("Unknown facts: \n" + fact_str)
                judge_list = ["unknown" for _ in facts]
                return judge_list
            ans = self.openai_complete(query, self.assist_model)
            lines = [line.strip() for line in ans.split("\n") if line]
            if len(lines) == len(facts):
                break
            print("Facts list: " + fact_str)
            print("Judge list: " + "\n".join(lines))
            print("Length not match\nRetrying...")
        judge_lst = []
        for line in lines:
            if "UNKNOWN" in line:  # [UNKNOWN]: [unknown]
                judge_lst.append("unknown")
            elif "TRUE" in line:  # [TRUE]: [true]
                judge_lst.append("true")
            elif  "FALSE" in line:  # [FALSE]: [false, [corrected fact]: xxx]
                try:
                    corrected_ans = line.split("[correction]:")[1].strip()
                except:
                    try:
                        corrected_ans = line.split("[Correction]:")[1].strip()
                    except Exception as e:
                        print("Error: " + str(e))
                        print("Empty corrected fact: " + line)
                        corrected_ans = ""
                judge_lst.append(
                    "false, [corrected fact]: " + corrected_ans
                )
            else:  # undetected: [unknown]
                print("Undetected judge: " + line)
                judge_lst.append("unknown")
        return judge_lst
                
    def generate_judge(self, data, prompt_path):
        """
        Generate judgements by the assist model.
        """
        with open(prompt_path, "r", encoding="utf-8") as f:
            context = f.read()
        for i in tqdm(range(len(data)), ncols=100):
            if (len(self.save_data) + 1) % self.frequency == 0:
                self.save()
            facts = data[i][self.model + "_fact"]
            judge_lst = self.get_judge_lst(facts, context)
            data[i][self.model + "_judge"] = judge_lst
            self.save_data.append(data[i]) 


if __name__ == "__main__":
    openai.api_key = "sk-AZFhjE7fZW33inqK0701D5A7B04f468d842c2eEa2fF43d71"
    openai.api_base = "https://api.aiguoguo199.com/v1"
    parser = argparse.ArgumentParser(description="Factual Statements Judgment")
    file_list = [
        "Bio-Medical",
        "Finance",
        "Science",
        "Education",
        "Open-Domain",
    ]
    parser.add_argument(
        "--all-files",
        action="store_true",
        help="whether to use all datasets",
    )
    parser.add_argument(
        "--file",
        default="Bio-Medical",
        choices=file_list,
        help="dataset to use if not using all datasets",
    )
    parser.add_argument(
        "--model",
        default="llama-2-13b-chat-hf",
        choices=[
            "chatgpt",
            "text-davinci-002",
            "text-davinci-003",
            "llama-7b",
            "llama-2-7b-chat-hf",
            "llama-2-13b-chat-hf",
            "alpaca-7b",
            "vicuna-7b",
            "vicuna-13b",
            # "llama-2-7b-hf",
            # "llama-2-13b-hf",
        ],
        help="chat model to use",
    )
    args = parser.parse_known_args()[0]
    parser.add_argument(
        "--data-dir",
        default=f"./fact/{args.model}_fact/",
        help="data root directory",
    )
    parser.add_argument(
        "--save-dir",
        default=f"./judge/{args.model}_judge/",
        help="save root directory",
    )
    parser.add_argument(
        "--assist-model",
        default="chatgpt",
        choices=[
            "chatgpt",
            # "gpt-4",
        ],
        help="judge model to use",
    )
    parser.add_argument(
        "--prompt-path",
        default="./prompt/determine_truthfulness_ins.txt",
        help="prompt path",
    )
    args = parser.parse_args()
    # print all args
    print("Arguments:")
    for arg in vars(args):
        print(f"  {arg}: {getattr(args, arg)}")
    all_files = args.all_files
    file_ = args.file
    model = args.model
    data_dir = args.data_dir
    save_dir = args.save_dir
    assist_model = args.assist_model
    prompt_path = args.prompt_path
    if all_files:
        files = file_list
    else:
        files = [file_]
    for file in files:
        data_path = os.path.join(data_dir, f"{file}.json")
        save_path = os.path.join(save_dir, f"{file}.json")
        check_exist(save_dir)
        with Judgebot(data_path, save_path, model, assist_model) as jubot:
            jubot.load_exist_data()
            data = jubot.load_data(part=0)
            data = data[len(jubot.save_data) :]
            jubot.generate_judge(data, prompt_path)
