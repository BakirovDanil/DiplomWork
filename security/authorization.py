from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from sqlmodel import select, or_
from database.ConnectionDB import SessionDep
from models.CharacterModels import Director
from typing import Annotated

security = HTTPBasic()
def verification_of_the_head_or_deputy(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                         session: SessionDep):
    """
    Функция, которая проверяет, является ли пользователь Заведующим или Заместителем
    :param credentials:
    :param session:
    :return:
    """
    director = session.exec(select(Director).where(Director.id == credentials.username,
                                                   or_(Director.post == "Заведующий", Director.post == "Заместитель"))).first()
    if director is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Некорректное имя пользователя или некорректная должность",
            headers = {"WWW-Authenticate": "Basic"}
        )
    is_correct_password = secrets.compare_digest(
        credentials.password.encode("utf8"), director.password.encode("utf8")
    )
    if not is_correct_password:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Неверный пароль пользователя",
            headers={"WWW-Authenticate": "Basic"}
        )

def verification_of_the_director(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                         session: SessionDep):
    """
    Функция, которая проверяет, является ли пользователь руководителем
    :param credentials:
    :param session:
    :return:
    """
    director = session.exec(select(Director).where(Director.id == credentials.username)).first()
    if director is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Некорректное имя пользователя",
            headers = {"WWW-Authenticate": "Basic"}
        )
    is_correct_password = secrets.compare_digest(
        credentials.password.encode("utf8"), director.password.encode("utf8")
    )
    if not is_correct_password:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Неверный пароль пользователя",
            headers={"WWW-Authenticate": "Basic"}
        )