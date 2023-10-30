# coding: utf-8
import os
import json
import random
from evaluate import read_json


def check_exist(path):
    """
    Check if the path exists, if not, create it.
    """
    if not os.path.exists(path):
        os.mkdir(path)


def sample_data(source, num, path):
    """
    Sample data from source.
    """
    if len(source) >= num:
        data = random.sample(source, num)
    else:
        raise ValueError(
            f"Sample number {num} is larger than data size {len(source)}, path: {path}"
        )
    return data


def add_ref(path, data):
    """
    Add reference answers or documents to data.
    """
    if "Bio-Medical" in path:
        ref = read_json(path)
        ref = {i["id"]: (i["user_query"], i["answer"]) for i in ref}
    elif "Finance" in path or "Science" in path:
        ref = read_json(path)
        ref = {i["id"]: (i["user_query"], "\n".join(i["docs"])) for i in ref}
    else:
        ref = None
    if ref:
        for i in range(len(data)):
            user_query = data[i]["user_query"]
            ref_query, info = ref[data[i]["id"]]
            try:
                assert user_query == ref_query
            except:
                print("query not match")
                print("user_query: " + user_query)
                print("ref_query: " + ref_query)
                raise ValueError
            data[i]["reference"] = info
    else:
        for i in range(len(data)):
            data[i]["reference"] = ""
    return data


if __name__ == "__main__":
    file_list = [
        "Bio-Medical",
        "Finance",
        "Science",
        "Education",
        "Open-Domain",
    ]
    model = "llama-2-7b-chat-hf"
    path = os.path.join(f"../llama-2-13b-chat-hf_judge/", "{}.json")
    # ref_path = os.path.join("../ref/", "{}_ref.json")
    sample_num = 200
    save = "./json/"
    check_exist(save)
    save_path_f = os.path.join(save, "{}.json")
    info = {path.format(i): sample_num for i in file_list}
    random.seed(42)
    for file in file_list:
        data_path = path.format(file)
        save_path = save_path_f.format(file)
        data = read_json(data_path, part=270)
        data = [i for i in data if len(i[f"{model}_fact"]) != 0]
        data = sample_data(data, info[data_path], data_path)
        # sort by id
        data = sorted(data, key=lambda x: x["id"])
        # add reference
        # data = add_ref(ref_path.format(file), data)
        with open(save_path, "w", encoding="utf-8") as g:
            json.dump(data, g, indent=2, ensure_ascii=False)
        print(f"Sample {len(data)} data from {data_path} to {save_path}")
