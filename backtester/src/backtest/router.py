import uuid
import logging
from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from src.backtest.configuration_schema import Configuration
from src.backtest.schemas import BacktestResponse, BacktestStatus
from src.core.celery_worker import run_backtest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/backtest", tags=['backtest'])

@router.post(
    "/", 
    summary="Create a new backtest",
    response_description="Returns backtest_id. Poll GET edpt for results",
    status_code=status.HTTP_201_CREATED,
    response_model=BacktestResponse
)
def create_backtest(config: Configuration) -> BacktestResponse:
    """
    1. Create the backtest id
    2. offload task to celery
    3. return id for polling
    """
    backtest_id = str(uuid.uuid4())

    run_backtest.delay(config)

    return BacktestResponse(
        backtest_id,
        BacktestStatus.STARTED
    )



