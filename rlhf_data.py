# coding: utf-8
import os
import json
import argparse
import requests
import multiprocessing
from tqdm import tqdm
from main import check_exist


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


def chatgpt_hi_request(
    message,
    # sys_msg="You are good at Text-to-SQL",
    model="4",
    # temperature=1.0,
    # top_p=0.9,
):
    """
    model type
    2: GPT3.5
    4: GPT4-8k
    5: GPT-4-32k
    """
    url = "https://hi-open.zhipin.com/open-apis/ai/open/api/send/message"
    headers = {
        "Authorization": "Bearer {0}".format(get_access_token()),
        "Content-Type": "application/json",
    }
    messages = [
        # {"role": "system", "content": sys_msg},
        {"role": "user", "content": message},
    ]
    payload = json.dumps(
        {
            "model": model,
            "messages": messages,
            # "temperature": temperature,
            # "top_p": top_p,
        }
    )
    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    # if data['code'] != 0:
    #     print(data)
    return data["data"]["choices"][0]["message"]["content"]


def gpt_4_complete(query):
    input = query["input"]
    count = 0
    while True:
        if count > 20:
            res = "NO"
            break
        try:
            res = chatgpt_hi_request(input)
            break
        except Exception as e:
            print("Exception: %s\nRetrying..." % e)
            count += 1
    query["llm_output"] = res
    return query


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser(description="RLHF Data Generation")
    args_parser.add_argument(
        "--model",
        default="alpaca-7b",
        choices=[
            "alpaca-7b",
            "vicuna-7b",
            "vicuna-13b",
        ],
    )
    args_parser.add_argument(
        "--data-dir",
        default="./rlhf_data/",
        help="data root directory",
    )
    args_parser.add_argument(
        "--save-dir",
        default="./rlhf/",
        help="save root directory",
    )
    args_parser.add_argument(
        "--hallu-prompt-path",
        default="./prompt/rlhf_hallu.txt",
    )
    args_parser.add_argument(
        "--correct-prompt-path",
        default="./prompt/rlhf_correct.txt",
    )
    args = args_parser.parse_args()
    data_dir = os.path.join(args.data_dir, args.model)
    with open(args.hallu_prompt_path, "r", encoding="utf-8") as f:
        hallu_prompt = f.read()
    with open(args.correct_prompt_path, "r", encoding="utf-8") as f:
        correct_prompt = f.read()
    check_exist(args.save_dir)
    file_list = [
        "Bio-Medical",
        "Finance",
        "Science",
        "Education",
        "Open-Domain",
    ]
    num_process = 145
    chunk_size = 1
    for file in file_list:
        print("Processing file: " + file)
        save_data = []
        data_path = os.path.join(data_dir, file + ".json")
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        prompts = [
            hallu_prompt.format(
                query=data[i]["user_query"], answer=data[i][args.model + "_response"]
            )
            for i in range(len(data))
        ]
        for i in range(len(data)):
            data[i]["input"] = prompts[i]
        res_lst = []
        with multiprocessing.Pool(num_process) as p:
            results = p.imap_unordered(gpt_4_complete, data, chunksize=chunk_size)
            for res in tqdm(results, total=len(data)):
                res_lst.append(
                    {
                        "id": res["id"],
                        "user_query": res["user_query"],
                        "original_response": res[args.model + "_response"],
                        "corrected_response": res[args.model + "_response"],
                        "hallucination": res["llm_output"],
                    }
                )
            res_lst = sorted(res_lst, key=lambda x: x["id"])
        filtered_res_lst = [i for i in res_lst if "NO" not in i["hallucination"]]
        count = 0
        while count < 5:
            if len(filtered_res_lst) == 0:
                break
            prompts = [
                correct_prompt.format(
                    query=filtered_res_lst[i]["user_query"],
                    answer=filtered_res_lst[i]["corrected_response"],
                    hallucination=filtered_res_lst[i]["hallucination"],
                )
                for i in range(len(filtered_res_lst))
            ]
            for i in range(len(filtered_res_lst)):
                filtered_res_lst[i]["input"] = prompts[i]
            res_lst = []
            with multiprocessing.Pool(num_process) as p:
                results = p.imap_unordered(
                    gpt_4_complete, filtered_res_lst, chunksize=chunk_size
                )
                for res in tqdm(results, total=len(filtered_res_lst)):
                    res_lst.append(
                        {
                            "id": res["id"],
                            "user_query": res["user_query"],
                            "original_response": res["original_response"],
                            "corrected_response": res["llm_output"],
                        }
                    )
                res_lst = sorted(res_lst, key=lambda x: x["id"])
            prompts = [
                hallu_prompt.format(
                    query=res_lst[i]["user_query"],
                    answer=res_lst[i]["corrected_response"],
                )
                for i in range(len(res_lst))
            ]
            for i in range(len(res_lst)):
                res_lst[i]["input"] = prompts[i]
            check_lst = []
            with multiprocessing.Pool(num_process) as p:
                results = p.imap_unordered(
                    gpt_4_complete, res_lst, chunksize=chunk_size
                )
                for res in tqdm(results, total=len(res_lst)):
                    check_lst.append(
                        {
                            "id": res["id"],
                            "user_query": res["user_query"],
                            "original_response": res["original_response"],
                            "corrected_response": res["corrected_response"],
                            "hallucination": res["llm_output"],
                        }
                    )
                check_lst = sorted(check_lst, key=lambda x: x["id"])
            save_lst = [
                {
                    "id": i["id"],
                    "user_query": i["user_query"],
                    "original_response": i["original_response"],
                    "corrected_response": i["corrected_response"],
                }
                for i in check_lst
                if "NO" in i["hallucination"]
            ]
            save_data.extend(save_lst)
            filtered_res_lst = [i for i in check_lst if "NO" not in i["hallucination"]]
            count += 1
        if len(filtered_res_lst) != 0:
            save_lst = [
                {
                    "id": i["id"],
                    "user_query": i["user_query"],
                    "original_response": i["original_response"],
                    "corrected_response": i["corrected_response"],
                }
                for i in filtered_res_lst
            ]
            save_data.extend(save_lst)
        save_data = sorted(save_data, key=lambda x: x["id"])
        save_path = os.path.join(args.save_dir, file + ".json")
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
