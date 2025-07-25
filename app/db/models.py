from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class PLCCommand(Base):
    __tablename__ = "plc_commands"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True, nullable=False, server_default="{}")
    status = Column(String, default="pending")
