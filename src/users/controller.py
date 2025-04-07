from fastapi import APIRouter, HTTPException, status
from uuid import UUID

from ..database.core import DbSession
from . import models
from . import service
from ..auth.service import CurrentUser

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# @router.get("/me", response_model=models.UserResponse)
# def get_current_user(current_user: CurrentUser, db: DbSession):
#     print("Current user ID:", current_user.get_uuid())
#     return service.get_user_by_id(db, current_user.get_uuid())

@router.get("/me", response_model=models.UserResponse)
def get_current_user(current_user: CurrentUser, db: DbSession):
    user_id = current_user.get_uuid()
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user ID")
    
    try:
        user = service.get_user_by_id(db, user_id)
        return user
    except HTTPException as e:
        raise e


@router.put("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    password_change: models.PasswordChange,
    db: DbSession,
    current_user: CurrentUser
):
    service.change_password(db, current_user.get_uuid(), password_change)
