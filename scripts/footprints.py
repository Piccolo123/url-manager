#!/usr/bin/env python3
"""
AI 足迹 Agent API 工具脚本

通过 Agent Token 访问个人/共享足迹数据。
用法：
  python3 footprints.py me
  python3 footprints.py search <query>
  python3 footprints.py list [--category-id <id>] [--limit <n>]
  python3 footprints.py get <id>
  python3 footprints.py add <url> --title <title> [--description <desc>] [--category-ids <ids>] [--tags <tags>]
  python3 footprints.py update <id> [--title <title>] [--description <desc>] [--category-ids <ids>] [--tags <tags>]
  python3 footprints.py batch-update '<json-array>'  # 批量更新，JSON 数组
  python3 footprints.py copy <id> --category-ids <ids>
  python3 footprints.py categories
  python3 footprints.py create-category <name> [--category-set-id <id>]
  python3 footprints.py category-sets
  python3 footprints.py create-category-set <name>
  python3 footprints.py tags

环境变量：
  FOOTPRINTS_TOKEN  — 访问令牌（在 AI 足迹后台生成）
  FOOTPRINTS_ENDPOINT — API 地址，默认 https://ai.ocean94.com
"""
import os
import sys
import json
import urllib.request
import urllib.error

ENDPOINT = os.environ.get("FOOTPRINTS_ENDPOINT", "https://ai.ocean94.com")
TOKEN = os.environ.get("FOOTPRINTS_TOKEN", "")

if not TOKEN:
    print("❌ FOOTPRINTS_TOKEN 环境变量未设置", file=sys.stderr)
    sys.exit(1)


def api(path, method="GET", data=None):
    url = f"{ENDPOINT.rstrip('/')}/api/v1/agent{path}"
    headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}
    body = None
    if data:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        try:
            err = json.loads(err_body)
            return {"error": err.get("detail", str(e))}
        except:
            return {"error": f"HTTP {e.code}: {err_body}"}


# ── 用户 ──

def me():
    result = api("/me")
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    print(f"用户名: {result.get('username')}")
    print(f"昵称: {result.get('nickname', '')}")
    return result


# ── 分类集 ──

def category_sets():
    result = api("/category-sets")
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    for s in result:
        tag = "🔗" if s.get("is_shared") else "📁"
        print(f"  {tag} [{s['id']}] {s['name']}")
    return result


def create_category_set(name):
    result = api("/category-sets", method="POST", data={"name": name})
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    print(f"✅ 分类集已创建: [{result['id']}] {result['name']}")
    return result


# ── 分类 ──

def categories():
    result = api("/categories")
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    for cat in result:
        mode_tag = ""
        if cat.get("mode") == "cocreate":
            mode_tag = " [共创]"
        elif cat.get("mode") == "subscribe":
            mode_tag = " [订阅]"
        print(f"  [{cat['id']}] {cat['name']}{mode_tag}")
    return result


def create_category(name, category_set_id=None):
    body = {"name": name}
    if category_set_id is not None:
        body["category_set_id"] = category_set_id
    result = api("/categories", method="POST", data=body)
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    verb = "已创建" if result.get("created") else "已存在"
    print(f"✅ {verb}: [{result['id']}] {result['name']}")
    return result


# ── 标签 ──

def tags():
    result = api("/tags")
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    for tag in result:
        print(f"  [{tag['id']}] {tag['name']}")
    return result


# ── 足迹 ──

def search(query):
    import urllib.parse
    q = urllib.parse.quote(query)
    result = api(f"/collections?q={q}&limit=20")
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    items = result.get("items", [])
    if not items:
        print("未找到匹配的足迹")
        return result
    for i, item in enumerate(items):
        print(f"{i+1}. {item['title']}")
        print(f"   {item['url']}")
        if item.get("description"):
            print(f"   {item['description'][:120]}")
        cats = ", ".join(item.get("category_names", []))
        if cats:
            print(f"   分类: {cats}")
        tags_list = ", ".join(item.get("tags", []))
        if tags_list:
            print(f"   标签: {tags_list}")
        print()
    return result


def list_collections(category_id=None, limit=20):
    path = f"/collections?limit={limit}"
    if category_id:
        path += f"&category_id={category_id}"
    result = api(path)
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    items = result.get("items", [])
    if not items:
        print("暂无足迹")
        return result
    for i, item in enumerate(items):
        print(f"{i+1}. {item['title']}")
        print(f"   {item['url']}")
        cats = ", ".join(item.get("category_names", []))
        if cats:
            print(f"   分类: {cats}")
        print()
    return result


def get_collection(collection_id):
    """获取单条足迹详情"""
    result = api(f"/collections/{collection_id}")
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    print(f"标题: {result.get('title')}")
    print(f"链接: {result.get('url')}")
    if result.get("description"):
        print(f"摘要: {result['description'][:200]}")
    cats = ", ".join(result.get("category_names", []))
    if cats:
        print(f"分类: {cats}")
    tags_list = ", ".join(result.get("tags", []))
    if tags_list:
        print(f"标签: {tags_list}")
    return result


