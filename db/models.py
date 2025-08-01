from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

'''
Contains SQLAlchemy models for User and ImageTrivia, representing your users and trivia data.
'''

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    trivia_entries = relationship("ImageTrivia", back_populates="user")


class ImageTrivia(Base):
    __tablename__ = "image_trivia"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    file_key = Column(String, nullable=False)
    trivia = Column(JSON, nullable=False)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    score = Column(Integer, nullable=True)

    user = relationship("User", back_populates="trivia_entries")
