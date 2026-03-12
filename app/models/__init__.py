from sqlalchemy import Column, Integer, String, Boolean, Text
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    website = Column(String)
    niche = Column(String, index=True)
    location = Column(String, index=True)
    details = Column(Text)
    analysis = Column(Text)  # JSON or formatted text
    proposal_text = Column(Text)
    status = Column(String, default="found") # found, analyzed, proposal_generated, sent
