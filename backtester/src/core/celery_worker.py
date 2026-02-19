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
def workflow_task(config: Configuration):
    """
    For now, have this handle DataLoader and all possible tasks needed in here
    """