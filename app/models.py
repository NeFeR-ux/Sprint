from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class StatusEnum(str, enum.Enum):
    new = "new"
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=False)
    full_name = Column(String, nullable=False)

    perevals = relationship("Pereval", back_populates="user")


class Coords(Base):
    __tablename__ = "coords"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    height = Column(Integer, nullable=False)

    pereval = relationship("Pereval", back_populates="coords", uselist=False)


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    winter = Column(String, nullable=True)
    summer = Column(String, nullable=True)
    autumn = Column(String, nullable=True)
    spring = Column(String, nullable=True)

    pereval = relationship("Pereval", back_populates="level", uselist=False)


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, nullable=False)  # URL или путь к изображению
    title = Column(String, nullable=True)

    pereval_id = Column(Integer, ForeignKey("perevals.id"))
    pereval = relationship("Pereval", back_populates="images")


class Pereval(Base):
    __tablename__ = "perevals"

    id = Column(Integer, primary_key=True, index=True)
    beauty_title = Column(String, nullable=True)
    title = Column(String, nullable=False)
    other_titles = Column(String, nullable=True)
    connect = Column(String, nullable=True)
    add_time = Column(DateTime, default=datetime.now)
    status = Column(Enum(StatusEnum), default=StatusEnum.new)

    # Внешние ключи
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    coords_id = Column(Integer, ForeignKey("coords.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)

    # Связи
    user = relationship("User", back_populates="perevals")
    coords = relationship("Coords", back_populates="pereval")
    level = relationship("Level", back_populates="pereval")
    images = relationship("Image", back_populates="pereval")