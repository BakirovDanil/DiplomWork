from contextlib import asynccontextmanager
from endpoint.department.DepartmentRequestPost import DepartmentPostRouter
from endpoint.director.DirectorRequestPost import DirectorPostRouter
from endpoint.report.ReportRequestPost import ReportPostRouter
from endpoint.specialization.SpecializationRequestPost import SpecializationPostRouter
from endpoint.student.StudentRequestPost import StudentPostRouter
from endpoint.MainRequestGet import MainGetRouter
from endpoint.department.DepartmentRequestGet import DepartmentGetRouter
from endpoint.director.DirectorRequestGet import DirectorGetRouter
from endpoint.report.ReportRequestGet import ReportGetRouter
from endpoint.specialization.SpecializationRequestGet import SpecializationGetRouter
from endpoint.student.StudentRequestGet import StudentGetRouter
from database.ConnectionDB import create_db_and_tables
import uvicorn
from fastapi import FastAPI

GetRouter = [MainGetRouter, DepartmentGetRouter, DirectorGetRouter,
             ReportGetRouter, SpecializationGetRouter, StudentGetRouter]

PostRouter = [DepartmentPostRouter, DirectorPostRouter, ReportPostRouter,
              SpecializationPostRouter, StudentPostRouter]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan = lifespan)
for post_router in PostRouter:
    app.include_router(post_router)
for get_router in GetRouter:
    app.include_router(get_router)

if __name__ == "__main__":
    uvicorn.run("main:app",port=8080, reload=True)