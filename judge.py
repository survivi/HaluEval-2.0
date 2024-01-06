# coding: utf-8
import os
from tqdm import tqdm
from response import Chatbot, Parser, check_exist


class Judgebot(Chatbot):
    """
    Chatbot for factual statements error judgment.
    """

    def __init__(self, data_path, save_path, model, file, assist_model):
        super().__init__(data_path, save_path, model, file)
        self.file = file  # file name
        self.assist_model = assist_model  # judge model

    def get_judge_lst(self, ans, facts):
        """
        Get judge list from the assist model's response.
        """
        try:
            lines = [line.strip() for line in ans.split("\n") if line.strip()]
            if len(lines) == 0:
                print("Empty judge: " + ans)
                return []
        except Exception as e:
            print("Error: " + str(e))
            print("Corresponding judge: " + ans)
            return []
        if len(lines) < len(facts):
            lines += ["unknown"] * (len(facts) - len(lines))
        elif len(lines) > len(facts):
            lines = lines[: len(facts)]
        judge_lst = []
        for line in lines:
            line_l = line.lower()
            if "unknown" in line_l:
                judge_lst.append("unknown")
            elif "true" in line_l and "false" in line_l:
                judge_lst.append("unknown")
            elif "true" in line_l:
                judge_lst.append("true")
            elif "false" in line_l:
                judge_lst.append("false")
            else:
                print("Undetected judge: " + line)
                judge_lst.append("unknown")
        return judge_lst

    def generate_judge(self, data, prompt, **kwargs):
        """
        Generate judgements by the assist model.
        """
        if len(data) == 0:
            return
        for i in tqdm(range(len(data)), ncols=100):
            if len(self.save_data) % self.frequency == 0:
                self.save()
            facts = data[i][self.model + "_fact"]
            if len(facts) == 0:
                judge_lst = []
            else:
                query = prompt.format(
                    facts="\n".join([f"{i+1}. {fact}" for i, fact in enumerate(facts)])
                )
                ans = self.openai_complete(query, self.assist_model, **kwargs)
                if ans == "FAILED" or ans == "TIMEOUT":
                    continue
                data[i][self.model + "_judge_raw"] = ans
                ans = self.post_process(ans)
                judge_lst = self.get_judge_lst(ans, facts)
            data[i][self.model + "_judge"] = judge_lst
            self.save_data.append(data[i])


if __name__ == "__main__":
    args_parser = Parser("Factual Statements Judgment")
    args_parser.general_args()
    args_parser.judge_args()
    args_parser.parse_args()
    args_parser.transform_args()
    args_parser.print_args()

    args = args_parser.args
    if args.all_files:
        files = args_parser.file_list
    else:
        files = [args.file]
    with open(args.prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()
    left = []  # list of (file, num of unfinished items)
    for file in files:
        data_path = os.path.join(args.data_dir, f"{file}.json")
        save_path = os.path.join(args.save_dir, f"{file}.json")
        check_exist(args.save_dir)
        with Judgebot(
            data_path, save_path, args.model, file, args.assist_model
        ) as jubot:
            data = jubot.load_data(part=0)
            data = jubot.load_exist_data(data)
            jubot.generate_judge(
                data,
                prompt,
                temperature=args.temperature,
                top_p=args.top_p,
            )
            left.append((file, jubot.file_length - len(jubot.save_data)))
    # list each file with unfinished items
    print(f"\nProcess ID: [{os.getpid()}] | Left:")
    for file, num in left:
        print(f"    {file}: {num}")
