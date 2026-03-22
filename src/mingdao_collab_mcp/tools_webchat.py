"""私信/聊天 (Webchat) module — 8 tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .api_client import api_get, api_post


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    def webchat_get_chat_list() -> dict:
        """获取聊天会话列表。"""
        return api_get("/v1/webchat/get_chat_list")

    @mcp.tool()
    def webchat_get_unread_count() -> dict:
        """获取未读消息总数。"""
        return api_get("/v1/webchat/get_chat_un_read_count")

    @mcp.tool()
    def webchat_get_messages(id: str, type: int = 1, pagesize: int = 20) -> dict:
        """获取与某人或某群的消息记录。type: 1=个人, 2=群组。id 为 account_id 或 group_id。"""
        return api_get("/v1/webchat/get_user_or_group_message",
                       id=id, type=type, pagesize=pagesize)

    @mcp.tool()
    def webchat_get_message_by_id(message_id: str) -> dict:
        """根据消息ID获取特定消息。"""
        return api_get("/v1/webchat/get_user_or_group_message_by_id", message_id=message_id)

    @mcp.tool()
    def webchat_get_message_count(id: str | None = None, type: int | None = None) -> dict:
        """获取消息数量。"""
        return api_get("/v1/webchat/get_user_or_group_message_count", id=id, type=type)

    @mcp.tool()
    def webchat_send_message(to_account_id: str, message: str, type: int = 1) -> dict:
        """发送消息卡片。to_account_id 为接收者ID，type: 1=个人, 2=群组。"""
        return api_post("/v1/webchat/send_message_card",
                        to_account_id=to_account_id, message=message, type=type)

    @mcp.tool()
    def webchat_delete_history(id: str) -> dict:
        """删除一条聊天记录。"""
        return api_post("/v1/webchat/delete_chat_history_item", id=id)

    @mcp.tool()
    def webchat_set_push(group_id: str | None = None, is_push: int | None = None) -> dict:
        """设置消息推送开关。"""
        return api_post("/v1/webchat/set_single_or_all_group_push",
                        group_id=group_id, is_push=is_push)