def add(url, title=None, description=None, category_ids=None, tags=None):
    data = {"url": url}
    if title:
        data["title"] = title
    if description:
        data["description"] = description
    if category_ids:
        data["category_ids"] = [int(x) for x in category_ids.split(",")]
    if tags:
        data["tag_names"] = [t.strip() for t in tags.split(",")]
    result = api("/collections", method="POST", data=data)
    if "error" in result:
        print(f"❌ {result['error']}")
    else:
        print(f"✅ 已保存: {result.get('title', url)}")
        cats = ", ".join(result.get("category_names", []))
        if cats:
            print(f"   分类: {cats}")
    return result


def update_collection(collection_id, title=None, description=None, category_ids=None, tags=None):
    """更新足迹（全部字段可选，传 None 不修改）"""
    data = {}
    if title is not None:
        data["title"] = title
    if description is not None:
        data["description"] = description
    if category_ids is not None:
        data["category_ids"] = [int(x.strip()) for x in category_ids.split(",")]
    if tags is not None:
        data["tag_names"] = [t.strip() for t in tags.split(",") if t.strip()]
    result = api(f"/collections/{collection_id}", method="PUT", data=data)
    if "error" in result:
        print(f"❌ {result['error']}")
    else:
        print(f"✅ 已更新: {result.get('title', collection_id)}")
    return result


def copy_collection(collection_id, category_ids):
    """将共享足迹复制到个人分类"""
    data = {"category_ids": [int(x) for x in category_ids.split(",")]}
    result = api(f"/collections/{collection_id}/copy", method="POST", data=data)
    if "error" in result:
        print(f"❌ {result['error']}")
    else:
        print(f"✅ 已复制到个人分类: {result.get('title', collection_id)}")
        cats = ", ".join(result.get("category_names", []))
        if cats:
            print(f"   分类: {cats}")
    return result


def batch_update_collections(updates_json):
    """批量更新足迹 — 接受 JSON 数组字符串"""
    try:
        updates = json.loads(updates_json)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        return {"error": str(e)}
    if not isinstance(updates, list):
        print("❌ 参数应为 JSON 数组")
        return {"error": "不是数组"}
    result = api("/collections/batch", method="PUT", data={"updates": updates})
    if "error" in result:
        print(f"❌ {result['error']}")
    else:
        print(f"✅ 成功 {result['ok']} 条" + (f"，失败 {result['errors']} 条" if result.get('errors') else ""))
        for e in result.get("error_details", []):
            print(f"   ❌ {e['id']}: {e['detail']}")
    return result


def show_help():
    print(__doc__)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    cmd = sys.argv[1]

    import argparse
    if cmd == "me":
        me()
    elif cmd == "category-sets":
        category_sets()
    elif cmd == "create-category-set":
        if len(sys.argv) < 3:
            print("用法: footprints.py create-category-set <名称>")
            sys.exit(1)
        create_category_set(sys.argv[2])
    elif cmd == "categories":
        categories()
    elif cmd == "create-category":
        parser = argparse.ArgumentParser()
        parser.add_argument("name")
        parser.add_argument("--category-set-id", type=int, default=None)
        args, _ = parser.parse_known_args(sys.argv[2:])
        create_category(args.name, args.category_set_id)
    elif cmd == "tags":
        tags()
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("用法: footprints.py search <关键词>")
            sys.exit(1)
        search(" ".join(sys.argv[2:]))
    elif cmd == "list":
        parser = argparse.ArgumentParser()
        parser.add_argument("--category-id", type=int, default=None)
        parser.add_argument("--limit", type=int, default=20)
        args, _ = parser.parse_known_args(sys.argv[2:])
        list_collections(category_id=args.category_id, limit=args.limit)
    elif cmd == "get":
        if len(sys.argv) < 3:
            print("用法: footprints.py get <足迹ID>")
            sys.exit(1)
        get_collection(sys.argv[2])
    elif cmd == "add":
        parser = argparse.ArgumentParser()
        parser.add_argument("url")
        parser.add_argument("--title", default=None)
        parser.add_argument("--description", default=None)
        parser.add_argument("--category-ids", default=None)
        parser.add_argument("--tags", default=None)
        args, _ = parser.parse_known_args(sys.argv[2:])
        add(args.url, args.title, args.description, args.category_ids, args.tags)
    elif cmd == "update":
        parser = argparse.ArgumentParser()
        parser.add_argument("id")
        parser.add_argument("--title", default=None)
        parser.add_argument("--description", default=None)
        parser.add_argument("--category-ids", default=None)
        parser.add_argument("--tags", default=None)
        args, _ = parser.parse_known_args(sys.argv[2:])
        update_collection(args.id, args.title, args.description, args.category_ids, args.tags)
    elif cmd == "copy":
        parser = argparse.ArgumentParser()
        parser.add_argument("id")
        parser.add_argument("--category-ids", required=True)
        args, _ = parser.parse_known_args(sys.argv[2:])
        copy_collection(args.id, args.category_ids)
    elif cmd == "batch-update":
        if len(sys.argv) < 3:
            print("用法: footprints.py batch-update '<json-array>'")
            sys.exit(1)
        batch_update_collections(sys.argv[2])
    elif cmd == "agent_register":
        agent_register()
    elif cmd == "agent_magic_link":
        agent_magic_link()
    elif cmd == "shared-categories":
        shared_categories()
    elif cmd == "create-shared-category":
        parser = argparse.ArgumentParser()
        parser.add_argument("name")
        parser.add_argument("--mode", required=True, choices=["subscribe", "cocreate"])
        parser.add_argument("--color", default=None)
        parser.add_argument("--description", default=None)
        args, _ = parser.parse_known_args(sys.argv[2:])
        create_shared_category(args.name, args.mode, args.color, args.description)
    elif cmd == "join-shared-category":
        if len(sys.argv) < 3:
            print("用法: footprints.py join-shared-category <邀请码>")
            sys.exit(1)
        join_shared_category(sys.argv[2])
    elif cmd == "add-to-shared":
        parser = argparse.ArgumentParser()
        parser.add_argument("sc_id", type=int)
        parser.add_argument("--collection-id", required=True)
        args, _ = parser.parse_known_args(sys.argv[2:])
        add_to_shared_category(args.sc_id, args.collection_id)
    elif cmd == "remove-from-shared":
        parser = argparse.ArgumentParser()
        parser.add_argument("sc_id", type=int)
        parser.add_argument("--collection-id", required=True)
        args, _ = parser.parse_known_args(sys.argv[2:])
        remove_from_shared_category(args.sc_id, args.collection_id)
    elif cmd == "create-invite-link":
        parser = argparse.ArgumentParser()
        parser.add_argument("sc_id", type=int)
        parser.add_argument("--duration-hours", type=int, default=24)
        args, _ = parser.parse_known_args(sys.argv[2:])
        create_invite_link(args.sc_id, args.duration_hours)
    elif cmd in ("help", "-h", "--help"):
        show_help()
    else:
        print(f"未知命令: {cmd}")
        show_help()
        sys.exit(1)


