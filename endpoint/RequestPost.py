from fastapi import UploadFile, Form, File, HTTPException, APIRouter, Request
from fastapi.responses import JSONResponse
from docx import Document
import json
from fastapi.templating import Jinja2Templates

from methods.CheckingCodes import search_chapter_codes, search_picture_codes
from models.CharacterModels import StudentBase, Student,Department, DepartmentBase
from models.TaskModel import Task, TaskBase
from typing import Annotated
from database.ConnectionDB import SessionDep

PostRouter = APIRouter()
templates = Jinja2Templates(directory = "templates")

def open_base_rules(file: str) -> dict:
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        base_rules = data["base_rules"]
        return base_rules

@PostRouter.post("/add_student")
async def add_student(number_gradebook: Annotated[str, Form(pattern = r"^\d{8}$")],
                      name: Annotated[str, Form()],
                      age: Annotated[int, Form()],
                      department_id: Annotated[int, Form()],
                      session: SessionDep,
                      request: Request):
    try:
        department = session.get(Department, department_id)
        check_number_gradebook = session.get(Student, number_gradebook)
        if not department:
            raise HTTPException(status_code = 404, detail = "Отдел с таким id не найден")
        if check_number_gradebook:
            raise HTTPException(status_code = 404, detail = "Студент с такой зачеткой есть в базе")
        student = StudentBase(
            number_gradebook = number_gradebook,
            name = name,
            age = age,
            department_id = department_id
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
async def add_department(name: Annotated[str, Form()],
                         faculty: Annotated[str, Form()],
                         session: SessionDep):
    try:
        department = DepartmentBase(
            name = name,
            faculty = faculty
        )
        department = Department.model_validate(department)
        session.add(department)
        session.commit()
        session.refresh(department)
        return {"ok": "Запись добавлена"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

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