from fastapi import  Form, HTTPException, APIRouter, Request
from typing import Annotated, Literal
from fastapi.templating import Jinja2Templates
from models.CharacterModels import Department, DepartmentBase
from database.ConnectionDB import SessionDep

templates_department = Jinja2Templates(directory = "templates/department")
DepartmentPostRouter = APIRouter()

@DepartmentPostRouter.post("/add_department")
async def add_department(code_department: Annotated[str, Form(pattern = r"^\d{8}$")],
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
        return templates_department.TemplateResponse(
            "add_department.html",
            {
                "request": request,
                "success_message": "Кафедра была добавлена",
                "department": department
            }
        )
    except Exception as e:
        return templates_department.TemplateResponse(
            "add_department.html",
            {
                "request": request,
                "error_message": f"Ошибка: {str(e)}"
            },
            status_code=500
        )