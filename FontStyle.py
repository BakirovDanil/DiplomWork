from docx import Document
from docx.shared import RGBColor
import json

font_status = {

}

with open('font_rules.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    base_rules = data["base_rules"]

document = Document("C:\\Users\\danil\\Desktop\\Lectures\\DiplomWork\\ВКР, текст.docx")
styles = document.styles

def checking_font_text(*names: str) -> int:
    """
    Функция для проверки шрифтов, которые студент использует в ВКР согласно правилам
    :param names: str
    :return:
    """
    for name in names:
        if name in styles:
            black_rgb = RGBColor(0x00, 0x00, 0x00)
            main_text = styles[name].font
            font_color = "Черный" if main_text.color.rgb == black_rgb else "Другой"
            font_bold = "Нет" if main_text.bold is None else "Да"
            font_italic = "Нет" if main_text.italic is None else "Да"
            font_underline = "Нет" if main_text.underline is None else "Да"
            font_status[name] = {"Размер шрифта": main_text.size.pt,
                                        "Цвет шрифта": font_color,
                                        "Жирный": font_bold,
                                        "Курсивный": font_italic,
                                        "Подчеркнутый": font_underline
                                        }
            if font_status[name] == base_rules[name]:
                font_status[name]["Заключение"] = "Шрифт соответствует правилам"
            else:
                font_status[name]["Заключение"] = "Шрифт несоответствует правилам"
        else:
            font_status[name] = {
                "Заключение": "Шрифт не был обнаружен"
            }
    return 0



checking_font_text("Основной_ПЗ", "Heading 1", "Heading 2", "Heading 3")
for key in font_status.keys():
    print(key)
    for parameter, value in font_status[key].items():
        print(f"\t{parameter}: {value}")