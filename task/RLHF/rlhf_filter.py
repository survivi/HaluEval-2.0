# coding: utf-8
import os
from tqdm import tqdm
from response import check_exist, Parser, Chatbot


class Filterbot(Chatbot):
    def __init__(self, data_path, save_path, model, file):
        super().__init__(data_path, save_path, model, file)

    def filter(self, data, prompt):
        if len(data) == 0:
            return
        query_lst = [
            prompt.format(
                query=data[i]["user_query"],
                answer=data[i][self.model + "_response"],
            )
            for i in range(len(data))
        ]
        for i in tqdm(range(len(query_lst)), ncols=100):
            if len(self.save_data) % self.frequency == 0:
                self.save()
            ans = self.openai_complete(query_lst[i], "gpt-4")
            if ans == "FAILED" or ans == "TIMEOUT":
                continue
            if "NO" in ans:
                ans = "NO"
            self.save_data.append(
                {
                    "id": data[i]["id"],
                    "user_query": data[i]["user_query"],
                    "original_response": data[i][self.model + "_response"],
                    "corrected_response": data[i][self.model + "_response"],
                    "hallucination": ans,
                }
            )


if __name__ == "__main__":
    args_parser = Parser("RLHF Data Filtering")
    args_parser.general_args()
    args = args_parser.parser.parse_known_args()[0]
    args_parser.parser.add_argument(
        "--data-dir",
        default=f"./rlhf_data/{args.model}/",
        help="data root directory",
    )
    args_parser.parser.add_argument(
        "--save-dir",
        default=f"./filtered_data/{args.model}/",
        help="save root directory",
    )
    args_parser.parser.add_argument(
        "--hallu-prompt-path",
        default="./prompt/rlhf_hallu.txt",
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
    check_exist(args.save_dir)
    left = []  # list of (file, num of unfinished items)
    for file in files:
        data_path = os.path.join(args.data_dir, f"{file}.json")
        save_path = os.path.join(args.save_dir, f"{file}.json")
        with Filterbot(data_path, save_path, args.model, file) as bot:
            data = bot.load_data(part=0)
            data = bot.load_exist_data(data)
            bot.filter(data, hallu_prompt)
            left.append((file, bot.file_length - len(bot.save_data)))
    # list each file with unfinished items
    print(f"\nProcess ID: [{os.getpid()}] | Left:")
    for file, num in left:
        print(f"    {file}: {num}")
