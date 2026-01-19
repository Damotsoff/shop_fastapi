from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from auth import utils as auth_utils
from users.schemas import UserSchema

router = APIRouter(prefix="/jwt", tags=["JWT"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/demo-auth/jwt/login/")


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = "Bearer"


john = UserSchema(
    username="john",
    password=auth_utils.hash_password("qwerty"),
    email="john@example.com",
)


sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password("secret"),
)

user_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}


def validate_auth_user(username: str = Form(), password: str = Form()):
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not (user := user_db.get(username)):
        raise unauthorized_exception
    if not auth_utils.validate_password(password, user.password):
        raise unauthorized_exception
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user


def get_current_token_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials token: {str(e)}",
        ) from e
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username = payload.get("sub")

    if not isinstance(username, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = user_db.get(username)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
    )



def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Inactive user",
    )


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user)):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = auth_utils.encode_jwt(payload=jwt_payload)
    return TokenInfo(access_token=token)


@router.get("/users/me/")
async def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {"username": user.username, "email": user.email, "logged_in_at": iat}
