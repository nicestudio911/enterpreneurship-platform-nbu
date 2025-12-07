from sqlalchemy.orm import Session
from typing import Optional
from app.models.token import Token


class TokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_token(self, token: str) -> Optional[Token]:
        return self.db.query(Token).filter(Token.token == token).first()

    def save(self, token: Token) -> Token:
        try:
            self.db.add(token)
            self.db.commit()
            self.db.refresh(token)
            return token
        except Exception:
            self.db.rollback()
            raise

    def delete(self, token: Token) -> None:
        try:
            self.db.delete(token)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def delete_by_token(self, token: str) -> None:
        token_obj = self.find_by_token(token)
        if token_obj:
            self.delete(token_obj)

