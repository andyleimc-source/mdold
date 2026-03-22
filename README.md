# mingdao-collab-mcp

MCP Server for Mingdao Collaboration-era v1 API.

> **注意：** 本项目封装的是明道**协作时代**的 v1 API，**非**明道云（HAP）零代码平台接口。这些接口在明道转型零代码后仍部分可用，主要覆盖动态、日程、私信、群组、通讯录等协作功能。

## 功能模块

| 模块 | 工具数 | 说明 |
|------|--------|------|
| post | 18 | 动态：发布、评论、点赞、收藏、查询 |
| calendar | 22 | 日程：创建、编辑、邀请、查询 |
| webchat | 8 | 私信/聊天：消息收发、聊天列表 |
| message | 3 | 收件箱：系统消息、动态消息 |
| group | 18 | 群组：创建、管理、成员操作 |
| user | 13 | 用户/通讯录：查找、好友管理 |
| company | 8 | 组织/部门：部门列表、组织查询 |
| passport | 11 | 个人账户：用户详情、设置 |

共计 **101 个工具**，覆盖 8 个模块。

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/user/mingdao-collab-mcp.git
cd mingdao-collab-mcp
```

### 2. 安装依赖

```bash
pip install -e .
# 或者
pip install "mcp[cli]"
```

### 3. 配置凭证

```bash
cp .env.example .env
```

编辑 `.env`，填入你在明道开放平台创建的应用凭证：

```env
MINGDAO_APP_KEY=你的app_key
MINGDAO_APP_SECRET=你的app_secret
MINGDAO_REDIRECT_URI=你的回调地址
```

> 在哪里获取？登录 https://open.mingdao.com ，创建一个应用，在应用设置中获取 app_key 和 app_secret。回调地址需与应用中配置的完全一致。

### 4. 首次授权

```bash
# 生成授权链接
python -m mingdao_collab_mcp.server authorize-url

# 在浏览器中打开链接，登录明道账号并授权
# 授权后浏览器会跳转到回调地址，从 URL 中复制 code 参数

# 用 code 换取 token
python -m mingdao_collab_mcp.server exchange-code 你拿到的code
```

Token 会保存在 `.secrets.json` 中（已在 .gitignore 中排除）。

### 5. 在 Claude Code 中使用

在你的项目目录创建 `.mcp.json`：

```json
{
  "mcpServers": {
    "mingdao": {
      "command": "python3",
      "args": ["-m", "mingdao_collab_mcp.server"],
      "cwd": "/path/to/mingdao-collab-mcp"
    }
  }
}
```

然后打开 Claude Code，就可以直接用自然语言操作明道了：

- "帮我看看张三最近发了什么动态"
- "创建一个明天上午 10 点的日程，邀请李四"
- "给王五发一条消息说下午 3 点开会"
- "列出公司所有部门"
- "查一下全体群有哪些成员"

## Token 生命周期

| Token | 有效期 | 说明 |
|-------|--------|------|
| access_token | 24 小时 | MCP Server 启动时自动检查，过期后自动用 refresh_token 刷新 |
| refresh_token | 14 天 | 自动续期，14 天内只要跑过一次就不会过期 |

如果超过 14 天没有使用，两个 token 都会过期，需要重新走一次浏览器授权流程（步骤 4）。

**建议：** 设置一个每周自动运行的定时任务来保持 token 活跃：

```bash
# crontab -e
0 9 * * 1 cd /path/to/mingdao-collab-mcp && python3 -c "from src.mingdao_collab_mcp.auth import ensure_access_token; ensure_access_token()"
```

## 安全提醒

- `.env` 和 `.secrets.json` 包含敏感凭证，**绝不要**提交到 git
- 这两个文件已在 `.gitignore` 中排除
- 如果你 fork 了本项目，请确认这些文件没有被提交

## 项目结构

```
mingdao-collab-mcp/
├── .env.example          # 环境变量模板
├── .gitignore            # 排除密钥文件
├── pyproject.toml        # 项目配置
├── README.md
├── REQUIREMENTS.md       # 需求文档
└── src/mingdao_collab_mcp/
    ├── __init__.py
    ├── server.py          # MCP Server 入口
    ├── auth.py            # OAuth token 管理
    ├── api_client.py      # HTTP 请求封装
    ├── tools_post.py      # 动态（18 个工具）
    ├── tools_calendar.py  # 日程（22 个工具）
    ├── tools_webchat.py   # 私信（8 个工具）
    ├── tools_message.py   # 收件箱（3 个工具）
    ├── tools_group.py     # 群组（18 个工具）
    ├── tools_user.py      # 用户（13 个工具）
    ├── tools_company.py   # 组织（8 个工具）
    └── tools_passport.py  # 个人账户（11 个工具）
```

## API 文档

本项目基于明道开放平台的 v1 API：https://open.mingdao.com/document

完整的接口参考见 [REQUIREMENTS.md](REQUIREMENTS.md)。

## License

MIT
