# coding: utf-8
import os
import openai
import argparse
from tqdm import tqdm
from main import Chatbot, Parser, check_exist


class Factbot(Chatbot):
    """
    Chatbot for factual statements generation.
    """

    def __init__(self, data_path, save_path, model, assist_model):
        super().__init__(data_path, save_path, model)
        self.assist_model = assist_model  # facts generation model
        self.frequency = 1000  # save frequency

    def get_facts_lst(self, ans):
        """
        Get facts list from the assist model's response.
        """
        if "NO FACTS" in ans:
            facts = []
        else:
            try:
                ans_cut = ans.split("\n")[1:]
                facts = [fact[2:].strip() for fact in ans_cut]
            except Exception as e:
                print("Error: " + str(e))
                print("Facts: " + ans)
                facts = []
        return facts

    def generate_facts(self, data, prompt_path):
        """
        Generate facts by the assist model.
        """
        with open(prompt_path, "r", encoding="utf-8") as f:
            context = f.read()
        for i in tqdm(range(len(data)), ncols=100):
            if (len(self.save_data) + 1) % self.frequency == 0:
                self.save()
            user_query = data[i]["user_query"]
            id = data[i]["id"]
            response = data[i][self.model + "_response"]
            query = f"{context}Context: <query>: {user_query} <answer>: {response}\nResponse: "
            ans = self.openai_complete(query, self.assist_model)
            ans = self.post_process(ans)
            facts = self.get_facts_lst(ans)
            data[i][self.model + "_fact"] = facts
            self.save_data.append(data[i])


if __name__ == "__main__":
    openai.api_key = "sk-AZFhjE7fZW33inqK0701D5A7B04f468d842c2eEa2fF43d71"
    openai.api_base = "https://api.aiguoguo199.com/v1"
    args_parser = Parser("Factual Statements Generation")
    args_parser.general_args()
    args_parser.fact_args()
    args = args_parser.parse_args()
    args_parser.print_args(args)
    if args.all_files:
        files = args_parser.file_list
    else:
        files = [args.file]
    for file in files:
        data_path = os.path.join(args.data_dir, f"{file}.json")
        save_path = os.path.join(args.save_dir, f"{file}.json")
        check_exist(args.save_dir)
        with Factbot(data_path, save_path, args.model, args.assist_model) as factbot:
            factbot.load_exist_data()
            data = factbot.load_data(part=0)
            data = data[len(factbot.save_data) :]
            factbot.generate_facts(data, args.prompt_path)
