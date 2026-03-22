"""群组 (Group) module — 18 tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .api_client import api_get, api_post


def register(mcp: FastMCP) -> None:

    # ── GET ──────────────────────────────────────────────

    @mcp.tool()
    def group_get_detail(group_id: str) -> dict:
        """获取群组详情（含成员信息）。"""
        return api_get("/v1/group/get_group_detail", group_id=group_id)

    @mcp.tool()
    def group_get_members(group_id: str, pagesize: int = 100) -> dict:
        """获取群组成员列表。"""
        return api_get("/v1/group/get_group_members", group_id=group_id, pagesize=pagesize)

    @mcp.tool()
    def group_get_my_joined() -> dict:
        """获取当前用户加入的所有群组。"""
        return api_get("/v1/group/get_account_joined_groups")

    @mcp.tool()
    def group_get_my_created() -> dict:
        """获取当前用户创建的所有群组。"""
        return api_get("/v1/group/get_my_created_groups")

    @mcp.tool()
    def group_get_project_groups(project_id: str | None = None) -> dict:
        """获取组织下所有群组。"""
        return api_get("/v1/group/get_project_groups", project_id=project_id)

    @mcp.tool()
    def group_get_project_members(group_id: str, pagesize: int = 100) -> dict:
        """获取组织群组的成员列表。"""
        return api_get("/v1/group/get_project_group_members", group_id=group_id, pagesize=pagesize)

    @mcp.tool()
    def group_get_mentioned() -> dict:
        """获取可 @ 的群组列表。"""
        return api_get("/v1/group/get_mentioned_group")

    @mcp.tool()
    def group_get_unaudited(group_id: str) -> dict:
        """获取群组中待审核的成员。"""
        return api_get("/v1/group/get_unaudited_members", group_id=group_id)

    # ── POST ─────────────────────────────────────────────

    @mcp.tool()
    def group_create(
        name: str,
        about: str | None = None,
        is_approval: int | None = None,
        project_id: str | None = None,
    ) -> dict:
        """创建一个新群组。"""
        return api_post("/v1/group/create_group",
                        name=name, about=about, is_approval=is_approval,
                        project_id=project_id)

    @mcp.tool()
    def group_create_discussion(
        name: str,
        account_ids: str | None = None,
    ) -> dict:
        """创建讨论组。account_ids 用逗号分隔。"""
        return api_post("/v1/group/create_discussion_group",
                        name=name, account_ids=account_ids)

    @mcp.tool()
    def group_edit(
        group_id: str,
        name: str | None = None,
        about: str | None = None,
        is_approval: int | None = None,
    ) -> dict:
        """编辑群组信息。"""
        return api_post("/v1/group/edit_group",
                        group_id=group_id, name=name, about=about,
                        is_approval=is_approval)

    @mcp.tool()
    def group_exit(group_id: str) -> dict:
        """退出一个群组。"""
        return api_post("/v1/group/exit_group", group_id=group_id)

    @mcp.tool()
    def group_add_admin(group_id: str, account_id: str) -> dict:
        """添加群组管理员。"""
        return api_post("/v1/group/add_group_admin",
                        group_id=group_id, account_id=account_id)

    @mcp.tool()
    def group_apply_join(group_id: str) -> dict:
        """申请加入群组。"""
        return api_post("/v1/group/apply_join_group", group_id=group_id)

    @mcp.tool()
    def group_chat_to_post(group_id: str) -> dict:
        """将聊天内容转为群组动态。"""
        return api_post("/v1/group/chat_to_post_group", group_id=group_id)

    @mcp.tool()
    def group_audit_member(group_id: str, account_id: str, is_pass: int = 1) -> dict:
        """审核加入群组的申请。is_pass: 1=通过, 0=拒绝。"""
        return api_post("/v1/group/pass_or_refuse_user_join_group",
                        group_id=group_id, account_id=account_id, is_pass=is_pass)

    @mcp.tool()
    def group_remove_admin(group_id: str, account_id: str) -> dict:
        """移除群组管理员角色。"""
        return api_post("/v1/group/remove_group_admin_role",
                        group_id=group_id, account_id=account_id)

    @mcp.tool()
    def group_remove_member(group_id: str, account_id: str) -> dict:
        """将成员从群组中移除。"""
        return api_post("/v1/group/remove_group_user_or_admin",
                        group_id=group_id, account_id=account_id)
