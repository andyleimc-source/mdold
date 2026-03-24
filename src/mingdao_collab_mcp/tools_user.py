"""用户/通讯录 (User) module — 12 tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .api_client import api_get, api_post


def register(mcp: FastMCP) -> None:

    # ── GET ──────────────────────────────────────────────

    @mcp.tool()
    def user_get_friends(pagesize: int = 100) -> dict:
        """获取当前用户的联系人列表。"""
        return api_get("/v1/user/get_my_friends", pagesize=pagesize)

    @mcp.tool()
    def user_get_project_users(project_id: str | None = None, pagesize: int = 100) -> dict:
        """获取组织通讯录（所有成员）。"""
        return api_get("/v1/user/get_project_users",
                       project_id=project_id, pagesize=pagesize)

    @mcp.tool()
    def user_get_mentioned(keywords: str | None = None) -> dict:
        """获取可 @ 的用户列表，可按关键词过滤。"""
        return api_get("/v1/user/get_mentioned_users", keywords=keywords)

    @mcp.tool()
    def user_get_by_phone(identifier: str) -> dict:
        """根据手机号或邮箱查找用户。"""
        return api_get("/v1/user/get_account_byphone", identifier=identifier)

    @mcp.tool()
    def user_get_address_recommend() -> dict:
        """获取通讯录推荐的用户。"""
        return api_get("/v1/user/get_mobile_address_recommend")

    @mcp.tool()
    def user_get_new_friends() -> dict:
        """获取新好友列表。"""
        return api_get("/v1/user/get_new_friends")

    @mcp.tool()
    def user_get_card(account_id: str) -> dict:
        """获取指定用户的名片信息。"""
        return api_get("/v1/user/get_user_card", account_id=account_id)

    @mcp.tool()
    def user_get_subordinate(project_id: str) -> dict:
        """获取下属列表。"""
        return api_get("/v1/user/get_user_subordinate", project_id=project_id)

    # ── POST ─────────────────────────────────────────────

    @mcp.tool()
    def user_add_friend(account_id: str) -> dict:
        """添加好友。"""
        return api_post("/v1/user/add_friend", account_id=account_id)

    @mcp.tool()
    def user_add_mobile_address(mobiles: str) -> dict:
        """通过手机号批量添加通讯录。mobiles 格式如 [13000000000,13000000001]。"""
        return api_post("/v1/user/add_mobile_address", mobiles=mobiles)

    @mcp.tool()
    def user_remove_friend(account_id: str) -> dict:
        """删除好友。"""
        return api_post("/v1/user/remove_friend", account_id=account_id)

    @mcp.tool()
    def user_shield_friend(account_id: str) -> dict:
        """屏蔽好友。"""
        return api_post("/v1/user/shield_friend", account_id=account_id)

    @mcp.tool()
    def user_update_friend_status(account_id: str, status: int) -> dict:
        """更新好友状态。"""
        return api_post("/v1/user/update_friend_status",
                        account_id=account_id, status=status)
