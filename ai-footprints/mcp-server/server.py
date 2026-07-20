"""
AI 足迹 MCP Server — ModelScope 部署版

通过 MCP 协议暴露 AI 足迹的核心功能：
搜索、添加、列出、更新足迹，管理分类和标签，共享分类协作。

认证：通过环境变量 FOOTPRINTS_TOKEN 配置 Agent Token。
获取 Token：在 https://ai.ocean94.com 个人中心 → 接入Agent → 访问令牌。
"""

import os
import httpx
from mcp.server.fastmcp import FastMCP

# ── 配置 ──────────────────────────────────────────────
ENDPOINT = os.getenv("FOOTPRINTS_ENDPOINT", "https://ai.ocean94.com")
TOKEN = os.getenv("FOOTPRINTS_TOKEN", "")
AUTH_HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

mcp = FastMCP(
    "ai-footprints",
    instructions="AI 驱动的智能足迹管理工具。用户用它跨平台收藏网页、文章、视频等任何有链接的内容。核心功能：搜索、添加、列出、更新足迹；管理分类和标签；共享分类协作。使用前需在 https://ai.ocean94.com 个人中心获取 Agent Token，设为环境变量 FOOTPRINTS_TOKEN。",
    host="0.0.0.0",
    port=int(os.getenv("PORT", "8000")),
)


# ── 辅助函数 ──────────────────────────────────────────

async def _api(method: str, path: str, **kwargs) -> dict:
    """调用 AI 足迹 API"""
    url = f"{ENDPOINT}{path}"
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.request(method, url, headers=AUTH_HEADERS, **kwargs)
        resp.raise_for_status()
        return resp.json()


def _check_auth():
    """检查是否已配置 Token"""
    if not TOKEN:
        return "❌ 未配置 FOOTPRINTS_TOKEN。请在 ModelScope MCP 配置中设置环境变量 FOOTPRINTS_TOKEN，Token 可在 https://ai.ocean94.com 个人中心获取。"
    return None


# ── 足迹工具 ──────────────────────────────────────────

@mcp.tool()
async def search_footprints(query: str, page: int = 1, page_size: int = 10) -> dict:
    """搜索足迹（标题、描述、URL），返回匹配的足迹列表。

    Args:
        query: 搜索关键词
        page: 页码（从 1 开始）
        page_size: 每页条数（默认 10，最大 50）
    """
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    return await _api("GET", "/api/search", params={"q": query, "page": page, "page_size": min(page_size, 50)})


@mcp.tool()
async def add_footprint(
    url: str,
    title: str = "",
    description: str = "",
    category_ids: str = "",
    tags: str = "",
) -> dict:
    """添加一条新足迹。

    Args:
        url: 网页链接（必填）
        title: 标题（留空则自动提取）
        description: 描述/摘要
        category_ids: 分类 ID，多个用逗号分隔，如 "1,3,5"
        tags: 标签，多个用逗号分隔，如 "AI,教程"
    """
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    body = {"url": url}
    if title:
        body["title"] = title
    if description:
        body["description"] = description
    if category_ids:
        body["category_ids"] = [int(x.strip()) for x in category_ids.split(",") if x.strip()]
    if tags:
        body["tags"] = [x.strip() for x in tags.split(",") if x.strip()]
    return await _api("POST", "/api/ai/collections", json=body)


@mcp.tool()
async def list_footprints(category_id: int = 0, page: int = 1, page_size: int = 20) -> dict:
    """列出足迹列表。

    Args:
        category_id: 分类 ID（0 表示全部）
        page: 页码
        page_size: 每页条数（默认 20，最大 50）
    """
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    params = {"page": page, "page_size": min(page_size, 50)}
    if category_id > 0:
        params["category_id"] = category_id
    return await _api("GET", "/api/collections", params=params)


@mcp.tool()
async def get_footprint(footprint_id: int) -> dict:
    """获取单条足迹的详细信息。

    Args:
        footprint_id: 足迹 ID
    """
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    return await _api("GET", f"/api/collections/{footprint_id}")


