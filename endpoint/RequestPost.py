from fastapi import UploadFile, Form, File, HTTPException, APIRouter, Request
from fastapi.responses import JSONResponse
from docx import Document
import json
from fastapi.templating import Jinja2Templates

from methods.CheckingCodes import search_chapter_codes, search_picture_codes
from models.CharacterModels import StudentBase, Student, Department, DepartmentBase, Specialization, SpecializationBase, Director, DirectorBase
from models.TaskModel import Task, TaskBase
from typing import Annotated
from database.ConnectionDB import SessionDep

PostRouter = APIRouter()
templates = Jinja2Templates(directory = "templates")

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

@PostRouter.post("/add_student")
async def add_student(number_gradebook: Annotated[str, Form(pattern = r"^\d{8}$")],
                      surname: Annotated[str, Form()],
                      name: Annotated[str, Form()],
                      patronymic: Annotated[str, Form()],
                      group_number: Annotated[str, Form()],
                      code_specialization: Annotated[str, Form()],
                      code_department: Annotated[str, Form()],
                      session: SessionDep,
                      request: Request):
    """
    Функция, которая добавляет нового студента в базу данных
    :param code_department:
    :param code_specialization:
    :param group_number:
    :param patronymic:
    :param surname:
    :param number_gradebook:
    :param name:
    :param session:
    :param request:
    :return:
    """
    try:
        check_code_department = session.get(Department, code_department)
        check_code_specialization = session.get(Specialization, code_specialization)
        check_number_gradebook = session.get(Student, number_gradebook)
        if not check_code_department:
            raise HTTPException(status_code = 404, detail = "Кафедра с таким кодом не найдена")
        if not check_code_specialization:
            raise HTTPException(status_code = 404, detail = "Специальность с таким кодом не найдена")
        if check_number_gradebook:
            raise HTTPException(status_code = 404, detail = "Студент с такой зачеткой есть в базе")
        student = StudentBase(
            number_gradebook = number_gradebook,
            surname = surname,
            name = name,
            patronymic = patronymic,
            group_number = group_number,
            code_specialization = code_specialization,
            code_department = code_department
        )
        student = Student.model_validate(student)
        session.add(student)
        session.commit()
        session.refresh(student)
        return templates.TemplateResponse(
            "add_student.html",
            {
                "request": request,
                "success_message": "Студент был добавлен",
                "student": student
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "add_student.html",
            {
                "request": request,
                "error_message": f"Ошибка: {str(e)}"
            },
            status_code=500
        )

@PostRouter.post("/add_department")
async def add_department(code_department: Annotated[str, Form()],
                         name: Annotated[str, Form()],
                         faculty: Annotated[str, Form()],
                         phone_number: Annotated[str, Form()],
                         mail: Annotated[str, Form()],
                         session: SessionDep,
                         request: Request):
    """
    Функция, которая добавляет новую кафедру в базу данных
    :param request:
    :param mail:
    :param phone_number:
    :param code_department:
    :param name:
    :param faculty:
    :param session:
    :return:
    """
    try:
        check_code_department = session.get(Department, code_department)
        if check_code_department:
            raise HTTPException(status_code=404, detail="Кафедра с таким кодом уже есть")
        department = DepartmentBase(
            code_department = code_department,
            name = name,
            faculty = faculty,
            phone_number = phone_number,
            mail = mail
        )
        department = Department.model_validate(department)
        session.add(department)
        session.commit()
        session.refresh(department)
        return templates.TemplateResponse(
            "add_department.html",
            {
                "request": request,
                "success_message": "Кафедра была добавлена",
                "department": department
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "add_department.html",
            {
                "request": request,
                "error_message": f"Ошибка: {str(e)}"
            },
            status_code=500
        )

@PostRouter.post("/add_specialization")
async def add_specialization(code_specialization: Annotated[str, Form()],
                             name: Annotated[str, Form()],
                             profile: Annotated[str, Form()],
                             form_of_education: Annotated[str, Form()],
                             level_of_education: Annotated[str, Form()],
                             code_department: Annotated[str, Form()],
                             session: SessionDep,
                             request: Request):
    """
    Функция, которая добавляет специальность в базу данных
    :param code_specialization:
    :param name:
    :param profile:
    :param form_of_education:
    :param level_of_education:
    :param code_department:
    :param session:
    :param request:
    :return:
    """
    try:
        check_code_specialization = session.get(Specialization, code_specialization)
        if check_code_specialization:
            raise HTTPException(status_code=404, detail="Специальность с таким кодом уже есть")
        specialization = SpecializationBase(
            code_specialization = code_specialization,
            name = name,
            profile = profile,
            form_of_education = form_of_education,
            level_of_education = level_of_education,
            code_department = code_department
        )
        specialization = Specialization.model_validate(specialization)
        session.add(specialization)
        session.commit()
        session.refresh(specialization)
        return templates.TemplateResponse(
            "add_specialization.html",
            {
                "request": request,
                "success_message": "Кафедра была добавлена",
                "specialization": specialization
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "add_specialization.html",
            {
                "request": request,
                "error_message": f"Ошибка: {str(e)}"
            },
            status_code=500
        )

@PostRouter.post("/add_director")
async def add_director(id: Annotated[str, Form(pattern = r"^\d{6}$")],
                      surname: Annotated[str, Form()],
                      name: Annotated[str, Form()],
                      patronymic: Annotated[str, Form()],
                      academic_title: Annotated[str, Form()],
                      post: Annotated[str, Form()],
                      code_department: Annotated[str, Form()],
                      session: SessionDep,
                      request: Request):
    """
    Функция, которая добавляет нового студента в базу данных
    :param post:
    :param academic_title:
    :param id:
    :param code_department:
    :param patronymic:
    :param surname:
    :param name:
    :param session:
    :param request:
    :return:
    """
    try:
        check_id_director = session.get(Director, id)
        if check_id_director:
            raise HTTPException(status_code=404, detail="Руководитель с таким ID уже есть")
        director = DirectorBase(
            id = id,
            surname = surname,
            name=name,
            patronymic = patronymic,
            academic_title = academic_title,
            post = post,
            code_department=code_department
        )
        director = Director.model_validate(director)
        session.add(director)
        session.commit()
        session.refresh(director)
        return templates.TemplateResponse(
            "add_director.html",
            {
                "request": request,
                "success_message": "Руководитель был добавлен",
                "director": director
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "add_director.html",
            {
                "request": request,
                "error_message": f"Ошибка: {str(e)}"
            },
            status_code=500
        )

@PostRouter.post("/check_document")
async def check_document(student_id: Annotated[int, Form()],
                         group: Annotated[str, Form()],
                         teacher_surname: Annotated[str, Form()],
                         teacher_name: Annotated[str, Form()],
                         file: Annotated[UploadFile, File()],
                         session: SessionDep):
    """
    Функция, которая возвращает результат проверки загруженного документа
    :param student_id:
    :param session:
    :param teacher_name:
    :param teacher_surname:
    :param group:
    :param file:
    :return:
    """
    try:
        document = Document(file.file)
        chapter_status = await search_chapter_codes(open_base_rules('rules/section_rules.json'),document) # проверка по содержанию
        picture_status = await search_picture_codes(open_base_rules('rules/section_rules.json'), document) # проверка по рисункам
        result = {
            "Отчет по разделам": chapter_status,
            "Отчет по рисункам": picture_status
        }
        checking_result = str(result)
        diplom_work_information = TaskBase(
            student_id = student_id,
            group = group,
            teacher_surname = teacher_surname,
            teacher_name = teacher_name,
            result = checking_result
        )
        diplom_work_information = Task.model_validate(diplom_work_information)
        session.add(diplom_work_information)
        session.commit()
        session.refresh(diplom_work_information)
        return result
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)