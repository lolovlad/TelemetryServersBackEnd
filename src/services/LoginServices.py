from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


from ..tables import User
from ..models.User import UserGet, UserLogin, Token

from ..repositories import UserRepository
from ..settings import settings
from datetime import datetime, timedelta


oauth2_cheme = OAuth2PasswordBearer(tokenUrl='/v1/login/sign-in/')


def get_current_user(token: str = Depends(oauth2_cheme)) -> UserGet:
    return LoginServices.validate_token(token)


class LoginServices:
    def __init__(self, repository: UserRepository = Depends()):
        self.__repository: UserRepository = repository

    @classmethod
    def validate_token(cls, token: str) -> UserGet:
        exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail="token",
                                  headers={
                                      "TelServer": 'Bearer'
                                  })
        try:
            payload = jwt.decode(token,
                                 settings.jwt_secret,
                                 algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise exception

        user_data = payload.get("user")

        try:
            user = UserGet.model_validate(user_data)
        except Exception:
            raise exception
        return user

    @classmethod
    def create_token(cls, user: User) -> Token:
        user_data = UserGet.model_validate(user, from_attributes=True)

        now = datetime.utcnow()

        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(user_data.uuid),
            'user': user_data.model_dump()
        }
        token = jwt.encode(payload,
                           settings.jwt_secret,
                           algorithm=settings.jwt_algorithm)
        return Token(access_token=token, user=user_data.model_dump())

    async def login_user(self, user_login: UserLogin) -> Token:
        user = await self.__repository.get_user_by_login(user_login.login)
        if user:
            if user.check_password(user_login.password):
                return self.create_token(user)