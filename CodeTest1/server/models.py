from sqlalchemy import Column, Integer, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel

class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    part_no = Column(Text, index=True)

class Time(Base):
    __tablename__ = "times"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    start_part_id = Column(Integer, ForeignKey('parts.id'), nullable=False)
    end_part_id = Column(Integer, ForeignKey('parts.id'), nullable=False)
    time = Column(Numeric, default=0)
    active = Column(Integer, default=0)
    update_time = Column(Text, nullable=False)

    start_part = relationship("Part", foreign_keys=[start_part_id])
    end_part = relationship("Part", foreign_keys=[end_part_id])

class NewPartRelation(BaseModel):
    start_part_no: str
    end_part_no: str
    time: float

class NewPartData(BaseModel):
    new_part_no: str
    part_relations: list[NewPartRelation]