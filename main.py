from endpoint.RequestPost import PostRouter
from endpoint.RequestGet import GetRouter
from database.ConnectionDB import create_db_and_tables
import uvicorn
from fastapi import FastAPI

app = FastAPI()
app.include_router(PostRouter)
app.include_router(GetRouter)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

if __name__ == "__main__":
    uvicorn.run("main:app",port=8080, reload=True)