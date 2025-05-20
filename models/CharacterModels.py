from sqlmodel import Field, SQLModel

"""
Классы кафедры
"""
class DepartmentBase(SQLModel):
    code_department: str = Field()
    name: str = Field(index = True)
    faculty: str = Field()

class Department(DepartmentBase, table = True):
    code_department: str = Field(index = True, primary_key=True)


"""
Классы специальности
"""
class SpecializationBase(SQLModel):
    code_specialization: str = Field()
    name: str = Field()
    profile: str = Field()
    form_of_education: str = Field()
    level_of_education: str = Field()
    department_id: str = Field(default = None, foreign_key = "department.id")

class Specialization(SpecializationBase, table = True):
    code_specialization: str = Field(index = True, primary_key = True)


"""
Классы студента
"""
class StudentBase(SQLModel):
    number_gradebook: str = Field()
    name: str = Field(index = True)
    age: int | None = Field(default = None, index = True)
    department_id: int = Field(default = None, foreign_key = "department.id")

class Student(StudentBase, table = True):
    number_gradebook: str = Field(index = True, primary_key = True)


"""
Классы руководителя
"""
class DirectorBase(SQLModel):
    surname: str = Field(index = True)
    name: str = Field()
    patronymic: str = Field()
    academic_title: str = Field()
    post: str = Field()
    department_id: int = Field(default = None, foreign_key = "department.id")

class Director(DirectorBase, table = True):
    id: int = Field(index = True, primary_key = True)


