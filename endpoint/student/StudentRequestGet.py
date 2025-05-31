from typing import Annotated

from fastapi import HTTPException, APIRouter, Request, Query, Depends

from models.CharacterModels import Student
from security.authorization import verification_of_the_head_or_deputy, verification_of_the_director
from database.ConnectionDB import SessionDep
from sqlmodel import select, or_
from fastapi.templating import Jinja2Templates

StudentGetRouter = APIRouter()
templates_student = Jinja2Templates(directory = "templates/student")

"""
Ниже функции для работы со студентами
"""
@StudentGetRouter.get("/get_all_student")
async def get_all_student(session: SessionDep,
                          request: Request,
                          current_user: Annotated[str, Depends(verification_of_the_head_or_deputy)]):
    """
    Функция, которая возвращает список всех студентов
    :param current_user:
    :param request:
    :param session:
    :return:
    """
    try:
        students = session.exec(select(Student)).all()
        return templates_student.TemplateResponse(
            "all_students.html",
            context={"request": request, 'students': students}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@StudentGetRouter.get("/get_student_by_number_gradebook")
async def get_student_by_number_gradebook(session: SessionDep,
                                          number_gradebook: Annotated[str, Query(pattern = r"^\d{8}$")],
                                          request: Request):
    """
    Функция, которая возвращает студента по номеру зачетной книжки
    :param number_gradebook:
    :param session:
    :param request:
    :return:
    """
    try:
        student = session.get(Student, number_gradebook)
        if not student:
            raise HTTPException(status_code = 404, detail = "Студента с таким номером нет")
        return templates_student.TemplateResponse(
            "get_student_by_number_gradebook.html",
            context={"request": request,
                     'student': student}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@StudentGetRouter.get("/get_student_by_surname_and_name")
async def get_student_by_surname_and_name(session: SessionDep,
                                          request: Request,
                                          surname: Annotated[str|None, Query()] = None,
                                          name: Annotated[str|None, Query()] = None):
    """
    Функция, которая возвращает результат поиска по имени или фамилии
    :param request:
    :param session:
    :param surname:
    :param name:
    :return:
    """
    try:
        if not name and not surname:
            raise HTTPException(status_code = 400, detail = "Одно из полей должно быть заполнено")
        students = session.exec(select(Student).where(or_(Student.surname == surname, Student.name == name))).all()
        if not students:
            raise HTTPException(status_code = 404, detail = "Студентов с такими данными нет")
        return templates_student.TemplateResponse(
            "get_student_by_surname_and_name.html",
            context={"request": request,
                     'students': students}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@StudentGetRouter.get("/add_student")
async def add_student_form(request: Request,
                           current_user: Annotated[str, Depends(verification_of_the_head_or_deputy)]):
    """
    Функция, которая возвращает форму для добавления студента
    :param current_user:
    :param request:
    :return:
    """
    try:
        return templates_student.TemplateResponse(
            "add_student.html",
            context = {"request": request}
        )
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))

@StudentGetRouter.get("/search_student_form_by_surname_and_name")
async def search_student_form_by_surname_and_name(request: Request,
                                                  current_user: Annotated[str, Depends(verification_of_the_director)]):
    """
    Функция, которая возвращает форму для поиска студента фамилии и имени
    :param current_user:
    :param request:
    :return:
    """
    try:
        return templates_student.TemplateResponse(
            "search_student_form_by_surname_and_name.html",
            context = {"request": request}
        )
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@StudentGetRouter.get("/search_student_form_by_number_gradebook")
async def search_student_form_by_number_gradebook(request: Request,
                                                  current_user: Annotated[str, Depends(verification_of_the_director)]):
    """
    Функция, которая возвращает форму для поиска студента по номеру зачетки
    :param current_user:
    :param request:
    :return:
    """
    try:
        return templates_student.TemplateResponse(
            "search_student_form_by_number_gradebook.html",
            context={"request": request}
        )
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))