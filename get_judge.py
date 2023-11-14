import json
import os
from main import check_exist

data_path = "./all_data/add_judge/"
save_path = "./all_data/update_add_judge/"
for path in os.listdir(data_path):
    # if path != "chatgpt_judge":
    #     continue
    for model in [
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
        "llama-2-7b-hf",
        "llama-2-13b-hf",
        "bloom-7b1",
    ]:
        if path.startswith(model):
            model_name = model
            break
    check_exist(os.path.join(save_path, path))
    for i in os.listdir(os.path.join(data_path, path)):
        p = os.path.join(data_path, path, i)
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            for index in range(len(data)):
                facts_lst = data[index][model_name + "_fact"]
                if len(facts_lst) == 0:
                    data[index][model_name + "_judge"] = []
                    continue
                ans = data[index][model_name + "_judge"]
                if ans == "NO FACTS":
                    data[index][model_name + "_judge"] = [
                        f"unknown" for _ in range(len(facts_lst))
                    ]
                    continue
                lines = [line.strip() for line in ans.split("\n") if line]
                if len(lines) != len(facts_lst):
                    print("File: " + p)
                    print("ID: " + str(data[index]["id"]))
                    print("Facts list: " + "\n".join(facts_lst))
                    print("Judge list: " + "\n".join(lines))
                    exit()
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
                                print("File: " + p)
                                print("ID: " + str(data[index]["id"]))
                                print("Error: " + str(e))
                                print("Empty corrected fact: " + line)
                                corrected_ans = ""
                                exit()
                        judge_lst.append("false, [corrected fact]: " + corrected_ans)
                    else:  # undetected: [unknown]
                        print("File: " + p)
                        print("ID: " + str(data[index]["id"]))
                        print("Undetected judge: " + line)
                        judge_lst.append("unknown")
                        exit()
                data[index][model_name + "_judge"] = judge_lst
        with open(os.path.join(save_path, path, i), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
