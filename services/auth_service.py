from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
import json
from datetime import datetime, timedelta, timezone
from models.learning_path import User, UserCreate, TokenData

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# File-based user storage
USERS_FILE = "users.json"

def load_users():
    """Load users from JSON file"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                data = json.load(f)
                users = {}
                for username, user_data in data.items():
                    # Convert string dates back to datetime objects
                    if user_data.get('created_at'):
                        user_data['created_at'] = datetime.fromisoformat(user_data['created_at'])
                    if user_data.get('last_login'):
                        user_data['last_login'] = datetime.fromisoformat(user_data['last_login'])
                    users[username] = User(**user_data)
                return users
    except Exception as e:
        print(f"Warning: Could not load users from file: {e}")
    return {}

def save_users(users):
    """Save users to JSON file"""
    try:
        # Convert datetime objects to ISO format strings for JSON serialization
        data = {}
        for username, user in users.items():
            user_dict = user.model_dump()
            if user_dict.get('created_at'):
                user_dict['created_at'] = user_dict['created_at'].isoformat()
            if user_dict.get('last_login'):
                user_dict['last_login'] = user_dict['last_login'].isoformat()
            data[username] = user_dict
        
        with open(USERS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save users to file: {e}")

# Load existing users
users_db = load_users()

class AuthService:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                return None
            token_data = TokenData(username=username)
            return token_data
        except JWTError:
            return None
    
    def register_user(self, user_create: UserCreate) -> User:
        """Register a new user"""
        # Check if username already exists
        if user_create.username in users_db:
            raise ValueError("Username already registered")
        
        # Check if email already exists
        for user in users_db.values():
            if user.email == user_create.email:
                raise ValueError("Email already registered")
        
        # Create new user
        user_id = str(len(users_db) + 1)  # Simple ID generation
        hashed_password = self.get_password_hash(user_create.password)
        
        user = User(
            id=user_id,
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password
        )
        
        users_db[user_create.username] = user
        save_users(users_db)
        return user
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password"""
        user = users_db.get(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        
        # Update last login
        user.last_login = datetime.now(timezone.utc)
        save_users(users_db)
        return user
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return users_db.get(username)
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        for user in users_db.values():
            if user.id == user_id:
                return user
        return None 