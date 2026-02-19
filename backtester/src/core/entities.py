import uuid 
from sqlalchemy import func, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB

from src.database.core import Base

class Backtest(Base):
    __tablename__ = "backtest"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_result = Column(JSONB, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

