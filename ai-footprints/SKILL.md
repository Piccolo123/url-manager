---
name: ai-footprints
description: 查询和创建 AI 足迹（收藏）— 通过 Agent Token 访问个人/共享足迹数据
---

# AI 足迹 — Agent 接入指南

「AI 足迹」是一个 AI 驱动的网页收藏工具。用户保存网页、AI 自动分类标签。你可以通过 API 替用户管理足迹。

## 概念

| 概念 | 说明 |
|------|------|
| **足迹** | 一条收藏记录，含标题/URL/摘要/标签/分类 |
| **分类** | 足迹的分组标签，一个足迹可属于多个分类 |
| **分类集** | 分类的容器，类似浏览器书签文件夹。切换分类集 = 切换一组分类 |
| **共享分类** | 共创模式（成员可添加足迹）+ 订阅模式（成员只读） |

## 接入流程

### 1. 引导用户注册并获取令牌

```
用户操作：访问 ai.ocean94.com → 微信/手机号注册 → 个人中心 → 账号设置 → 访问令牌 → 新建令牌
```

令牌以 `FA_` 开头，**只展示一次**，让用户妥善保管。

### 2. 配置

```bash
export FOOTPRINTS_TOKEN="FA_xxxxxxxxxxxx"
export FOOTPRINTS_ENDPOINT="https://ai.ocean94.com"  # 默认值
```

### 3. 调用 API

所有请求带 `Authorization: Bearer FA_xxx` 头。令牌永不过期，手动撤销。

## API 参考

Base URL: `{FOOTPRINTS_ENDPOINT}/api/v1/agent`

### 用户

```
GET /me
→ { "id": "uuid", "username": "piccolo", "nickname": "Piccolo" }
```

### 分类集

```
GET /category-sets
→ [{ "id": 125, "name": "我的分类", "is_shared": false, "sort_order": 0 }, ...]

POST /category-sets
← { "name": "新分类集" }
→ { "id": 171, "name": "新分类集", "is_shared": false, "sort_order": 3 }
```

同名分类集返回 409。

### 分类

```
GET /categories
→ [{ "id": 263, "name": "默认分类", "mode": null }, ...]
```

`mode`: `null`=个人分类，`cocreate`=共创共享，`subscribe`=订阅共享。

```
POST /categories
← { "name": "新分类", "category_set_id": 125 }
→ { "id": 448, "name": "新分类", "mode": null, "created": true }
```

- `category_set_id` 可选，默认归入「我的分类」
- 同分类集下同名不重复创建，返回已有 ID（`created: false`）

### 标签

```
GET /tags
→ [{ "id": 1, "name": "技术" }, ...]
```

### 足迹

```
GET /collections?q=关键词&category_id=263&limit=20&offset=0
→ {
    "items": [
      {
        "id": "uuid",
        "url": "https://...",
        "title": "页面标题",
        "description": "AI 提取的摘要",
        "favicon_url": "https://...",
        "tags": ["标签1", "标签2"],
        "category_ids": [263],
        "category_names": ["默认分类"],
        "created_at": "2026-06-26T04:20:05Z"
      }
    ],
    "total": 1
  }
```

- `q` — 搜索标题/URL/摘要
- `category_id` — 按分类过滤
- `limit` — 每页数量（默认 20，最大 100）
- `offset` — 偏移量

```
GET /collections/{id}
→ 同上单条结构，额外含 updated_at
```

无法访问的足迹返回 404（不暴露存在性）。

```
POST /collections
← {
    "url": "https://example.com/article",
    "title": "文章标题",
    "description": "文章摘要",
    "category_ids": [263],
    "tag_names": ["标签1", "标签2"]
  }
→ 创建的足迹对象
```

- `url` 必填
- `title` 和 `description` 可选（建议 agent 自行爬取后填入）
- `category_ids` 和 `tag_names` 可选
- 不走 AI Pipeline（不扣点），纯入库

```
PUT /collections/{id}
← { "title": "新标题", "category_ids": [263, 264], "tag_names": ["新标签"] }
→ 更新后的足迹对象
```

全部字段可选，传 `null` 不修改：
- `title` — 标题
- `url` — 链接
- `description` — 摘要
- `category_ids` — 分类 ID 列表（全量替换）
- `tag_names` — 标签名列表（`null` 不修改，`[]` 清空，有值全量替换）

仅所有者可更新，非所有者返回 404。

## 使用建议

1. **搜索优先** — 用 `GET /collections?q=关键词` 搜索，不要先列全量
2. **添加前爬取** — 用你自己的 web 工具爬页面提取标题和摘要，再调 `POST /collections`
3. **分类模糊时询问** — 不确定该选哪个分类时，先列 `GET /categories` 让用户选择
4. **创建分类** — 需要新分类时先 `POST /categories`，用返回的 ID 调创建足迹
5. **订阅模式只读** — 如果分类 `mode` 是 `subscribe`，写入会返回 403

## 限制

- 令牌有完整读写权限，不可细化 scope
- LLM / AI 解析不开给外部 Agent（走 AI Pipeline 扣点）。Agent 应自行爬取内容后写入
- 订阅模式共享分类下，非创建者无法添加足迹
- 内容需通过审核（阿里云绿网），标题和摘要不要含违规内容
