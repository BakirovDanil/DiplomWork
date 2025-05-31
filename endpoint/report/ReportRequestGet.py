from fastapi import HTTPException, APIRouter, Request

from models.TaskModel import Report
from database.ConnectionDB import SessionDep
from sqlmodel import select
from fastapi.templating import Jinja2Templates

ReportGetRouter = APIRouter()
templates_reports = Jinja2Templates(directory = "templates/reports")

"""
Ниже функции для работы с отчетами
"""
@ReportGetRouter.get("/get_all_task")
async def get_all_result(session: SessionDep):
    """
    Функция, которая возвращает все записи из базы
    :param session:
    :return:
    """
    result = session.exec(select(Report)).all()
    return result

@ReportGetRouter.get("/get_task_by_id")
async def get_result_by_id(value: int,
                           session: SessionDep):
    """
    Функция, которая возвращает результат записи по id записи
    :param value:
    :param session:
    :return:
    """
    try:
        report = session.get(Report, value)
        if not report:
            raise HTTPException(status_code = 404, detail = "Запись не найдена")
        return report
    except:
        raise HTTPException(status_code = 404, detail = "Неизвестная ошибка")

@ReportGetRouter.get("/check_document_form")
async def check_document_form(request: Request):
    return templates_reports.TemplateResponse(
        "upload_file_form.html",
        context= {"request": request}
    )