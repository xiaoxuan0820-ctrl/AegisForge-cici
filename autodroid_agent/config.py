"""AutoDroid Agent 配置模块"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==================== LLM 配置 ====================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")

# ==================== ADB 配置 ====================
ADB_PATH = os.getenv("ADB_PATH", "/opt/homebrew/bin/adb")  # ADB 可执行文件路径
ADB_HOST = os.getenv("ADB_HOST", "127.0.0.1")
ADB_PORT = int(os.getenv("ADB_PORT", "5555"))
ADB_DEVICE = os.getenv("ADB_DEVICE", "")  # 留空则使用唯一设备

# ==================== 飞书配置 ====================
FEISHU_WEBHOOK_PORT = int(os.getenv("FEISHU_WEBHOOK_PORT", "5000"))
FEISHU_VERIFY_TOKEN = os.getenv("FEISHU_VERIFY_TOKEN", "")
FEISHU_BOT_NAME = os.getenv("FEISHU_BOT_NAME", "AutoDroid助手")

# ==================== 安全机制 ====================
MAX_TAPS = int(os.getenv("MAX_TAPS", "5"))           # 连续点击上限
MAX_EXECUTION_TIME = int(os.getenv("MAX_EXECUTION_TIME", "60"))  # 总执行时间上限（秒）
MAX_STEPS = int(os.getenv("MAX_STEPS", "30"))        # 最大步骤数

# ==================== 路径 ====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
LOG_FILE = os.path.join(LOG_DIR, "run.log")
PROMPT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompt.txt")
