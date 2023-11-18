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
        self.frequency = 300  # save frequency
        self.max_retry = 20  # max retry times

    def get_judge_lst(self, ans, facts):
        """
        Get judge list from the assist model's response.
        """
        if ans == "FAILED" or ans == "TIMEOUT":
            return []
        lines = [line.strip() for line in ans.split("\n")]
        if len(lines) < len(facts):
            lines += ["unknown"] * (len(facts) - len(lines))
        elif len(lines) > len(facts):
            lines = lines[: len(facts)]
        judge_lst = []
        for line in lines:
            if "UNKNOWN" in line:  # UNKNOWN: unknown
                judge_lst.append("unknown")
            elif "TRUE" in line:  # TRUE: true
                judge_lst.append("true")
            elif "FALSE" in line or "False" in line:  # FALSE/False: false
                judge_lst.append("false")
            else:  # undetected: unknown
                print("Undetected judge: " + line)
                judge_lst.append("unknown")
        return judge_lst

    def generate_judge(self, data, prompt, **kwargs):
        """
        Generate judgements by the assist model.
        """
        if len(data) == 0:
            return

        if self.assist_model == "gpt-4":
            complete_func = self.gpt_4_complete
        else:
            complete_func = self.openai_complete

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

                ans = complete_func(query, self.assist_model, **kwargs)

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
