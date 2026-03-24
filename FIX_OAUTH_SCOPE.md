# 修复：calendar 和 webchat 写接口无权限

## 问题

`calendar_create_event` 和 `webchat_send_message` 调用失败，返回"请求异常"和"添加失败"。

经排查，**不是 token 过期，不是代理，不是代码 bug**，而是当前 OAuth 应用未授权 calendar 和 webchat 模块的写权限。

## 根本原因

OAuth app（app_key: `E338F086534D`）在明道开放平台注册时，scope 没有包含 `calendar` 和 `webchat` 模块，导致这两个模块的 POST 接口均被服务端拒绝。

**佐证：**
- GET 接口（读动态、读日程通过 iCal）正常
- 动态模块 POST 接口正常返回业务错误（说明 POST 请求链路没问题）
- calendar/create_event 返回 `{"error_code":0, "error_msg":"请求异常"}`
- webchat/send_message_card 返回 `{"error_code":99999, "error_msg":"添加失败"}`
- 两者均与明道文档中 scope 不足时的返回一致

## 修复步骤

1. 登录明道开放平台：https://open.mingdao.com
2. 找到 app_key 为 `E338F086534D` 的应用
3. 在「权限范围（Scope）」中勾选：
   - `calendar`（日程读写）
   - `webchat`（私信读写）
4. 保存后，重新走 OAuth 授权流程，获取新 token：

```bash
cd /Users/andy/Desktop/project/mingdao-collab-mcp

# 1. 构造授权 URL（redirect_uri 见 .env）
# 在浏览器打开：
# https://api.mingdao.com/oauth2/authorize?app_key=E338F086534D&redirect_uri=https://api.mingdao.com/workflow/hooks/NjliMTQwYTRmMzljMWYxYTIyZWRiMjFm&state=mcp-auth

# 2. 授权后从回调 URL 中获取 code 参数，执行：
.venv/bin/mingdao-collab-mcp exchange-code <code>
```

5. 新 token 会自动写入 `.secrets.json`，同时更新 Claude Code MCP 配置中的环境变量：

```bash
claude mcp remove "mingdao" -s user

claude mcp add --scope user \
  -e MINGDAO_APP_KEY=E338F086534D \
  -e MINGDAO_APP_SECRET=DEE73B40ADFC5A3257DF9FD1E9B71577 \
  -e "MINGDAO_REDIRECT_URI=https://api.mingdao.com/workflow/hooks/NjliMTQwYTRmMzljMWYxYTIyZWRiMjFm" \
  -e MINGDAO_ACCESS_TOKEN= \
  -e PYTHONPATH=/Users/andy/Desktop/project/mingdao-collab-mcp/src \
  -- /Users/andy/Desktop/project/mingdao-collab-mcp/.venv/bin/python3 -m mingdao_collab_mcp.server mingdao
```

## 验证

修复后用 curl 验证：

```bash
TOKEN=$(python3 -c "import json; print(json.load(open('.secrets.json'))['access_token'])")

# 创建日程
curl -s --noproxy '*' -X POST "https://api.mingdao.com/v1/calendar/create_event" \
  --data-urlencode "access_token=${TOKEN}" \
  --data-urlencode "format=json" \
  --data-urlencode "name=去苏州" \
  --data-urlencode "start_date=2026-03-26 09:00" \
  --data-urlencode "end_date=2026-03-26 18:00"

# 发私信给陆楠（account_id: 1d1e98a1-c05d-4891-9849-dfc0b3db0593）
curl -s --noproxy '*' -X POST "https://api.mingdao.com/v1/webchat/send_message_card" \
  --data-urlencode "access_token=${TOKEN}" \
  --data-urlencode "format=json" \
  --data-urlencode "to_account_id=1d1e98a1-c05d-4891-9849-dfc0b3db0593" \
  --data-urlencode "message=周四去苏州。这条消息是自动发送的，不需要回" \
  --data-urlencode "type=1"
```
