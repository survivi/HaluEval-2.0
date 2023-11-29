# coding: utf-8
import os
import json
import argparse


def load_pure_data(data_path, file):
    """
    Load data and filter out data with no facts.
    """
    with open(os.path.join(data_path, f"{file}.json"), "r", encoding="utf-8") as f:
        raw = json.load(f)
        data = [d for d in raw if d[model + "_judge"]]
        print(
            f"Total: {len(data)}, original: {len(raw)}, filtered: {len(raw) - len(data)}"
        )
    return data


def cal_matrics(count):
    """
    Calculate metrics.
    """
    micro = sum([i[1] for i in count]) / len(count)
    macro = sum([i[2] for i in count]) / len(count)
    micro = micro * 100
    macro = macro * 100
    micro = round(micro, 2)
    macro = round(macro, 2)
    return f"{macro:.2f}", f"{micro:.2f}"


def get_info(judge_list):
    """
    Get info from judge list.
    """
    true = judge_list.count("true")
    false_unknown = len(judge_list) - true
    info = [(false_unknown, len(judge_list)), false_unknown / len(judge_list)]
    if false_unknown:
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
        "--model",
        default="chatgpt",
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
            # "llama-2-7b-hf",
            # "llama-2-13b-hf",
            # "bloom-7b1",
        ],
        help="chat model to use",
    )
    args = parser.parse_known_args()[0]
    parser.add_argument(
        "--data-dir",
        default=f"./judge/{args.model}_judge/",
        help="data root directory",
    )
    args = parser.parse_args()
    # print all args
    print("Arguments:")
    for arg in vars(args):
        print(f"  {arg}: {getattr(args, arg)}")
    data_path = args.data_dir
    model = args.model
    total_count = []
    metrics = []
    PRINT_METRICS = 0
    for file in file_list:
        print("Current file: ", file)
        data = load_pure_data(data_path, file)
        count = []
        for i in range(len(data)):
            judge_list = data[i][model + "_judge"]
            info = get_info(judge_list)
            count.append(info)
        total_count.extend(count)
        # calculate file average
        macro, micro = cal_matrics(count)
        if PRINT_METRICS:
            print(f"Metrics(%) -> Macro: {macro}, Micro: {micro}")
            print("========================================")
        else:
            metrics.append(macro)
            metrics.append(micro)

    if PRINT_METRICS:
        # calculate total average
        print("Total average:")
        macro, micro = cal_matrics(total_count)
        print(f"Metrics(%) -> Macro: {macro}, Micro: {micro}")
    else:
        print(" & ".join(metrics))

print("\n\n")
