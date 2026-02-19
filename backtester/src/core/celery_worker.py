import time
from typing import Dict
from celery import Celery
from src.core.config import settings

# Instantiate and configure the Celery object
celery = Celery("backend")
celery.conf.broker_url = settings.CELERY_BROKER_URL # type: ignore
celery.conf.result_backend= settings.CELERY_RESULT_BACKEND # type: ignore

# ==============================================================================================================
# ==============================================================================================================
# ==============================================================================================================

"""
run_backtest task
"""
import logging
from src.backtest.configuration_schema import Configuration
logger = logging.getLogger(__name__)

@celery.task(name="run_backtest")
def run_backtest(config: Configuration):
    """
    For now, have this handle DataLoader and all possible tasks needed in here

    1. Look through the Configuration to find the required data and fetch it
    2. Once the data is fetched, run the core logic for the rolling window backtest
    3. Once the backtest is done, with SessionLocal(), we are going to add it to the database
    """
    

