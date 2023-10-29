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
    # Query Score
    query_scores = process_cell(tables, 2, split=True)
    for i in range(len(query_scores)):  # check length and value
        try:
            assert len(query_scores[i]) == 3
            query_scores[i] = [int(j) for j in query_scores[i]]
            assert min(query_scores[i]) >= 1
            assert max(query_scores[i]) <= 10
        except:
            raise ValueError(
                f"query score error in file: {path}\nid: {ids[i]}\nscore: {query_scores[i]}"
            )
    # Response-level Hallucination
    response_hallu = process_cell(tables, 4)
    response_hallu = [int(i) if i else 0 for i in response_hallu]
    for i in range(len(response_hallu)):  # check value
        try:
            assert response_hallu[i] in [0, 1, 2]
        except:
            raise ValueError(
                f"response-level error in file: {path}\nid: {ids[i]}\nhallucination id: {response_hallu[i]}"
            )
    # Hallucination Facts ID
    fact_ids = process_cell(tables, 6, split=True)
    fact_ids = [[] if i == [""] else i for i in fact_ids]
    fact_ids = [[int(j) for j in i] for i in fact_ids]
    # Fact-level Hallucinations
    fact_hallu = process_cell(tables, 7, split=True)
    fact_hallu = [[] if i == [""] else i for i in fact_hallu]
    fact_hallu = [[int(j) for j in i] for i in fact_hallu]
    for i in range(len(fact_hallu)):  # check length and value
        try:
            len(fact_hallu[i]) == len(fact_ids[i])
            min(fact_hallu[i]) >= 1
            max(fact_hallu[i]) <= 5
        except:
            raise ValueError(
                f"fact-level error in file: {path}\nid: {ids[i]}\nfact id: {fact_ids[i]}\nhallucination id: {fact_hallu[i]}"
            )

    return query_scores, response_hallu, fact_ids, fact_hallu


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
    doc_path = os.path.join("./docs/", "{}.docx")
    json_path = os.path.join("./json/", "{}.json")
    total_human_id = []
    total_gpt_id = []
    for file in file_list:
        print("current file: ", file)
        query_scores, response_hallu, fact_ids, fact_hallu = read_docx(
            doc_path.format(file), part=1
        )
        data = read_json(json_path.format(file), part=1)
        gpt_id = [
            [1 if "true" in jud else 0 for jud in d[f"{model}_judge"]] for d in data
        ]
        lens = [[i + 1 for i in range(len(d[f"{model}_judge"]))] for d in data]
        # check length and value
        assert len(fact_ids) == len(gpt_id)
        for i in range(len(fact_ids)):
            try:
                assert min(fact_ids[i]) >= 1
                assert max(fact_ids[i]) <= len(gpt_id[i])
            except:
                raise ValueError(
                    f"length or value error in file: {file}\nid: {data[i]['id']}\nhuman id: {fact_ids[i]}\ngpt id: {gpt_id[i]}"
                )
        fact_ids = [[0 if i in h else 1 for i in l] for h, l in zip(fact_ids, lens)]
        show_id(fact_ids, gpt_id)
        print_metrics(fact_ids, gpt_id)
        total_human_id.extend(fact_ids)
        total_gpt_id.extend(gpt_id)
        print("================================")

    print("total")
    print_metrics(total_human_id, total_gpt_id)
