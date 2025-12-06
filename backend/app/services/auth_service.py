from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models.user import User
import uuid


class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def login(self, username: str, password: str) -> str:
        # Mock implementation - returns a UUID token
        # In a real implementation, you would verify credentials here
        return str(uuid.uuid4())

    def register(self, username: str, password: str) -> User:
        # Check if user already exists
        existing_user = self.user_repository.find_by_username(username)
        if existing_user:
            raise ValueError("Username already exists")
        
        # Create new user
        # Note: In a real implementation, password should be hashed (e.g., using bcrypt)
        new_user = User(username=username, password=password)
        return self.user_repository.save(new_user)

