# coding: utf-8
import os
import openai
import argparse
from tqdm import tqdm
from main import Chatbot, check_exist


class Correctbot(Chatbot):
    """
    Chatbot for response correction.
    """

    def __init__(self, data_path, save_path, model, assist_model):
        super().__init__(data_path, save_path, model)
        self.assist_model = assist_model  # response correction model

    def correct_response(self, query, prompt_path):
        """
        Correct responses by the assist model.
        """
        with open(prompt_path, "r", encoding="utf-8") as f:
            context = f.read()
        for i in tqdm(range(len(query)), ncols=100):
            if len(self.data) % self.frequency == 0:
                self.save_data()
            if len(query[i]["judge"]) == 0:  # NO FACTS: [] -> None
                query[i][self.model + "_corrected_response"] = None
                self.data.append(query[i])
                continue
            # filter out [true] and [unknown]
            res_false = [
                res for res in query[i]["judge"] if res != "unknown" and res != "true"
            ]
            if len(res_false) == 0:  # all [unknown] or [true] -> ""
                query[i][self.model + "_corrected_response"] = ""
                self.data.append(query[i])
            else:  # exist [FALSE]: [false, [corrected fact]: xxx] -> [xxx]
                user_query = query[i]["user_query"]
                response = query[i][self.model + "_response"]
                sources = [res.split("[corrected fact]: ")[1] for res in res_false]
                sources = [s for s in sources if s]
                # construct verification sources
                sources = "\n".join([f"{ind+1}. {s}" for ind, s in enumerate(sources)])
                q = f"{context}\nContext: <query>: {user_query} <answer>: {response}\nFrom some verification sources,\n{sources}\nResponse: "
                ans = self.complete(q, self.assist_model)
                try:
                    ans = "\n".join(ans.split("\n")[1:])
                except Exception as e:
                    print(e)
                    print(ans)
                    ans = None
                query[i][self.model + "_corrected_response"] = ans
                self.data.append(query[i])


if __name__ == "__main__":
    openai.api_key = "sk-VQvnIStmhyz6LLVq0d178eA4Af4f4129B6E0D4643579B3A0"
    openai.api_base = "https://api.aiguoguo199.com/v1"
    parser = argparse.ArgumentParser(description="Response Correction")
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
    args = parser.parse_known_args()[0]
    parser.add_argument(
        "--data-dir",
        default=f"./temp/",
        help="data root directory",
    )
    parser.add_argument(
        "--save-dir",
        default=f"./{args.model}_correct/",
        help="save root directory",
    )
    parser.add_argument(
        "--assist-model",
        default="chatgpt",
        choices=[
            "chatgpt",
            # "gpt-4",
        ],
        help="correct model to use",
    )
    parser.add_argument(
        "--prompt-path",
        default="./prompt/correct_response_ins.txt",
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
    with Correctbot(data_path, save_path, model, assist_model) as cbot:
        cbot.load_exist()
        query = cbot.load_data(part=0)
        query = query[len(cbot.data) :]
        cbot.correct_response(query, prompt_path)
