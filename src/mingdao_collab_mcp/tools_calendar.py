"""日程 (Calendar) module — 21 tools.

NOTE: The /v1/calendar/get_events_by_conditions endpoint is broken on the
server side (returns "请求异常" regardless of parameters).  As a workaround,
calendar_get_events fetches the iCal subscription feed via
get_calendar_subscription_url and parses it client-side.
The /v1/calendar/get_conflicted_events endpoint is also broken and removed.
"""

from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime, timedelta, timezone

from mcp.server.fastmcp import FastMCP

from .api_client import api_get, api_post

_CST = timezone(timedelta(hours=8))


def _parse_ical_events(ical_text: str,
                       start_filter: str | None = None,
                       end_filter: str | None = None) -> list[dict]:
    """Parse VEVENT blocks from iCal text and optionally filter by date range.

    Parameters
    ----------
    ical_text : raw iCal text
    start_filter : inclusive lower bound, YYYY-MM-DD (CST)
    end_filter : inclusive upper bound, YYYY-MM-DD (CST)
    """
    if start_filter:
        filter_start = datetime.strptime(start_filter, "%Y-%m-%d").replace(tzinfo=_CST)
    else:
        filter_start = None
    if end_filter:
        # end of that day
        filter_end = datetime.strptime(end_filter, "%Y-%m-%d").replace(
            hour=23, minute=59, second=59, tzinfo=_CST)
    else:
        filter_end = None

    def _get(block: str, name: str) -> str:
        # Handle folded lines and parameters (e.g. DTSTART;TZID=...)
        m = re.search(rf'^{name}[;:](.*)$', block, re.MULTILINE)
        return m.group(1).strip() if m else ""

    def _parse_dt(raw: str) -> datetime | None:
        s = raw.replace("Z", "")
        try:
            if "T" in s:
                dt = datetime.strptime(s, "%Y%m%dT%H%M%S")
                if raw.endswith("Z"):
                    dt = dt.replace(tzinfo=timezone.utc).astimezone(_CST)
                else:
                    dt = dt.replace(tzinfo=_CST)
            else:
                dt = datetime.strptime(s, "%Y%m%d").replace(tzinfo=_CST)
            return dt
        except ValueError:
            return None

    results: list[dict] = []
    for m in re.finditer(r"BEGIN:VEVENT(.*?)END:VEVENT", ical_text, re.DOTALL):
        block = m.group(1)
        dt_start = _parse_dt(_get(block, "DTSTART"))
        if dt_start is None:
            continue

        # Apply date filter
        if filter_start and dt_start < filter_start:
            continue
        if filter_end and dt_start > filter_end:
            continue

        dt_end = _parse_dt(_get(block, "DTEND"))
        summary = _get(block, "SUMMARY")
        description = _get(block, "DESCRIPTION")
        location = _get(block, "LOCATION")
        uid = _get(block, "UID")
        organizer = _get(block, "ORGANIZER")
        # Clean up organizer MAILTO:
        if "MAILTO:" in organizer:
            organizer = organizer.split("MAILTO:")[-1]

        results.append({
            "event_id": uid,
            "summary": summary,
            "start_time": dt_start.strftime("%Y-%m-%d %H:%M"),
            "end_time": dt_end.strftime("%Y-%m-%d %H:%M") if dt_end else "",
            "location": location,
            "description": description[:500] if description else "",
            "organizer": organizer,
        })

    results.sort(key=lambda e: e["start_time"])
    return results


