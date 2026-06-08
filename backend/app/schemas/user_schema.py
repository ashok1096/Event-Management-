from pydantic import BaseModel, EmailStr, field_validator
import re


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "attendee"

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        """
        Validate password strength:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one number
        - At least one special character
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character (!@#$%^&*(),.?":{}|<>)')
        
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"