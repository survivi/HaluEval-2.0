# coding: utf-8
import os
from response import check_exist, Parser, Chatbot


class Genbot(Chatbot):
    def __init__(self, data_path, save_path, model, file):
        super().__init__(data_path, save_path, model, file)

    def append_data(self, d, ans, label="0"):
        self.save_data.append(
            {
                "id": d["id"],
                "user_query": d["user_query"],
                "original_response": d["original_response"],
                "corrected_response": ans,
                "label": label,
            }
        )

    def correct(self, d, prompt):
        correct_d = None
        if d["hallucination"] == "NO":
            self.append_data(d, "NO", label="-2")
        elif d["hallucination"] == "FAILED":
            self.append_data(d, "FAILED", label="-1")
        elif d["hallucination"] == "TIMEOUT":
            self.append_data(d, "TIMEOUT", label="-1")
        else:
            q = prompt.format(
                query=d["user_query"],
                answer=d["corrected_response"],
                hallucination=d["hallucination"],
            )
            ans = self.gpt_4_complete(q, "gpt-4")
            if ans == "FAILED":
                self.append_data(d, "FAILED", label="-1")
            elif ans == "TIMEOUT":
                self.append_data(d, "TIMEOUT", label="-1")
            else:
                correct_d = {
                    "id": d["id"],
                    "user_query": d["user_query"],
                    "original_response": d["original_response"],
                    "corrected_response": ans,
                }
        return correct_d

    def filter(self, d, prompt):
        q = prompt.format(
            query=d["user_query"],
            answer=d["corrected_response"],
        )
        filter_d = None
        ans = self.gpt_4_complete(q)
        if ans == "FAILED":
            self.append_data(d, "FAILED", label="-1")
        elif ans == "TIMEOUT":
            self.append_data(d, "TIMEOUT", label="-1")
        elif "NO" in ans:
            self.append_data(d, d["corrected_response"])
        else:
            filter_d = {
                "id": d["id"],
                "user_query": d["user_query"],
                "original_response": d["original_response"],
                "corrected_response": d["corrected_response"],
                "hallucination": ans,
            }
        return filter_d

    def generate_data(self, data, hallu_prompt, correct_prompt):
        for i in range(len(data)):
            if len(self.save_data) % self.frequency == 0:
                self.save()
            count = 0
            filter_d = data[i]
            while count < 5:
                count += 1
                correct_d = self.correct(filter_d, correct_prompt)
                if correct_d is None:
                    break
                filter_d = self.filter(correct_d, hallu_prompt)
                if filter_d is None:
                    break
            if filter_d is not None and correct_d is not None:
                self.append_data(filter_d, filter_d["corrected_response"], label="1")


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
    for file in files:
        data_path = os.path.join(args.data_dir, f"{file}.json")
        save_path = os.path.join(args.save_dir, f"{file}.json")
        with Genbot(data_path, save_path, args.model, file) as bot:
            data = bot.load_data(part=0)
            data = bot.load_exist_data(data)
            bot.generate_data(data, hallu_prompt, correct_prompt)
