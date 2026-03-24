"""任务 (Task) module.

IMPORTANT: Most task GET endpoints (list/detail/reply) are deprecated and return 404.
Mingdao migrated to low-code platform. Only POST endpoints survive.

Verified working (2026-03-25):
  POST: add_task, delete_task, update_task_name, update_task_status,
        update_task_deadline, update_task_stage, update_task_charge_user,
        update_task_priority, update_task_project, update_task_description,
        add_task_member, delete_task_member, add_task_observer, add_task_reply,
        delete_task_reply, add_task_project, edit_task_project, delete_task_project
  GET:  get_task_log (returns ec=10002 for bad ID, not 404 — path is alive)

Official SDK (mingdaocom/api_python) params use: t_id, t_title, t_des, t_ed, u_id.
Our endpoints use: task_id, task_name, task_description, deadline, account_id.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .api_client import api_get, api_post


def register(mcp: FastMCP) -> None:

    # ── 查询 GET (仅 get_task_log 路径存活) ───────────────

    @mcp.tool()
    def task_get_log(task_id: str) -> dict:
        """获取任务操作日志。task_id 必须是真实任务ID，否则返回 ec=10002。"""
        return api_get("/v1/task/get_task_log", task_id=task_id)

    # ── 新增/创建 POST ────────────────────────────────────

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
    def task_add_project(title: str) -> dict:
        """创建任务项目（文件夹）。title 为项目名称（需唯一）。"""
        return api_post("/v1/task/add_task_project", title=title)

    @mcp.tool()
    def task_add_member(task_id: str, account_id: str) -> dict:
        """给任务添加成员。"""
        return api_post("/v1/task/add_task_member", task_id=task_id, account_id=account_id)

    @mcp.tool()
    def task_add_observer(task_id: str, account_ids: str) -> dict:
        """给任务添加旁观成员。account_ids 多个用逗号隔开。"""
        return api_post("/v1/task/add_task_observer", task_id=task_id, account_ids=account_ids)

    @mcp.tool()
    def task_add_reply(task_id: str, reply_msg: str, reply_id: str | None = None) -> dict:
        """给任务添加讨论。reply_id 为回复某条讨论时填写。"""
        return api_post("/v1/task/add_task_reply",
                        task_id=task_id, reply_msg=reply_msg, reply_id=reply_id)

    # ── 修改 POST ─────────────────────────────────────────

    @mcp.tool()
    def task_update_name(task_id: str, task_name: str) -> dict:
        """修改任务名称。"""
        return api_post("/v1/task/update_task_name",
                        task_id=task_id, task_name=task_name)

    @mcp.tool()
    def task_update_description(task_id: str, task_description: str) -> dict:
        """修改任务描述。"""
        return api_post("/v1/task/update_task_description",
                        task_id=task_id, task_description=task_description)

    @mcp.tool()
    def task_update_status(task_id: str, status: int = 1) -> dict:
        """更新任务状态。status: 0=未完成, 1=已完成。"""
        return api_post("/v1/task/update_task_status",
                        task_id=task_id, status=status)

    @mcp.tool()
    def task_update_deadline(task_id: str, deadline: str, include_sub_tasks: bool = False) -> dict:
        """修改任务截止日期。格式 YYYY-MM-DD。include_sub_tasks: 是否同步修改子任务。"""
        return api_post("/v1/task/update_task_deadline",
                        task_id=task_id, deadline=deadline,
                        include_sub_tasks=include_sub_tasks)

    @mcp.tool()
    def task_update_charge(task_id: str, account_id: str) -> dict:
        """修改任务负责人。account_id 为新负责人的用户ID。"""
        return api_post("/v1/task/update_task_charge_user",
                        task_id=task_id, account_id=account_id)

    @mcp.tool()
    def task_update_stage(task_id: str, folder_id: str, folder_stage_id: str) -> dict:
        """更新任务所属阶段。folder_id 和 folder_stage_id 均必填。"""
        return api_post("/v1/task/update_task_stage",
                        task_id=task_id, folder_id=folder_id,
                        folder_stage_id=folder_stage_id)

    @mcp.tool()
    def task_update_priority(task_id: str, priority: int = 1) -> dict:
        """修改任务重要性。priority: 0=不重要, 1=重要。"""
        return api_post("/v1/task/update_task_priority",
                        task_id=task_id, priority=priority)

    @mcp.tool()
    def task_update_project(task_id: str, project_id: str | None = None) -> dict:
        """修改任务所属项目。project_id 为空时则任务独立于项目之外。"""
        return api_post("/v1/task/update_task_project",
                        task_id=task_id, project_id=project_id)

    @mcp.tool()
    def task_edit_project(folder_id: str, name: str) -> dict:
        """编辑任务项目（文件夹）名称。name 需唯一。"""
        return api_post("/v1/task/edit_task_project", folder_id=folder_id, name=name)

    # ── 删除 POST ─────────────────────────────────────────

    @mcp.tool()
    def task_delete(task_id: str) -> dict:
        """删除一个任务。"""
        return api_post("/v1/task/delete_task", task_id=task_id)

    @mcp.tool()
    def task_delete_project(folder_id: str) -> dict:
        """删除任务项目（文件夹）。"""
        return api_post("/v1/task/delete_task_project", folder_id=folder_id)

    @mcp.tool()
    def task_delete_member(task_id: str, account_id: str) -> dict:
        """从任务中移除成员。"""
        return api_post("/v1/task/delete_task_member", task_id=task_id, account_id=account_id)

    @mcp.tool()
    def task_delete_reply(task_id: str, reply_id: str) -> dict:
        """删除任务讨论。"""
        return api_post("/v1/task/delete_task_reply", task_id=task_id, reply_id=reply_id)
