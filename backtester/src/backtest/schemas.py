from uuid import UUID
from enum import Enum
from pydantic import BaseModel

class BacktestStatus(Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"

class BacktestResponse(BaseModel):
    backtest_id: UUID
    status: BacktestStatus