# 🤝 Contributing to CiCi

感谢你的关注！CiCi 是一个开源项目，期待你的贡献 🦞

## 贡献方式

### 🐛 报告 Bug

在 Issues 中提交，请包含以下信息：
- Android 版本 + 手机型号
- CiCi 版本号（Web 配置页底部可见）
- 复现步骤 + 期望行为 + 实际行为
- 相关截图或日志

### 💡 功能建议

提出新功能前，先搜索是否有类似的已有提案或实现。描述清楚使用场景和价值。

### 🔧 提交 PR

```bash
# 1. Fork 本仓库
# 2. 创建功能分支
git checkout -b feat/my-feature

# 3. 如果是 Android 代码修改，文件放在 patches/hermes-agent/ 下对应路径
#    模仿现有 patch 文件风格编写

# 4. 提交
git commit -m "feat: 你的功能描述"

# 5. Push 并创建 PR
```

### 📝 补丁开发规范

本项目通过 patch 文件增强上游 [hermes-agent](https://github.com/xiaoxuan0820-ctrl/hermes-agent) (android 目录)。每个 patch 文件：
- 必须能**完整替换**上游同路径文件
- 保持与上游一致的包名和类名
- 新增类放在对应业务包下（如 memory、skill、scheduler）
- 新增依赖在 CI workflow 的 build.gradle 注入步骤中声明

### 🏗 本地验证

```bash
# 克隆上游
git clone https://github.com/xiaoxuan0820-ctrl/hermes-agent
cd hermes-agent/android

# 应用 patch
cp -r /path/to/AegisForge/patches/hermes-agent/src/main/java/com/apk/claw/android/* \
     app/src/main/java/com/apk/claw/android/

# 构建
./gradlew assembleDebug

# 安装测试
adb install app/build/outputs/apk/debug/*.apk
```

### 🌍 文档贡献

如果你发现文档有误或不够清楚，欢迎直接提 PR 修改 `README.md`

## 行为准则

- 友善、尊重地交流
- 接受建设性批评
- 关注对社区最有利的方案
- 展现同理心

---

再次感谢！每一份贡献都让闲置手机更有用 🦞
