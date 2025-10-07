from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    consent: bool


class RegisterResponse(BaseModel):
    message: str


class VerifyRequest(BaseModel):
    token: str


class VerifyResponse(BaseModel):
    message: str


