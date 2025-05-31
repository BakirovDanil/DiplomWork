from fastapi import Form, HTTPException, APIRouter, Request
from typing import Annotated
from fastapi.templating import Jinja2Templates
from models.CharacterModels import StudentBase, Student, Department, Specialization
from database.ConnectionDB import SessionDep

StudentPostRouter = APIRouter()
templates_student = Jinja2Templates(directory = "templates/student")

@StudentPostRouter.post("/add_student")
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
        return templates_student.TemplateResponse(
            "add_student.html",
            {
                "request": request,
                "success_message": "Студент был добавлен",
                "student": student
            }
        )
    except Exception as e:
        return templates_student.TemplateResponse(
            "add_student.html",
            {
                "request": request,
                "error_message": f"Ошибка: {str(e)}"
            },
            status_code=500
        )