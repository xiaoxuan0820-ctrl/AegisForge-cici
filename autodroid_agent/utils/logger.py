"""日志工具模块"""

import os
import logging
from datetime import datetime

from autodroid_agent.config import LOG_DIR, LOG_FILE


def setup_logger(name: str = "autodroid") -> logging.Logger:
    """配置并返回日志器"""
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 防止重复添加 handler
    if logger.handlers:
        return logger

    # 文件日志
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_fmt)

    # 控制台日志
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_fmt = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler.setFormatter(console_fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = "autodroid") -> logging.Logger:
    """获取日志器"""
    return logging.getLogger(name)
