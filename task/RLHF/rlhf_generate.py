# coding: utf-8
import os
import json
from tqdm import tqdm
from response import check_exist, Parser, Chatbot


class Genbot(Chatbot):
    def __init__(self, data_path, save_path, model, file):
        super().__init__(data_path, save_path, model, file)

    def update_data(self, d, label=0):
        idx_lst = [i["id"] for i in self.save_data]
        idx = idx_lst.index(d["id"])
        self.save_data[idx]["corrected_response"] = d["corrected_response"]
        if label:
            self.save_data[idx]["round"] = -1
        else:
            self.save_data[idx]["hallucination"] = d["hallucination"]
            self.save_data[idx]["round"] += 1

    def correct(self, d, prompt):
        q = prompt.format(
            query=d["user_query"],
            answer=d["corrected_response"],
            hallucination=d["hallucination"],
        )
        # ans = self.gpt_4_complete(q, "gpt-4")
        ans = self.openai_complete(q, "gpt-4")
        if ans == "FAILED" or ans == "TIMEOUT":
            return None
        correct_d = {
            "id": d["id"],
            "user_query": d["user_query"],
            "original_response": d["original_response"],
            "corrected_response": ans,
            "round": d["round"],
        }
        return correct_d

    def filter(self, d, prompt):
        q = prompt.format(
            query=d["user_query"],
            answer=d["corrected_response"],
        )
        # ans = self.gpt_4_complete(q, "gpt-4")
        ans = self.openai_complete(q, "gpt-4")
        if ans == "FAILED" or ans == "TIMEOUT":
            return None
        if "NO" in ans:
            print(f"Round: {d['round']} | Finish")
            self.update_data(d, label=1)
            return None
        filter_d = {
            "id": d["id"],
            "user_query": d["user_query"],
            "original_response": d["original_response"],
            "corrected_response": d["corrected_response"],
            "hallucination": ans,
            "round": d["round"],
        }
        return filter_d

    def generate_data(self, data, hallu_prompt, correct_prompt):
        for i in tqdm(range(len(data)), ncols=100):
            filter_d = data[i]
            while filter_d["round"] < 5 and filter_d["round"] != -1:
                correct_d = self.correct(filter_d, correct_prompt)
                if correct_d is None:
                    break
                filter_d = self.filter(correct_d, hallu_prompt)
                if filter_d is None:
                    break
                self.update_data(filter_d)
                filter_d["round"] += 1
                print(f"Round: {filter_d['round']} | Continue")

    def load_data(self, part=0):
        """
        Load data from data path.
        """
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            data = [i for i in data if i["hallucination"] != "NO"]
            if part:
                data = data[:part]
            print(
                f"Process ID: [{os.getpid()}] | Loading data from {self.data_path} | Total {len(data)}"
            )
        return data

    def load_exist_data(self, data):
        """
        Load exist data from save path.
        """
        if os.path.exists(self.save_path):
            with open(self.save_path, "r", encoding="utf-8") as f:
                self.save_data = json.load(f)
            print(
                f"Process ID: [{os.getpid()}] | Loading exist data from {self.save_path} | Total {len(self.save_data)}"
            )
            assert len(data) == len(self.save_data)
            data = [i for i in self.save_data if i["round"] < 5 and i["round"] != -1]
        else:
            self.save_data = data
            self.save()
        return data


if __name__ == "__main__":
    args_parser = Parser("RLHF Data Generation")
    args_parser.general_args()
    args = args_parser.parser.parse_known_args()[0]
    args_parser.parser.add_argument(
        "--data-dir",
        default=f"./filtered_data/{args.model}/",
        help="data root directory",
    )
    args_parser.parser.add_argument(
        "--save-dir",
        default=f"./save_data/{args.model}/",
        help="save root directory",
    )
    args_parser.parser.add_argument(
        "--hallu-prompt-path",
        default="./prompt/rlhf_hallu.txt",
    )
    args_parser.parser.add_argument(
        "--correct-prompt-path",
        default="./prompt/rlhf_correct.txt",
    )
    args_parser.parse_args()
    args_parser.print_args()
    args = args_parser.args
    if args.all_files:
        files = args_parser.file_list
    else:
        files = [args.file]
    with open(args.hallu_prompt_path, "r", encoding="utf-8") as f:
        hallu_prompt = f.read()
    with open(args.correct_prompt_path, "r", encoding="utf-8") as f:
        correct_prompt = f.read()
    check_exist(args.save_dir)
    left = []  # list of (file, num of unfinished items)
    for file in files:
        data_path = os.path.join(args.data_dir, f"{file}.json")
        save_path = os.path.join(args.save_dir, f"{file}.json")
        with Genbot(data_path, save_path, args.model, file) as bot:
            data = bot.load_data(part=0)
            data = bot.load_exist_data(data)
            bot.generate_data(data, hallu_prompt, correct_prompt)
            left_num = len(
                [i for i in bot.save_data if i["round"] < 5 and i["round"] != -1]
            )
            left.append((file, left_num))
    # list each file with unfinished items
    print(f"\nProcess ID: [{os.getpid()}] | Left:")
    for file, num in left:
        print(f"    {file}: {num}")
