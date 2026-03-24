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
    def webchat_get_messages(account_id: str | None = None, group_id: str | None = None,
                              pageindex: int = 1, pagesize: int = 20,
                              keyword: str | None = None) -> dict:
        """获取与某人或某群的消息记录。account_id 和 group_id 二选一。"""
        return api_get("/v1/webchat/get_user_or_group_message",
                       account_id=account_id, group_id=group_id,
                       pageindex=pageindex, pagesize=pagesize, keyword=keyword)

    @mcp.tool()
    def webchat_get_message_by_id(message_id: str, account_id: str | None = None,
                                   group_id: str | None = None, size: int | None = None) -> dict:
        """根据消息ID获取前后消息。account_id 和 group_id 二选一。"""
        return api_get("/v1/webchat/get_user_or_group_message_by_id",
                       message_id=message_id, account_id=account_id,
                       group_id=group_id, size=size)

    @mcp.tool()
    def webchat_get_message_count(account_id: str | None = None, group_id: str | None = None) -> dict:
        """获取与某人或某群的消息总数。account_id 和 group_id 二选一。"""
        return api_get("/v1/webchat/get_user_or_group_message_count",
                       account_id=account_id, group_id=group_id)

    @mcp.tool()
    def webchat_send_message(message: str, account_id: str | None = None, group_id: str | None = None) -> dict:
        """给用户或群组发送文本消息。account_id 和 group_id 二选一。"""
        return api_post("/v1/webchat/send_message",
                        account_id=account_id, group_id=group_id, message=message)

    @mcp.tool()
    def webchat_delete_history(account_id: str | None = None, group_id: str | None = None) -> dict:
        """删除聊天记录。account_id 和 group_id 二选一。"""
        return api_post("/v1/webchat/delete_chat_history_item",
                        account_id=account_id, group_id=group_id)

    @mcp.tool()
    def webchat_set_push(is_push: bool, choose_type: bool = True, group_id: str | None = None) -> dict:
        """设置消息推送开关。choose_type: True=单个群组, False=全部群组。"""
        return api_post("/v1/webchat/set_single_or_all_group_push",
                        is_push=is_push, choose_type=choose_type, group_id=group_id)
