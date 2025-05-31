from typing import Annotated

from fastapi import HTTPException, APIRouter, Request, Query, Depends

from models.CharacterModels import Department
from security.authorization import verification_of_the_head_or_deputy, verification_of_the_director
from database.ConnectionDB import SessionDep
from sqlmodel import select, or_
from fastapi.templating import Jinja2Templates

DepartmentGetRouter = APIRouter()
templates_department = Jinja2Templates(directory = "templates/department")

"""
Ниже функции для работы с кафедрами
"""
@DepartmentGetRouter.get("/get_all_department")
async def get_all_department(session: SessionDep,
                          request: Request):
    """
    Функция, которая возвращает список всех кафедр
    :param request:
    :param session:
    :return:
    """
    try:
        departments = session.exec(select(Department)).all()
        return templates_department.TemplateResponse(
            "all_departments.html",
            context={"request": request, 'departments': departments}
        )
    except Exception as e:
        return {"Ошибка": e}

@DepartmentGetRouter.get("/get_department_by_code_department")
async def get_department_by_code_department(session: SessionDep,
                                            code_department: Annotated[str, Query(pattern = r"^\d{4}$")]):
    """
    Функция, которая возвращает результат поиска кафедры по коду
    :param session:
    :param code_department:
    :return:
    """
    try:
        department = session.get(Department, code_department)
        if not department:
            return HTTPException(status_code = 404, detail = "Кафедры с таким кодом нет")
        return department
    except Exception as e:
        return HTTPException(status_code = 404, detail = e)

@DepartmentGetRouter.get("/add_department")
async def add_department_form(request: Request):
    """
    Функция, которая возвращает форму для добавления кафедры
    :param request:
    :return:
    """
    return templates_department.TemplateResponse(
        "add_department.html",
        context = {"request": request}
    )