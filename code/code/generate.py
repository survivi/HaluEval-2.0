# coding: utf-8
import os
from tqdm import tqdm
from main import Chatbot, Parser, check_exist


class Factbot(Chatbot):
    """
    Chatbot for factual statements generation.
    """

    def __init__(self, data_path, save_path, model, file, assist_model):
        super().__init__(data_path, save_path, model)
        self.file = file  # file name
        self.assist_model = assist_model  # facts generation model
        self.frequency = 1000  # save frequency

    def get_facts_lst(self, ans):
        """
        Get facts list from the assist model's response.
        """
        if "NO FACTS" in ans or "FAILED" in ans or "TIMEOUT" in ans:
            facts = []
        else:
            try:
                ans_cut = ans.split("\n")[1:]
                facts = [fact[2:].strip() for fact in ans_cut]
                facts = [fact for fact in facts if fact]
            except Exception as e:
                # print("Error: " + str(e))
                # print("Facts: " + ans)
                facts = []
        return facts

    def generate_facts(self, data, prompt, **kwargs):
        """
        Generate facts by the assist model.
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
            user_query = data[i]["user_query"]
            response = data[i][self.model + "_response"]
            query = prompt.format(query=user_query, answer=response)

            ans = complete_func(query, self.assist_model, **kwargs)

            data[i][self.model + "_fact_raw"] = ans

            ans = self.post_process(ans, query)
            facts = self.get_facts_lst(ans)
            data[i][self.model + "_fact"] = facts
            self.save_data.append(data[i])


if __name__ == "__main__":
    args_parser = Parser("Factual Statements Generation")
    args_parser.general_args()
    args_parser.fact_args()
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
        with Factbot(
            data_path, save_path, args.model, file, args.assist_model
        ) as factbot:
            data = factbot.load_data(part=0)
            data = factbot.load_exist_data(data)
            factbot.generate_facts(
                data,
                prompt,
                temperature=args.temperature,
                top_p=args.top_p,
            )
