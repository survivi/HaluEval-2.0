# coding: utf-8
import os
import torch
import openai
import argparse
from tqdm import tqdm
import json
import time
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    AutoModel,
)


def check_exist(path):
    """
    Check if the path exists, if not, create it.
    """
    if not os.path.exists(path):
        os.makedirs(path)


class Bot(object):
    """
    Base class for chatbot.
    """

    def __init__(self, model):
        self.model = model  # chat model
        self.model2path = {
            "llama-7b": "/media/public/models/huggingface/llama-7b/",
            "llama-2-7b-chat-hf": "/media/public/models/huggingface/meta-llama/Llama-2-7b-chat-hf/",
            "llama-2-13b-chat-hf": "/media/public/models/huggingface/meta-llama/Llama-2-13b-chat-hf/",
            "alpaca-7b": "/media/public/models/huggingface/alpaca-7b/",
            "vicuna-7b": "/media/public/models/huggingface/vicuna-7b/",
            "vicuna-13b": "/media/public/models/huggingface/vicuna-13b-v1.1/",
            # "llama-2-7b-hf": "/media/public/models/huggingface/meta-llama/Llama-2-7b-hf/",
            # "llama-2-13b-hf": "/media/public/models/huggingface/meta-llama/Llama-2-13b-hf/",
        }  # local model path

    def load_model(self):
        """
        Load local models and tokenizers.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device == "cuda":
            device_id = torch.cuda.current_device()
            print(f"device: cuda:{device_id}")
        else:
            print(f"device: {self.device}")
        if self.model.startswith("vicuna"):  # vicuna-7b, vicuna-13b
            legacy = False
        else:
            legacy = True
        if self.model not in [
            "chatgpt",
            "text-davinci-002",
            "text-davinci-003",
        ]:
            model_path = self.model2path[self.model]
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=True,
                use_fast=True,
                legacy=legacy,
            )
            self.llm = AutoModelForCausalLM.from_pretrained(
                model_path,
                low_cpu_mem_usage=True,
                trust_remote_code=True,
                torch_dtype=torch.float16,
            ).cuda()
        else:
            self.tokenizer = None
            self.llm = None


class Chatbot(Bot):
    """
    Chatbot for response generation.
    """

    def __init__(self, data_path, save_path, model):
        super().__init__(model)
        self.data_path = data_path  # path to data
        self.save_path = save_path  # path to save
        self.save_data = []  # data to save
        self.max_retry = 500  # max retry times
        self.frequency = 1000  # save frequency

    def load_data(self, part=0):
        """
        Load data from data path.
        """
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if part:
                data = data[:part]
            print(f"Loading data from {self.data_path}, total {len(data)}")
        return data

    def save(self):
        """
        Save data to save path.
        """
        print(f"Saving data to {self.save_path}, total {len(self.save_data)}")
        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(self.save_data, f, indent=2, ensure_ascii=False)

    def load_exist_data(self):
        """
        Load exist data from save path.
        """
        if os.path.exists(self.save_path):
            print(f"Loading exist data from {self.save_path}")
            with open(self.save_path, "r", encoding="utf-8") as f:
                self.save_data = json.load(f)

    def openai_complete(self, query, chat_model, **kwargs):
        """
        Generate a response for a given query using openai api.
        """
        retry = 0
        while retry < self.max_retry:
            retry += 1
            try:
                if chat_model == "chatgpt":
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": query}],
                        temperature=kwargs["temperature"],
                        top_p=kwargs["top_p"],
                        # greedy search: temperature=0
                        # top_p sampling: temperature=1, top_p=0.5 (0.2, 0.4, 0.6, 0.8, 1.0)
                    )
                elif chat_model.startswith("text-davinci-00"):
                    response = openai.Completion.create(
                        model=chat_model,
                        prompt=query,
                        max_tokens=512,
                        temperature=kwargs["temperature"],
                        top_p=kwargs["top_p"],
                    )
                break
            except openai.error.AuthenticationError as e:
                print("openai.error.AuthenticationError\nRetrying...")
                if "The token quota has been used up" in str(e):
                    print("You exceeded your current quota: %s" % openai.api_key)
                time.sleep(60)
            except openai.error.RateLimitError as e:
                print("openai.error.RateLimitError\nRetrying...")
                time.sleep(60)
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
                print(f"Error: {str(e)}\nRetrying...")
                time.sleep(10)
        if retry >= self.max_retry:
            raise ValueError("Failed to generate response")
        if chat_model == "chatgpt":
            ans = response["choices"][0]["message"]["content"]
        elif chat_model.startswith("text-davinci-00"):
            ans = response["choices"][0]["text"]
        return ans

    def complete(self, query, chat_model, **kwargs):
        """
        Generate a response for a given query using local models.
        """
        input_ids = self.tokenizer([query]).input_ids
        output_ids = self.llm.generate(
            torch.as_tensor(input_ids).cuda(),
            max_new_tokens=512,
            do_sample=kwargs["do_sample"],
            top_k=kwargs["top_k"],
            top_p=kwargs["top_p"],
            temperature=kwargs["temperature"],
            num_beams=kwargs["num_beams"],
            early_stopping=kwargs["early_stopping"],
            # greedy search: do_sample=False
            # top_p sampling: do_sample=True, top_k=0, top_p=0.5 (0.2, 0.4, 0.6, 0.8, 1.0)
            # top_k sampling: do_sample=True, top_k=50
            # beam search: num_beams=5, early_stopping=True
        )
        output_ids = output_ids[0][len(input_ids[0]) :]
        ans = self.tokenizer.decode(output_ids, skip_special_tokens=True)
        return ans

    def post_process(self, ans, query):
        """
        Remove query and empty lines.
        """
        ans = ans.replace(query, "").strip().split("\n")
        ans = "\n".join([_ for _ in ans if _])
        return ans

    def generate_response(self, query_lst, **kwargs):
        """
        Generate response for query list.
        """
        if len(query_lst) == 0:
            return
        if self.model.startswith("chatgpt") or self.model.startswith("text-davinci-00"):
            complete_func = self.openai_complete
        else:
            complete_func = self.complete
        if self.model.startswith("llama-2"):
            kwargs["eos_token_id"] = self.tokenizer.eos_token_id
            kwargs["pad_token_id"] = self.tokenizer.eos_token_id
        for i in tqdm(range(len(query_lst)), ncols=100):
            if (len(self.save_data) + 1) % self.frequency == 0:
                self.save()
            query = query_lst[i]["user_query"]
            ans = complete_func(query, self.model, **kwargs)
            ans = self.post_process(ans, query)
            query_lst[i][self.model + "_response"] = ans
            self.save_data.append(query_lst[i])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Save data when exit.
        """
        self.save()


