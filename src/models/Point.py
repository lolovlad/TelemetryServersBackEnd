from pydantic import BaseModel
from datetime import datetime


class TypePoint(BaseModel):
    id: int
    name: str
    notation: str
    description: str
    type_data: str


class BasePoint(BaseModel):
    value: str
    default_value: str = "0.0"


class PostPoint(BasePoint):
    id_type_point: int


class GetPoint(BasePoint):
    type_point: TypePoint
    datareg: datetime


class OneGrade(BaseModel):
    type_point: TypePoint
    grade: int


class GradeEquipment(BaseModel):
    all_grade: int
    list_grades: list[OneGrade]
