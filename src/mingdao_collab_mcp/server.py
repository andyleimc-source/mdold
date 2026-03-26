"""MCP Server entry point for Mingdao Collaboration API."""

from __future__ import annotations

import sys

from mcp.server.fastmcp import FastMCP

from . import tools_post, tools_calendar, tools_webchat, tools_message
from . import tools_group, tools_user, tools_company, tools_passport
from . import tools_task

mcp = FastMCP(
    "mingdao-collab",
    instructions=(
        "明道协作时代 v1 API 工具集。"
        "覆盖动态(post)、日程(calendar)、私信(webchat)、收件箱(message)、"
        "群组(group)、用户(user)、组织(company)、个人账户(passport)、任务(task) 九个模块。"
        "所有工具需要有效的 access_token，启动前请确保 .env 和 .secrets.json 已配置。"
    ),
)

# Register all modules
tools_post.register(mcp)
tools_calendar.register(mcp)
tools_webchat.register(mcp)
tools_message.register(mcp)
tools_group.register(mcp)
tools_user.register(mcp)
tools_company.register(mcp)
tools_passport.register(mcp)
tools_task.register(mcp)


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "exchange-code":
        from .auth import exchange_code, get_env_config
        if len(sys.argv) < 3:
            print("Usage: mdold exchange-code <code>")
            sys.exit(1)
        config = get_env_config()
        result = exchange_code(
            app_key=config["app_key"],
            app_secret=config["app_secret"],
            redirect_uri=config["redirect_uri"],
            code=sys.argv[2],
        )
        if result.get("success"):
            print("Token saved to .secrets.json")
        else:
            print(f"Error: {result}")
            sys.exit(1)
    elif len(sys.argv) > 1 and sys.argv[1] == "authorize-url":
        from .auth import build_authorize_url, get_env_config
        config = get_env_config()
        url = build_authorize_url(config["app_key"], config["redirect_uri"])
        print(f"Open this URL in your browser:\n{url}")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
