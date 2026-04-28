"""截图工具模块"""

import os
import subprocess
from datetime import datetime

from autodroid_agent.config import SCREENSHOTS_DIR
from autodroid_agent.utils.logger import get_logger

logger = get_logger(__name__)


def take_screenshot(device_id: str = "") -> str:
    """通过 ADB 截取手机屏幕，返回截图文件路径"""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)

    adb_prefix = _adb_prefix(device_id)

    try:
        cmd = adb_prefix + ["exec-out", "screencap", "-p"]
        result = subprocess.run(cmd, capture_output=True, timeout=15)

        if result.returncode != 0:
            error_msg = result.stderr.decode("utf-8", errors="replace").strip()
            logger.error(f"截图失败: {error_msg}")
            return ""

        with open(filepath, "wb") as f:
            f.write(result.stdout)

        if os.path.getsize(filepath) == 0:
            logger.error("截图文件为空")
            os.remove(filepath)
            return ""

        logger.info(f"截图已保存: {filepath}")
        return filepath

    except subprocess.TimeoutExpired:
        logger.error("截图超时")
        return ""
    except FileNotFoundError:
        logger.error("adb 命令未找到，请确保已安装 ADB")
        return ""
    except Exception as e:
        logger.error(f"截图异常: {e}")
        return ""


def _adb_prefix(device_id: str = "") -> list:
    """构造 ADB 命令前缀"""
    from autodroid_agent.config import ADB_PATH
    cmd = [ADB_PATH]
    if device_id:
        cmd.extend(["-s", device_id])
    return cmd
