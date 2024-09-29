from pydantic import BaseModel


class UserRequest(BaseModel):
    """User request model"""
    user_id: str

class UserResponse(BaseModel):
    """User response model"""
    answer: bool