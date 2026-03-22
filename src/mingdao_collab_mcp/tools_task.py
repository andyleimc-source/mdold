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
        des: str | None = None,
        charge_account_id: str | None = None,
        folder_id: str | None = None,
        dead_line: str | None = None,
        color: int | None = None,
    ) -> dict:
        """创建一个新任务。task_name 为任务名称，可指定负责人(charge_account_id)、文件夹(folder_id)、截止日期(dead_line, 格式 YYYY-MM-DD)。"""
        return api_post("/v1/task/add_task",
                        task_name=task_name, des=des,
                        charge_account_id=charge_account_id,
                        folder_id=folder_id, dead_line=dead_line,
                        color=color)

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
    def task_update_stage(task_id: str, folder_id: str, stage_id: str | None = None) -> dict:
        """更新任务所属阶段。需要 folder_id（任务文件夹ID）。"""
        return api_post("/v1/task/update_task_stage",
                        task_id=task_id, folder_id=folder_id,
                        stage_id=stage_id)

    @mcp.tool()
    def task_update_deadline(task_id: str, dead_line: str) -> dict:
        """修改任务截止日期。格式 YYYY-MM-DD。"""
        return api_post("/v1/task/update_task_deadline",
                        task_id=task_id, dead_line=dead_line)

    @mcp.tool()
    def task_update_name(task_id: str, task_name: str) -> dict:
        """修改任务名称。"""
        return api_post("/v1/task/update_task_name",
                        task_id=task_id, task_name=task_name)
