from fastapi import Depends, HTTPException, status

from ..repositories import PointRepository, UserRepository, TypePointRepository
from ..models.Point import PostPoint, TypePoint, GetPoint, OneGrade, GradeEquipment
from ..tables import Point

from datetime import datetime
from math import fabs


class PointServices:
    def __init__(self,
                 point_repository: PointRepository = Depends(),
                 user_repository: UserRepository = Depends(),
                 type_point_repository: TypePointRepository = Depends()):
        self.__point_repository: PointRepository = point_repository
        self.__user_repository: UserRepository = user_repository
        self.__type_point_repository: TypePointRepository = type_point_repository

    async def app_point(self, uuid_user: str, point_data: PostPoint):
        user = await self.__user_repository.get_by_uuid(uuid_user)
        point = Point(
            id_user=user.id,
            id_type_point=point_data.id_type_point,
            value=point_data.value,
            default_value=point_data.default_value
        )
        try:
            await self.__point_repository.add(point)
        except Exception:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async def get_type_point_all(self) -> list[TypePoint]:
        entity = await self.__type_point_repository.get_all()
        return [TypePoint.model_validate(i, from_attributes=True) for i in entity]

    async def get_list_point_all(self, date: str, uuid_user: str) -> list[GetPoint]:
        user = await self.__user_repository.get_by_uuid(uuid_user)
        date = datetime.strptime(date, '%d.%m.%Y')
        entity_point = await self.__point_repository.list_point_in_data_all(date, user.id)
        return [GetPoint.model_validate(i, from_attributes=True) for i in entity_point]

    async def get_list_point_type(self, date: str, uuid_user: str, type_point: int) -> list[GetPoint]:
        user = await self.__user_repository.get_by_uuid(uuid_user)
        date = datetime.strptime(date, '%d.%m.%Y')
        entity_point = await self.__point_repository.list_point_in_data_type(date, user.id, type_point)
        return [GetPoint.model_validate(i, from_attributes=True) for i in entity_point]

    def __deviation(self, val: float | int, val_usr: float | int) -> float:
        return fabs((val * 100 / val_usr) - 100)

    def __grade_to_type_point(self, point: Point) -> int:
        if point.type_point.name in ("leak", "dust", "gas"):
            if point.type_point.type_data == "bool":
                val = bool(int(point.value))
                if val:
                    return 3
                return 1
        elif point.type_point.name in ("temperature", "humidity"):
            if point.type_point.type_data == "float":
                val = float(point.value)
                val_ust = float(point.default_value)
                dev = self.__deviation(val, val_ust)
                if dev < 10:
                    return 1
                elif 10 <= dev < 20:
                    return 2
                else:
                    return 3
        elif point.type_point.name == "disk_size":
            if point.type_point.type_data == "float":
                val = float(point.value)
                val_ust = float(point.default_value)
                dev = self.__deviation(val, val_ust)
                if dev > 30:
                    return 1
                elif 30 >= dev >= 20:
                    return 2
                else:
                    return 3
        elif point.type_point.name == "CPU_load":
            if point.type_point.type_data == "float":
                val = float(point.value)
                if val < 70:
                    return 1
                elif 70 <= val < 85:
                    return 2
                else:
                    return 3

        else:
            return 1

    async def grade_equipment(self, date: str, uuid_user: str, type_point: str) -> GradeEquipment:
        list_type_point = list(map(int, type_point.split(",")))

        user = await self.__user_repository.get_by_uuid(uuid_user)
        date = datetime.strptime(date, '%d.%m.%Y')

        grades = []

        all_grade = 1

        for type_point in list_type_point:
            point = await self.__point_repository.get_last_points_in_date(date, user.id, type_point)

            grade = self.__grade_to_type_point(point)
            one_grade = OneGrade(grade=grade,
                                 type_point=TypePoint.model_validate(point.type_point, from_attributes=True))
            grades.append(one_grade)

            if all_grade < grade:
                all_grade = grade

        return GradeEquipment(
            all_grade=all_grade,
            list_grades=grades
        )