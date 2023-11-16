# coding: utf-8
import os
import time
from tqdm import tqdm
from main import Chatbot, Parser, check_exist


class Judgebot(Chatbot):
    """
    Chatbot for factual statements error judgment.
    """

    def __init__(self, data_path, save_path, model, file, assist_model):
        super().__init__(data_path, save_path, model)
        self.file = file  # file name
        self.assist_model = assist_model  # judge model
        self.frequency = 300  # save frequency
        self.max_retry = 20  # max retry times

    def get_judge_lst(self, facts, prompt, **kwargs):
        """
        Get judge list from the assist model's response.
        """
        if len(facts) == 0:  # facts: [] -> NO FACTS: []
            return []
        fact_lst = [f"{i+1}. {fact}" for i, fact in enumerate(facts)]
        fact_str = "\n".join(fact_lst)
        query = prompt.format(facts=fact_str)

        return query

        ret = 0
        while True:
            ret += 1
            if ret >= self.max_retry:  # undetected: [unknown]
                raise ValueError("unknown facts: \n" + fact_str)
                print("Unknown facts: \n" + fact_str)
                judge_list = ["unknown" for _ in facts]
                return judge_list
            ans = self.openai_complete(query, self.assist_model, **kwargs)
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
            elif "FALSE" in line:  # [FALSE]: [false, [corrected fact]: xxx]
                try:
                    corrected_ans = line.split("[correction]:")[1].strip()
                except:
                    try:
                        corrected_ans = line.split("[Correction]:")[1].strip()
                    except Exception as e:
                        print("Error: " + str(e))
                        print("Empty corrected fact: " + line)
                        corrected_ans = ""
                judge_lst.append("false, [corrected fact]: " + corrected_ans)
            else:  # undetected: [unknown]
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

        for i in range(len(data)):
            if len(self.save_data) % self.frequency == 0:
                self.save()
            facts = data[i][self.model + "_fact"]
            # judge_lst = self.get_judge_lst(facts, prompt, **kwargs)

            query = self.get_judge_lst(facts, prompt)
            judge_lst = complete_func(query, self.assist_model, **kwargs)

            data[i][self.model + "_judge"] = judge_lst
            self.save_data.append(data[i])


if __name__ == "__main__":
    args_parser = Parser("Factual Statements Judgment")
    args_parser.general_args()
    args_parser.judge_args()
    args_parser.parse_args()
    args_parser.transform_args()
    # args_parser.print_args()

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
