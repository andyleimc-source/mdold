"""动态 (Post) module — 18 tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .api_client import api_get, api_post


def register(mcp: FastMCP) -> None:

    # ── GET ──────────────────────────────────────────────

    @mcp.tool()
    def post_get_all_posts(
        pagesize: int = 20,
        keywords: str | None = None,
        post_type: int | None = None,
        max_id: str | None = None,
        group_id: str | None = None,
        project_id: str | None = None,
        post_filter_share: int | None = None,
    ) -> dict:
        """获取全公司可见的动态流。可按关键词、类型、群组过滤。用 max_id 翻页。"""
        return api_get("/v1/post/get_all_posts",
                       pagesize=pagesize, keywords=keywords, post_type=post_type,
                       max_id=max_id, group_id=group_id, project_id=project_id,
                       post_filter_share=post_filter_share)

    @mcp.tool()
    def post_get_my_posts(pagesize: int = 20, max_id: str | None = None) -> dict:
        """获取当前用户自己发布的动态。"""
        return api_get("/v1/post/get_my_posts", pagesize=pagesize, max_id=max_id)

    @mcp.tool()
    def post_get_user_posts(account_id: str, pagesize: int = 20, max_id: str | None = None) -> dict:
        """获取指定用户的动态。account_id 为目标用户ID。"""
        return api_get("/v1/post/get_user_posts", account_id=account_id, pagesize=pagesize, max_id=max_id)

    @mcp.tool()
    def post_get_group_posts(group_id: str, pagesize: int = 20, max_id: str | None = None) -> dict:
        """获取指定群组的动态。"""
        return api_get("/v1/post/get_group_posts", group_id=group_id, pagesize=pagesize, max_id=max_id)

    @mcp.tool()
    def post_get_post_detail(post_id: str) -> dict:
        """获取单条动态的详细信息。"""
        return api_get("/v1/post/get_post_detail", post_id=post_id)

    @mcp.tool()
    def post_get_post_reply(post_id: str, pagesize: int = 20, max_id: str | None = None) -> dict:
        """获取某条动态的评论列表。"""
        return api_get("/v1/post/get_post_reply", post_id=post_id, pagesize=pagesize, max_id=max_id)

    @mcp.tool()
    def post_get_category_posts(category_id: str | None = None, pagesize: int = 20, max_id: str | None = None) -> dict:
        """按分类获取动态。"""
        return api_get("/v1/post/get_category_posts", category_id=category_id, pagesize=pagesize, max_id=max_id)

    @mcp.tool()
    def post_get_common_categories() -> dict:
        """获取常用的动态分类列表。"""
        return api_get("/v1/post/get_common_categories")

    @mcp.tool()
    def post_get_post_select_groups() -> dict:
        """获取当前用户可以发布动态的群组列表。"""
        return api_get("/v1/post/get_post_select_groups")

    @mcp.tool()
    def post_get_reply_by_me_posts(pagesize: int = 20, max_id: str | None = None) -> dict:
        """获取当前用户评论过的动态列表。"""
        return api_get("/v1/post/get_reply_by_me_posts", pagesize=pagesize, max_id=max_id)

    # ── POST ─────────────────────────────────────────────

    @mcp.tool()
    def post_add_post(
        post_msg: str,
        group_id: str | None = None,
        category_id: str | None = None,
        scope: int | None = None,
    ) -> dict:
        """发布一条新动态。post_msg 为动态内容，可指定群组和分类。"""
        return api_post("/v1/post/add_post",
                        post_msg=post_msg, group_id=group_id,
                        category_id=category_id, scope=scope)

    @mcp.tool()
    def post_add_post_reply(post_id: str, reply_msg: str) -> dict:
        """给指定动态添加评论。"""
        return api_post("/v1/post/add_post_reply", post_id=post_id, reply_msg=reply_msg)

    @mcp.tool()
    def post_delete_post(post_id: str) -> dict:
        """删除一条动态。"""
        return api_post("/v1/post/delete_post", post_id=post_id)

    @mcp.tool()
    def post_delete_post_reply(reply_id: str) -> dict:
        """删除一条动态评论。"""
        return api_post("/v1/post/delete_post_reply", reply_id=reply_id)

    @mcp.tool()
    def post_like(post_id: str) -> dict:
        """点赞或取消点赞一条动态。"""
        return api_post("/v1/post/update_like_or_cancel_like_post", post_id=post_id)

    @mcp.tool()
    def post_collect(post_id: str) -> dict:
        """收藏或取消收藏一条动态。"""
        return api_post("/v1/post/update_collect_or_cancel_collect_post", post_id=post_id)

    @mcp.tool()
    def post_top(post_id: str) -> dict:
        """置顶一条动态。"""
        return api_post("/v1/post/top_post", post_id=post_id)

    @mcp.tool()
    def post_vote(post_id: str, option_index: int) -> dict:
        """对动态中的投票进行投票。option_index 为选项序号。"""
        return api_post("/v1/post/add_cast_options", post_id=post_id, option_index=option_index)
