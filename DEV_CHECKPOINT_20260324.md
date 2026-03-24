# 开发节点归档 — 2026-03-24

## 项目概述

明道协作 MCP Server，封装明道开放平台 v1 API，供 Claude Code 通过 MCP 协议调用。
项目路径：`/Users/andy/Desktop/project/mingdao-collab-mcp`

---

## 本次会话做了什么

### 目标
验证并修复 calendar（日程）和 webchat（私信）两个模块的写接口无法调用的问题，并将全部模块的 API 参数按官方文档重新对齐。

### 结论
**根本原因：代码里的参数名与官方文档不符，不是权限问题，不是 token 问题。**

---

## 错误清单与修复

### calendar 模块（`tools_calendar.py`）

| 错误类型 | 旧参数名 | 正确参数名 |
|---|---|---|
| 日程开始时间 | `start_date` | `begin_date` |
| 日程描述 | `description` | `event_description` |
| 全天日程 | `is_all_day` | `is_all_day_event` |
| 私人日程 | `is_private` | `is_private_event` |
| 创建分类名称 | `name` | `category_name` |
| 分类颜色类型 | `str` | `int`（0=红,1=紫,2=青,3=橙,4=蓝,5=绿,6=黄）|
| 分享属性 | `is_share` | `is_shareable` |
| 分类属性名称 | `name` | `category_name` |
| 提醒类型 | `remind_type` | `reminder_type` |
| 搜索关键词 | `keywords` | `keyword` |
| 删除日程 | 缺少 `removing_all_recurring_events` | 已补充 |
| `edit_event` | `start_date`, `description` | `begin_date`, `event_description` |

### webchat 模块（`tools_webchat.py`）

| 错误类型 | 旧值 | 正确值 |
|---|---|---|
| 发送消息接口路径 | `/v1/webchat/send_message_card` | `/v1/webchat/send_message` |
| 接收者参数名 | `to_account_id` | `account_id` |
| 获取消息参数 | `id` + `type` | `account_id` / `group_id` |
| 获取消息数参数 | `id` + `type` | `account_id` / `group_id` |
| 删除记录参数 | `id` | `account_id` / `group_id` |
| 推送开关参数 | `is_push` (无 `choose_type`) | 补充 `choose_type: bool` |

> **注意**：官方 JS 文档中 `send_message` URL 写的是 `send_message_card`，但实测 `send_message_card` 返回 99999 失败，`send_message` 成功。以实测为准，保持 `/v1/webchat/send_message`。

### post 模块（`tools_post.py`）

| 错误类型 | 旧值 | 正确值 |
|---|---|---|
| 发布动态群组参数 | `group_id` | `group_ids`（复数，逗号分隔）|
| 发布动态缺少必要参数 | 无 `post_type` | 已补充，默认 0 |
| 投票参数名 | `option_index` | `options`（格式 `"1\|3"`）|
| 点赞缺少方向参数 | 无 `is_like` | 已补充 `is_like: bool` |
| 收藏缺少方向参数 | 无 `is_collect` | 已补充 `is_collect: bool` |
| 置顶缺少时长参数 | 无 `hour` | 已补充 `hour: int \| None` |
| 删除评论缺少 post_id | 无 `post_id` | 已补充为必填 |

### task 模块（`tools_task.py`）

| 错误类型 | 旧参数名 | 正确参数名 |
|---|---|---|
| 任务描述 | `des` | `task_description` |
| 截止日期 | `dead_line` | `deadline` |
| 负责人 | `charge_account_id` | `charge_user_account_id` |
| 阶段 ID | `stage_id` | `folder_stage_id` |
| 修改截止日期缺少参数 | 无 `include_sub_tasks` | 已补充 |

### user 模块（`tools_user.py`）

| 错误类型 | 旧参数名 | 正确参数名 |
|---|---|---|
| 按手机/邮箱查用户 | `phone` | `identifier` |
| 批量添加通讯录 | `phones` | `mobiles` |

---

## 如何获取官方接口文档

明道文档页面是动态渲染的（JS 驱动），WebFetch 直接抓拿不到参数内容。**正确方法是直接访问官方 JS 数据文件：**

```
https://open.mingdao.com/Content/javascript/apiSetting.js
```

这个文件约 170KB，包含所有接口模块的完整参数定义（约 2772 行），是文档页面的数据来源。用 `Bash + curl` 或 `WebFetch` 直接抓这个文件，就能拿到所有参数。

文档入口页面：`https://open.mingdao.com/document`
接口详情页规律：`https://open.mingdao.com/doc/v1/{模块}/{接口名}`（如 `calendar/create_event`）

---

## 当前认证状态

- **当前使用的 app_key**：`E338F086534D`（已写入 `.env` 和 `.secrets.json`）
- **token 状态**：本次会话末尾已重新授权，有效期 24 小时（约到 2026-03-25 23:00）
- **refresh_token 有效期**：14 天

重新授权流程：
```bash
# 1. 浏览器打开（localhost:8080 需提前启动 http.server）
https://api.mingdao.com/oauth2/authorize?app_key=E338F086534D&redirect_uri=http://localhost:8080/callback&state=mcp-auth

# 2. 获取 code 后执行
PYTHONPATH=src .venv/bin/python3 -c "
import sys, os
os.environ['MINGDAO_APP_KEY'] = 'E338F086534D'
os.environ['MINGDAO_APP_SECRET'] = 'DEE73B40ADFC5A3257DF9FD1E9B71577'
os.environ['MINGDAO_REDIRECT_URI'] = 'http://localhost:8080/callback'
sys.argv = ['mingdao-collab-mcp', 'exchange-code', '<CODE>']
from mingdao_collab_mcp.server import main
main()
"
```

---

## 当前状态：未提交

所有修改均已完成但**尚未 git commit**。涉及文件：
- `src/mingdao_collab_mcp/tools_calendar.py`
- `src/mingdao_collab_mcp/tools_webchat.py`
- `src/mingdao_collab_mcp/tools_post.py`
- `src/mingdao_collab_mcp/tools_task.py`
- `src/mingdao_collab_mcp/tools_user.py`
- `src/mingdao_collab_mcp/auth.py`（有少量改动）
- `.env`（已切换为 `E338F086534D`）

---

## 明天开启新会话后该做什么

1. **先 commit 当前改动**（重要，防止丢失）
2. **重启 Claude Code** 让 MCP 加载新代码（`/restart`）
3. **验证三个原始任务**：
   - 发布动态 ✅（本次已成功）
   - 创建日程（修复后应可用，待重启后验证）
   - 给陆楠发私信（修复后应可用，待重启后验证）
4. **可选**：继续检查其他模块（group、passport、message、company）是否也有参数名错误，方法同上——对照 `apiSetting.js` 逐一核查

---

## 已知的其他问题（本次未处理）

- `get_events_by_conditions` 和 `get_conflicted_events`：服务端 bug，返回"请求异常"，已用 iCal 订阅方式绕过，无需修复
- group、passport、message、company 模块未做参数核查，可能存在类似问题
