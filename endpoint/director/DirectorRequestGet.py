from typing import Annotated

from fastapi import HTTPException, APIRouter, Request, Query, Depends

from models.CharacterModels import Director
from security.authorization import verification_of_the_head_or_deputy, verification_of_the_director
from database.ConnectionDB import SessionDep
from sqlmodel import select, or_
from fastapi.templating import Jinja2Templates

DirectorGetRouter = APIRouter()
templates_director = Jinja2Templates(directory = "templates/director")

"""
Ниже функции для работы с руководителями
"""
@DirectorGetRouter.get("/get_all_director")
async def get_all_director(session: SessionDep,
                           request: Request,
                           current_user: Annotated[str, Depends(verification_of_the_director)]):
    """
    Функция, которая возвращает список всех руководителей
    :param current_user:
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

@DirectorGetRouter.get("/get_director_by_id")
async def get_director_by_id(session: SessionDep,
                             request: Request,
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
        return templates_director.TemplateResponse(
            "get_director_by_id.html",
            context = {'request': request,
                       'director': director}
        )
    except Exception as e:
        return HTTPException(status_code = 404, detail = e)

@DirectorGetRouter.get("/get_director_by_surname_and_name")
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
            "get_director_by_surname_and_name.html",
            context={"request": request,
                     'directors': directors}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@DirectorGetRouter.get("/add_director")
async def add_director_form(request: Request,
                            current_user: Annotated[str, Depends(verification_of_the_head_or_deputy)]):
    """
    Функция, которая возвращает форму для добавления директора
    :param request:
    :return:
    """
    return templates_director.TemplateResponse(
        "add_director.html",
        context = {"request": request}
    )

@DirectorGetRouter.get("/search_director_form_by_surname_and_name")
async def search_director_form(request: Request,
                               current_user: Annotated[str, Depends(verification_of_the_head_or_deputy)]):
    """
    Функция, которая возвращает форму для поиска руководителя по фамилии и имени
    :param current_user:
    :param request:
    :return:
    """
    return templates_director.TemplateResponse(
        "search_director_form_by_surname_and_name.html",
        context = {"request": request}
    )

@DirectorGetRouter.get("/search_director_form_by_id")
async def search_director_form(request: Request,
                               current_user: Annotated[str, Depends(verification_of_the_head_or_deputy)]):
    """
    Функция, которая возвращает форму для поиска руководителя по id
    :param current_user:
    :param request:
    :return:
    """
    return templates_director.TemplateResponse(
        "search_director_form_by_id.html",
        context = {"request": request}
    )