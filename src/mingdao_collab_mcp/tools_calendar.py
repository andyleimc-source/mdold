"""日程 (Calendar) module — 21 tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .api_client import api_get, api_post


def register(mcp: FastMCP) -> None:

    # ── GET ──────────────────────────────────────────────

    @mcp.tool()
    def calendar_get_events(
        start_date: str | None = None,
        end_date: str | None = None,
        is_private: int | None = None,
        category_id: str | None = None,
        member_id: str | None = None,
    ) -> dict:
        """按条件获取日程列表。日期格式 YYYY-MM-DD。"""
        return api_get("/v1/calendar/get_events_by_conditions",
                       start_date=start_date, end_date=end_date,
                       is_private=is_private, category_id=category_id,
                       member_id=member_id)

    @mcp.tool()
    def calendar_get_event_details(event_id: str) -> dict:
        """获取单个日程的详细信息。"""
        return api_get("/v1/calendar/get_event_details", Event_id=event_id)

    @mcp.tool()
    def calendar_get_unconfirmed_events() -> dict:
        """获取当前用户未确认的日程邀请。"""
        return api_get("/v1/calendar/get_unconfirmed_events")

    @mcp.tool()
    def calendar_get_conflicted_events(start_date: str | None = None, end_date: str | None = None) -> dict:
        """获取时间冲突的日程。"""
        return api_get("/v1/calendar/get_conflicted_events",
                       start_date=start_date, end_date=end_date)

    @mcp.tool()
    def calendar_get_categories() -> dict:
        """获取所有自定义日程分类。"""
        return api_get("/v1/calendar/get_all_user_defined_categories")

    @mcp.tool()
    def calendar_get_subscription_url() -> dict:
        """获取日历订阅 URL（可导入到其他日历应用）。"""
        return api_get("/v1/calendar/get_calendar_subscription_url")

    @mcp.tool()
    def calendar_search(keywords: str) -> dict:
        """按关键词搜索日程。"""
        return api_get("/v1/calendar/search_events_by_keyword", keywords=keywords)

    # ── POST ─────────────────────────────────────────────

    @mcp.tool()
    def calendar_create_event(
        name: str,
        start_date: str,
        end_date: str,
        address: str | None = None,
        description: str | None = None,
        is_all_day: int | None = None,
        is_private: int | None = None,
        category_id: str | None = None,
        member_ids: str | None = None,
        frequency: int | None = None,
        interval: int | None = None,
        recurcount: int | None = None,
    ) -> dict:
        """创建日程。日期格式 YYYY-MM-DD HH:MM。member_ids 用逗号分隔多个用户ID。"""
        return api_post("/v1/calendar/create_event",
                        name=name, start_date=start_date, end_date=end_date,
                        address=address, description=description,
                        is_all_day=is_all_day, is_private=is_private,
                        category_id=category_id, member_ids=member_ids,
                        frequency=frequency, interval=interval, recurcount=recurcount)

    @mcp.tool()
    def calendar_create_category(name: str, color: str | None = None) -> dict:
        """创建自定义日程分类。"""
        return api_post("/v1/calendar/create_user_defined_category", name=name, color=color)

    @mcp.tool()
    def calendar_add_members(event_id: str, member_ids: str) -> dict:
        """给日程添加成员。member_ids 用逗号分隔。"""
        return api_post("/v1/calendar/add_members_to_event",
                        Event_id=event_id, member_ids=member_ids)

    @mcp.tool()
    def calendar_confirm_invitation(event_id: str) -> dict:
        """确认日程邀请。"""
        return api_post("/v1/calendar/confirm_event_invitation", Event_id=event_id)

    @mcp.tool()
    def calendar_reject_invitation(event_id: str) -> dict:
        """拒绝日程邀请。"""
        return api_post("/v1/calendar/reject_event_invitation", Event_id=event_id)

    @mcp.tool()
    def calendar_reinvite_member(event_id: str, member_id: str) -> dict:
        """重新邀请某成员加入日程。"""
        return api_post("/v1/calendar/reinvite_a_member_to_event",
                        Event_id=event_id, member_id=member_id)

    @mcp.tool()
    def calendar_remove_member(event_id: str, member_id: str) -> dict:
        """从日程中移除某成员。"""
        return api_post("/v1/calendar/remove_a_member_on_event",
                        Event_id=event_id, member_id=member_id)

    @mcp.tool()
    def calendar_edit_event(
        event_id: str,
        name: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        address: str | None = None,
        description: str | None = None,
    ) -> dict:
        """修改日程的基本属性（名称、时间、地点、描述）。"""
        return api_post("/v1/calendar/edit_common_properties_on_event",
                        Event_id=event_id, name=name,
                        start_date=start_date, end_date=end_date,
                        address=address, description=description)

    @mcp.tool()
    def calendar_edit_category(event_id: str, category_id: str) -> dict:
        """修改日程的分类。"""
        return api_post("/v1/calendar/edit_category_of_an_event",
                        Event_id=event_id, category_id=category_id)

    @mcp.tool()
    def calendar_edit_share(event_id: str, is_share: int) -> dict:
        """修改日程的分享属性。is_share: 1=分享, 0=不分享。"""
        return api_post("/v1/calendar/edit_share_property_on_event",
                        Event_id=event_id, is_share=is_share)

    @mcp.tool()
    def calendar_edit_private(event_id: str, is_private: int) -> dict:
        """修改日程的私密属性。is_private: 1=私密, 0=公开。"""
        return api_post("/v1/calendar/edit_is_private_property_on_event",
                        Event_id=event_id, is_private=is_private)

    @mcp.tool()
    def calendar_edit_category_props(category_id: str, name: str | None = None, color: str | None = None) -> dict:
        """修改日程分类的属性（名称、颜色）。"""
        return api_post("/v1/calendar/edit_properites_on_category",
                        category_id=category_id, name=name, color=color)

    @mcp.tool()
    def calendar_edit_reminder(event_id: str, remind_time: int | None = None, remind_type: int | None = None) -> dict:
        """修改日程的提醒设置。"""
        return api_post("/v1/calendar/edit_reminder_on_event",
                        Event_id=event_id, remind_time=remind_time, remind_type=remind_type)

    @mcp.tool()
    def calendar_remove_event(event_id: str) -> dict:
        """删除日程。"""
        return api_post("/v1/calendar/remove_event", Event_id=event_id)

    @mcp.tool()
    def calendar_remove_category(category_id: str) -> dict:
        """删除自定义日程分类。"""
        return api_post("/v1/calendar/remove_user_defined_category", category_id=category_id)
