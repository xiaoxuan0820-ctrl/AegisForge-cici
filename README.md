# 🤖 AutoDroid Agent

基于 [AutoDroid](https://github.com/solivansprvill-droid/AutoDroid) 的最小侵入式改造，构建一套 **CLI + 飞书双入口** 的 Android 自动化控制系统。

## 架构概览

```
用户输入（CLI 或 飞书）
        ↓
  统一 Router（消息标准化）
        ↓
  Agent（LLM → 动作序列）
        ↓
  Executor（ADB 执行）
        ↓
  手机操作 → 截图 + 日志
```

**核心思路：** 不修改 AutoDroid 原有的 Android APK 代码，通过 Python 封装 ADB 命令作为外部控制层，用 LLM 把自然语言翻译成手机操作指令。

## 项目结构

```
project/
├── autodroid_agent/          # Agent 核心模块
│   ├── main.py               # 启动入口（CLI + 飞书）
│   ├── router.py             # 消息分发标准化
│   ├── agent.py              # LLM 处理（自然语言 → 动作序列）
│   ├── executor.py           # ADB 执行器
│   ├── config.py             # 配置文件
│   ├── prompt.txt            # 系统提示词
│   └── utils/
│       ├── logger.py         # 日志工具
│       └── screenshot.py     # 截图工具
├── im/
│   └── feishu_bot.py         # 飞书 Webhook 服务
├── logs/                     # 执行日志
├── screenshots/              # 截图文件
├── requirements.txt
├── .env                      # 环境变量（需自行创建）
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
# LLM 配置（兼容 OpenAI 接口的服务均可）
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o

# 飞书 Webhook 配置
FEISHU_WEBHOOK_PORT=5000
FEISHU_VERIFY_TOKEN=your_verify_token
```

### 3. 连接手机

```bash
# 开启手机 USB 调试，连接电脑
adb devices
# 确认设备已列出
```

### 4. 运行 CLI

```bash
# 交互模式
python -m autodroid_agent.main

# 单次执行
python -m autodroid_agent.main "打开YouTube并搜索猫猫视频"
```

### 5. 配置飞书机器人

1. 在飞书开发者后台创建**自定义机器人**
2. 配置 Webhook 地址：`http://你的服务器IP:5000/feishu/webhook`
3. 获取 Verify Token 填入 `.env` 的 `FEISHU_VERIFY_TOKEN`
4. 启动包含飞书服务的完整系统：

```bash
python -m autodroid_agent.main
```

飞书 Webhook 服务会自动在后台启动。

## 支持的 ADB 操作

| 动作 | 说明 | 示例 |
|------|------|------|
| `tap(x,y)` | 点击坐标 | `{"action":"tap","value":[500,1200]}` |
| `swipe(x1,y1,x2,y2)` | 滑动 | `{"action":"swipe","value":[300,800,300,200]}` |
| `open_app(name)` | 打开应用 | `{"action":"open_app","value":"YouTube"}` |
| `input(text)` | 输入文本 | `{"action":"input","value":"hello"}` |
| `wait(seconds)` | 等待 | `{"action":"wait","value":3}` |
| `screenshot()` | 截屏 | `{"action":"screenshot"}` |

## 安全机制

- 🛑 **连续点击超限** — 连续点击超过 5 次自动停止
- ⏱️ **执行超时** — 总执行时间超过 60 秒自动终止
- 📝 **异常捕获** — 所有异常记录到日志

## 常用应用包名

| 应用 | 包名 |
|------|------|
| YouTube | `com.google.android.youtube` |
| Chrome | `com.android.chrome` |
| 微信 | `com.tencent.mm` |
| 抖音 | `com.ss.android.ugc.aweme` |
| 支付宝 | `com.eg.android.AlipayGphone` |

在 `executor.py` 的 `APP_PACKAGE_MAP` 中可按需扩展。

## 日志与截图

- 日志文件：`logs/run.log`
- 截图文件：`screenshots/screenshot_时间戳.png`
- 每步执行状态都会打印到控制台

## 示例命令

```bash
# 打开应用
python -m autodroid_agent.main "打开微信"

# 组合操作
python -m autodroid_agent.main "打开YouTube，搜索cat videos，点击第一个结果"

# 滑动操作
python -m autodroid_agent.main "向下滑动页面"

# 交互模式
python -m autodroid_agent.main
```

## GitHub Actions 自动构建 APK

推送代码到 GitHub 后，CI 会自动：

1. 拉取 AutoDroid 源码
2. 安装 JDK 17 + Android SDK
3. 执行 `./gradlew assembleDebug`
4. 上传 APK 构建产物

构建产物可在 Actions 页面的 Artifacts 中下载。

---

**License:** Apache 2.0
