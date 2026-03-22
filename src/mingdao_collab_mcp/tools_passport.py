"""个人账户 (Passport) module — 11 tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .api_client import api_get, api_post


def register(mcp: FastMCP) -> None:

    # ── GET ──────────────────────────────────────────────

    @mcp.tool()
    def passport_get_detail() -> dict:
        """获取当前登录用户的详细信息。"""
        return api_get("/v1/passport/get_passport_detail")

    @mcp.tool()
    def passport_get_setting() -> dict:
        """获取当前用户的账户设置。"""
        return api_get("/v1/passport/get_passport_setting")

    @mcp.tool()
    def passport_get_unread_count() -> dict:
        """获取各类未读消息数量。"""
        return api_get("/v1/passport/get_un_read_count")

    @mcp.tool()
    def passport_get_user_card() -> dict:
        """获取当前用户的个人名片。"""
        return api_get("/v1/passport/get_user_card")

    # ── POST ─────────────────────────────────────────────

    @mcp.tool()
    def passport_logout() -> dict:
        """退出登录（使当前 token 失效）。"""
        return api_post("/v1/passport/log_out")

    @mcp.tool()
    def passport_send_verify_code(phone: str | None = None, email: str | None = None) -> dict:
        """发送验证码到手机或邮箱。"""
        return api_post("/v1/passport/send_verify_code", phone=phone, email=email)

    @mcp.tool()
    def passport_update_account(
        email: str | None = None,
        phone: str | None = None,
    ) -> dict:
        """更新账户信息（邮箱、手机号）。"""
        return api_post("/v1/passport/update_passport_account",
                        email=email, phone=phone)

    @mcp.tool()
    def passport_update_detail(
        full_name: str | None = None,
        profession: str | None = None,
        company_name: str | None = None,
    ) -> dict:
        """更新个人详情（姓名、职位、公司）。"""
        return api_post("/v1/passport/update_passport_detail",
                        full_name=full_name, profession=profession,
                        company_name=company_name)

    @mcp.tool()
    def passport_update_password(old_password: str, new_password: str) -> dict:
        """修改密码。"""
        return api_post("/v1/passport/update_passport_pwd",
                        old_password=old_password, new_password=new_password)

    @mcp.tool()
    def passport_update_user_card(
        full_name: str | None = None,
        company_name: str | None = None,
        profession: str | None = None,
    ) -> dict:
        """更新个人名片。"""
        return api_post("/v1/passport/update_user_card",
                        full_name=full_name, company_name=company_name,
                        profession=profession)

    @mcp.tool()
    def passport_add_scale(scale: int | None = None) -> dict:
        """添加评分。"""
        return api_post("/v1/passport/add_passport_scale", scale=scale)
