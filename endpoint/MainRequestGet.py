from fastapi import APIRouter, Request

from fastapi.templating import Jinja2Templates

MainGetRouter = APIRouter()
templates_main = Jinja2Templates(directory = "templates/main_page")

templates_specialization = Jinja2Templates(directory = "templates/specialization")

@MainGetRouter.get("/")
async def base_page(request: Request):
    return templates_main.TemplateResponse(
        "base.html",
        context = {"request": request}
    )











