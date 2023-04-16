from bson.objectid import ObjectId
import json
from utils.database import user_collection
from functools import wraps
from fastapi_jwt_auth import AuthJWT
from fastapi import FastAPI, HTTPException, Depends, Request


def generate_access_jwt_token(Authorize, inserted_id, email, hashed_pass):
    access_token = Authorize.create_access_token(
        subject=json.dumps(
            {"_id": inserted_id, "email": email, "hashed_pass": hashed_pass}
        ),
        expires_time=False,
    )
    return {"access_token": access_token, "token_type": "jwt"}


async def has_owner_permissions(Authorize, user_id):
    Authorize.jwt_required()
    current_jwt_user = json.loads(Authorize.get_jwt_subject())
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    return (
        (
            user_id == current_jwt_user.get("_id")
            and current_jwt_user.get("email") == user.get("email")
            and current_jwt_user.get("hashed_pass") == user.get("hashed_pass")
        )
        if user
        else False
    )


async def has_admin_permissions(authorize):
    authorize.jwt_required()
    current_jwt_user = json.loads(authorize.get_jwt_subject())
    user = await user_collection.find_one(
        {"_id": ObjectId(current_jwt_user.get("_id"))}
    )
    return user.get("role") == "admin" if user else False


async def admin_required(authorize: AuthJWT = Depends()):
    if not await has_admin_permissions(authorize):
        raise HTTPException(
            status_code=403, detail="There is no admin permissions for the action"
        )
    return authorize


def owner_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if  not await has_owner_permissions(
            kwargs.get("authorize"), kwargs.get("user_id")
        ):
            raise HTTPException(
                status_code=403,
                detail="There is no owner permissions for the action "
                "(You are not owner or regenerate access token"
                " with /api/users/token for new credentials",
            )
        return await func(*args, **kwargs)

    return wrapper
