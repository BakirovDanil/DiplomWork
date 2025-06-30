from fastapi import UploadFile, Form, File, HTTPException, APIRouter, Request
from docx import Document
import json
from typing import Annotated
from fastapi.templating import Jinja2Templates

from methods.CheckingCodes import search_chapter_codes, search_picture_codes, check_len_subsection
from models.CharacterModels import Student
from models.TaskModel import Report, ReportBase
from database.ConnectionDB import SessionDep

ReportPostRouter = APIRouter()
templates_reports = Jinja2Templates(directory = "templates/reports")

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

@ReportPostRouter.post("/check_document")
async def check_document(number_gradebook: Annotated[str, Form()],
                         file: Annotated[UploadFile, File()],
                         session: SessionDep,
                         request: Request):
    """
    Функция, которая возвращает результат проверки загруженного документа
    :param request:
    :param number_gradebook:
    :param session:
    :param file:
    :return:
    """
    try:
        check_number_gradebook = session.get(Student, number_gradebook)
        if not check_number_gradebook:
            raise HTTPException(status_code = 404, detail = "Студента с такой зачеткой нет в базе")
        document = Document(file.file)
        chapter_status = await search_chapter_codes(open_base_rules('rules/section_rules.json'),document) # проверка по содержанию
        picture_status = await search_picture_codes(open_base_rules('rules/section_rules.json'), document) # проверка по рисункам
        subsection_status = await check_len_subsection(open_base_rules('rules/section_rules.json'), document) # проверка по размерам
        result = {
            "Отчет по разделам": chapter_status,
            "Отчет по рисункам": picture_status,
            "Отчет по размерам": subsection_status
        }
        checking_result = str(result)
        diplom_work_information = ReportBase(
            number_gradebook = number_gradebook,
            result = checking_result
        )
        diplom_work_information = Report.model_validate(diplom_work_information)
        session.add(diplom_work_information)
        session.commit()
        session.refresh(diplom_work_information)
        return templates_reports.TemplateResponse(
            "get_result_report.html",
            context = {"request": request, "result": result}
        )
    except Exception as e:
        return templates_reports.TemplateResponse(
            "get_result_report.html",
            {"request": request, "error": str(e)},
            status_code=500
        )