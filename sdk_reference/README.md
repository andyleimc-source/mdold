# 明道官方 SDK 参考资料

来源：https://github.com/mingdaocom/api_python

## 文件说明

| 文件 | 大小 | 说明 |
|------|------|------|
| `mingdao_api.json` | 103KB | **核心文件**。所有接口的完整定义：路径、方法、参数名、参数类型、是否必填、参数说明 |
| `mingdao_api_description.json` | 10KB | 各接口的中文描述索引（模块→接口→说明） |
| `mingdao_api_errorcode.json` | 3KB | 错误码对照表（10101=token不存在，10105=token过期，等） |

## 重要说明

1. **官方 SDK 是 Python 2.7** (`from urllib import urlencode`)，我们的项目是 Python 3.12。
2. **官方 SDK 路径格式**是 `{module}/{action}`（如 `task/create`），对应我们的 `/v1/task/create`。
3. **大量接口已废弃**：特别是 task 和 calendar 的 GET 列表接口，Mingdao 迁移到低代码平台后返回 404。
4. **参数名差异**：官方 SDK 用 `t_id`, `t_title`, `t_des`, `c_name`, `c_stime` 等；我们的 /v1/ API 用 `task_id`, `task_name`, `event_id`, `name`, `begin_date` 等——以实测为准。

## 查询方法

```python
import json

with open("sdk_reference/mingdao_api.json") as f:
    apis = json.load(f)

# 找某个接口的参数
for item in apis:
    if item["api"] == "task/create":
        for arg in item["args"]:
            print(f"  {'★' if arg['required'] else ' '} {arg['name']} ({arg['type']}) — {arg['description']}")
```

## 授权说明

- `access_token` 有效期 24 小时
- `refresh_token` 自动续期（已在 `auth.py::ensure_access_token()` 实现）
- refresh_token 过期后需手动重新授权：见 `DEV_CHECKPOINT_20260324.md`
