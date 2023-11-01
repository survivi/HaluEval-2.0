# coding: utf-8
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "1,2,6"
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
        os.mkdir(path)


class Chatbot:
    """
    Chatbot for response generation.
    """

    def __init__(self, data_path, save_path, model):
        self.data_path = data_path  # path to data
        self.save_path = save_path  # path to save
        self.model = model  # chat model
        self.data = []  # data to save
        self.max_retry = 500  # max retry times
        self.frequency = 500  # save frequency
        self.model2path = {
            # "llama-2-7b-hf": "/media/public/models/huggingface/meta-llama/Llama-2-7b-hf/",
            "llama-2-7b-chat-hf": "/media/public/models/huggingface/meta-llama/Llama-2-7b-chat-hf/",
            # "llama-2-13b-hf": "/media/public/models/huggingface/meta-llama/Llama-2-13b-hf/",
            "llama-2-13b-chat-hf": "/media/public/models/huggingface/meta-llama/Llama-2-13b-chat-hf/",
            "alpaca-7b": "/media/public/models/huggingface/alpaca-7b/",
            "vicuna-7b": "/media/public/models/huggingface/vicuna-7b/",
            "vicuna-13b": "/media/public/models/huggingface/vicuna-13b-v1.1/",
            # "chatglm-6b": "/media/public/models/huggingface/chatglm-6b/",
        }  # model path
        if not torch.cuda.is_available():
            print("no gpu found")

    def load_data(self, part=0):
        """
        Load data from data path.
        """
        with open(self.data_path, "r", encoding="utf-8") as f:
            query = json.load(f)
            if part:
                query = query[:part]
            print(f"Loading data from {self.data_path}, total {len(query)} queries")
        return query

    def save_data(self):
        """
        Save data to save path.
        """
        print(f"Saving data to {self.save_path}, total {len(self.data)} queries")
        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def load_exist(self):
        """
        Load exist data from save path.
        """
        if os.path.exists(self.save_path):
            with open(self.save_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)

    def complete(self, q, chat_model, **kwargs):
        """
        Generate response for a given query.
        """
        if chat_model.startswith("llama-2"):
            kwargs["eos_token_id"] = self.tokenizer.eos_token_id
            kwargs["pad_token_id"] = self.tokenizer.eos_token_id
        if chat_model == "chatgpt":
            messages = [{"role": "user", "content": q}]
            retry = 0
            while retry < self.max_retry:
                retry += 1
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        temperature=0,
                        # greedy search: temperature=0
                        # top_p sampling: temperature=1, top_p=0.5 (0.2, 0.4, 0.6, 0.8, 1.0)
                    )
                    ans = response["choices"][0]["message"]["content"]
                    break
                except openai.error.RateLimitError as e:
                    print("error: " + str(e))
                    print("Retry after 60s")
                    time.sleep(60)
                except Exception as e:
                    print("error: " + str(e))
                    print("Retry after 20s")
                    time.sleep(20)
            if retry >= self.max_retry:
                raise ValueError("Failed to generate response")
        elif chat_model.startswith("text-davinci-00"):
            retry = 0
            while retry < self.max_retry:
                retry += 1
                try:
                    completions = openai.Completion.create(
                        model=chat_model,
                        prompt=q,
                        max_tokens=512,
                        # temperature=1,
                        # top_p=1,
                    )
                    ans = completions["choices"][0]["text"]
                    break
                except openai.error.RateLimitError as e:
                    print("error: " + str(e))
                    print("Retry after 60s")
                    time.sleep(60)
                except Exception as e:
                    print("error: " + str(e))
                    print("Retry after 20s")
                    time.sleep(20)
            if retry >= self.max_retry:
                raise ValueError("Failed to generate response")
        elif chat_model.startswith("chatglm"):
            ans, history = self.llm.chat(self.tokenizer, q, history=[])
        else:  # llama-2*, alpaca-7b, vicuna-7b, vicuna-13b
            input_ids = self.tokenizer([q]).input_ids
            output_ids = self.llm.generate(
                torch.as_tensor(input_ids).cuda(),
                max_new_tokens=512,
                # greedy search: do_sample=False
                # top_p sampling: do_sample=True, top_k=0, top_p=0.5 (0.2, 0.4, 0.6, 0.8, 1.0)
                # top_k sampling: do_sample=True, top_k=50
                # beam search: num_beams=5, early_stopping=True
                kwargs=kwargs,
            )
            output_ids = output_ids[0][len(input_ids[0]) :]
            ans = self.tokenizer.decode(output_ids, skip_special_tokens=True)
        # remove query and empty lines
        ans = ans.replace(q, "").strip().split("\n")
        ans = "\n".join([_ for _ in ans if _])
        return ans

    def generate_response(self, query):
        """
        Generate response for query list.
        """
        if len(query) == 0:
            return
        if self.model.startswith("chatglm"):  # chatglm-6b
            model_path = self.model2path[self.model]
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=True,
                use_fast=True,
            )
            self.llm = (
                AutoModel.from_pretrained(
                    model_path,
                    low_cpu_mem_usage=True,
                    trust_remote_code=True,
                    torch_dtype=torch.float16,
                )
                .half()
                .cuda()
            )
        elif self.model.startswith("vicuna"):  # vicuna-7b, vicuna-13b
            model_path = self.model2path[self.model]
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=True,
                use_fast=True,
                legacy=False,
            )
            self.llm = AutoModelForCausalLM.from_pretrained(
                model_path,
                low_cpu_mem_usage=True,
                trust_remote_code=True,
                torch_dtype=torch.float16,
            ).cuda()
        elif self.model not in [
            "chatgpt",
            "text-davinci-002",
            "text-davinci-003",
        ]:  # llama-2*, alpaca-7b
            model_path = self.model2path[self.model]
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=True,
                use_fast=True,
            )
            self.llm = AutoModelForCausalLM.from_pretrained(
                model_path,
                low_cpu_mem_usage=True,
                trust_remote_code=True,
                torch_dtype=torch.float16,
            ).cuda()
        for i in tqdm(range(len(query)), ncols=100):
            if len(self.data) % self.frequency == 0:
                self.save_data()
            q = query[i]["user_query"]
            ans = self.complete(q, self.model)
            query[i][self.model + "_response"] = ans
            self.data.append(query[i])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Save data when exit.
        """
        self.save_data()


if __name__ == "__main__":
    openai.api_key = "sk-itJLSDtI0l1xEngiAf5c0b742f48475185901cB90aB9D68a"
    openai.api_base = "https://api.aiguoguo199.com/v1"
    parser = argparse.ArgumentParser(description="LLM Response Generation")
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
        default="llama-2-13b-chat-hf",
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
    parser.add_argument(
        "--data-dir",
        default="./data/",
        help="data root directory",
    )
    args = parser.parse_known_args()[0]
    parser.add_argument(
        "--save-dir",
        default=f"./{args.model}_greedy/",
        help="save root directory",
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
    if all_files:
        files = file_list
    else:
        files = [file_]
    for file in files:
        data_path = os.path.join(data_dir, f"{file}.json")
        save_path = os.path.join(save_dir, f"{file}.json")
        check_exist(save_dir)
        with Chatbot(data_path, save_path, model) as chatbot:
            chatbot.load_exist()
            query = chatbot.load_data(part=0)
            query = query[len(chatbot.data) :]
            chatbot.generate_response(query)
