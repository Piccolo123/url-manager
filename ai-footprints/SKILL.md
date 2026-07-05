---
name: ai-footprints
description: 查询和创建 AI 足迹（收藏）— 通过 Agent Token 访问个人/共享足迹数据
---

# AI 足迹 — Agent 接入 Skill

让你的 AI Agent 访问你在「AI 足迹」中的收藏数据。

## 浏览器扩展

[📥 下载 AI 足迹浏览器扩展](https://github.com/Piccolo123/ai-footprints/raw/main/AI%E8%B6%B3%E8%BF%B9%E6%89%A9%E5%B1%95.zip)

一键保存当前浏览的网页到你的 AI 足迹。支持 Chrome / Edge 等 Chromium 内核浏览器。

## 前置条件

1. 在 AI 足迹（https://ai.ocean94.com）中，进入**个人中心 → 接入Agent → 访问令牌**，生成一个令牌
2. 配置环境变量：
   ```yaml
   # ~/.hermes/config.yaml
   env:
     FOOTPRINTS_TOKEN: FA_xxxxxxxxxxxx
     FOOTPRINTS_ENDPOINT: https://ai.ocean94.com  # 或 http://192.168.0.88:8080
   ```

## 核心概念

### 足迹（Collection）
用户保存的网页/内容记录。每一条足迹包含：
- `title` — 页面标题
- `url` — 页面链接
- `description` — 摘要（填写提取到的页面描述）
- `favicon_url` — 网站图标
- `tags` — 标签（多个，自由创建）
- 所属分类（可属于多个分类）

> ⚠️ 足迹 ≠ 书签。书签是静态链接，足迹包含标题、摘要、标签、分类等多维信息，支持搜索和多维分类。

### 分类（Category）
对足迹的逻辑分组。一个足迹可以属于多个分类。
- 分类有名称，在分类集内唯一
- 分类可以有子分类（树形结构）

### 分类集（Category Set）
分类的容器。就像一个浏览器窗口里的标签页组。
- 每个用户有一个默认「我的分类」集
- 用户可以创建额外的分类集
- 切换分类集 = 切换一组完全不同的分类

### 共享分类
两种模式：
- **共创模式（cocreate）**：所有成员都可以添加/编辑足迹。适合团队共同维护的知识库。
- **订阅模式（subscribe）**：只有创建者能添加足迹，订阅者只能查看。适合分享自己的精选集给他人。

### 标签（Tag）
跨分类的轻量标记。同一个标签可以出现在不同分类的足迹上。

## 可用工具

所有工具通过 `scripts/footprints.py` 调用。

### footprints_me()
获取当前用户信息（用户名、昵称）。

### footprints_search(query)
搜索足迹。`query` 匹配标题、描述、URL。

### footprints_list(category_id=None, limit=20)
列出足迹。可按分类过滤。

### footprints_get(id)
获取单条足迹详情（含标题、链接、摘要、分类、标签）。

### footprints_add(url, title=None, description=None, category_ids=None, tag_names=None)
创建足迹。传入提取到的标题和摘要。

### footprints_update(id, title=None, description=None, category_ids=None, tag_names=None)
更新足迹。所有字段可选，传空不修改。`category_ids`/`tag_names` 传 `[]` 清空。

### footprints_batch_update(updates)
批量更新足迹。`updates` 为数组，每项含 `id` + 可选 `title`/`description`/`category_ids`。
最多 50 条，部分失败不影响其他。比逐条调 `footprints_update` 快得多。
适用场景：批量搬家、批量加标签、合并分类后批量迁移。

### footprints_copy(id, category_ids)
**将共享足迹复制到个人分类。** 必传 `--category-ids`（目标个人分类 ID，逗号分隔）。

### footprints_categories()
列出当前用户的所有分类（含参与共享的分类）。返回每个分类的 id、name、mode。

### footprints_create_category(name, set_id=None)
创建个人分类。`--set-id` 指定目标分类集，默认归入「我的分类」。

### footprints_category_sets()
列出当前用户的所有分类集。

### footprints_create_category_set(name)
创建新的个人分类集。

### footprints_tags()
列出当前用户的所有标签。

## 共享分类工作流

Agent 处理"帮我收藏这个"类请求的标准流程：

1. `footprints_categories()` — 列出分类，区分个人分类和共享分类（带 [共创]/[订阅] 标记）
2. 如果用户在共享分类中，需要"保存到个人"：先让用户选目标个人分类，再调 `footprints_copy(id, --category-ids <ids>)`
3. 如果是新内容：Agent 提取页面内容 → `footprints_add(url, --title, --description, --category-ids, --tags)`

## 组合操作示例

### 移动足迹到另一个分类

足迹没有"移动"API，通过组合操作实现：

1. `footprints_get(id)` — 获取足迹当前所属分类
2. 确认目标分类是否存在：
   - 不存在 → `footprints_create_category(name)` 创建
   - 存在 → 记下目标分类 ID
3. 构建新的分类 ID 列表 = 当前分类 + 目标分类 - 要移除的分类
4. `footprints_update(id, --category-ids <新列表>)` — 一步完成加减

示例：把足迹 42 从"阅读"移到"技术"
```
# 查当前状态
footprints_get(42)
# → categories: [{id: 3, name: "阅读"}, {id: 5, name: "AI"}]

# 目标：去掉 3(阅读)，加上 7(技术)，保留 5(AI)
footprints_update(42, --category-ids 5,7)
```

### 批量整理：把多篇足迹归入同一个新分类

1. `footprints_create_category(name)` — 创建新分类，记下 ID
2. 对每条要整理的足迹：
   - `footprints_get(id)` — 获取当前分类 ID 列表
   - 把新分类 ID 追加进去
   - `footprints_update(id, --category-ids <合并后的列表>)`

### 清理某个分类下的所有足迹

1. `footprints_list(category_id=X)` — 列出该分类下所有足迹
2. 逐条展示给用户确认
3. 对确认的每条：去掉该分类 ID 后 `footprints_update(id, --category-ids <剩余分类>)`

### 合并两个分类（如"后端"并入"技术"）

1. `footprints_categories()` — 确认两个分类 ID
2. `footprints_list(category_id=<源分类ID>)` — 列出源分类下所有足迹
3. 逐条：`footprints_get(id)` 获取当前分类列表，把源分类 ID 替换为目标分类 ID
4. `footprints_update(id, --category-ids <新列表>)`
5. 全部迁移完成后提醒用户可手动删除空分类

### 按标签筛选并批量加分类

用户说"把所有打了 #docker 标签的足迹也归入'容器'分类"：

1. `footprints_search(docker)` 或 `GET /collections?q=docker` — 搜索
2. 过滤出 tag_names 包含 "docker" 的足迹
3. 确认目标分类 "容器" 是否存在，不存在则创建
4. 逐条 `footprints_update(id, --category-ids <现有分类+容器ID>)`

### 整理未分类足迹

用户说"把那些没分类的足迹归入'待整理'"：

1. `footprints_list(limit=100)` 列出最近足迹
2. 过滤出 `category_ids` 为空或只有默认分类的
3. 列出让用户挑选
4. 为选中的每条 `footprints_update(id, --category-ids <待整理ID>)`

### 按域名自动建分类并归类

用户说"把 github.com 的足迹都归到一个'GitHub'分类里"：

1. `footprints_list(limit=100)` 列出所有足迹
2. 过滤 URL 包含 "github.com" 的
3. `footprints_create_category("GitHub")` 新建分类
4. 逐条追加分类：`footprints_update(id, --category-ids <现有+GithubID>)`

### 定期备份：导出某分类的足迹清单

用户说"帮我导出'技术'分类的所有足迹"：

1. `footprints_list(category_id=<技术ID>, limit=100)` — 获取全部
2. 格式化为 Markdown 表格或列表
3. 回显给用户（含标题、URL、标签、创建时间）

### 智能补全：根据已有标签推荐分类

1. `footprints_tags()` — 获取用户的所有标签及使用频率
2. `footprints_categories()` — 对比现有分类
3. 发现高频标签没有对应分类时，建议"要不要为 #docker 创建一个'容器'分类？"

## 敏感操作确认

以下操作**必须先向用户二次确认**后再执行：

- **删除分类**：`footprints_update` 清空足迹的分类关联（不可逆）
- **删除足迹**：暂无直接删除 API，通过去掉所有分类实现"归档"
- **清空标签**：`footprints_update(id, --tags [])` 会清除所有标签
- **修改共享分类**：subscribe 模式写入会 403，共创模式修改影响所有成员

确认原则：变动不可逆或影响他人的操作，必须等用户明确回复"是/确认/好的"再动手。

1. **搜索优先**：用户说"找那篇Docker文章"→ 先用 `footprints_search` 搜索，不要先列全量
2. **添加前提取**：提取页面标题和摘要后调 `footprints_add` 写入
3. **分类模糊时询问**：用户说"存起来"但没说哪个分类时，先调 `footprints_categories` 列出分类让用户选
4. **共享分类写入注意**：subscribe 模式的分类写入会返回 403，收到后告知用户该分类只读
