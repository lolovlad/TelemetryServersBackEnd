from src.tables import User, TypeUser, TypePoint
from src.database import async_session
from asyncio import run
from uuid import uuid4


async def create_point_context():
    async with async_session() as session:
        type_points = [
            TypePoint(
                name="temperature",
                notation="t",
                type_data="float",
                description="Температура"

            ),
            TypePoint(
                name="humidity",
                notation="%",
                type_data="float",
                description="Влажность"
            ),
            TypePoint(
                name="leak",
                notation="",
                type_data="bool",
                description="Протечка"
            ),
            TypePoint(
                name="dust",
                notation="",
                type_data="bool",
                description="пыль"
            ),
            TypePoint(
                name="gas",
                notation="",
                type_data="bool",
                description="газовый"
            ),
            TypePoint(
                name="disk_size",
                notation="Gb",
                type_data="float",
                description="Размер диска"
            ),
            TypePoint(
                name="CPU_load",
                notation="%",
                type_data="float",
                description="Нагрузка процессора"
            ),
            TypePoint(
                name="CPU_temperature",
                notation="t",
                type_data="int",
                description="Температура процессора"
            ),
            TypePoint(
                name="cooler_rotation_speed",
                notation="об/c",
                type_data="int",
                description="Скорость вращения кулера"
            )

        ]

        session.add_all(type_points)
        await session.commit()


async def create_user_context():
    async with async_session() as session:
        types_user = [
            TypeUser(
                name="admin",
                description="admin"
            ),
            TypeUser(
                name="user",
                description="user"
            ),
            TypeUser(
                name="equipment",
                description="equipment"
            )
        ]

        user_admin = User(
            uuid=uuid4(),
            login="admin",
            id_type=1
        )

        user_mob = User(
            uuid=uuid4(),
            login="mobile",
            id_type=2
        )

        user_equ_1 = User(
            uuid=uuid4(),
            login="server_room_1",
            id_type=3
        )

        user_equ_2 = User(
            uuid=uuid4(),
            login="server_pc_1",
            id_type=3
        )

        user_admin.password = "admin"
        user_mob.password = "mobile"
        user_equ_1.password = "server_room_1"
        user_equ_2.password = "server_pc_1"

        session.add_all(types_user)
        session.add_all([
            user_admin,
            user_mob,
            user_equ_1,
            user_equ_2
        ])

        await session.commit()


async def main():
    await create_point_context()
    await create_user_context()


run(main())