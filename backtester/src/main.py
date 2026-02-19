"""
FASTAPI ROOT FILE 
"""

from fastapi import FastAPI
from src.logging import configure_logging, LogLevels
from src.backtest.router import router as backtest_router

configure_logging(LogLevels.info)

app = FastAPI()

app.include_router(backtest_router)