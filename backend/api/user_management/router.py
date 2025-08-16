from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from models.user import User, UserCreate, UserUpdate, Token
from services.auth_service import AuthService
from database.connection import get_database

router = APIRouter()
security = HTTPBearer()
auth_service = AuthService()

# Login request model
class LoginRequest(BaseModel):
    username: str
    password: str
    email: str = None

@router.post("/register", response_model=User)
async def register(user_data: UserCreate, db=Depends(get_database)):
    """Register a new user"""
    try:
        return await auth_service.create_user(user_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db=Depends(get_database)):
    """Login user and return access token - Fixed to accept JSON body"""
    try:
        # Try authenticating with username or email
        user = None
        if login_data.email:
            user = await auth_service.authenticate_user(login_data.email, login_data.password, db)
        elif login_data.username:
            # If username is provided, treat it as email for now
            user = await auth_service.authenticate_user(login_data.username, login_data.password, db)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = auth_service.create_access_token(data={"sub": user.email if hasattr(user, 'email') else user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        # Return a more specific error for debugging
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Login processing failed: {str(e)}"
        )

@router.get("/profile", response_model=User)
async def get_profile(current_user: User = Depends(auth_service.get_current_user)):
    """Get current user profile"""
    return current_user

@router.put("/profile", response_model=User)
async def update_profile(
    user_update: UserUpdate, 
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Update user profile"""
    return await auth_service.update_user(current_user.id, user_update, db)