class Parser(object):
    """
    Parser for arguments.
    """

    def __init__(self, description):
        self.parser = argparse.ArgumentParser(description=description)
        self.file_list = [
            "Bio-Medical",
            "Finance",
            "Science",
            "Education",
            "Open-Domain",
        ]

    def general_args(self):
        """
        Parse arguments for all tasks.
        """
        self.parser.add_argument(
            "--all-files",
            action="store_true",
            help="whether to use all datasets",
        )
        self.parser.add_argument(
            "--file",
            default="Bio-Medical",
            choices=["Bio-Medical", "Finance", "Science", "Education", "Open-Domain"],
            help="dataset to use if not using all datasets",
        )
        self.parser.add_argument(
            "--model",
            default="llama-2-13b-chat-hf",
            choices=[
                "chatgpt",
                "text-davinci-002",
                "text-davinci-003",
                "llama-7b",
                "llama-2-7b-chat-hf",
                "llama-2-13b-chat-hf",
                "alpaca-7b",
                "vicuna-7b",
                "vicuna-13b",
                "claude-2",
                # "llama-2-7b-hf",
                # "llama-2-13b-hf",
            ],
            help="chat model to use",
        )
        self.parser.add_argument(
            "--temperature",
            default=1,
            help="sampling temperature to use",
        )
        self.parser.add_argument(
            "--top-p",
            default=1,
            help="only the smallest set of most probable tokens with probabilities\
                that add up to top_p or higher are kept for generation",
        )
        self.parser.add_argument(
            "--early-stopping",
            action="store_true",
            help="the stopping condition for beam-based methods, like beam-search",
        )
        self.parser.add_argument(
            "--do-sample",
            action="store_true",
            help="whether or not to use sampling, use greedy decoding otherwise",
        )
        self.parser.add_argument(
            "--num-beams",
            default=1,
            help="number of beams for beam search. 1 means no beam search",
        )
        self.parser.add_argument(
            "--top-k",
            default=50,
            help="the number of highest probability vocabulary tokens to keep for top-k-filtering",
        )

    def response_args(self):
        """
        Parse arguments for response generation.
        """
        args = self.parser.parse_known_args()[0]
        self.parser.add_argument(
            "--data-dir",
            default="./data/",
            help="data root directory",
        )
        self.parser.add_argument(
            "--save-dir",
            default=f"./response/{args.model}/",
            help="save root directory",
        )

    def fact_args(self):
        """
        Parse arguments for factual statements generation.
        """
        args = self.parser.parse_known_args()[0]
        self.parser.add_argument(
            "--data-dir",
            default=f"./response/{args.model}/",
            help="data root directory",
        )
        self.parser.add_argument(
            "--save-dir",
            default=f"./fact/{args.model}/",
            help="save root directory",
        )
        self.parser.add_argument(
            "--assist-model",
            default="chatgpt",
            choices=[
                "chatgpt",
                # "gpt-4",
            ],
            help="facts generation model to use",
        )
        self.parser.add_argument(
            "--prompt-path",
            default="./prompt/generate_fact_ins.txt",
            help="prompt path",
        )

    def judge_args(self):
        """
        Parse arguments for factual statements judgment.
        """
        args = self.parser.parse_known_args()[0]
        self.parser.add_argument(
            "--data-dir",
            default=f"./fact/{args.model}/",
            help="data root directory",
        )
        self.parser.add_argument(
            "--save-dir",
            default=f"./judge/{args.model}/",
            help="save root directory",
        )
        self.parser.add_argument(
            "--assist-model",
            default="chatgpt",
            choices=[
                "chatgpt",
                # "gpt-4",
            ],
            help="judge model to use",
        )
        self.parser.add_argument(
            "--prompt-path",
            default="./prompt/determine_truthfulness_ins.txt",
            help="prompt path",
        )

    def parse_args(self):
        """
        Parse all arguments.
        """
        self.args = self.parser.parse_args()

    def transform_args(self):
        """
        Transform some arguments to the correct type.
        """
        self.args.num_beams = int(self.args.num_beams)
        self.args.temperature = float(self.args.temperature)
        self.args.top_k = int(self.args.top_k)
        self.args.top_p = float(self.args.top_p)

    def print_args(self):
        """
        Print all arguments.
        """
        print("Arguments:")
        for arg in vars(self.args):
            print(f"  {arg}: {getattr(self.args, arg)}")


if __name__ == "__main__":
    args_parser = Parser("LLM Response Generation")
    args_parser.general_args()
    args_parser.response_args()
    args_parser.parse_args()
    args_parser.transform_args()
    args_parser.print_args()
    args = args_parser.args
    if args.all_files:
        files = args_parser.file_list
    else:
        files = [args.file]
    bot = Bot(args.model)
    bot.load_model()
    for file in files:
        data_path = os.path.join(args.data_dir, f"{file}.json")
        save_path = os.path.join(args.save_dir, f"{file}.json")
        check_exist(args.save_dir)
        with Chatbot(data_path, save_path, args.model) as chatbot:
            chatbot.tokenizer = bot.tokenizer
            chatbot.llm = bot.llm
            chatbot.load_exist_data()
            data = chatbot.load_data(part=0)
            data = data[len(chatbot.save_data) :]
            chatbot.generate_response(
                data,
                early_stopping=args.early_stopping,
                do_sample=args.do_sample,
                num_beams=args.num_beams,
                temperature=args.temperature,
                top_k=args.top_k,
                top_p=args.top_p,
            )
