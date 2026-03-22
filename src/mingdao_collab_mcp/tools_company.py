"""组织/部门 (Company) module — 8 tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .api_client import api_get, api_post


def register(mcp: FastMCP) -> None:

    # ── GET ──────────────────────────────────────────────

    @mcp.tool()
    def company_get_projects() -> dict:
        """获取当前用户所属的组织列表。"""
        return api_get("/v1/company/get_project_list")

    @mcp.tool()
    def company_get_departments(project_id: str) -> dict:
        """获取组织的部门列表。"""
        return api_get("/v1/company/get_project_departments", project_id=project_id)

    @mcp.tool()
    def company_get_worksite(project_id: str) -> dict:
        """获取组织的工作地点列表。"""
        return api_get("/v1/company/get_project_worksite", project_id=project_id)

    @mcp.tool()
    def company_get_by_code(project_code: str) -> dict:
        """根据组织代码查询组织信息。"""
        return api_get("/v1/company/get_project_byprojectcode", project_code=project_code)

    @mcp.tool()
    def company_get_by_id(project_id: str) -> dict:
        """根据组织ID查询组织信息。"""
        return api_get("/v1/company/get_project_byprojectid", project_id=project_id)

    # ── POST ─────────────────────────────────────────────

    @mcp.tool()
    def company_join_by_code(project_code: str) -> dict:
        """根据组织代码申请加入组织。"""
        return api_post("/v1/company/join_project_byprojectcode", project_code=project_code)

    @mcp.tool()
    def company_join_by_id(project_id: str) -> dict:
        """根据组织ID申请加入组织。"""
        return api_post("/v1/company/join_project_byprojectid", project_id=project_id)

    @mcp.tool()
    def company_refuse_invitation(project_id: str) -> dict:
        """拒绝组织邀请。"""
        return api_post("/v1/company/refuse_project_invitation", project_id=project_id)