# ── 共享分类 ──

def shared_categories():
    """列出共享分类（通过分类接口过滤 mode != null 的条目）"""
    result = api("/categories")
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    shared = [c for c in result if c.get("mode")]
    if not shared:
        print("暂无共享分类")
        return result
    for c in shared:
        mode_tag = "[共创]" if c.get("mode") == "cocreate" else "[订阅]"
        print(f"  [{c['id']}] {c['name']} {mode_tag}")
    return shared


def create_shared_category(name, mode, color=None, description=None):
    """创建共享分类"""
    data = {"name": name, "mode": mode}
    if color:
        data["color"] = color
    if description:
        data["description"] = description
    result = api("/shared-categories", method="POST", data=data)
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    print(f"✅ 共享分类已创建: [{result['id']}] {result['name']}")
    if result.get("invite_code"):
        print(f"   邀请码: {result['invite_code']}")
    if result.get("mode"):
        print(f"   模式: {result['mode']}")
    return result


def join_shared_category(code):
    """通过邀请码加入共享分类"""
    result = api("/shared-categories/join", method="POST", data={"code": code})
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    print(f"✅ 已加入共享分类")
    return result


def add_to_shared_category(sc_id, collection_id):
    """将足迹加入共享分类"""
    result = api(f"/shared-categories/{sc_id}/collections", method="POST",
                 data={"collection_id": str(collection_id)})
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    print(f"✅ 足迹已加入共享分类 [{sc_id}]")
    return result


def remove_from_shared_category(sc_id, collection_id):
    """将足迹移出共享分类"""
    result = api(f"/shared-categories/{sc_id}/collections/{collection_id}",
                 method="DELETE")
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    print(f"✅ 足迹已移出共享分类 [{sc_id}]")
    return result


def create_invite_link(sc_id, duration_hours=24):
    """为共享分类生成邀请链接，可发给人类或其他 Agent"""
    data = {}
    if duration_hours is not None:
        data["duration_hours"] = duration_hours
    result = api(f"/shared-categories/{sc_id}/invite-link", method="POST", data=data)
    if "error" in result:
        print(f"❌ {result['error']}")
        return result
    print(f"✅ 邀请链接已生成:")
    print(f"   URL: {result.get('url')}")
    if result.get("code"):
        print(f"   邀请码: {result['code']}")
    if result.get("expires_at"):
        print(f"   有效期至: {result['expires_at']}")
    print(f"\n📨 可将链接或邀请码发送给人类或其他 Agent，对方加入后即可协作")
    return result


def agent_register():
    """Agent 自主注册：创建新账号并返回访问令牌"""
    r = api.post("/agent/register")
    data = r.json()
    print(f"Token: {data['token']}")
    print(f"\n{data.get('message', '')}")


def agent_magic_link():
    """生成一次性登录链接"""
    r = api.post("/agent/magic-link")
    data = r.json()
    print(f"链接: {data['url']}")
    print(f"有效期: {data['expires_in']} 秒（{data['expires_in'] // 60} 分钟）")
