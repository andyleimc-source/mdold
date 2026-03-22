# mingdao-collab-mcp 需求文档

## 项目定位

封装明道协作时代的 v1 API 为 MCP Server，供 Claude Code 直接调用。

> 本项目封装的是明道协作时代的 v1 API，非明道云（HAP）零代码平台接口。
> 这些接口在明道转型零代码后仍部分可用，主要覆盖动态、日程、私信、群组、通讯录等协作功能。

## 目标

1. **Claude Code 集成** — 用户在 Claude Code 中直接说自然语言（如"查一下张三上周的动态"、"创建一个明天的日程"），Claude 自动调用对应 API 完成
2. **开源** — 其他明道用户 clone 后配置自己的凭证即可使用

## 技术方案

- **MCP Server**（stdio 模式），基于 `mcp` Python SDK
- 零外部依赖（除 mcp 包外，全部使用 Python 标准库）
- Token 管理复用现有 OAuth 逻辑（access_token 自动刷新，refresh_token 14天有效期）

## API 基础信息

- Base URL: `https://api.mingdao.com`
- 认证: 所有接口需要 `access_token` 参数
- GET 接口: URL query params
- POST 接口: form-urlencoded body
- 授权方式: OAuth 2.0 Authorization Code Grant（不支持 password grant）

## 模块范围

### 包含（共 ~95 个接口）

| 模块 | 接口数 | 说明 |
|------|--------|------|
| post | 18 | 动态：发布、评论、点赞、收藏、查询 |
| calendar | 21 | 日程：创建、编辑、邀请、查询 |
| webchat | 8 | 私信/聊天：消息收发、聊天列表 |
| message | 3 | 收件箱：系统消息、动态消息 |
| group | 18 | 群组：创建、管理、成员操作 |
| user | 12 | 用户/通讯录：查找、好友管理 |
| company | 8 | 组织/部门：部门列表、组织查询 |
| passport | 11 | 个人账户：用户详情、设置 |

### 排除

| 模块 | 原因 |
|------|------|
| kc (知识中心) | 用户明确排除 |
| task (任务) | 全部 404，已下线 |
| search | 排除 |
| qiniu | 排除 |
| application | 排除 |

## 项目结构

```
mingdao-collab-mcp/
├── .gitignore
├── .env.example
├── pyproject.toml
├── README.md
├── REQUIREMENTS.md
└── src/mingdao_collab_mcp/
    ├── __init__.py
    ├── server.py          # MCP Server 入口
    ├── auth.py            # OAuth token 管理
    ├── api_client.py      # HTTP 请求封装
    ├── tools_post.py      # 动态模块
    ├── tools_calendar.py  # 日程模块
    ├── tools_webchat.py   # 私信模块
    ├── tools_message.py   # 收件箱模块
    ├── tools_group.py     # 群组模块
    ├── tools_user.py      # 用户模块
    ├── tools_company.py   # 组织模块
    └── tools_passport.py  # 个人账户模块
```

## Token 生命周期

1. access_token 有效期 24 小时
2. refresh_token 有效期 14 天
3. MCP Server 启动时自动检查并刷新 access_token
4. 若 refresh_token 也过期，返回授权 URL 提示用户重新授权
