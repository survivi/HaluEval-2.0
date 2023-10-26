# coding: utf-8
import json
from docx import Document
from docx.shared import Inches
from sample import check_exist


def main(samples, file):
    document = Document()
    document.add_heading("幻象标注", 0)
    for sample in samples:
        table = document.add_table(rows=5, cols=2, style="Table Grid")
        col_width_dic = {0: 3, 1: 7}
        for col_num in range(2):
            table.cell(0, col_num).width = Inches(col_width_dic[col_num])

        hdr_cells = table.columns[0].cells
        hdr_cells[0].text = "ID"
        hdr_cells[1].text = "User Query"
        hdr_cells[2].text = "Model Response"
        hdr_cells[3].text = "Related Facts"
        hdr_cells[4].text = "Hallucination Facts (separate by ',')"

        hdr_cells = table.columns[1].cells
        hdr_cells[0].text = str(sample["id"])
        hdr_cells[1].text = sample["user_query"]
        hdr_cells[2].text = sample["llama-2-13b-chat-hf_response"]
        hdr_cells[3].text = "\n".join(
            [
                str(id) + ". " + fact
                for id, fact in enumerate(sample["llama-2-13b-chat-hf_fact"], 1)
            ]
        )
        para = document.add_paragraph()
        para.add_run("\n")
    print("saving...")
    document.save(f"./docs/{file}.docx")


if __name__ == "__main__":
    files = [
        "Bio-Medical",
        "Finance",
        "Science",
        "Education",
        "Open-Domain",
    ]
    check_exist("./docs")
    for file in files:
        with open(f"./json/{file}.json", "r") as fin:
            data = json.load(fin)
        main(data, file)
