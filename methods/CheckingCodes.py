from textwrap import wrap
import re
from docx import Document


def checking_code(code: str, base_rules: dict, chapter: str) -> bool:
    """
    Функция, для проверки полученного кода по базе правил кодирования
    :param chapter:
    :param code:
    :param base_rules:
    :return:
    """
    decoder = wrap(code, base_rules[chapter]["Длина части кода"])
    answer = ''
    for position in decoder:
        if position in base_rules[chapter]:
            answer += position
        else:
            return False
    return True


async def search_chapter_codes(base_rules: dict, document: Document) -> dict:
    """
    Функция, которая проверяет кодирование абзацев
    :param base_rules:
    :param document:
    :return:
    """
    chapter_status = {
        "Общее количество заголовков": 0,
        "Количество верно закодированных абзацев": 0,
        "Количество незакодированных абзацев": 0,
        "Заголовки с нарушениями кодирования": {

        }
    }
    number_paragraph = 1
    for paragraph in document.paragraphs:
        if paragraph.style.name in base_rules["chapter_rules"]["Допустимые стили"]:
            chapter_status["Общее количество заголовков"] += 1
            match = re.findall(fr"\b\d{{{base_rules["chapter_rules"]["Длина всего кода"]}}}\b", paragraph.text)
            if match:
                if checking_code(match[0], base_rules, "chapter_rules"):
                    chapter_status["Количество верно закодированных абзацев"] += 1
                else:
                    chapter_status["Заголовки с нарушениями кодирования"][number_paragraph] = {
                        "Номер заголовка": number_paragraph,
                        "Название заголовка": paragraph.text,
                        "Ошибка": "Ошибка в позиции кодирования",
                        "Заключение": "Код не соответствует кодировке"
                    }
                    chapter_status["Количество незакодированных абзацев"] += 1
            else:
                chapter_status["Заголовки с нарушениями кодирования"][number_paragraph] = {
                    "Номер заголовка": number_paragraph,
                    "Название заголовка": paragraph.text,
                    "Ошибка": "Несоответствие стилю кодирования",
                    "Заключение": "Код не соответствует кодировке"
                }
                chapter_status["Количество незакодированных абзацев"] += 1
        else:
            continue
        number_paragraph += 1
    return chapter_status


async def search_picture_codes(base_rules: dict, document: Document) -> dict:
    """
    Функция, которая проверяет кодирование рисунков
    :param base_rules:
    :param document:
    :return:
    """
    picture_status = {
        "Общее количество рисунков": 0,
        "Количество верно закодированных рисунков": 0,
        "Количество незакодированных рисунков": 0,
        "Рисунки с нарушением кодирования": {

        }
    }
    picture_number = 1
    for paragraph in document.paragraphs:
        if (paragraph.style.name in base_rules["picture_rules"]["Допустимые стили"]
            and re.findall(f"Рис", paragraph.text)):
            picture_status["Общее количество рисунков"] += 1
            match = re.findall(fr"\b\d{{{base_rules["picture_rules"]["Длина всего кода"]}}}\b", paragraph.text)
            if match:
                if checking_code(match[0], base_rules, "picture_rules"):
                    picture_status["Количество верно закодированных рисунков"] += 1
                else:
                    picture_status["Рисунки с нарушением кодирования"][picture_number] = {
                        "Номер рисунка": picture_number,
                        "Название рисунка": paragraph.text,
                        "Ошибка": "Ошибка в позиции кодирования",
                        "Заключение": "Код не соответствует кодировке"
                    }
                    picture_status["Количество незакодированных рисунков"] += 1
            else:
                picture_status["Рисунки с нарушением кодирования"][picture_number] = {
                    "Номер рисунка": picture_number,
                    "Название рисунка": paragraph.text,
                    "Ошибка": "Несоответствие стилю кодирования",
                    "Заключение": "Код не соответствует кодировке"
                }
                picture_status["Количество незакодированных рисунков"] += 1
        else:
            continue
        picture_number += 1
    return picture_status