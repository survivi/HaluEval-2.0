# coding: utf-8
import os
import json
from docx import Document


def read_docx(path, part=0):
    """
    Read hallucination fact ids from docx file.
    """
    document = Document(path)
    tables = document.tables
    # id position
    fact_ids = [table.cell(5, 1).text for table in tables]
    fact_ids = [
        i.replace("，", ",").replace(" ", "").replace("\n", "") for i in fact_ids
    ]
    fact_ids = [i.split(",") for i in fact_ids]
    fact_ids = [[] if i == [""] else i for i in fact_ids]
    fact_ids = [[int(j) for j in i] for i in fact_ids]
    if part:
        fact_ids = fact_ids[:part]
    return fact_ids


def read_json(path, part=0):
    """
    Read json file.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if part:
        data = data[:part]
    return data


def show_id(human_id, gpt_id):
    """
    Show human annotated ID vs. ChatGPT ID.
    """
    print("human annotated ID vs. ChatGPT ID")
    for i, (h, g) in enumerate(zip(human_id, gpt_id)):
        print(f"{i}: {h} vs. {g}")


def print_metrics(human_id, gpt_id):
    """
    Calculate overlap ratio.
    """
    total_ratio = []
    for h, g in zip(human_id, gpt_id):
        intersection = sum([1 if i == j else 0 for i, j in zip(h, g)])
        length = len(h)
        total_ratio.append((intersection, length))
    total_intersection = sum([i for i, _ in total_ratio])
    total_length = sum([j for _, j in total_ratio])
    macro_ratio = total_intersection / total_length
    micro_ratio = sum([i / j for i, j in total_ratio]) / len(total_ratio)
    print("macro ratio: ", macro_ratio)
    print("micro ratio: ", micro_ratio)


if __name__ == "__main__":
    file_list = [
        "Bio-Medical",
        "Finance",
        "Science",
        "Education",
        "Open-Domain",
    ]
    model = "llama-2-13b-chat-hf"
    doc_path = "./docs/{}.docx"
    json_path = "./json/{}.json"
    total_human_id = []
    total_gpt_id = []
    for file in file_list:
        print("current file: ", file)
        human_id = read_docx(doc_path.format(file), part=20)
        data = read_json(json_path.format(file), part=20)
        gpt_id = [
            [1 if "true" in jud else 0 for jud in d[f"{model}_judge"]] for d in data
        ]
        lens = [[i + 1 for i in range(len(d[f"{model}_judge"]))] for d in data]
        # check length
        assert len(human_id) == len(gpt_id)
        for i in range(len(human_id)):
            num = len(gpt_id[i])
            try:
                assert max(human_id[i]) <= num
                assert min(human_id[i]) >= 1
            except:
                raise ValueError(
                    f"length error in file: {file}\nid: {data[i]['id']}\nhuman id: {human_id[i]}\ngpt id: {gpt_id[i]}"
                )
        human_id = [[0 if i in h else 1 for i in l] for h, l in zip(human_id, lens)]
        show_id(human_id, gpt_id)
        print_metrics(human_id, gpt_id)
        total_human_id.extend(human_id)
        total_gpt_id.extend(gpt_id)
        print("================================")
    print("total")
    print_metrics(total_human_id, total_gpt_id)
