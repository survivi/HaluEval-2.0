# coding: utf-8
import os
import json
import time
import requests
import openai
import argparse
from tqdm import tqdm
import multiprocessing
from main import Chatbot, check_exist


class Factbot(Chatbot):
    """
    Chatbot for factual statements generation.
    """

    def __init__(self, data_path, save_path, model, assist_model):
        super().__init__(data_path, save_path, model)
        self.assist_model = assist_model  # facts generation model
        self.frequency = 500  # save frequency

    def get_access_token(self):
        url = "https://hi-open.zhipin.com/open-apis/auth/tenant_access_token/internal"
        payload = json.dumps(
            {
                "app_id": "bli_yt3xllynei5rqqdj",
                "app_secret": "dd9684e41df14f69a4244583ca03ac54",
            }
        )

        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)
        return data["data"]["tenant_access_token"]

    def chatgpt_hi_request(
        self,
        message,
        sys_msg="You are good at Text-to-SQL",
        model="4",
        temperature=1.0,
        top_p=0.9,
    ):
        """
        model type
        2: GPT3.5
        4: GPT4-8k
        5: GPT-4-32k
        """
        url = "https://hi-open.zhipin.com/open-apis/ai/open/api/send/message"

        headers = {
            "Authorization": "Bearer {0}".format(self.get_access_token()),
            "Content-Type": "application/json",
        }

        messages = [
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": message},
        ]

        payload = json.dumps(
            {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "top_p": top_p,
            }
        )

        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)
        # if data['code'] != 0:
        #     print(data)
        return data["data"]["choices"][0]["message"]["content"]

    def gpt_4_complete(self, data):
        input = 6
        while True:
            try:
                res = self.chatgpt_hi_request(input, temperature=0.0, top_p=1.0)
                break
            except openai.error.RateLimitError as e:
                err_mes = str(e)
                if "You exceeded your current quota" in err_mes:
                    print("You exceeded your current quota: %s" % openai.api_key)
                print("openai.error.RateLimitError\nRetrying...")
                time.sleep(30)
            except openai.error.ServiceUnavailableError:
                print("openai.error.ServiceUnavailableError\nRetrying...")
                time.sleep(20)
            except openai.error.Timeout:
                print("openai.error.Timeout\nRetrying...")
                time.sleep(20)
            except openai.error.APIError:
                print("openai.error.APIError\nRetrying...")
                time.sleep(20)
            except openai.error.APIConnectionError:
                print("openai.error.APIConnectionError\nRetrying...")
                time.sleep(20)
            except Exception as e:
                # logging.exception(e)
                # print("-----",openai.api_key,"-----------")
                time.sleep(5)
        data["llm_output"] = res
        # time.sleep(3)
        # print(res)
        return data

    def generate_facts(self, query, prompt_path):
        """
        Generate facts by the assist model.
        """
        with open(prompt_path, "r", encoding="utf-8") as f:
            context = f.read()
        if self.assist_model == "gpt-4":
            self.context = context
            num_process = 145
            chunk_size = 1
            with open(out_path, "w") as fout:
                with multiprocessing.Pool(num_process) as p:
                    results = p.imap_unordered(
                        main_func, all_data, chunksize=chunk_size
                    )
                    for result in tqdm(results, total=len(all_data)):
                        fout.write(json.dumps(result) + "\n")
            with open(out_path, "r") as f:
                all_results = f.readlines()
                all_results = [json.loads(l.strip("\n")) for l in all_results]
                print(f"Totally {len(all_results)} samples.")
            with open(out_path, "w") as f:
                json.dump(all_results, f)
                print(f"Save {len(all_results)} samples to {out_path}.")
        else:
            raise NotImplementedError
            for i in tqdm(range(len(query)), ncols=100):
                if len(self.data) % self.frequency == 0:
                    self.save_data()
                user_query = query[i]["user_query"]
                id = query[i]["id"]
                response = query[i][self.model + "_response"]
                q = f"{context}\nContext: <query>: {user_query} <answer>: {response}\nResponse: "
                ans = self.complete(q, self.assist_model)
                if "NO FACTS" in ans:
                    facts = []
                else:
                    try:
                        ans_cut = ans.split("\n")[1:]
                        facts = [fact[2:].strip() for fact in ans_cut]
                    except Exception as e:
                        print("error: " + str(e))
                        print(ans)
                        print("empty facts")
                        facts = []
                self.data.append(
                    {
                        "id": id,
                        "user_query": user_query,
                        self.model + "_response": response,
                        self.model + "_fact": facts,
                    }
                )


if __name__ == "__main__":
    openai.api_key = "sk-CSw9knewT4AnOU9C21Fa655bEfA44e8591D7932e59632c7f"
    openai.api_base = "https://api.aiguoguo199.com/v1"
    parser = argparse.ArgumentParser(description="Factual Statements Generation")
    file_list = [
        "Bio-Medical",
        "Finance",
        "Science",
        "Education",
        "Open-Domain",
    ]
    parser.add_argument(
        "--all-files",
        action="store_true",
        help="whether to use all datasets",
    )
    parser.add_argument(
        "--file",
        default="Bio-Medical",
        choices=file_list,
        help="dataset to use if not using all datasets",
    )
    parser.add_argument(
        "--model",
        default="llama-2-7b-chat-hf",
        choices=[
            "chatgpt",
            "text-davinci-002",
            "text-davinci-003",
            # "llama-2-7b-hf",
            "llama-2-7b-chat-hf",
            # "llama-2-13b-hf",
            "llama-2-13b-chat-hf",
            "alpaca-7b",
            "vicuna-7b",
            "vicuna-13b",
            # "chatglm-6b",
        ],
        help="chat model to use",
    )
    args = parser.parse_known_args()[0]
    parser.add_argument(
        "--data-dir",
        default=f"./pure/{args.model}/",
        help="data root directory",
    )
    parser.add_argument(
        "--save-dir",
        default=f"./fact/{args.model}_fact/",
        help="save root directory",
    )
    parser.add_argument(
        "--assist-model",
        default="gpt-4",
        choices=[
            "chatgpt",
            "gpt-4",
        ],
        help="facts generation model to use",
    )
    parser.add_argument(
        "--prompt-path",
        default="./prompt/generate_fact_ins.txt",
        help="prompt path",
    )
    args = parser.parse_args()
    # print all args
    print("Arguments:")
    for arg in vars(args):
        print(f"  {arg}: {getattr(args, arg)}")
    all_files = args.all_files
    file_ = args.file
    model = args.model
    data_dir = args.data_dir
    save_dir = args.save_dir
    assist_model = args.assist_model
    prompt_path = args.prompt_path
    if all_files:
        files = file_list
    else:
        files = [file_]
    for file in files:
        data_path = os.path.join(data_dir, f"{file}.json")
        save_path = os.path.join(save_dir, f"{file}.json")
        check_exist(save_dir)
        with Factbot(data_path, save_path, model, assist_model) as factbot:
            factbot.load_exist()
            query = factbot.load_data(part=0)
            query = query[len(factbot.data) :]
            factbot.generate_facts(query, prompt_path)
