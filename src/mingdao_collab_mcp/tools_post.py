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
        post_type: int = 0,
        group_ids: str | None = None,
        project_ids: str | None = None,
    ) -> dict:
        """发布一条新动态。post_type: 0=普通,1=链接,2=图片,3=文档,4=提问,7=投票。group_ids/project_ids 逗号分隔。"""
        return api_post("/v1/post/add_post",
                        post_msg=post_msg, post_type=post_type,
                        group_ids=group_ids, project_ids=project_ids)

    @mcp.tool()
    def post_add_post_reply(post_id: str, reply_msg: str, reply_id: str | None = None) -> dict:
        """给指定动态添加评论。reply_id 为回复某条评论时填写。"""
        return api_post("/v1/post/add_post_reply", post_id=post_id, reply_msg=reply_msg, reply_id=reply_id)

    @mcp.tool()
    def post_delete_post(post_id: str) -> dict:
        """删除一条动态。"""
        return api_post("/v1/post/delete_post", post_id=post_id)

    @mcp.tool()
    def post_delete_post_reply(post_id: str, reply_id: str | None = None) -> dict:
        """删除一条动态评论。post_id 必填，reply_id 为要删除的评论ID。"""
        return api_post("/v1/post/delete_post_reply", post_id=post_id, reply_id=reply_id)

    @mcp.tool()
    def post_like(post_id: str, is_like: bool = True) -> dict:
        """点赞或取消点赞一条动态。is_like: True=点赞, False=取消。"""
        return api_post("/v1/post/update_like_or_cancel_like_post", post_id=post_id, is_like=is_like)

    @mcp.tool()
    def post_collect(post_id: str, is_collect: bool = True) -> dict:
        """收藏或取消收藏一条动态。is_collect: True=收藏, False=取消。"""
        return api_post("/v1/post/update_collect_or_cancel_collect_post", post_id=post_id, is_collect=is_collect)

    @mcp.tool()
    def post_top(post_id: str, hour: int | None = None) -> dict:
        """置顶一条动态（仅网络管理员）。hour 为置顶时长（小时），不填则不限时长。"""
        return api_post("/v1/post/top_post", post_id=post_id, hour=hour)

    @mcp.tool()
    def post_vote(post_id: str, options: str) -> dict:
        """对投票动态投票。options 格式如 '1|3' 表示选第1和第3项。"""
        return api_post("/v1/post/add_cast_options", post_id=post_id, options=options)
