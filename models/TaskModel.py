from sqlmodel import Field, SQLModel


class ReportBase(SQLModel):
    result: str = Field()
    number_gradebook: str = Field(default=None, foreign_key="student.number_gradebook")


class Report(ReportBase, table = True):
    report_id: int = Field(default = None, primary_key = True)
