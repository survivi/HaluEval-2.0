# coding: utf-8
import os
import json
from docx import Document
from collections import defaultdict


def process_cell(tables, index, split=False):
    """
    Process annotated string list.
    """
    info = [table.cell(index, 1).text for table in tables]
    info = [i.replace("，", ",").replace(" ", "").replace("\n", "") for i in info]
    if split:
        info = [[j for j in i.split(",") if j] for i in info]
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
            # print(path.split("/")[-1])
            # return [], [], []
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
            # print(path.split("/")[-1])
            # return [], [], []
            raise ValueError(
                f"response-level error in file: {path}\nID: {ids[i]}\nhallucination IDs: {response_hallu[i]}"
            )
    # length
    lens = [len(table.cell(6, 1).text.split("\n")) for table in tables]
    # segment-level hallucinations
    fact_hallu = process_cell(tables, 7, split=True)
    for i in range(len(fact_hallu)):  # check length and value
        if response_hallu[i] == 2:
            fact_hallu[i] = []
            continue
        try:
            fact_hallu[i] = [int(j) for j in fact_hallu[i]]
            assert lens[i] == len(fact_hallu[i])
            assert min(fact_hallu[i]) >= 1
            assert max(fact_hallu[i]) <= 8
        except:
            # print(path.split("/")[-1])
            # return [], [], []
            raise ValueError(
                f"fact-level error in file: {path}\nID: {ids[i]}\nhallucination IDs: {fact_hallu[i]}"
            )

    return query_scores, response_hallu, fact_hallu, ids


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


def print_metrics(human_id, gpt_id, response_hallu):
    """
    Calculate overlap ratio.
    """
    total_ratio = []
    for h, g, flag in zip(human_id, gpt_id, response_hallu):
        if flag == 2:
            continue
        assert len(h) == len(g)
        intersection = sum([1 if i == j else 0 for i, j in zip(h, g)])
        length = len(h)
        total_ratio.append((intersection, length))
    total_intersection = sum([i for i, _ in total_ratio])
    total_length = sum([j for _, j in total_ratio])
    macro_ratio = total_intersection / total_length
    micro_ratio = sum([i / j for i, j in total_ratio]) / len(total_ratio)
    print("match rate: ", macro_ratio)
    # print("micro ratio: ", micro_ratio)


