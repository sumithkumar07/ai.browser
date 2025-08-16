from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from models.user import User, UserCreate, UserUpdate, Token
from services.enhanced_auth_service import enhanced_auth_service
from database.connection import get_database
import time

router = APIRouter()
security = HTTPBearer()

class EnhancedLoginRequest(BaseModel):
    username: str = None
    email: EmailStr = None
    password: str

class TestUserRequest(BaseModel):
    create_test_user: bool = True

@router.post("/register", response_model=User)
async def enhanced_register(user_data: UserCreate, db=Depends(get_database)):
    """Enhanced user registration with better validation"""
    try:
        return await enhanced_auth_service.create_user(user_data, db)
    except ValueError as e:
        if "email already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        elif "username already taken" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def enhanced_login(login_data: EnhancedLoginRequest, db=Depends(get_database)):
    """Enhanced login with improved error handling and validation"""
    try:
        # Validate input
        identifier = login_data.username or login_data.email
        if not identifier:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Either username or email is required"
            )
        
        if not login_data.password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password is required"
            )
            
        # Authenticate user
        user = await enhanced_auth_service.authenticate_user(identifier, login_data.password, db)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        token_subject = user.email if user.email else user.username
        access_token = enhanced_auth_service.create_access_token(data={"sub": token_subject})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username,
            "expires_in": 1800  # 30 minutes
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login processing failed: {str(e)}"
        )

@router.post("/create-test-user", response_model=Token)
async def create_test_user_and_login(request: TestUserRequest, db=Depends(get_database)):
    """Create a test user for development and return login token"""
    try:
        # Check if test user already exists
        existing_user = await db.users.find_one({"username": "testuser"})
        
        if existing_user:
            # Login existing test user
            user = User(
                id=str(existing_user["_id"]),
                username=existing_user["username"],
                email=existing_user["email"],
                full_name=existing_user.get("full_name", "Test User"),
                is_active=existing_user.get("is_active", True)
            )
        else:
            # Create new test user
            test_user_data = UserCreate(
                username="testuser",
                email="test@example.com",
                password="testpass",
                full_name="Test User"
            )
            user = await enhanced_auth_service.create_user(test_user_data, db)
        
        # Create access token
        access_token = enhanced_auth_service.create_access_token(data={"sub": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username,
            "expires_in": 1800,
            "test_user": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Test user creation failed: {str(e)}"
        )

@router.get("/profile", response_model=User)
async def get_enhanced_profile(current_user: User = Depends(enhanced_auth_service.get_current_user)):
    """Get current user profile with enhanced details"""
    return current_user

@router.put("/profile", response_model=User)
async def update_enhanced_profile(
    user_update: UserUpdate, 
    current_user: User = Depends(enhanced_auth_service.get_current_user),
    db=Depends(get_database)
):
    """Update user profile with enhanced validation"""
    try:
        return await enhanced_auth_service.update_user(current_user.id, user_update, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile update failed: {str(e)}"
        )

@router.get("/auth-status")
async def check_auth_status(current_user: User = Depends(enhanced_auth_service.get_current_user)):
    """Check authentication status"""
    return {
        "authenticated": True,
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "timestamp": int(time.time())
    }

@router.post("/refresh-token", response_model=Token)
async def refresh_access_token(current_user: User = Depends(enhanced_auth_service.get_current_user)):
    """Refresh access token"""
    try:
        new_token = enhanced_auth_service.create_access_token(data={"sub": current_user.email})
        
        return {
            "access_token": new_token,
            "token_type": "bearer",
            "user_id": current_user.id,
            "username": current_user.username,
            "expires_in": 1800
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )