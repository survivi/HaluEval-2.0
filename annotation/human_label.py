# coding: utf-8
import os
import json
from docx import Document
from docx.shared import Inches
from sample import check_exist
from docx.oxml.ns import qn
from docx.shared import Pt

def set_font(run):
    run.font.name = "仿宋"
    run.font.size = Pt(11)
    r = run._element
    r.rPr.rFonts.set(qn("w:eastAsia"), "仿宋")

def main(model, file, samples, save_path):
    document = Document()
    document.add_heading("幻象标注", 0)

    for sample in samples:
        table = document.add_table(rows=8, cols=2, style="Table Grid")
        col_width_dic = {0: 3, 1: 7}
        for col_num in range(2):
            table.cell(0, col_num).width = Inches(col_width_dic[col_num])

        hdr_cells = table.columns[0].cells
        hdr_cells[0].text = "ID"
        run = hdr_cells[1].paragraphs[0].add_run("领域")
        set_font(run)
        run = hdr_cells[2].paragraphs[0].add_run("用户问题")
        set_font(run)
        run = hdr_cells[3].paragraphs[0].add_run("问题打分（逗号分隔）：\n可读性（1-5）\n规范性（1-5）\n具体性（1-5）")
        set_font(run)
        run = hdr_cells[4].paragraphs[0].add_run("模型回复")
        set_font(run)
        run = hdr_cells[5].paragraphs[0].add_run("回复标注（三选一）：\n1-回复与问题相关且有效回复\n2-回复与问题相关但无效回复\n3-回复与问题完全无关")
        set_font(run)
        run = hdr_cells[6].paragraphs[0].add_run("提取的事实")
        set_font(run)
        run = hdr_cells[7].paragraphs[0].add_run("事实标注\n（每条事实六选一）：\n1-没有事实错误\n2-相似的事实错误\n3-差异的事实错误\n4-关键信息缺失\n5-信息过时\n6-无法验证")
        set_font(run)

        hdr_cells = table.columns[1].cells
        hdr_cells[0].text = str(sample["id"])
        hdr_cells[1].text = file
        hdr_cells[2].text = sample["user_query"]
        hdr_cells[4].text = sample[f"{model}_response"]
        hdr_cells[6].text = "\n".join(
            [
                str(id) + ". " + fact
                for id, fact in enumerate(sample[f"{model}_fact"], 1)
            ]
        )
        para = document.add_paragraph()

        para.add_run("\n")
    print("saving to: " + save_path)
    document.save(save_path)


if __name__ == "__main__":
    file_list = [
        "Bio-Medical",
        "Finance",
        "Science",
        "Education",
        "Open-Domain",
    ]
    model = "llama-2-13b-chat-hf"
    json_dir = "./json/"
    save_dir = "./docs/"
    check_exist(save_dir)
    for file in file_list:
        with open(os.path.join(json_dir, f"{file}.json"), "r") as fin:
            data = json.load(fin)
        save_path = os.path.join(save_dir, f"{file}.docx")
        main(model, file, data, save_path)
