"""任务 (Task) module — 7 tools.

Note: Most task endpoints were deprecated when Mingdao transitioned
to the low-code platform. These are the surviving endpoints that
still respond (verified 2026-03-22).
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .api_client import api_get, api_post


def register(mcp: FastMCP) -> None:

    # ── GET ──────────────────────────────────────────────

    @mcp.tool()
    def task_get_log(task_id: str) -> dict:
        """获取任务操作日志。"""
        return api_get("/v1/task/get_task_log", task_id=task_id)

    # ── POST ─────────────────────────────────────────────

    @mcp.tool()
    def task_add(
        task_name: str,
        task_description: str | None = None,
        charge_user_account_id: str | None = None,
        members: str | None = None,
        folder_id: str | None = None,
        folder_stage_id: str | None = None,
        deadline: str | None = None,
        parent_id: str | None = None,
        is_star: bool | None = None,
        project_id: str | None = None,
    ) -> dict:
        """创建任务。deadline 格式 YYYY-MM-DD。members 逗号分隔。folder_id 填了则 folder_stage_id 必填。"""
        return api_post("/v1/task/add_task",
                        task_name=task_name, task_description=task_description,
                        charge_user_account_id=charge_user_account_id,
                        members=members, folder_id=folder_id,
                        folder_stage_id=folder_stage_id, deadline=deadline,
                        parent_id=parent_id, is_star=is_star, project_id=project_id)

    @mcp.tool()
    def task_delete(task_id: str) -> dict:
        """删除一个任务。"""
        return api_post("/v1/task/delete_task", task_id=task_id)

    @mcp.tool()
    def task_update_status(task_id: str, status: int = 1) -> dict:
        """更新任务状态。status: 0=未完成, 1=已完成。"""
        return api_post("/v1/task/update_task_status",
                        task_id=task_id, status=status)

    @mcp.tool()
    def task_update_stage(task_id: str, folder_id: str, folder_stage_id: str) -> dict:
        """更新任务所属阶段。folder_id 和 folder_stage_id 均必填。"""
        return api_post("/v1/task/update_task_stage",
                        task_id=task_id, folder_id=folder_id,
                        folder_stage_id=folder_stage_id)

    @mcp.tool()
    def task_update_deadline(task_id: str, deadline: str, include_sub_tasks: bool = False) -> dict:
        """修改任务截止日期。格式 YYYY-MM-DD。include_sub_tasks: 是否同步修改子任务。"""
        return api_post("/v1/task/update_task_deadline",
                        task_id=task_id, deadline=deadline,
                        include_sub_tasks=include_sub_tasks)

    @mcp.tool()
    def task_update_name(task_id: str, task_name: str) -> dict:
        """修改任务名称。"""
        return api_post("/v1/task/update_task_name",
                        task_id=task_id, task_name=task_name)
