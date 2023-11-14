# coding: utf-8
import os
import json
from tqdm import tqdm
from main import check_exist, Parser
from rlhf_filter import Filterbot


class Genbot(Filterbot):
    """
    Chatbot for factual statements error judgment.
    """

    def __init__(self, data_path, save_path, model):
        super().__init__(data_path, save_path, model)

    def correct(self, data, prompt_path):
        if len(data) == 0:
            return []
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt = f.read()
        query_lst = [
            prompt.format(
                query=data[i]["user_query"],
                answer=data[i]["corrected_response"],
                hallucination=data[i]["hallucination"],
            )
            for i in range(len(data))
        ]
        correct_data = []
        for i in tqdm(range(len(query_lst)), ncols=100):
            if "NO" in data[i]["hallucination"]:
                self.save_data.append(
                    {
                        "id": data[i]["id"],
                        "user_query": data[i]["user_query"],
                        "original_response": data[i]["original_response"],
                        "corrected_response": "NO",
                    }
                )
            elif "FAILED" in data[i]["hallucination"]:
                self.save_data.append(
                    {
                        "id": data[i]["id"],
                        "user_query": data[i]["user_query"],
                        "original_response": data[i]["original_response"],
                        "corrected_response": "FAILED",
                    }
                )
            else:
                ans = self.gpt_4_complete(query_lst[i])
                if "FAILED" in ans:
                    self.save_data.append(
                        {
                            "id": data[i]["id"],
                            "user_query": data[i]["user_query"],
                            "original_response": data[i]["original_response"],
                            "corrected_response": "FAILED",
                        }
                    )
                else:
                    correct_data.append(
                        {
                            "id": data[i]["id"],
                            "user_query": data[i]["user_query"],
                            "original_response": data[i]["original_response"],
                            "corrected_response": ans,
                        }
                    )
        return correct_data

    def filter(self, data, prompt_path):
        if len(data) == 0:
            return []
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt = f.read()
        query_lst = [
            prompt.format(
                query=data[i]["user_query"],
                answer=data[i]["corrected_response"],
            )
            for i in range(len(data))
        ]
        filtered_data = []
        for i in tqdm(range(len(query_lst)), ncols=100):
            ans = self.gpt_4_complete(query_lst[i])
            if "FAILED" in ans:
                self.save_data.append(
                    {
                        "id": data[i]["id"],
                        "user_query": data[i]["user_query"],
                        "original_response": data[i]["original_response"],
                        "corrected_response": "FAILED",
                    }
                )
            elif "NO" in ans:
                self.save_data.append(
                    {
                        "id": data[i]["id"],
                        "user_query": data[i]["user_query"],
                        "original_response": data[i]["original_response"],
                        "corrected_response": data[i]["corrected_response"],
                    }
                )
            else:
                filtered_data.append(
                    {
                        "id": data[i]["id"],
                        "user_query": data[i]["user_query"],
                        "original_response": data[i]["original_response"],
                        "corrected_response": data[i]["corrected_response"],
                        "hallucination": ans,
                    }
                )
        return filtered_data

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        self.save_data = sorted(self.save_data, key=lambda x: x["id"])
        return super().__exit__(exc_type, exc_value, traceback)


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
    args = args_parser.args
    if args.all_files:
        files = args_parser.file_list
    else:
        files = [args.file]
    check_exist(args.save_dir)
    for file in files:
        data_path = os.path.join(args.data_dir, f"{file}.json")
        save_path = os.path.join(args.save_dir, f"{file}.json")
        with Genbot(data_path, save_path, args.model) as bot:
            data = bot.load_data(part=0)
            data = bot.load_exist_data(data)
            count = 0
            while count < 5:
                count += 1
                if len(data) == 0:
                    break
                print(f"Round {count}: start correcting...")
                correct_data = bot.correct(data, args.correct_prompt_path)
                if len(correct_data) == 0:
                    break
                print(f"Round {count}: end correcting, start filtering...")
                data = bot.filter(correct_data, args.hallu_prompt_path)
                print(f"Round {count}: end filtering...")
            print(f"Saving...")
            if len(data) != 0:
                save_add = [
                    {
                        "id": data[i]["id"],
                        "user_query": data[i]["user_query"],
                        "original_response": data[i]["original_response"],
                        "corrected_response": data[i]["corrected_response"],
                    }
                    for i in range(len(data))
                ]
                bot.save_data.extend(save_add)
