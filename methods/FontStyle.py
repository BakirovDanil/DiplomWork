from docx import Document
from docx.shared import RGBColor
import json
from methods.dictWork import dictionary_output

def open_base_rules(file: str) -> dict:
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        base_rules = data["base_rules"]
        return base_rules

def checking_styles_in_document(base_rules: dict, doc: Document, *names: str) -> dict:
    """
    Функция для проверки шрифтов, которые студент использует в ВКР согласно правилам
    :param doc:
    :param base_rules:
    :param names: str
    :return:
    """
    font_status = {

    }
    black_rgb = RGBColor(0x00, 0x00, 0x00) # код черного цвета для сравнения
    styles = doc.styles
    for name in names:
        if name in styles:
            font_text = styles[name].font
            font_color = "Черный" if font_text.color.rgb == black_rgb else "Другой"
            font_bold = "Нет" if font_text.bold is None else "Да"
            font_italic = "Нет" if font_text.italic is None else "Да"
            font_underline = "Нет" if font_text.underline is None else "Да"
            font_status[name] = {"Шрифт": font_text.name,
                                        "Размер стиля": font_text.size.pt,
                                        "Цвет стиля": font_color,
                                        "Жирный": font_bold,
                                        "Курсивный": font_italic,
                                        "Подчеркнутый": font_underline
                                        }
            if name in base_rules:
                if font_status[name] == base_rules[name]:
                    font_status[name]["Заключение"] = "Стиль соответствует правилам"
                else:
                    font_status[name]["Заключение"] = "Стиль несоответствует правилам"
            else:
                font_status[name]["Заключение"] = "Стиль отсутствует в базе правил"
        else:
            font_status[name] = {
                "Заключение": "Стиль не был обнаружен"
            }
    return font_status

def main(path: str):
    document = Document(path)
    check_result = checking_styles_in_document(open_base_rules('../rules/font_rules.json'), document, "Основной_ПЗ", "Heading 1", "Heading 2", "Heading 3", "Caption")
    dictionary_output(check_result)
    with open('../style_result.json', 'w', encoding='utf-8') as f:
        json.dump(check_result, f, ensure_ascii = False, indent = 1)

if __name__ == "__main__":
    main("C:\\Users\\danil\\Desktop\\Lectures\\DiplomWork\\ВКР, текст.docx")