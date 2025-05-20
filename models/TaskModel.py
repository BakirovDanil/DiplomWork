from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    group: str = Field()
    teacher_surname: str = Field()
    teacher_name: str = Field()
    result: str = Field()
    student_number_gradebook: int = Field(default = None, foreign_key = "student.number_gradebook", primary_key = True)


class Task(TaskBase, table = True):
    id: int | None = Field(default = None, primary_key = True)
