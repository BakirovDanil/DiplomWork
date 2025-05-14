from docx import Document
from docx.shared import RGBColor

async def checking_styles_in_document(base_rules: dict, doc: Document) -> dict:
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
        if style_name in styles_valid_list:
            font_style = style.font
            font_name = font_style.name
            font_color = "Черный" if font_style.color.rgb == black_rgb else "Другой" # получение цвета используемого шрифта
            font_bold = "Нет" if font_style.bold is None or False else "Да"
            font_italic = "Нет" if font_style.italic is None or False else "Да"
            font_underline = "Нет" if font_style.underline is None or False else "Да"
            font_size = font_style.size.pt if font_style.size else None
            font_status[style_name] = {"Используемый шрифт": font_name,
                                        "Размер стиля": font_size,
                                        "Цвет стиля": font_color,
                                        "Жирный": font_bold,
                                        "Курсивный": font_italic,
                                        "Подчеркнутый": font_underline
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