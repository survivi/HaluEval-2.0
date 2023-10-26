import os
import json
import argparse


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
    parser = argparse.ArgumentParser(description="Metric Calculation")
    file_list = [
        "Bio-Medical",
        "Finance",
        "Science",
        "Education",
        "Open-Domain",
    ]
    parser.add_argument(
        "--data-dir",
        default="./judge/",
        help="data root directory",
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
            "chatglm-6b",
        ],
        help="chat model to use",
    )
    args = parser.parse_args()
    data_path = args.data_dir
    model = args.model
    total_count = []
    for file in file_list:
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
