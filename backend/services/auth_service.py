import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.user import User, UserCreate, UserUpdate, UserInDB
from database.connection import get_database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def create_user(self, user_data: UserCreate, db):
        # Check if user exists
        existing_user = await db.users.find_one({"email": user_data.email})
        if existing_user:
            raise ValueError("User with this email already exists")

        existing_username = await db.users.find_one({"username": user_data.username})
        if existing_username:
            raise ValueError("Username already taken")

        # Create user
        hashed_password = self.get_password_hash(user_data.password)
        user_in_db = UserInDB(
            **user_data.dict(exclude={"password"}),
            hashed_password=hashed_password
        )
        
        await db.users.insert_one(user_in_db.dict())
        return User(**user_in_db.dict())

    async def authenticate_user(self, email_or_username: str, password: str, db):
        # Try to find user by email first, then by username
        user_data = await db.users.find_one({"email": email_or_username})
        if not user_data:
            user_data = await db.users.find_one({"username": email_or_username})
        
        if not user_data:
            return False
            
        user = UserInDB(**user_data)
        if not self.verify_password(password, user.hashed_password):
            return False
        
        # Update last login
        await db.users.update_one(
            {"$or": [{"email": email_or_username}, {"username": email_or_username}]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        return User(**user.dict())

    async def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db=Depends(get_database)
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
            
        user_data = await db.users.find_one({"email": email})
        if user_data is None:
            raise credentials_exception
        return User(**user_data)

    async def update_user(self, user_id: str, user_update: UserUpdate, db):
        update_data = user_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        await db.users.update_one(
            {"id": user_id},
            {"$set": update_data}
        )
        
        updated_user = await db.users.find_one({"id": user_id})
        return User(**updated_user)