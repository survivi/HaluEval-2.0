# coding: utf-8
import os
import json
from docx import Document


def process_cell(tables, index, split=False):
    """
    Process annotated string list.
    """
    info = [table.cell(index, 1).text for table in tables]
    info = [i.replace("，", ",").replace(" ", "").replace("\n", "") for i in info]
    if split:
        info = [i.split(",") for i in info]
    return info


def read_docx(path, part=0):
    """
    Read docx file.
    """
    document = Document(path)
    tables = document.tables
    if part:
        tables = tables[:part]
    # ID
    ids = process_cell(tables, 0)
    # query score
    query_scores = process_cell(tables, 3, split=True)
    for i in range(len(query_scores)):  # check length and value
        try:
            assert len(query_scores[i]) == 3
            query_scores[i] = [int(j) for j in query_scores[i]]
            assert min(query_scores[i]) >= 1
            assert max(query_scores[i]) <= 5
        except:
            raise ValueError(
                f"query score error in file: {path}\nID: {ids[i]}\nscore: {query_scores[i]}"
            )
    # response relevance
    response_hallu = process_cell(tables, 5)
    for i in range(len(response_hallu)):  # check value
        try:
            response_hallu[i] = int(response_hallu[i])
            assert response_hallu[i] in (1, 2)
        except:
            raise ValueError(
                f"response-level error in file: {path}\nID: {ids[i]}\nhallucination IDs: {response_hallu[i]}"
            )
    # length
    lens = [len(table.cell(6, 1).text.split("\n")) for table in tables]
    # segment-level hallucinations
    fact_hallu = process_cell(tables, 7, split=True)
    for i in range(len(fact_hallu)):  # check length and value
        try:
            fact_hallu[i] = [int(j) for j in fact_hallu[i]]
            assert lens[i] == len(fact_hallu[i])
            assert min(fact_hallu[i]) >= 1
            assert max(fact_hallu[i]) <= 8
        except:
            raise ValueError(
                f"fact-level error in file: {path}\nID: {ids[i]}\nhallucination IDs: {fact_hallu[i]}"
            )

    return query_scores, response_hallu, fact_hallu


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
    model = "chatgpt"
    doc_path = os.path.join("./docs/", "{}.docx")
    json_path = os.path.join("./json/", "{}.json")
    total_human_id = []
    total_gpt_id = []
    for file in file_list:
        print("current file: ", file)
        query_scores, response_hallu, fact_hallu = read_docx(
            doc_path.format(file), part=1
        )
        data = read_json(json_path.format(file), part=1)
        gpt_id = [
            [1 if "true" in jud else 0 for jud in d[f"{model}_judge"]] for d in data
        ]
        # check length and value
        assert len(fact_hallu) == len(gpt_id)
        for i in range(len(fact_hallu)):
            fact_hallu = [[1 if i == 1 else 0 for i in l] for l in fact_hallu]
        show_id(fact_hallu, gpt_id)
        print_metrics(fact_hallu, gpt_id)
        total_human_id.extend(fact_hallu)
        total_gpt_id.extend(gpt_id)
        print("================================")
        print(query_scores, response_hallu, fact_hallu)
        exit()

    print("total")
    print_metrics(total_human_id, total_gpt_id)
