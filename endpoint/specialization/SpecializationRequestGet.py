from typing import Annotated

from fastapi import HTTPException, APIRouter, Request, Query, Depends

from models.CharacterModels import Specialization
from database.ConnectionDB import SessionDep
from sqlmodel import select, or_
from fastapi.templating import Jinja2Templates

SpecializationGetRouter = APIRouter()
templates_specialization = Jinja2Templates(directory = "templates/specialization")

"""
Ниже функции для работы со специальностями
"""
@SpecializationGetRouter.get("/get_all_specialization")
async def get_all_specialization(session: SessionDep,
                          request: Request):
    """
    Функция, которая возвращает список всех специальностей
    :param request:
    :param session:
    :return:
    """
    try:
        specializations = session.exec(select(Specialization)).all()
        return templates_specialization.TemplateResponse(
            "all_specializations.html",
            context={"request": request, 'specializations': specializations}
        )
    except Exception as e:
        return {"Ошибка": e}

@SpecializationGetRouter.get("/get_specialization_by_code_specialization")
async def get_specialization_by_code_specialization(session: SessionDep,
                                                    code_specialization: Annotated[str, Query(pattern = r"^\d{2}\.\d{2}\.\d{2}$")]):
    """
    Функция, которая возвращает результат поиска специальности по коду
    :param session:
    :param code_specialization:
    :return:
    """
    try:
        specialization = session.get(Specialization, code_specialization)
        if not specialization:
            return HTTPException(status_code = 404, detail = "Специальности с таким кодом нет")
        return specialization
    except Exception as e:
        return HTTPException(status_code = 404, detail = e)

@SpecializationGetRouter.get("/add_specialization")
async def add_specialization_form(request: Request):
    """
    Функция, которая возвращает форму для добавления специальности
    :param request:
    :return:
    """
    return templates_specialization.TemplateResponse(
        "add_specialization.html",
        context = {"request": request}
    )