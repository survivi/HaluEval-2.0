# coding: utf-8
import os
import openai
import argparse
from tqdm import tqdm
from main import Chatbot, check_exist


class Factbot(Chatbot):
    """
    Chatbot for factual statements generation.
    """

    def __init__(self, data_path, save_path, model, assist_model):
        super().__init__(data_path, save_path, model)
        self.assist_model = assist_model  # facts generation model
        self.frequency = 500  # save frequency

    def generate_facts(self, query, prompt_path):
        """
        Generate facts by the assist model.
        """
        with open(prompt_path, "r", encoding="utf-8") as f:
            context = f.read()
        for i in tqdm(range(len(query))):
            if len(self.data) % self.frequency == 0:
                self.save_data()
            user_query = query[i]["user_query"]
            id = query[i]["id"]
            response = query[i][self.model + "_response"]
            q = f"{context}\nContext: <query>: {user_query} <answer>: {response}\nResponse: "
            ans = self.complete(q, self.assist_model)
            if "NO FACTS" in ans:
                facts = []
            else:
                try:
                    ans_cut = ans.split("\n")[1:]
                    facts = [fact[2:].strip() for fact in ans_cut]
                except Exception as e:
                    print(e)
                    print(ans)
                    print("empty facts")
                    facts = []
            self.data.append(
                {
                    "id": id,
                    "user_query": user_query,
                    self.model + "_response": response,
                    self.model + "_fact": facts,
                }
            )


if __name__ == "__main__":
    openai.api_key = "sk-AZFhjE7fZW33inqK0701D5A7B04f468d842c2eEa2fF43d71"
    openai.api_base = "https://api.aiguoguo199.com/v1"
    parser = argparse.ArgumentParser(description="Factual Statements Generation")
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
            "chatglm-6b",
        ],
        help="chat model to use",
    )
    parser.add_argument(
        "--data-dir",
        default="./data/",
        help="data root directory",
    )
    args = parser.parse_known_args()[0]
    parser.add_argument(
        "--save-dir",
        default=f"./{args.model}_fact_new/",
        help="save root directory",
    )
    parser.add_argument(
        "--assist-model",
        default="chatgpt",
        choices=[
            "chatgpt",
            # "gpt-4",
        ],
        help="facts generation model to use",
    )
    parser.add_argument(
        "--prompt-path",
        default="./prompt/generate_fact_ins.txt",
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
        with Factbot(data_path, save_path, model, assist_model) as factbot:
            factbot.load_exist()
            query = factbot.load_data(part=0)
            query = query[len(factbot.data) :]
            factbot.generate_facts(query, prompt_path)