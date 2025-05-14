from fastapi import UploadFile, Form, File, HTTPException, APIRouter, Depends
from fastapi.responses import JSONResponse
from docx import Document
import json

from methods.CheckingCodes import search_chapter_codes, search_picture_codes
from models.CharacterModels import Student, StudentBase, Department, DepartmentBase
from models.TaskModel import Task, TaskBase
from typing import Annotated
from database.ConnectionDB import SessionDep

PostRouter = APIRouter()

def open_base_rules(file: str) -> dict:
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        base_rules = data["base_rules"]
        return base_rules

@PostRouter.post("/add_student")
async def add_student(name: Annotated[str, Form()],
                      age: Annotated[int, Form()],
                      department_id: Annotated[int, Form()],
                      session: SessionDep):
    try:
        department = session.get(Department, department_id)
        if not department:
            raise HTTPException(status_code = 404, detail = "Отдел с таким id не найден")
        student = StudentBase(
            name = name,
            age = age,
            department_id = department_id
        )
        session.add(Student.model_validate(student))
        session.commit()
        session.refresh(student)
        return {"ok": "Запись добавлена"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code = 500, detail = "Данные не добавлены")

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
async def check_document(student_surname: Annotated[str, Form()],
                         student_name: Annotated[str, Form()],
                         group: Annotated[str, Form()],
                         teacher_surname: Annotated[str, Form()],
                         teacher_name: Annotated[str, Form()],
                         file: Annotated[UploadFile, File()],
                         session: SessionDep):
    """
    Функция, которая возвращает результат проверки загруженного документа
    :param session:
    :param teacher_name:
    :param teacher_surname:
    :param student_name:
    :param student_surname:
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
            student_surname = student_surname,
            student_name = student_name,
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