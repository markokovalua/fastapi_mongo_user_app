from hashlib import sha256
from enum import Enum
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, validator, root_validator
from os import environ
from dotenv import load_dotenv

load_dotenv()
PASSWORD_SALT = environ.get("PASSWORD_SALT")


class Role(str, Enum):
    admin = "admin"
    dev = "dev"
    simple_mortal = "simple mortal"


class UserAuth(BaseModel):
    email: str
    hashed_pass: str

    @validator("hashed_pass")
    def validate_length_and_make_password_hashed(cls, password):
        assert len(password) >= 6, "Pass at least 6 characters for password"
        # use salt for better security to avoid password selection by hash from hash:password dictionaries
        # even though somebody has the hash
        return sha256(f"{PASSWORD_SALT}{password}".encode("utf-8")).hexdigest()

    @validator("email")
    def validate_email(cls, email):
        # simple email validator just for example
        assert len(email) >= 8, "email length must be at least 12 characters"
        assert "@" in email, "@ character must be in email"
        return email


class UserCreate(UserAuth):
    first_name: str = Field(min_length=1, max_length=30)
    last_name: str = Field(min_length=1, max_length=30)
    role: Role = "simple mortal"
    is_active: bool = False
    created_at: str = str(datetime.now())
    last_login: str = str(datetime.now())

    class Config:
        use_enum_values = True


class MongoObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid MongoObjectId")
        return ObjectId(v)


class UserRead(BaseModel):
    id: MongoObjectId = Field(default_factory=MongoObjectId, alias="_id")
    first_name: str
    last_name: str
    role: Role
    is_active: bool
    created_at: str
    last_login: str
    email: str

    class Config:
        json_encoders = {ObjectId: str}


class UserUpdateBase(BaseModel):
    first_name: str = Field(None, min_length=1, max_length=30)
    last_name: str = Field(None, min_length=1, max_length=30)
    role: Role = None
    is_active: bool = None



class UserUpdateByOwner(UserUpdateBase, UserAuth):
    last_login: str = None
    email: str = None
    hashed_pass: str = None

    @root_validator
    def update_owner_last_login(cls, values):
        values["last_login"] = str(datetime.now())
        return values
