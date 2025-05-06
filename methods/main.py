from textwrap import wrap
import re
import json
from docx import Document

with open('../rules/section_rules.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    sections_code = data["section_codes"]

code_run_text = []

dict_checking_code = {

}

def checking(code):
    checking_flag = True
    decoder = wrap(code, 3)
    answer = ''
    for position in decoder:
        if position in sections_code:
            sections_code[position]["Количество"] += 1
            answer += position
        else:
            dict_checking_code[code] = f"Код не соответствует кодировке. Позиция {position} отсутствует в таблице кодов"
            checking_flag = False
            break
    if checking_flag:
        dict_checking_code[answer] = "Код соответствует кодировке"

def paragraphs(document):
    """Ищет коды в заголовках Heading 1"""
    for paragraph in document.paragraphs:
        if paragraph.style.name in ["Heading 1", "Heading 2", "Heading 3"]:
            match = re.findall(r"0\d{8}", paragraph.text)
            if match:
                code_run_text.append(match[0])
            else:
                dict_checking_code[paragraph.text] = "В заголовке отсутствует код."