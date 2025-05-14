from sqlmodel import Field, SQLModel

class DepartmentBase(SQLModel):
    name: str = Field(index = True)
    faculty: str = Field()

class Department(DepartmentBase, table = True):
    id: int | None = Field(default=None, primary_key=True)

class StudentBase(SQLModel):
    name: str = Field(index = True)
    age: int | None = Field(default = True, index = True)
    department_id: int = Field(default = None, foreign_key = "department.id")

class Student(StudentBase, table = True):
    id: int | None = Field(default=None, primary_key=True)