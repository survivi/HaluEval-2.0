import json
import os
from main import check_exist

data_path = "./judge/"
save_path = "./judge_up/"
for path in os.listdir(data_path):
    if path != "chatgpt_judge":
        continue
    check_exist(os.path.join(save_path, path))
    for i in os.listdir(os.path.join(data_path, path)):
        p = os.path.join(data_path, path, i)
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            for index in range(len(data)):
                # facts_lst = data[index][path.split("_jud")[0] + "_fact"]
                facts_lst = data[index]["llama-7b_fact"]
                if len(facts_lst) == 0:
                    data[index]["llama-7b_judge"] = []
                    continue
                ans = data[index]["llama-7b_judge"]
                lines = [line.strip() for line in ans.split("\n") if line]
                if len(lines) != len(facts_lst):
                    print("file: " + p)
                    print("id: " + str(data[index]["id"]))
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
                                print("file: " + p)
                                print("id: " + str(data[index]["id"]))
                                print("Error: " + str(e))
                                print("Empty corrected fact: " + line)
                                corrected_ans = ""
                                exit()
                        judge_lst.append("false, [corrected fact]: " + corrected_ans)
                    else:  # undetected: [unknown]
                        print("file: " + p)
                        print("id: " + str(data[index]["id"]))
                        print("Undetected judge: " + line)
                        judge_lst.append("unknown")
                        exit()
                # data[index][path] = judge_lst
                data[index]["llama-7b_judge"] = judge_lst
        with open(os.path.join(save_path, path, i), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
