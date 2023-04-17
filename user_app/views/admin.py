from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from schemas.user_schema import UserRead, UserUpdateBase
from auth.helpers import admin_required
from bson.objectid import ObjectId
from utils.helpers import find_user
from utils.database import user_collection

# TODO: maybe it should be done one point of access to the collection somehow
router = APIRouter()


@router.patch("/update-user/{user_id}",
              summary="Update User | use Authorization:Bearer {access_token} from /token endpoint for auth in Postman",
              response_model=UserRead)
async def update_user(
    user_id: str, user: UserUpdateBase, authorize: AuthJWT = Depends(admin_required)
):
    await user_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": user.dict(exclude_none=True)}
    )
    return await find_user(user_id)
