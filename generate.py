# coding: utf-8
import os
import multiprocessing
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

    def generate_facts(self, data, prompt_path, **kwargs):
        """
        Generate facts by the assist model.
        """
        if len(data) == 0:
            return
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt = f.read()
        if self.assist_model == "gpt-4":
            user_query_lst = [data[i]["user_query"] for i in range(len(data))]
            response_lst = [data[i][self.model + "_response"] for i in range(len(data))]
            prompts = [
                prompt.format(query=user_query_lst[i], answer=response_lst[i])
                for i in range(len(data))
            ]
            for i in range(len(data)):
                data[i]["input"] = prompts[i]
            num_process = 145
            chunk_size = 1
            with multiprocessing.Pool(num_process) as p:
                results = p.imap_unordered(
                    self.gpt_4_complete, data, chunksize=chunk_size
                )
                temp = []
                for res in tqdm(results, total=len(data)):
                    ans = res["llm_output"]
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
                    temp.append(
                        {
                            "id": res["id"],
                            "user_query": res["user_query"],
                            self.model + "_response": res[self.model + "_response"],
                            self.model + "_fact": facts,
                        }
                    )
                temp = sorted(temp, key=lambda x: x["id"])
                self.save_data = temp
        else:
            raise ValueError("Not using GPT-4 as assist model")
            for i in tqdm(range(len(data)), ncols=100):
                if (len(self.save_data) + 1) % self.frequency == 0:
                    self.save()
                user_query = data[i]["user_query"]
                response = data[i][self.model + "_response"]
                query = prompt.format(query=user_query, answer=response)
                ans = self.openai_complete(query, self.assist_model, **kwargs)
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
    for file in files:
        data_path = os.path.join(args.data_dir, f"{file}.json")
        save_path = os.path.join(args.save_dir, f"{file}.json")
        check_exist(args.save_dir)
        with Factbot(data_path, save_path, args.model, args.assist_model) as factbot:
            factbot.load_exist_data()
            data = factbot.load_data(part=0)
            data = data[len(factbot.save_data) :]
            factbot.generate_facts(
                data,
                args.prompt_path,
                temperature=args.temperature,
                top_p=args.top_p,
            )
