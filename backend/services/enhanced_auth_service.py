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

class EnhancedAuthService:
    """Enhanced Authentication Service with improved error handling and validation"""
    
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
        """Create new user with enhanced validation"""
        try:
            # Check if user exists by email
            existing_user = await db.users.find_one({"email": user_data.email})
            if existing_user:
                raise ValueError("User with this email already exists")

            # Check if username exists
            existing_username = await db.users.find_one({"username": user_data.username})
            if existing_username:
                raise ValueError("Username already taken")

            # Create user document
            hashed_password = self.get_password_hash(user_data.password)
            user_doc = {
                "username": user_data.username,
                "email": user_data.email,
                "full_name": user_data.full_name,
                "hashed_password": hashed_password,
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "last_login": None
            }
            
            # Insert user
            result = await db.users.insert_one(user_doc)
            user_doc["_id"] = result.inserted_id
            
            # Return User object (without password)
            return User(
                id=str(result.inserted_id),
                username=user_doc["username"],
                email=user_doc["email"],
                full_name=user_doc["full_name"],
                is_active=user_doc["is_active"],
                created_at=user_doc["created_at"],
                updated_at=user_doc["updated_at"],
                last_login=user_doc["last_login"]
            )
            
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"User creation failed: {str(e)}")

    async def authenticate_user(self, identifier: str, password: str, db):
        """Enhanced user authentication with better error handling"""
        try:
            # Try to find user by email first, then by username
            user_data = await db.users.find_one({
                "$or": [
                    {"email": identifier},
                    {"username": identifier}
                ]
            })
            
            if not user_data:
                return None
                
            # Verify password
            if not self.verify_password(password, user_data["hashed_password"]):
                return None
            
            # Update last login
            await db.users.update_one(
                {"_id": user_data["_id"]},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            
            # Return User object
            return User(
                id=str(user_data["_id"]),
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data.get("full_name"),
                is_active=user_data.get("is_active", True),
                created_at=user_data.get("created_at"),
                updated_at=user_data.get("updated_at")
            )
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return None

    async def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db=Depends(get_database)
    ):
        """Enhanced current user retrieval with better error handling"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            # Decode JWT token
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
            identifier: str = payload.get("sub")
            if identifier is None:
                raise credentials_exception
                
        except JWTError as e:
            print(f"JWT decode error: {e}")
            raise credentials_exception
            
        try:
            # Find user by email or username
            user_data = await db.users.find_one({
                "$or": [
                    {"email": identifier},
                    {"username": identifier}
                ]
            })
            
            if user_data is None:
                raise credentials_exception
                
            return User(
                id=str(user_data["_id"]),
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data.get("full_name"),
                is_active=user_data.get("is_active", True),
                created_at=user_data.get("created_at"),
                updated_at=user_data.get("updated_at")
            )
            
        except Exception as e:
            print(f"User lookup error: {e}")
            raise credentials_exception

    async def update_user(self, user_id: str, user_update: UserUpdate, db):
        """Enhanced user update with validation"""
        try:
            update_data = user_update.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            # Convert string ID to ObjectId if needed
            from bson import ObjectId
            if isinstance(user_id, str):
                user_id = ObjectId(user_id)
            
            result = await db.users.update_one(
                {"_id": user_id},
                {"$set": update_data}
            )
            
            if result.modified_count == 0:
                raise ValueError("User not found or no changes made")
            
            updated_user = await db.users.find_one({"_id": user_id})
            if not updated_user:
                raise ValueError("User not found after update")
                
            return User(
                id=str(updated_user["_id"]),
                username=updated_user["username"],
                email=updated_user["email"],
                full_name=updated_user.get("full_name"),
                is_active=updated_user.get("is_active", True),
                created_at=updated_user.get("created_at"),
                updated_at=updated_user.get("updated_at")
            )
            
        except Exception as e:
            raise ValueError(f"User update failed: {str(e)}")

# Create singleton instance
enhanced_auth_service = EnhancedAuthService()