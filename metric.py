import os
import json


def cal_matrics(count):
    """
    Calculate metrics.
    """
    micro = sum([i[1] for i in count]) / len(count)
    macro = sum([i[2] for i in count]) / len(count)
    micro = round(micro, 4)
    macro = round(macro, 4)
    print(f"micro: {micro}, macro: {macro}")


def load_pure_data(data_path, file):
    """
    Load data and filter out data with no facts.
    """
    with open(os.path.join(data_path, f"{file}.json"), "r", encoding="utf-8") as f:
        raw = json.load(f)
        data = [d for d in raw if d[model + "_judge"]]
        dif = len(raw) - len(data)
        print(f"total: {len(data)}, filtered: {dif}")
    return data


def get_info(judge_list):
    """
    Get info from judge list.
    """
    true = judge_list.count("true")
    failed = judge_list.count("unknown")
    false = len(judge_list) - true - failed
    info = [(false, len(judge_list)), false / len(judge_list)]
    if false:
        info.append(1)
    else:
        info.append(0)
    return info


if __name__ == "__main__":
    data_path = "./judge"
    model = "llama-2-13b-chat-hf"
    files = [
        "Bio-Medical",
        "Finance",
        "Science",
        "Education",
        "Open-Domain",
    ]
    total_count = []
    for file in files:
        print("current file: ", file)
        data = load_pure_data(data_path, file)
        count = []
        for i in range(len(data)):
            judge_list = data[i][model + "_judge"]
            info = get_info(judge_list)
            count.append(info)
        total_count.extend(count)
        # calculate file average
        cal_matrics(count)
        print("========================================")
    # calculate total average
    cal_matrics(total_count)
