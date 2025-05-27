from typing import Annotated

from fastapi import HTTPException, APIRouter, Request, Query

from models.TaskModel import Task
from models.CharacterModels import Student, Director, Department, Specialization
from database.ConnectionDB import SessionDep
from sqlmodel import select, or_
from fastapi.templating import Jinja2Templates

GetRouter = APIRouter()
templates_main = Jinja2Templates(directory = "templates/main_page")
templates_student = Jinja2Templates(directory = "templates/student")
templates_director = Jinja2Templates(directory = "templates/director")
templates_specialization = Jinja2Templates(directory = "templates/specialization")
templates_department = Jinja2Templates(directory = "templates/department")

@GetRouter.get("/")
async def base_page(request: Request):
    return templates_main.TemplateResponse(
        "base.html",
        context = {"request": request}
    )

# ниже функции для работы с записями проверок
@GetRouter.get("/get_all_task")
async def get_all_result(session: SessionDep):
    """
    Функция, которая возвращает все записи из базы
    :param session:
    :return:
    """
    result = session.exec(select(Task)).all()
    return result

@GetRouter.get("/get_task_by_id")
async def get_result_by_id(value: int,
                           session: SessionDep):
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


"""
Ниже функции для работы со студентами
"""
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
        return templates_student.TemplateResponse(
            "all_students.html",
            context={"request": request, 'students': students}
        )
    except Exception as e:
        return {"Ошибка": e}

@GetRouter.get("/get_student_by_number_gradebook")
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
        return student
    except Exception as e:
        raise HTTPException(status_code = 404, detail = e)

@GetRouter.get("/get_student_by_surname_and_name")
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
            "get_student_by_name_and_surname.html",
            context={"request": request,
                     'students': students}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@GetRouter.get("/add_student")
async def add_student_form(request: Request):
    """
    Функция, которая возвращает форму для добавления студента
    :param request:
    :return:
    """
    return templates_student.TemplateResponse(
        "add_student.html",
        context = {"request": request}
    )

@GetRouter.get("/search_student_form")
async def search_student_form(request: Request):
    """
    Функция, которая возвращает форму для поиска студента
    :param request:
    :return:
    """
    return templates_student.TemplateResponse(
        "search_student_form.html",
        context = {"request": request}
    )


"""
Ниже функции для работы с руководителями
"""
@GetRouter.get("/get_all_director")
async def get_all_director(session: SessionDep,
                          request: Request):
    """
    Функция, которая возвращает список всех руководителей
    :param request:
    :param session:
    :return:
    """
    try:
        directors = session.exec(select(Director)).all()
        return templates_director.TemplateResponse(
            "all_directors.html",
            context={"request": request, 'directors': directors}
        )
    except Exception as e:
        return {"Ошибка": e}

@GetRouter.get("/get_director_by_id")
async def get_director_by_id(session: SessionDep,
                             id: Annotated[str, Query(pattern = r"^\d{6}$")]):
    """
    Функция, которая возвращает результат поиска руководителя по ID
    :param session:
    :param id:
    :return:
    """
    try:
        director = session.get(Director, id)
        if not director:
            return HTTPException(status_code = 404, detail = "Руководителя с таким ID нет")
        return director
    except Exception as e:
        return HTTPException(status_code = 404, detail = e)

@GetRouter.get("/get_director_by_surname_and_name")
async def get_director_by_surname_and_name(session: SessionDep,
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
        directors = session.exec(select(Director).where(or_(Director.surname == surname, Director.name == name))).all()
        if not directors:
            raise HTTPException(status_code = 404, detail = "Руководителей с такими данными нет")
        return templates_director.TemplateResponse(
            "get_director_by_name_and_surname.html",
            context={"request": request,
                     'directors': directors}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@GetRouter.get("/add_director")
async def add_director_form(request: Request):
    """
    Функция, которая возвращает форму для добавления директора
    :param request:
    :return:
    """
    return templates_director.TemplateResponse(
        "add_director.html",
        context = {"request": request}
    )

@GetRouter.get("/search_director_form")
async def search_director_form(request: Request):
    """
    Функция, которая возвращает форму для поиска руководителя
    :param request:
    :return:
    """
    return templates_director.TemplateResponse(
        "search_director_form.html",
        context = {"request": request}
    )


"""
Ниже функции для работы с кафедрами
"""
@GetRouter.get("/get_all_department")
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

@GetRouter.get("/get_department_by_code_department")
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

@GetRouter.get("/add_department")
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


"""
Ниже функции для работы со специальностями
"""
@GetRouter.get("/get_all_specialization")
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
        return templates_department.TemplateResponse(
            "all_specializations.html",
            context={"request": request, 'specializations': specializations}
        )
    except Exception as e:
        return {"Ошибка": e}

@GetRouter.get("/get_specialization_by_code_specialization")
async def get_specialization_by_code_specialization(session: SessionDep,
                                                    code_specialization: Annotated[str, Query(pattern = r"^\d{8}$")]):
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

@GetRouter.get("/add_specialization")
async def add_specialization_form(request: Request):
    """
    Функция, которая возвращает форму для добавления специальности
    :param request:
    :return:
    """
    return templates_department.TemplateResponse(
        "add_specialization.html",
        context = {"request": request}
    )