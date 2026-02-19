import uuid 
from sqlalchemy import func, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from src.backtest.schemas import BacktestStatus
from src.database.core import Base

backtest_status_enum = SQLEnum(
    BacktestStatus,
    name="scan_type_enum",
    native_enum=True,
    create_type=True
)

class Backtest(Base):
    __tablename__ = "backtest"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_result = Column(JSONB, nullable=True)
    status = Column(backtest_status_enum, nullable=False, default=BacktestStatus.STARTED)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

