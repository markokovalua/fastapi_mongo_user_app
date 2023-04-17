from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from bson.objectid import ObjectId
from utils.helpers import find_user
from utils.database import user_collection
from schemas.user_schema import UserCreate, UserRead, UserUpdateByOwner, UserAuth
from auth.helpers import generate_access_token, owner_required

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=201)
async def create_user(user: UserCreate):
    result = await user_collection.insert_one(user.dict())
    return await find_user(str(result.inserted_id))

@router.get("/", response_model=list[UserRead])
async def list_users():
    return [user async for user in user_collection.find()]


@router.get("/{user_id}", response_model=UserRead)
async def retrieve_user(user_id: str):
    return await find_user(user_id)


@router.delete("/{user_id}",
               summary="Delete User | use Authorization:Bearer {access_token} from /token endpoint for auth in Postman")
@owner_required
async def delete_user(user_id: str, authorize: AuthJWT = Depends()):
    await user_collection.delete_one({"_id": ObjectId(user_id)})
    return JSONResponse(status_code=204, content={"detail": "user is deleted"})

@router.patch("/{user_id}", response_model=UserRead,
              summary="Update User | use Authorization:Bearer {access_token} from /token endpoint for auth in Postman")
@owner_required
async def update_user(
    user_id: str, user: UserUpdateByOwner, authorize: AuthJWT = Depends()
):
    await user_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": user.dict(exclude_none=True)}
    )
    return await find_user(user_id)


@router.post("/token")
async def get_token(user: UserAuth, authorize: AuthJWT = Depends()):
    user = await user_collection.find_one(user.dict())
    return (
        generate_access_token(authorize, str(user.get("_id")), user.get("email"), user.get("hashed_pass"))
        if user
        else JSONResponse(
            status_code=404,
            content={"detail": "user with following credentials is not found"},
        )
    )
