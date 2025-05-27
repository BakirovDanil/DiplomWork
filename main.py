from contextlib import asynccontextmanager
from endpoint.RequestPost import PostRouter
from endpoint.RequestGet import GetRouter
from database.ConnectionDB import create_db_and_tables
import uvicorn
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan = lifespan)
app.include_router(PostRouter)
app.include_router(GetRouter)

if __name__ == "__main__":
    uvicorn.run("main:app",host = '0.0.0.0', port=8080, reload=True)