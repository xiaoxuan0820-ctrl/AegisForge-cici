"""消息路由模块：标准化所有来源的输入"""

from dataclasses import dataclass, asdict
from typing import Literal
from datetime import datetime

SourceType = Literal["cli", "feishu"]


@dataclass
class RoutedMessage:
    """统一的消息格式"""
    user_id: str
    text: str
    source: SourceType
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return asdict(self)


def route_cli(text: str, user_id: str = "cli_user") -> RoutedMessage:
    """路由 CLI 输入"""
    return RoutedMessage(user_id=user_id, text=text, source="cli")


def route_feishu(text: str, user_id: str, timestamp: str = "") -> RoutedMessage:
    """路由飞书输入"""
    return RoutedMessage(
        user_id=user_id,
        text=text,
        source="feishu",
        timestamp=timestamp,
    )


def route_raw(source: SourceType, text: str, user_id: str = "unknown") -> RoutedMessage:
    """通用路由入口"""
    if source == "cli":
        return route_cli(text, user_id)
    elif source == "feishu":
        return route_feishu(text, user_id)
    else:
        raise ValueError(f"不支持的消息来源: {source}")
