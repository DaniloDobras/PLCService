from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class PLCCommand(Base):
    __tablename__ = "plc_commands"

    id = Column(Integer, primary_key=True, index=True)
    bucket_id = Column(Integer, nullable=False)
    material_id = Column(Integer, nullable=False)
    qty = Column(Integer, nullable=False)
    status = Column(String, default="pending")