def register(mcp: FastMCP) -> None:

    # ── GET ──────────────────────────────────────────────

    @mcp.tool()
    def calendar_get_events(
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict:
        """获取日程列表。通过日历订阅接口拉取 iCal 数据并解析。

        日期格式 YYYY-MM-DD，用于过滤日程范围（北京时间）。
        不传日期则返回所有日程。
        """
        # Step 1: get subscription URL
        resp = api_get("/v1/calendar/get_calendar_subscription_url")
        if not resp.get("success"):
            return resp
        sub_url = resp.get("data", {}).get("subscription_url", "")
        if not sub_url:
            return {"success": False, "error_msg": "无法获取日历订阅地址"}

        # Step 2: fetch iCal feed
        req = urllib.request.Request(sub_url, method="GET",
                                     headers={"User-Agent": "mdold/0.1"})
        with urllib.request.urlopen(req, timeout=60) as r:
            ical_text = r.read().decode("utf-8")

        # Step 3: parse & filter
        events = _parse_ical_events(ical_text, start_date, end_date)
        return {"data": events, "count": len(events), "success": True, "error_code": 1}

    @mcp.tool()
    def calendar_get_event_details(event_id: str) -> dict:
        """获取单个日程的详细信息。"""
        return api_get("/v1/calendar/get_event_details", event_id=event_id)

    @mcp.tool()
    def calendar_get_unconfirmed_events(page_index: int = 1, page_size: int = 20) -> dict:
        """获取当前用户未确认的日程邀请。"""
        return api_get("/v1/calendar/get_unconfirmed_events", page_index=page_index, page_size=page_size)

    @mcp.tool()
    def calendar_get_categories() -> dict:
        """获取所有自定义日程分类。"""
        return api_get("/v1/calendar/get_all_user_defined_categories")

    @mcp.tool()
    def calendar_get_subscription_url() -> dict:
        """获取日历订阅 URL（可导入到其他日历应用）。"""
        return api_get("/v1/calendar/get_calendar_subscription_url")

    @mcp.tool()
    def calendar_search(keyword: str, begin_date: str | None = None, end_date: str | None = None) -> dict:
        """按关键词搜索日程。begin_date/end_date 格式 YYYY-MM-DD。"""
        return api_get("/v1/calendar/search_events_by_keyword",
                       keyword=keyword, begin_date=begin_date, end_date=end_date)

    # ── POST ─────────────────────────────────────────────

    @mcp.tool()
    def calendar_create_event(
        name: str,
        begin_date: str,
        end_date: str,
        address: str | None = None,
        event_description: str | None = None,
        is_all_day_event: bool | None = None,
        is_private_event: bool | None = None,
        category_id: str | None = None,
        member_ids: str | None = None,
        is_recurring_event: bool | None = None,
        repeat_frequency: int | None = None,
        repeat_interval: int | None = None,
        repeat_times: int | None = None,
        reminder_type: int | None = None,
        remind_time: int | None = None,
    ) -> dict:
        """创建日程。日期格式 YYYY-MM-DD HH:MM。member_ids 用逗号分隔多个用户ID。"""
        return api_post("/v1/calendar/create_event",
                        name=name, begin_date=begin_date, end_date=end_date,
                        address=address, event_description=event_description,
                        is_all_day_event=is_all_day_event, is_private_event=is_private_event,
                        category_id=category_id, member_ids=member_ids,
                        is_recurring_event=is_recurring_event, repeat_frequency=repeat_frequency,
                        repeat_interval=repeat_interval, repeat_times=repeat_times,
                        reminder_type=reminder_type, remind_time=remind_time)

    @mcp.tool()
    def calendar_create_category(category_name: str, color: int | None = None) -> dict:
        """创建自定义日程分类。color: 0=红,1=紫,2=青,3=橙,4=蓝,5=绿,6=黄。"""
        return api_post("/v1/calendar/create_user_defined_category",
                        category_name=category_name, color=color)

    @mcp.tool()
    def calendar_add_members(
        event_id: str,
        member_ids: str | None = None,
        invited_accounts: str | None = None,
        event_recurring_time: str | None = None,
        modifying_all_recurring_events: bool | None = None,
    ) -> dict:
        """给日程添加成员。member_ids 逗号分隔（明道用户），invited_accounts 为非明道用户（格式 ["电话","邮箱"]）。"""
        return api_post("/v1/calendar/add_members_to_event",
                        event_id=event_id, member_ids=member_ids,
                        invited_accounts=invited_accounts,
                        event_recurring_time=event_recurring_time,
                        modifying_all_recurring_events=modifying_all_recurring_events)

    @mcp.tool()
    def calendar_confirm_invitation(event_id: str, event_recurring_time: str | None = None) -> dict:
        """确认日程邀请。"""
        return api_post("/v1/calendar/confirm_event_invitation",
                        event_id=event_id, event_recurring_time=event_recurring_time)

    @mcp.tool()
    def calendar_reject_invitation(event_id: str, reason_for_rejecting: str = "", event_recurring_time: str | None = None) -> dict:
        """拒绝日程邀请。reason_for_rejecting 为拒绝原因。"""
        return api_post("/v1/calendar/reject_event_invitation",
                        event_id=event_id, reason_for_rejecting=reason_for_rejecting,
                        event_recurring_time=event_recurring_time)

    @mcp.tool()
    def calendar_reinvite_member(event_id: str, member_id: str,
                                  event_recurring_time: str | None = None,
                                  modifying_all_recurring_events: bool | None = None) -> dict:
        """重新邀请某成员加入日程。"""
        return api_post("/v1/calendar/reinvite_a_member_to_event",
                        event_id=event_id, member_id=member_id,
                        event_recurring_time=event_recurring_time,
                        modifying_all_recurring_events=modifying_all_recurring_events)

    @mcp.tool()
    def calendar_remove_member(event_id: str, member_id: str | None = None,
                                event_recurring_time: str | None = None,
                                modifying_all_recurring_events: str | None = None,
                                third_party_user_id: str | None = None) -> dict:
        """从日程中移除某成员。"""
        return api_post("/v1/calendar/remove_a_member_on_event",
                        event_id=event_id, member_id=member_id,
                        event_recurring_time=event_recurring_time,
                        modifying_all_recurring_events=modifying_all_recurring_events,
                        third_party_user_id=third_party_user_id)

    @mcp.tool()
    def calendar_edit_event(
        event_id: str,
        name: str | None = None,
        begin_date: str | None = None,
        end_date: str | None = None,
        address: str | None = None,
        event_description: str | None = None,
        is_all_day_event: bool | None = None,
        is_recurring_event: bool | None = None,
        repeat_frequency: int | None = None,
        repeat_interval: int | None = None,
        repeat_weekday: int | None = None,
        repeat_times: int | None = None,
        repeat_end_date: str | None = None,
        modifying_all_recurring_events: bool | None = None,
        event_recurring_time: str | None = None,
    ) -> dict:
        """修改日程属性（名称、时间、地点、描述等）。日期格式 YYYY-MM-DD HH:MM。"""
        return api_post("/v1/calendar/edit_common_properties_on_event",
                        event_id=event_id, name=name,
                        begin_date=begin_date, end_date=end_date,
                        address=address, event_description=event_description,
                        is_all_day_event=is_all_day_event,
                        is_recurring_event=is_recurring_event,
                        repeat_frequency=repeat_frequency, repeat_interval=repeat_interval,
                        repeat_weekday=repeat_weekday, repeat_times=repeat_times,
                        repeat_end_date=repeat_end_date,
                        modifying_all_recurring_events=modifying_all_recurring_events,
                        event_recurring_time=event_recurring_time)

    @mcp.tool()
    def calendar_edit_category(event_id: str, category_id: str) -> dict:
        """修改日程的分类。"""
        return api_post("/v1/calendar/edit_category_of_an_event",
                        event_id=event_id, category_id=category_id)

    @mcp.tool()
    def calendar_edit_share(event_id: str, is_shareable: bool,
                             event_recurring_time: str | None = None) -> dict:
        """修改日程的分享属性。is_shareable: True=分享, False=不分享。"""
        return api_post("/v1/calendar/edit_share_property_on_event",
                        event_id=event_id, is_shareable=is_shareable,
                        event_recurring_time=event_recurring_time)

    @mcp.tool()
    def calendar_edit_private(event_id: str, is_private_event: bool) -> dict:
        """修改日程的私密属性。is_private_event: True=私密, False=公开。"""
        return api_post("/v1/calendar/edit_is_private_property_on_event",
                        event_id=event_id, is_private_event=is_private_event)

    @mcp.tool()
    def calendar_edit_category_props(category_id: str, category_name: str, color: int) -> dict:
        """修改日程分类的属性。color: 0=红,1=紫,2=青,3=橙,4=蓝,5=绿,6=黄。"""
        return api_post("/v1/calendar/edit_properites_on_category",
                        category_id=category_id, category_name=category_name, color=color)

    @mcp.tool()
    def calendar_edit_reminder(event_id: str, remind_time: int, reminder_type: int) -> dict:
        """修改日程的提醒设置。reminder_type: 0=无提醒,1=分钟,2=小时,3=日。"""
        return api_post("/v1/calendar/edit_reminder_on_event",
                        event_id=event_id, remind_time=remind_time, reminder_type=reminder_type)

    @mcp.tool()
    def calendar_remove_event(event_id: str, removing_all_recurring_events: str = "false",
                               event_recurring_time: str | None = None) -> dict:
        """删除日程。removing_all_recurring_events: 是否删除所有循环日程。"""
        return api_post("/v1/calendar/remove_event", event_id=event_id,
                        removing_all_recurring_events=removing_all_recurring_events,
                        event_recurring_time=event_recurring_time)

    @mcp.tool()
    def calendar_remove_category(category_id: str) -> dict:
        """删除自定义日程分类。"""
        return api_post("/v1/calendar/remove_user_defined_category", category_id=category_id)
