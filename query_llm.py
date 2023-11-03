import json
import os
import time
from tqdm import tqdm
import random
import logging
import argparse
import multiprocessing
import openai
from tqdm import tqdm
import sys
import time
import requests
import pandas as pd
import numpy as np


def main_func(data):
    input = data["input"]
    # print(input)
    while True:
        try:
            res = chatgpt_hi_request(input, temperature=0.0, top_p=1.0)
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


def get_access_token():
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


# 调用模型类型 2：GPT3.5；4：GPT4-8k；5：GPT-4-32k
def chatgpt_hi_request(
    message,
    sys_msg="You are good at Text-to-SQL",
    model="4",
    temperature=1.0,
    top_p=0.9,
):
    url = "https://hi-open.zhipin.com/open-apis/ai/open/api/send/message"

    headers = {
        "Authorization": "Bearer {0}".format(get_access_token()),
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


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inp_path", required=True, type=str)
    parser.add_argument("--out_path", required=True, type=str)
    # parser.add_argument('--api_key', required=True, type=str)
    # parser.add_argument('--prompt', required=True, type=str)
    # parser.add_argument('--model_name', required=True, type=str)
    # parser.add_argument('--sample_path', type=str)
    # parser.add_argument('--dem_k', type=int)
    # parser.add_argument('--batch_size', type=int)
    # parser.add_argument('--num_process', type=int)
    # parser.add_argument('--debug', action="store_true")
    # parser.add_argument('--icl', action="store_true")
    # parser.add_argument('--overwrite', action="store_true")

    args = parser.parse_args()

    print("Starting convert generated sql to description")
    return args


if __name__ == "__main__":
    # python query_llm_kbqa.py --model_name chatgpt --inp_path ./data/webqsp/LLM4KG/webqsp_simple_test.jsonl --oup_path ./data/webqsp/LLM4KG/webqsp_test_gpt_pred.jsonl --sample_path ./data/webqsp/LLM4KG/webqsp_simple_train.jsonl --batch_size 10 --debug
    args = _parse_args()

    inp_path = args.inp_path
    out_path = args.out_path
    with open(inp_path, "r") as f:
        all_data = json.load(f)
        print("Totally load %d data." % len(all_data))

    # if not args.overwrite and os.path.exists(out_path):
    #     with open(out_path, "r") as f:
    #         processed_samples = f.readlines()
    #         processed_samples = [json.loads(sample) for sample in processed_samples]
    #         processed_ids = [sample["qid"] for sample in processed_samples]
    #         print("Load %d processed samples" % len(processed_ids))

    # if args.debug:
    #     main_func(0, inp_path, out_path)
    # else:
    #     p = mp.Pool(num_process)
    #     for idx in range(num_process):
    #         p.apply_async(main_func, args=(idx, inp_path, out_path))
    #     p.close()
    #     p.join()
    #     print("All of the child processes over!")
    num_process = 145
    chunk_size = 1
    with open(out_path, "w") as fout:
        with multiprocessing.Pool(num_process) as p:
            results = p.imap_unordered(main_func, all_data, chunksize=chunk_size)
            for result in tqdm(results, total=len(all_data)):
                fout.write(json.dumps(result) + "\n")
    with open(out_path, "r") as f:
        all_results = f.readlines()
        all_results = [json.loads(l.strip("\n")) for l in all_results]
        print(f"Totally {len(all_results)} samples.")
    with open(out_path, "w") as f:
        json.dump(all_results, f)
        print(f"Save {len(all_results)} samples to {out_path}.")
