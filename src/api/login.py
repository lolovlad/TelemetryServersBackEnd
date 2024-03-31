from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from ..models.User import UserLogin, Token, UserSigIn, UserGet
from ..models.Message import Message
from ..services import LoginServices

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/sign-in", response_model=Token, responses={status.HTTP_406_NOT_ACCEPTABLE: {"model": Message}})
async def sign_in(request: Request,
                  form_data: OAuth2PasswordRequestForm = Depends(),
                  login_services: LoginServices = Depends()):
    user = await login_services.login_user(UserLogin(login=form_data.username,
                                                     password=form_data.password))
    if user:
        return user
    else:
        return JSONResponse(content={"message": "неправильный логин или пароль"},
                            status_code=status.HTTP_406_NOT_ACCEPTABLE)