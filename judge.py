# coding: utf-8
import os
import openai
import argparse
from tqdm import tqdm
from main import Chatbot, Parser, check_exist


class Judgebot(Chatbot):
    """
    Chatbot for factual statements error judgment.
    """

    def __init__(self, data_path, save_path, model, assist_model):
        super().__init__(data_path, save_path, model)
        self.assist_model = assist_model  # judge model
        self.frequency = 1000  # save frequency
        self.max_retry = 20  # max retry times

    def get_judge_lst(self, facts, context, **kwargs):
        """
        Get judge list from the assist model's response.
        """
        if len(facts) == 0:  # facts: [] -> NO FACTS: []
            return []
        fact_lst = [f"{i+1}. {fact}" for i, fact in enumerate(facts)]
        fact_str = "\n".join(fact_lst)
        query = f"{context}Context: <statements>:\n{fact_str}\nResponse:\n"
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

    def generate_judge(self, data, prompt_path, **kwargs):
        """
        Generate judgements by the assist model.
        """
        with open(prompt_path, "r", encoding="utf-8") as f:
            context = f.read()
        for i in tqdm(range(len(data)), ncols=100):
            if (len(self.save_data) + 1) % self.frequency == 0:
                self.save()
            facts = data[i][self.model + "_fact"]
            judge_lst = self.get_judge_lst(facts, context, **kwargs)
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
    for file in files:
        data_path = os.path.join(args.data_dir, f"{file}.json")
        save_path = os.path.join(args.save_dir, f"{file}.json")
        check_exist(args.save_dir)
        with Judgebot(data_path, save_path, args.model, args.assist_model) as jubot:
            jubot.load_exist_data()
            data = jubot.load_data(part=0)
            data = data[len(jubot.save_data) :]
            jubot.generate_judge(
                data,
                args.prompt_path,
                temperature=args.temperature,
                top_p=args.top_p,
            )
