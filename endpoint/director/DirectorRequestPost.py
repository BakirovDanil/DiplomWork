from fastapi import  Form, HTTPException, APIRouter, Request
from typing import Annotated, Literal
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from models.CharacterModels import Department, Director, DirectorBase
from database.ConnectionDB import SessionDep

DirectorPostRouter = APIRouter()
ROLES = Literal["Заведующий", "Заместитель", "Преподаватель"]
templates_director = Jinja2Templates(directory = "templates/director")

@DirectorPostRouter.post("/add_director")
async def add_director(id: Annotated[str, Form(pattern = r"^\d{6}$")],
                       surname: Annotated[str, Form()],
                       name: Annotated[str, Form()],
                       patronymic: Annotated[str, Form()],
                       academic_title: Annotated[str, Form()],
                       post: Annotated[ROLES, Form()],
                       code_department: Annotated[str, Form()],
                       password: Annotated[str, Form()],
                       session: SessionDep,
                       request: Request):
    """
    Функция, которая добавляет нового руководителя в базу данных
    :param password:
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
        check_code_department = session.get(Department, code_department)
        if not check_code_department:
            raise HTTPException(status_code = 404, detail = "Нет кафедры с таким кодом")
        if post in ("Заведующий", "Заместитель"):
            check_post_director = session.exec(select(Director).where(Director.post == post)).first()
            if check_post_director:
                raise HTTPException(status_code = 404, detail = "Невозможно добавить еще одно заведующего или заместителя")
        director = DirectorBase(
            id = id,
            surname = surname,
            name=name,
            patronymic = patronymic,
            academic_title = academic_title,
            post = post,
            password = password,
            code_department=code_department,
        )
        director = Director.model_validate(director)
        session.add(director)
        session.commit()
        session.refresh(director)
        return templates_director.TemplateResponse(
            "add_director.html",
            {
                "request": request,
                "success_message": "Руководитель был добавлен",
                "director": director
            }
        )
    except Exception as e:
        raise HTTPException(status_code = 404, detail = str(e))