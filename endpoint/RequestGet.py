from fastapi import HTTPException, APIRouter
from models.TaskModel import Task
from database.ConnectionDB import SessionDep
from sqlmodel import select

GetRouter = APIRouter()

@GetRouter.get("/get_all")
async def get_all_result(session: SessionDep):
    result = session.exec(select(Task)).all()
    return result


@GetRouter.get("/get_by_id")
async def get_result_by_id(value: int, session: SessionDep):
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