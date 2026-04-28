"""启动入口：支持 CLI 交互 + 飞书 Webhook 服务"""

import sys
import threading

from autodroid_agent.config import FEISHU_WEBHOOK_PORT
from autodroid_agent.router import route_cli
from autodroid_agent.agent import parse_actions
from autodroid_agent.executor import execute_actions
from autodroid_agent.utils.logger import setup_logger, get_logger

logger = setup_logger()


def handle_message(user_text: str, user_id: str = "cli_user") -> dict:
    """处理用户消息的完整管道"""
    # 1. 路由
    message = route_cli(user_text, user_id)
    logger.info(f"📨 收到指令 [{message.source}]: {message.text}")

    # 2. Agent 解析
    try:
        actions = parse_actions(message.text)
    except Exception as e:
        logger.error(f"❌ 指令解析失败: {e}")
        return {"success": False, "error": str(e), "logs": []}

    # 3. 执行
    result = execute_actions(actions)

    return result.to_dict()


def run_cli():
    """CLI 交互模式"""
    print("🤖 AutoDroid Agent CLI")
    print("=" * 40)
    print("输入指令控制手机，输入 'exit' 退出")
    print()

    while True:
        try:
            user_input = input("📱 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 再见！")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "q"):
            print("👋 再见！")
            break

        result = handle_message(user_input)

        print()
        if result["success"]:
            print(f"✅ 执行完成！({result['steps_executed']}/{result['total_steps']} 步)")
        else:
            print(f"❌ 执行失败: {result.get('error', '未知错误')}")

        for log in result.get("logs", []):
            print(f"  {log}")

        if result.get("screenshot_path"):
            print(f"📸 截图: {result['screenshot_path']}")
        print()


def run_once(text: str):
    """单次 CLI 执行模式"""
    result = handle_message(text)

    if result["success"]:
        print(f"\n✅ 执行完成！({result['steps_executed']}/{result['total_steps']} 步)")
    else:
        print(f"\n❌ 执行失败: {result.get('error', '未知错误')}")

    for log in result.get("logs", []):
        print(f"  {log}")

    if result.get("screenshot_path"):
        print(f"📸 截图: {result['screenshot_path']}")


def start_feishu_server():
    """启动飞书 Webhook 服务（后台线程）"""
    try:
        from im.feishu_bot import app as feishu_app
        logger.info(f"🚀 飞书 Webhook 服务启动于端口 {FEISHU_WEBHOOK_PORT}")
        feishu_app.run(
            host="0.0.0.0",
            port=FEISHU_WEBHOOK_PORT,
            debug=False,
            use_reloader=False,
        )
    except ImportError:
        logger.warning("⚠️ Flask 未安装，飞书服务无法启动")
    except Exception as e:
        logger.error(f"❌ 飞书服务异常: {e}")


def main():
    """主入口"""
    if len(sys.argv) > 1:
        # CLI 单次执行: python main.py "指令文本"
        user_text = " ".join(sys.argv[1:])
        run_once(user_text)
    else:
        # 交互模式: 同时启动 CLI + 飞书服务
        feishu_thread = threading.Thread(target=start_feishu_server, daemon=True)
        feishu_thread.start()

        run_cli()


if __name__ == "__main__":
    main()
