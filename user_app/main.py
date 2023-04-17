from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel, Field
from bson.errors import BSONError
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError

app = FastAPI()


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(BSONError)
def bson_exception_handler(request: Request, exc: BSONError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

@app.exception_handler(DuplicateKeyError)
def email_duplicates_exception_handler(request: Request, exc: DuplicateKeyError):
    return JSONResponse(
        status_code=400,
        content={"detail": "The user with such an email already exists"},
    )

@app.exception_handler(ServerSelectionTimeoutError)
def email_duplicates_exception_handler(request: Request, exc: ServerSelectionTimeoutError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Please check if mongodb database is running"},
    )

@app.get("/")
async def index():
    return Response("USER API CRUD APP: use /redoc endpoint to see possible endpoints "
                    "and for example Postman for testing")


from views.user import router as user_router
from views.admin import router as admin_router

app.include_router(user_router, prefix="/api/users")
app.include_router(admin_router, prefix="/api/admins")
