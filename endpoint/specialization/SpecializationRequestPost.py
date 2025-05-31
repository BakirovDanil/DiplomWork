from fastapi import Form, HTTPException, APIRouter, Request
from typing import Annotated
from fastapi.templating import Jinja2Templates

from models.CharacterModels import Specialization, SpecializationBase
from database.ConnectionDB import SessionDep

SpecializationPostRouter = APIRouter()
templates_specialization = Jinja2Templates(directory = "templates/specialization")

@SpecializationPostRouter.post("/add_specialization")
async def add_specialization(code_specialization: Annotated[str, Form(pattern = r"^\d{2}\.\d{2}\.\d{2}$")],
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
        return templates_specialization.TemplateResponse(
            "add_specialization.html",
            {
                "request": request,
                "success_message": "Кафедра была добавлена",
                "specialization": specialization
            }
        )
    except Exception as e:
        return templates_specialization.TemplateResponse(
            "add_specialization.html",
            {
                "request": request,
                "error_message": f"Ошибка: {str(e)}"
            },
            status_code=500
        )
