import os
import uuid
from sqlalchemy import (
    Column, String, Boolean, Integer, ForeignKey, JSON, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = os.environ["DATABASE_URL"]
# Database URL
# DATABASE_URL = (
#     "postgresql+asyncpg://myuser:mypassword@postgres:5432/mydb"  # Change to your DB URL
# )

# SQLAlchemy setup for models and session
engine = create_engine(DATABASE_URL.replace("postgresql+asyncpg", "postgresql"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AppUsers(Base):
    __tablename__ = "app_users"

    id = Column(String, unique=True, index=True, primary_key=True)
    identifier = Column(String, default="user")
    username = Column(String)
    password = Column(String)
    createdAt = Column(String, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identifier = Column(String, nullable=False, unique=True)
    meta = Column("metadata",JSON, nullable=False)
    createdAt = Column(String)

    threads = relationship("Thread", back_populates="user", cascade="all, delete")

class Thread(Base):
    __tablename__ = "threads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    createdAt = Column(String)
    name = Column(String)
    userId = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    userIdentifier = Column(String)
    tags = Column(ARRAY(String))
    meta = Column("metadata",JSON)

    user = relationship("User", back_populates="threads")
    steps = relationship("Step", back_populates="thread", cascade="all, delete")
    elements = relationship("Element", back_populates="thread", cascade="all, delete")
    feedbacks = relationship("Feedback", back_populates="thread", cascade="all, delete")

class Step(Base):
    __tablename__ = "steps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    threadId = Column(UUID(as_uuid=True), ForeignKey("threads.id", ondelete="CASCADE"), nullable=False)
    parentId = Column(UUID(as_uuid=True))
    streaming = Column(Boolean, nullable=False)
    waitForAnswer = Column(Boolean)
    isError = Column(Boolean)
    meta = Column("metadata",JSON)
    tags = Column(ARRAY(String))
    input = Column(String)
    output = Column(String)
    createdAt = Column(String)
    command = Column(String)
    start = Column(String)
    defaultOpen = Column(Boolean)
    end = Column(String)
    generation = Column(JSON)
    showInput = Column(String)
    language = Column(String)
    indent = Column(Integer)

    thread = relationship("Thread", back_populates="steps")

class Element(Base):
    __tablename__ = "elements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    threadId = Column(UUID(as_uuid=True), ForeignKey("threads.id", ondelete="CASCADE"))
    type = Column(String)
    url = Column(String)
    chainlitKey = Column(String)
    name = Column(String, nullable=False)
    display = Column(String)
    objectKey = Column(String)
    size = Column(String)
    page = Column(Integer)
    language = Column(String)
    forId = Column(UUID(as_uuid=True))
    mime = Column(String)
    props = Column(JSON)

    thread = relationship("Thread", back_populates="elements")

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forId = Column(UUID(as_uuid=True), nullable=False)
    threadId = Column(UUID(as_uuid=True), ForeignKey("threads.id", ondelete="CASCADE"), nullable=False)
    value = Column(Integer, nullable=False)
    comment = Column(String)

    thread = relationship("Thread", back_populates="feedbacks")
