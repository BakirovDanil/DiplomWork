from fastapi import HTTPException, APIRouter, Request
from httpx import request

from models.TaskModel import Task
from models.CharacterModels import StudentBase, Student
from database.ConnectionDB import SessionDep
from sqlmodel import select
from fastapi.templating import Jinja2Templates

GetRouter = APIRouter()
templates = Jinja2Templates(directory = "templates")

@GetRouter.get("/get_all_task")
async def get_all_result(session: SessionDep):
    result = session.exec(select(Task)).all()
    return result


@GetRouter.get("/get_task_by_id")
async def get_result_by_id(value: int, session: SessionDep):
    """
    Функция, которая возвращает результат записи по id записи
    :param value:
    :param session:
    :return:
    """
    try:
        work = session.get(Task, value)
        if not work:
            raise HTTPException(status_code = 404, detail = "Запись не найдена")
        return work
    except:
        raise HTTPException(status_code = 404, detail = "Неизвестная ошибка")


@GetRouter.get("/get_all_student")
async def get_all_student(session: SessionDep,
                          request: Request):
    """
    Функция, которая возвращает список всех студентов
    :param request:
    :param session:
    :return:
    """
    try:
        students = session.exec(select(Student)).all()
        return templates.TemplateResponse(
            "all_students.html",
            context={"request": request, 'students': students}
        )
    except Exception as e:
        return {"Ошибка": e}

@GetRouter.get("/add_student")
async def add_student_form(request: Request):
    return templates.TemplateResponse(
        "add_student.html",
        context = {"request": request}
    )