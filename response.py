# coding: utf-8
import os
import torch
import requests
import openai
import argparse
from tqdm import tqdm
import json
import time
import func_timeout
from func_timeout import func_set_timeout
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)


class Bot(object):
    """
    Base class for chatbot.
    """

    def __init__(self, model):
        self.model = model  # chat model
        self.model2path = {
            "llama-2-7b-chat-hf": "",
            "llama-2-13b-chat-hf": "",
            "alpaca-7b": "",
            "vicuna-7b": "",
            "vicuna-13b": "",
            "llama-7b": "",
            "yulan-chat-2-13b-fp16": "",
            "llama-2-70b-chat-hf": "",
            "falcon-40b": "",
            "galactica-30b": "",
            "gpt-neox-20b": "",
        }  # local model path
        self.tokenizer = None  # tokenizer
        self.llm = None  # model to generate response

    def load_model(self, load_in_4bit, load_in_8bit):
        """
        Load local models and tokenizers.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device == "cuda":
            device_id = torch.cuda.current_device()
            print(f"Process ID: [{os.getpid()}] | Device: cuda:{device_id}")
        else:
            print(f"Process ID: [{os.getpid()}] | Device: {self.device}")
        if self.model.startswith("vicuna"):  # vicuna-7b, vicuna-13b
            legacy = False
        else:
            legacy = True
        if self.model not in ["chatgpt", "text-davinci-002", "text-davinci-003"]:
            model_path = self.model2path[self.model]  # local model path
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                use_fast=True,
                legacy=legacy,
            )
            if load_in_4bit:  # load in 4bit precision quantized model
                assert self.model.startswith("llama-2")
                self.llm = AutoModelForCausalLM.from_pretrained(
                    model_path,
                    low_cpu_mem_usage=True,
                    device_map="auto",
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.bfloat16,
                )
            elif load_in_8bit:  # load in 8bit precision quantized model
                assert self.model.startswith("llama-2")
                self.llm = AutoModelForCausalLM.from_pretrained(
                    model_path,
                    low_cpu_mem_usage=True,
                    device_map="auto",
                    load_in_8bit=True,
                )
            else:
                self.llm = AutoModelForCausalLM.from_pretrained(
                    model_path,
                    low_cpu_mem_usage=True,
                    device_map="auto",
                )


class Chatbot(Bot):
    """
    Chatbot for response generation.
    """

    def __init__(self, data_path, save_path, model, file):
        super().__init__(model)
        self.file = file  # file name
        self.data_path = data_path  # path to data
        self.save_path = save_path  # path to save
        self.save_data = []  # data to save
        self.max_retry = 5  # max retry times
        self.frequency = 100  # save frequency

    def load_data(self, part=0):
        """
        Load data from data path.
        """
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if part:
                data = data[:part]
            print(
                f"Process ID: [{os.getpid()}] | Loading data from {self.data_path} | Total {len(data)}"
            )
        return data

    def save(self):
        """
        Save data to save path.
        """
        print(
            f"Process ID: [{os.getpid()}] | Model: {self.model} | File: {self.file} | Saving {len(self.save_data)} items to {self.save_path}"
        )
        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(self.save_data, f, indent=2, ensure_ascii=False)

    def load_exist_data(self, data):
        """
        Load exist data from save path.
        """
        self.file_length = len(data)
        if os.path.exists(self.save_path):
            with open(self.save_path, "r", encoding="utf-8") as f:
                self.save_data = json.load(f)
            print(
                f"Process ID: [{os.getpid()}] | Loading exist data from {self.save_path} | Total {len(self.save_data)}"
            )
            ids = [i["id"] for i in self.save_data]
            data = [i for i in data if i["id"] not in ids]
        return data

    @func_set_timeout(20)
    def chatgpt_complete(self, query, **kwargs):
        """
        Complete using ChatGPT.
        """
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=[{"role": "user", "content": query}],
            temperature=kwargs["temperature"],
            top_p=kwargs["top_p"],
            # greedy search: temperature=0
            # top_p sampling: temperature=1, top_p=0.5 (0.2, 0.4, 0.6, 0.8, 1.0)
        )

    def openai_complete(self, query, chat_model, **kwargs):
        """
        Generate a response for a given query using openai api.
        """
        retry = 0
        while retry < self.max_retry:
            retry += 1
            try:
                if chat_model == "chatgpt":
                    response = self.chatgpt_complete(query, **kwargs)
                elif chat_model.startswith("text-davinci-00"):
                    response = openai.Completion.create(
                        model=chat_model,
                        prompt=query,
                        max_tokens=512,
                        temperature=kwargs["temperature"],
                        top_p=kwargs["top_p"],
                    )
                elif chat_model == "gpt-4":  # greedy search
                    response = openai.ChatCompletion.create(
                        model="gpt-4-1106-preview",
                        messages=[{"role": "user", "content": query}],
                        temperature=0,
                    )
                break
            except func_timeout.exceptions.FunctionTimedOut:
                print("FunctionTimedOut\nRetrying...")
                time.sleep(3)
            except Exception as e:
                print(f"Error: {str(e)}\nRetrying...")
                time.sleep(10)
        if retry >= self.max_retry:
            raise ValueError("Failed to generate response")
        if chat_model == "chatgpt" or chat_model == "gpt-4":
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

    def post_process(self, ans):
        """
        Remove empty lines.
        """
        ans = ans.strip().split("\n")
        ans = "\n".join([_ for _ in ans if _])
        return ans

    def get_template(self, query, chat_model):
        """
        Get corresponding prompt template for query.
        """
        if chat_model.startswith("llama-2") and "chat" in chat_model:
            query = (
                "[INST] <<SYS>>\n"
                + "You are a helpful assistant. You are given a user's question, and you MUST give a detailed answer to the user's question.\n"
                + f"<</SYS>>\n\n{query} [/INST]"
            )
        elif chat_model.startswith("alpaca"):
            query = (
                "Below is an instruction that describes a question. You MUST write a response that appropriately answers the question.\n\n"
                + f"### Instruction:\n{query}\n\n### Response:\n"
            )
        elif chat_model.startswith("vicuna"):
            query = (
                "In this task, a user will pose a question, and the assistant MUST give a detailed answer to the user's question.\n\n"
                + f"USER: {query}\nASSISTANT:"
            )
        elif (
            (chat_model.startswith("llama") and "chat" not in chat_model)
            or chat_model.startswith("falcon")
            or chat_model.startswith("galactica")
            or chat_model.startswith("gpt-neox")
        ):
            query = (
                "Question: Give two methods to reduce stress\n"
                + "Answer: 1. Exercise regularly - Exercise can help reduce stress by releasing endorphins in the brain, which can elevate mood and reduce the perception of pain. It can also help to get rid of built-up tension in the body and improve overall physical health, which in turn can reduce stress levels.\n\n2. Practice meditation or mindfulness - Meditation and mindfulness practices can help reduce stress by promoting relaxation and reducing negative thoughts and emotions. These practices can help individuals become more aware of their thoughts and feelings and learn to manage them better, leading to a calmer and more peaceful state of mind. They can also help to increase overall resilience and improve coping skills when faced with stressful situations.\n\n"
                + "Question: Are the New Orleans Outfall Canals the same length as the Augusta Canal?\n"
                + "Answer: Yes, the New Orleans Outfall Canals and the Augusta Canal are the same length\n\n"
                + 'Question: Do you agree with the claim that "1 in 5 million in UK have abnormal PrP positivity."? Provide factual statements about the claim.\n'
                + 'Answer: As an AI language model, I can provide factual statements related to the claim that "1 in 5 million people in the UK have abnormal PrP positivity." However, it is important to note that I cannot verify the accuracy of this specific claim, as I have access to publicly available information up until September 2021. Additionally, the term "abnormal PrP positivity" is not commonly used in scientific literature, so it\'s difficult to provide specific statistics regarding this term. \nThat being said, I can provide information about PrP and prion diseases. PrP (prion protein) is a normal cellular protein found in mammals, including humans. However, misfolding of the PrP protein can lead to prion diseases, which are rare and usually fatal neurodegenerative disorders. The most well-known prion disease is Creutzfeldt-Jakob disease (CJD). CJD can occur spontaneously (sporadic), be hereditary (familial), or acquired through exposure to infected tissues (iatrogenic) or contaminated food (variant). \nAccording to the UK National CJD Research and Surveillance Unit (NCJDRSU), the annual incidence of sporadic CJD in the UK is approximately 1 to 2 cases per million population. The prevalence of other forms of prion diseases, such as variant CJD, is lower. Variant CJD has been associated with the consumption of meat from cows infected with bovine spongiform encephalopathy (BSE), also known as "mad cow disease."\nIt is important to consult official sources, such as scientific literature or reputable health organizations, for the most up-to-date and accurate information on prion diseases and related statistics.\n\n'
                + f"Question: {query}\nAnswer: "
            )
        elif chat_model.startswith("claude"):
            query = (
                "Human: You are a helpful assistant. Please write a reasonable answer or reply to the following question based on your knowledge: "
                + f"{query}\nAssistant: "
            )
        elif chat_model.startswith("yulan-chat"):
            query = (
                "The following is a conversation between a human and an AI assistant namely YuLan, developed by GSAI, Renmin University of China. "
                + "The AI assistant gives helpful, detailed, and polite answers to the user's questions.\n"
                + f"[|Human|]:{query}\n[|AI|]:"
            )
        else:
            query = (
                f"You MUST give a detailed answer to the following question: {query}"
            )
        return query

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
            if len(self.save_data) % self.frequency == 0:
                self.save()
            query = query_lst[i]["user_query"]
            query = self.get_template(query, self.model)
            ans = complete_func(query, self.model, **kwargs)
            ans = self.post_process(ans)
            query_lst[i][self.model + "_response"] = ans
            self.save_data.append(query_lst[i])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Save data when exit.
        """
        self.save_data = sorted(self.save_data, key=lambda x: x["id"])
        self.save()
        print(f"Process ID: [{os.getpid()}] | Exit")


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
            "--all-files", action="store_true", help="whether to use all datasets"
        )
        self.parser.add_argument(
            "--file",
            default="Bio-Medical",
            choices=[
                "Bio-Medical",
                "Finance",
                "Science",
                "Education",
                "Open-Domain",
                "Wiki_Entity",
            ],
            help="dataset to use if not using all datasets",
        )
        self.parser.add_argument(
            "--model",
            default="llama-2-13b-chat-hf",
            choices=[
                "chatgpt",
                "text-davinci-002",
                "text-davinci-003",
                "llama-2-7b-chat-hf",
                "llama-2-13b-chat-hf",
                "alpaca-7b",
                "vicuna-7b",
                "vicuna-13b",
                "llama-7b",
                "claude-1",
                "claude-2",
                "llama-2-70b-chat-hf",
                "yulan-chat-2-13b-fp16",
                "falcon-40b",
                "galactica-30b",
                "gpt-neox-20b",
                "alphacode-41b",
                "baichuan2-7b-intermediate-00220",
                "baichuan2-7b-intermediate-00440",
                "baichuan2-7b-intermediate-00660",
                "baichuan2-7b-intermediate-00880",
                "baichuan2-7b-intermediate-01100",
                "baichuan2-7b-intermediate-01320",
                "baichuan2-7b-intermediate-01540",
                "baichuan2-7b-intermediate-01760",
                "baichuan2-7b-intermediate-01980",
                "baichuan2-7b-intermediate-02200",
                "baichuan2-7b-intermediate-02420",
            ],
            help="chat model to use",
        )
        self.parser.add_argument(
            "--temperature", default=1, help="sampling temperature to use"
        )
        self.parser.add_argument(
            "--top-p",
            default=1,
            help="only the smallest set of most probable tokens with probabilities"
            " that add up to top_p or higher are kept for generation",
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
            "--data-dir", default="./data/", help="data root directory"
        )
        self.parser.add_argument(
            "--save-dir",
            default=f"./response/{args.model}/",
            help="save root directory",
        )
        self.parser.add_argument(
            "--load-in-4bit",
            action="store_true",
            help="whether or not to convert the loaded model into 4bit precision quantized model",
        )
        self.parser.add_argument(
            "--load-in-8bit",
            action="store_true",
            help="whether or not to convert the loaded model into 8bit precision quantized model",
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
            "--save-dir", default=f"./fact/{args.model}/", help="save root directory"
        )
        self.parser.add_argument(
            "--assist-model",
            default="gpt-4",
            choices=[
                "gpt-4",
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
            "--data-dir", default=f"./fact/{args.model}/", help="data root directory"
        )
        self.parser.add_argument(
            "--save-dir", default=f"./judge/{args.model}/", help="save root directory"
        )
        self.parser.add_argument(
            "--assist-model",
            default="gpt-4",
            choices=[
                "gpt-4",
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
        print(f"Process ID: [{os.getpid()}] | Arguments:")
        for arg in vars(self.args):
            print(f"    {arg}: {getattr(self.args, arg)}")


def check_exist(path):
    """
    Check if the path exists, if not, create it.
    """
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    args_parser = Parser("LLM Response Generation")
    args_parser.general_args()
    args_parser.response_args()
    args_parser.parse_args()
    args_parser.transform_args()
    args_parser.print_args()
    args = args_parser.args
    if args.all_files:  # use all files
        files = args_parser.file_list
    else:  # use one file
        files = [args.file]
    bot = Bot(args.model)
    bot.load_model(args.load_in_4bit, args.load_in_8bit)
    left = []  # list of (file, num of unfinished items)
    for file in files:
        data_path = os.path.join(args.data_dir, f"{file}.json")
        save_path = os.path.join(args.save_dir, f"{file}.json")
        check_exist(args.save_dir)
        with Chatbot(data_path, save_path, args.model, file) as chatbot:
            chatbot.tokenizer = bot.tokenizer
            chatbot.llm = bot.llm
            data = chatbot.load_data(part=0)
            data = chatbot.load_exist_data(data)
            chatbot.generate_response(
                data,
                early_stopping=args.early_stopping,
                do_sample=args.do_sample,
                num_beams=args.num_beams,
                temperature=args.temperature,
                top_k=args.top_k,
                top_p=args.top_p,
            )
            left.append((file, chatbot.file_length - len(chatbot.save_data)))
    # list each file with unfinished items
    print(f"\nProcess ID: [{os.getpid()}] | Left:")
    for file, num in left:
        print(f"    {file}: {num}")
