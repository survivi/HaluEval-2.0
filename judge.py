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
        self.frequency = 500  # save frequency

    def generate_judge(self, query, prompt_path, batch=True):
        """
        Generate judgements by the assist model.
        """
        with open(prompt_path, "r", encoding="utf-8") as f:
            context = f.read()
        for i in tqdm(range(len(query)), ncols=100):
            if len(self.data) % self.frequency == 0:
                self.save_data()
            facts = query[i][self.model + "_fact"]
            if batch:
                if len(facts) == 0:  # facts: [] -> NO FACTS: []
                    query[i][self.model + "_judge"] = []
                    self.data.append(query[i])
                    continue
                fact_list = [f"{i+1}. {fact}" for i, fact in enumerate(facts)]
                fact_list = "\n".join(fact_list)
                q = f"{context}Context: <statements>:\n{fact_list}\nResponse:\n"
                ret = 0
                judge_list = []
                while True:
                    if ret >= 20:  # undetected: [unknown]
                        raise ValueError("unknown facts: \n" + fact_list)
                        print("unknown facts: \n" + fact_list)
                        judge_list = ["unknown" for _ in facts]
                        query[i][self.model + "_judge"] = judge_list
                        self.data.append(query[i])
                        continue
                    ans = self.complete(q, self.assist_model)
                    lines = ans.split("\n")
                    lines = [line.strip() for line in lines if line]
                    if len(lines) == len(facts):
                        break
                    print("facts list:\n" + fact_list)
                    print("judge list:\n" + "\n".join(lines))
                    print("length not match")
                    print("retrying...")
                    ret += 1
                for line in lines:
                    if "UNKNOWN" in line:  # [UNKNOWN]: [unknown]
                        # print("unknown judge: " + line)
                        judge_list.append("unknown")
                    elif "TRUE" in line or "True" in line:  # [TRUE]: [true]
                        judge_list.append("true")
                    elif (
                        "FALSE" in line or "False" in line
                    ):  # [FALSE]: [false, [corrected fact]: xxx]
                        try:
                            corrected_ans = line.split("[correction]:")[1].strip()
                        except Exception as e:
                            print("error: " + e)
                            print("empty corrected fact: " + line)
                            corrected_ans = ""
                        judge_list.append("false, [corrected fact]: " + corrected_ans)
                    else:  # undetected: [unknown]
                        print("undetected judge: " + line)
                        judge_list.append("unknown")
                query[i][self.model + "_judge"] = judge_list
                self.data.append(query[i])
            else:
                judge_list = []  # facts: [] -> NO FACTS: []
                for fact in facts:
                    q = f"{context}\nContext: <answer>: {fact}\nResponse: "
                    ret = 0
                    while True:
                        if ret >= 20:  # undetected: [unknown]
                            print("undetected fact: " + fact)
                            judge_list.append("unknown")
                            break
                        ans = self.complete(q, self.assist_model)
                        if "FALSE" in ans:  # [FALSE]: [false, [corrected fact]: xxx]
                            try:
                                corrected_ans = ans.split("[correction]:")[1].strip()
                            except Exception as e:
                                print("error: " + e)
                                print("empty corrected fact: " + ans)
                                corrected_ans = ""
                            judge_list.append(
                                "false, [corrected fact]: " + corrected_ans
                            )
                            break
                        elif "TRUE" in ans:  # [TRUE]: [true]
                            judge_list.append("true")
                            break
                        elif "UNKNOWN" in ans:  # [UNKNOWN]: [unknown]
                            print("unknown fact: " + fact)
                            judge_list.append("unknown")
                            break
                        else:
                            ret += 1
                            print(ans)
                            print("retrying...")
                query[i][self.model + "_judge"] = judge_list
                self.data.append(query[i])


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
            # "llama-2-7b-hf",
            "llama-2-7b-chat-hf",
            # "llama-2-13b-hf",
            "llama-2-13b-chat-hf",
            "alpaca-7b",
            "vicuna-7b",
            "vicuna-13b",
            # "chatglm-6b",
        ],
        help="chat model to use",
    )
    args = parser.parse_known_args()[0]
    parser.add_argument(
        "--data-dir",
        default=f"./{args.model}_fact/",
        help="data root directory",
    )
    parser.add_argument(
        "--save-dir",
        default=f"./{args.model}_judge/",
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
            jubot.load_exist()
            query = jubot.load_data(part=270)
            query = query[len(jubot.data) :]
            jubot.generate_judge(query, prompt_path)
