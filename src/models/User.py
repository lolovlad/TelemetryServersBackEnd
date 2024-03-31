from pydantic import BaseModel, UUID4, field_serializer


class TypeUser(BaseModel):
    id: int
    name: str
    description: str


class UserBase(BaseModel):
    uuid: UUID4
    login: str

    @field_serializer('uuid')
    def serialize_uuid(self, uuid: UUID4, _info):
        return str(uuid)


class UserGet(UserBase):
    type: TypeUser


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: UserGet


class UserSigIn(BaseModel):
    user: UserGet
    token: Token


class UserLogin(BaseModel):
    login: str
    password: str