"""LLM Agent 模块：将用户指令转为动作序列"""

import json
import time

from openai import OpenAI

from autodroid_agent.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    LLM_MODEL,
    PROMPT_FILE,
)
from autodroid_agent.utils.logger import get_logger

logger = get_logger(__name__)


def _load_system_prompt() -> str:
    """读取系统提示词"""
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def _build_client() -> OpenAI:
    """构建 OpenAI 客户端（兼容任意 OpenAI 接口的服务）"""
    return OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)


def parse_actions(user_input: str) -> list[dict]:
    """
    将用户指令解析为动作序列

    参数:
        user_input: 用户自然语言指令

    返回:
        动作字典列表，格式:
        [
            {"action": "tap", "value": [500, 1200]},
            {"action": "wait", "value": 3},
            ...
        ]

    异常:
        ValueError: LLM 返回格式错误
        Exception: API 调用失败
    """
    if not OPENAI_API_KEY:
        raise ValueError("未配置 OPENAI_API_KEY，请在 .env 文件中设置")

    system_prompt = _load_system_prompt()
    client = _build_client()

    logger.info(f"正在调用 LLM ({LLM_MODEL}) 解析指令: {user_input}")

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )
    except Exception as e:
        logger.error(f"LLM 调用失败: {e}")
        raise

    content = response.choices[0].message.content
    if not content:
        raise ValueError("LLM 返回内容为空")

    logger.debug(f"LLM 原始返回: {content}")

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"JSON 解析失败: {e}")
        raise ValueError(f"LLM 返回无法解析为 JSON: {content}") from e

    # 兼容两种格式：直接数组 或 {"actions": [...]}
    if isinstance(parsed, dict):
        actions = parsed.get("actions", parsed.get("steps", []))
    elif isinstance(parsed, list):
        actions = parsed
    else:
        raise ValueError(f"LLM 返回格式异常: {content}")

    if not isinstance(actions, list):
        raise ValueError(f"动作序列应为数组，实际类型: {type(actions)}")

    # 验证每个动作
    for i, action in enumerate(actions):
        if not isinstance(action, dict):
            raise ValueError(f"第 {i+1} 个动作格式错误: {action}")
        if "action" not in action:
            raise ValueError(f"第 {i+1} 个动作缺少 action 字段: {action}")

    logger.info(f"解析到 {len(actions)} 个动作")
    return actions
