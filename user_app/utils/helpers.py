from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from utils.database import user_collection


async def find_user(user_id):
    data = await user_collection.find_one({"_id": ObjectId(user_id)})
    return (
        data
        if data
        else JSONResponse(status_code=404, content={"detail": "user is not found"})
    )