@mcp.tool()
async def update_footprint(
    footprint_id: int,
    title: str = "",
    description: str = "",
    category_ids: str = "",
    tags: str = "",
) -> dict:
    """更新足迹的标题、描述、分类或标签。
    注意：category_ids 会替换整个分类列表，不是追加。

    Args:
        footprint_id: 足迹 ID
        title: 新标题（留空不修改）
        description: 新描述（留空不修改）
        category_ids: 新分类 ID 列表，逗号分隔（留空不修改）
        tags: 新标签列表，逗号分隔（留空不修改）
    """
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    body = {}
    if title:
        body["title"] = title
    if description:
        body["description"] = description
    if category_ids:
        body["category_ids"] = [int(x.strip()) for x in category_ids.split(",") if x.strip()]
    if tags:
        body["tags"] = [x.strip() for x in tags.split(",") if x.strip()]
    if not body:
        return {"error": "至少需要提供一个要修改的字段"}
    return await _api("PUT", f"/api/collections/{footprint_id}", json=body)


# ── 分类工具 ──────────────────────────────────────────

@mcp.tool()
async def list_categories() -> dict:
    """列出当前用户的所有分类。"""
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    return await _api("GET", "/api/categories")


@mcp.tool()
async def create_category(name: str, category_set_id: int = 0) -> dict:
    """创建新分类。

    Args:
        name: 分类名称
        category_set_id: 所属分类集 ID（0 表示默认分类集）
    """
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    body = {"name": name}
    if category_set_id > 0:
        body["category_set_id"] = category_set_id
    return await _api("POST", "/api/categories", json=body)


@mcp.tool()
async def list_tags() -> dict:
    """列出当前用户的所有标签。"""
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    return await _api("GET", "/api/search/tags")


# ── 分类集工具 ────────────────────────────────────────

@mcp.tool()
async def list_category_sets() -> dict:
    """列出所有分类集。"""
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    return await _api("GET", "/api/category-sets")


@mcp.tool()
async def create_category_set(name: str) -> dict:
    """创建新分类集。

    Args:
        name: 分类集名称
    """
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    return await _api("POST", "/api/category-sets", json={"name": name})


# ── 共享分类工具 ──────────────────────────────────────

@mcp.tool()
async def list_shared_categories() -> dict:
    """列出我参与的共享分类（共创和订阅）。"""
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    return await _api("GET", "/api/shared-categories")


@mcp.tool()
async def create_shared_category(
    name: str,
    mode: str = "cocreate",
    description: str = "",
) -> dict:
    """创建共享分类。

    Args:
        name: 分类名称
        mode: 模式 - "cocreate"（共创，多人编辑）或 "subscribe"（订阅，只读分享）
        description: 分类描述
    """
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    body = {"name": name, "mode": mode}
    if description:
        body["description"] = description
    return await _api("POST", "/api/shared-categories", json=body)


@mcp.tool()
async def join_shared_category(invite_code: str) -> dict:
    """通过邀请码加入共享分类。

    Args:
        invite_code: 邀请码
    """
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    return await _api("POST", "/api/shared-categories/join", json={"code": invite_code})


@mcp.tool()
async def create_invite_link(shared_category_id: int, duration_hours: int = 24) -> dict:
    """生成共享分类的邀请链接（发给其他人加入）。

    Args:
        shared_category_id: 共享分类 ID
        duration_hours: 链接有效时长（小时，默认 24）
    """
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    return await _api("POST", f"/api/shared-categories/{shared_category_id}/invite",
                      json={"duration_hours": duration_hours})


# ── 用户信息 ──────────────────────────────────────────

@mcp.tool()
async def my_info() -> dict:
    """查看当前用户信息（用户名、会员状态等）。"""
    auth_err = _check_auth()
    if auth_err:
        return {"error": auth_err}
    return await _api("GET", "/api/auth/me")


# ── 启动入口 ──────────────────────────────────────────

def main():
    """启动 MCP 服务器（Streamable HTTP 模式，供 ModelScope 托管）。"""
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
