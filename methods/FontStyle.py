from docx import Document
from docx.shared import RGBColor
import json
from dictWork import dictionary_output

def open_base_rules(file: str) -> dict:
    """
    Функция для открытия файла с правилами
    :param file:
    :return:
    """
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        base_rules = data["base_rules"]
        return base_rules

def checking_styles_in_document(base_rules: dict, doc: Document) -> dict:
    alignment_dict = {
        1: "По центру",
        2: "По правому краю",
        3: "По ширине"
    }
    """
    Функция для проверки шрифтов, которые студент использует в ВКР согласно правилам
    :param doc: проверяемый документ
    :param base_rules: база правил в формате json
    :return:
    """
    # Словарь для хранения результатов проверки
    font_status = {

    }
    black_rgb = RGBColor(0x00, 0x00, 0x00) # код черного цвета для сравнения
    styles_valid_list = [key for key in base_rules] # список допустимых стилей из базы правил
    styles = doc.styles # получение списка всех стилей используемых в проверяемом документе
    for style in styles:
        style_name = style.name
        print(style_name)
        if style_name in styles_valid_list:
            font_style = style.font
            font_name = font_style.name
            font_color = "Черный" if font_style.color.rgb == black_rgb or None else "Другой"  # получение цвета используемого шрифта
            font_bold = "Да" if font_style.bold else "Нет"
            font_italic = "Да" if font_style.italic else "Нет"
            font_underline = "Да" if font_style.underline else "Нет"
            font_size = font_style.size.pt if font_style.size else None
            line_spacing = style.paragraph_format.line_spacing
            first_line_indent = style.paragraph_format.first_line_indent.cm if style.paragraph_format.first_line_indent else 0
            space_after = style.paragraph_format.space_after.pt if style.paragraph_format.space_after else 0
            space_before = style.paragraph_format.space_before.pt if style.paragraph_format.space_before else 0
            alignment = alignment_dict[
            style.paragraph_format.alignment] if style.paragraph_format.alignment in alignment_dict else "По левому краю"
            font_status[style_name] = {"Используемый шрифт": font_name,
                                        "Размер шрифта": font_size,
                                        "Цвет шрифта": font_color,
                                        "Жирный": font_bold,
                                        "Курсивный": font_italic,
                                        "Подчеркнутый": font_underline,
                                        "Межстрочный интервал": float(line_spacing),
                                        "Отступ первой строки": float(round(first_line_indent, 2)),
                                        "Отступ после абзаца": float(space_after),
                                        "Отступ перед абзацем": float(space_before),
                                        "Выравнивание": alignment
                                        }
            if font_status[style_name] == base_rules[style_name]:
                    font_status[style_name]["Заключение"] = "Стиль соответствует правилам"
            else:
                font_status[style_name]["Заключение"] = "Стиль несоответствует правилам"
        else:
            continue
    return font_status

# def main(path: str):
#     document = Document(path)
#     check_result = checking_styles_in_document(open_base_rules('../rules/font_rules.json'), document)
#     dictionary_output(check_result)
#     with open('../style_result.json', 'w', encoding='utf-8') as f:
#         json.dump(check_result, f, ensure_ascii = False, indent = 1)
#
# if __name__ == "__main__":
#     main("C:\\Users\\danil\\Desktop\\Lectures\\DiplomWork\\ВКР, текст.docx")