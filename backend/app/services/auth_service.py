from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.repositories.token_repository import TokenRepository
from app.models.user import User
from app.models.token import Token
import uuid


class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.token_repository = TokenRepository(db)

    def login(self, username: str, password: str) -> str:
        # Find user by username
        user = self.user_repository.find_by_username(username)
        if not user:
            raise ValueError("Invalid username or password")
        
        # Verify password (in a real implementation, use bcrypt to hash/verify)
        # For now, simple string comparison (NOT SECURE - should use password hashing)
        if user.password != password:
            raise ValueError("Invalid username or password")
        
        # Generate token
        token = str(uuid.uuid4())
        
        # Store token with user_id
        token_obj = Token(token=token, user_id=user.id)
        self.token_repository.save(token_obj)
        
        return token

    def get_user_by_token(self, token: str) -> User | None:
        """Get user by token"""
        token_obj = self.token_repository.find_by_token(token)
        if not token_obj:
            return None
        return self.user_repository.find_by_id(token_obj.user_id)

    def register(self, username: str, password: str) -> User:
        # Check if user already exists
        existing_user = self.user_repository.find_by_username(username)
        if existing_user:
            raise ValueError("Username already exists")
        
        # Create new user
        # Note: In a real implementation, password should be hashed (e.g., using bcrypt)
        new_user = User(username=username, password=password)
        return self.user_repository.save(new_user)

