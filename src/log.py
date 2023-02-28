# encoding: utf-8
"""
Logs Config
"""
import sys
from loguru import logger

# LOGGER CONFIG
logger.remove()
logger.add(
    sys.stdout,
    format="[{time:YYYY-MM-DD HH:mm:ss}] [{level}] {message}",
    level="INFO",
)


def info(txt: str):
    return logger.info(txt)


def error(txt: str):
    return logger.error(txt)
