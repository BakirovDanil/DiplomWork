from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    student_surname: str = Field(index = True)
    student_name: str = Field()
    group: str = Field()
    teacher_surname: str = Field()
    teacher_name: str = Field()
    result: str = Field()


class Task(TaskBase, table = True):
    id: int | None = Field(default = None, primary_key = True)