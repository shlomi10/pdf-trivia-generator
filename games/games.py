from sqlalchemy.orm import Session

from db.db import SessionLocal
from db.models import ImageTrivia
from datetime import datetime

'''
CRUD logic for saving and retrieving trivia games tied to users. Uses the DB models.
'''


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_game_by_id(game_id: int, db: Session = None) -> ImageTrivia | None:
    if not db:
        db = next(get_db())
    return db.query(ImageTrivia).filter(ImageTrivia.id == game_id).first()


def get_games_by_user(user_id: int, db: Session = None) -> list[ImageTrivia]:
    if not db:
        db = next(get_db())
    return db.query(ImageTrivia).filter(ImageTrivia.user_id == user_id).order_by(ImageTrivia.uploaded_at.desc()).all()


def create_game(user_id: int, file_key: str, trivia: list, db: Session = None) -> ImageTrivia:
    if not db:
        db = next(get_db())
    game = ImageTrivia(
        user_id=user_id,
        file_key=file_key,
        trivia=trivia,
        uploaded_at=datetime.utcnow()
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    return game