if __name__ == "__main__":
    file_list = [
        "Bio-Medical",
        "Finance",
        "Science",
        "Education",
        "Open-Domain",
    ]
    model = "chatgpt"
    doc_path_1 = os.path.join("./docs/", "{}_1.docx")
    doc_path_2 = os.path.join("./docs/", "{}_2.docx")
    doc_path_3 = os.path.join("./docs/", "{}_3.docx")
    doc_path_4 = os.path.join("./docs/", "{}_4.docx")
    # doc_path_1 = os.path.join("./docs/", "{}_1_1.docx")
    # doc_path_2 = os.path.join("./docs/", "{}_2_1.docx")
    # doc_path_3 = os.path.join("./docs/", "{}_3_1.docx")
    # doc_path_4 = os.path.join("./docs/", "{}_4_1.docx")
    # doc_path_1 = os.path.join("./docs/", "{}_1_2.docx")
    # doc_path_2 = os.path.join("./docs/", "{}_2_2.docx")
    # doc_path_3 = os.path.join("./docs/", "{}_3_2.docx")
    # doc_path_4 = os.path.join("./docs/", "{}_4_2.docx")
    json_path = os.path.join("./json/", "{}.json")
    total_human_id = []
    total_gpt_id = []
    total_response_hallu = []
    PRINT_HALLU_ID = False
    PRINT_QUERY_SCORE = True
    SHOW_DIFF = False
    PRINT_NUM = False
    PRINT_METRIC = False
    for file in file_list:
        print("current file: ", file)
        query_scores_1, response_hallu_1, fact_hallu_1, ids_1 = read_docx(
            doc_path_1.format(file), part=0
        )
        query_scores_2, response_hallu_2, fact_hallu_2, ids_2 = read_docx(
            doc_path_2.format(file), part=0
        )
        query_scores_3, response_hallu_3, fact_hallu_3, ids_3 = read_docx(
            doc_path_3.format(file), part=0
        )
        query_scores_4, response_hallu_4, fact_hallu_4, ids_4 = read_docx(
            doc_path_4.format(file), part=0
        )
        query_scores = query_scores_1 + query_scores_2 + query_scores_3 + query_scores_4
        response_hallu = (
            response_hallu_1 + response_hallu_2 + response_hallu_3 + response_hallu_4
        )
        fact_hallu_raw = fact_hallu_1 + fact_hallu_2 + fact_hallu_3 + fact_hallu_4
        ids = ids_1 + ids_2 + ids_3 + ids_4
        data = read_json(json_path.format(file), part=0)
        gpt_id = [
            [1 if "true" in jud else 0 for jud in d[f"{model}_judge"]] for d in data
        ]
        # gpt_id = [
        #     [0 if "false" in jud else 1 for jud in d[f"{model}_judge"]] for d in data
        # ]
        # check length and value
        assert len(fact_hallu_raw) == len(gpt_id)
        fact_hallu = [[1 if i == 1 else 0 for i in l] for l in fact_hallu_raw]

        if PRINT_HALLU_ID:
            fact_hallu_flatten = [i for l in fact_hallu_raw for i in l]
            count = [fact_hallu_flatten.count(i) for i in range(1, 9)]
            for idx, c in enumerate(count):
                print(f"{idx + 1}: {c}")

        if PRINT_QUERY_SCORE:
            # query score
            readable = [i[0] for i in query_scores]
            formal = [i[1] for i in query_scores]
            concrete = [i[2] for i in query_scores]
            # score: list of [(false_unknown, sum), false_unknown / sum, hallu_flag]
            readable_dist = defaultdict(lambda: [])
            formal_dist = defaultdict(lambda: [])
            concrete_dist = defaultdict(lambda: [])
            assert len(query_scores) == len(gpt_id)
            for i in range(len(gpt_id)):
                false_unknown = gpt_id[i].count(0)
                sum_ = len(gpt_id[i])
                flag = 1 if false_unknown else 0
                readable_dist[readable[i]].append(
                    (false_unknown, sum_, false_unknown / sum_, flag)
                )
                formal_dist[formal[i]].append(
                    (false_unknown, sum_, false_unknown / sum_, flag)
                )
                concrete_dist[concrete[i]].append(
                    (false_unknown, sum_, false_unknown / sum_, flag)
                )
            print("Readability:")
            for i in range(1, 6):
                print(f"{i}: ", end="")
                micro = (
                    sum([j[2] for j in readable_dist[i]]) / len(readable_dist[i])
                    if len(readable_dist[i])
                    else -0.01
                )
                macro = (
                    sum([j[3] for j in readable_dist[i]]) / len(readable_dist[i])
                    if len(readable_dist[i])
                    else -0.01
                )
                micro = micro * 100
                macro = macro * 100
                avg = round((macro + micro) / 2, 2)
                macro = round(macro, 2)
                micro = round(micro, 2)
                print(
                    f"Num: {len(readable_dist[i])}, Macro: {macro}, Micro: {micro}, Avg: {avg}"
                )
            print("Formality:")
            for i in range(1, 6):
                print(f"{i}: ", end="")
                micro = (
                    sum([j[2] for j in formal_dist[i]]) / len(formal_dist[i])
                    if len(formal_dist[i])
                    else -0.01
                )
                macro = (
                    sum([j[3] for j in formal_dist[i]]) / len(formal_dist[i])
                    if len(formal_dist[i])
                    else -0.01
                )
                micro = micro * 100
                macro = macro * 100
                avg = round((macro + micro) / 2, 2)
                macro = round(macro, 2)
                micro = round(micro, 2)
                print(
                    f"Num: {len(formal_dist[i])}, Macro: {macro}, Micro: {micro}, Avg: {avg}"
                )
            print("Concreteness:")
            for i in range(1, 6):
                print(f"{i}: ", end="")
                micro = (
                    sum([j[2] for j in concrete_dist[i]]) / len(concrete_dist[i])
                    if len(concrete_dist[i])
                    else -0.01
                )
                macro = (
                    sum([j[3] for j in concrete_dist[i]]) / len(concrete_dist[i])
                    if len(concrete_dist[i])
                    else -0.01
                )
                micro = micro * 100
                macro = macro * 100
                avg = round((macro + micro) / 2, 2)
                macro = round(macro, 2)
                micro = round(micro, 2)
                print(
                    f"Num: {len(concrete_dist[i])}, Macro: {macro}, Micro: {micro}, Avg: {avg}"
                )
            print("================================")

        if SHOW_DIFF:
            for id, h, g, flag in zip(ids, fact_hallu, gpt_id, response_hallu):
                if flag == 2:
                    continue
                assert len(h) == len(g)
                print(id + "-> ", end="")
                for i in range(len(h)):
                    if h[i] != g[i]:
                        print(str(i + 1) + ", ", end="")
                print("\n")

        if PRINT_NUM:
            # calculate number of 1 and 0
            print("number of 1 and 0")
            print("# 1: ")
            print("human: ", sum([i.count(1) for i in fact_hallu]))
            print("gpt: ", sum([i.count(1) for i in gpt_id]))
            print("# 0: ")
            print("human: ", sum([i.count(0) for i in fact_hallu]))
            print("gpt: ", sum([i.count(0) for i in gpt_id]))

        if PRINT_METRIC:
            # show_id(fact_hallu, gpt_id)
            print_metrics(fact_hallu, gpt_id, response_hallu)
            total_human_id.extend(fact_hallu)
            total_gpt_id.extend(gpt_id)
            total_response_hallu.extend(response_hallu)
            print("================================")

    if PRINT_METRIC:
        print("done!")
        print("total")
        print_metrics(total_human_id, total_gpt_id, total_response_hallu)
