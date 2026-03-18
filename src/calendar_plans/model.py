from sqlalchemy import Column, Integer, BigInteger, DateTime, func, Text
from sqlalchemy.dialects.postgresql import JSONB
from src.database import Base

class CalendarPlan(Base):
    __tablename__ = "calendar_plan"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    educational_plan_id = Column(BigInteger, nullable=False)
    data = Column(JSONB, nullable=False, default={})
    file_path = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
