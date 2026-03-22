"""收件箱消息 (Message) module — 3 tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .api_client import api_get, api_post


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    def message_get_system(pagesize: int = 20) -> dict:
        """获取系统消息列表。"""
        return api_get("/v1/message/get_inbox_system_message", pagesize=pagesize)

    @mcp.tool()
    def message_get_post(pagesize: int = 20) -> dict:
        """获取与动态相关的收件箱消息。"""
        return api_get("/v1/message/get_inbox_post_message", pagesize=pagesize)

    @mcp.tool()
    def message_favorite(message_id: str) -> dict:
        """收藏或取消收藏一条收件箱消息。"""
        return api_post("/v1/message/update_inbox_message_favorite", message_id=message_id)
