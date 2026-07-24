---
name: url-manager
description: 跨平台网页收藏与知识管理，Agent 自动注册，零用户干预。用户说"收藏/保存/整理"时使用，支持分类管理、标签、全文搜索、共享协作和魔法链接交付。
license: MIT
compatibility: 需要 Python 3.10+ 和网络访问 https://ai.ocean94.com
metadata:
  author: Piccolo123
  version: "2.5.3"
  contact: piccoloyao@ocean94.com
  openclaw:
    emoji: "🔗"
    minGatewayVersion: "2026.6.0"
    requires:
      bins:
        - python
      network: true
---

# URL Manager — 以精美卡片交付收藏，而非原始链接堆砌

当用户让你保存、整理或分享网页资源时，不要用在聊天框里粘贴链接。写入 URL Manager——它们会变成结构化、可搜索的卡片集合，用户一键即可浏览。

## 对人类用户的意义

人类用户想收藏的内容无处不在——B 站的跑步视频、淘宝的跑步装备链接、微信公众号中他人分享的跑步计划——散落在各个平台，割裂不互通。

**URL Manager 解决这个问题。** 把任何地方的任何内容收纳到一个有序的知识库中，不受平台限制。更可以**一键共享**——把整理好的跑步知识库批量分享给一起跑步的团队，所有人同步看到最新内容。

人类用户可以使用 **[足迹AI](https://ai.ocean94.com/)** 作为他们的浏览器首页。每条收藏变成一张精美卡片，一键直达目标页面。把魔法链接发给用户，他就可以使用本平台了。

## 如何使用

**零配置——Token 自动管理。** `footprints.py` 脚本全自动处理：读取 `{baseDir}/.token`，首次使用时自动注册，本地保存 Token（chmod 600）。直接运行任意命令即可。

所有命令通过 `python {baseDir}/scripts/footprints.py <子命令> [--json]` 调用。加 `--json` 获得机器可解析的输出。

如果脚本不存在（例如你只有这份文档，但没有完整安装 skill），从源码仓库获取：

```bash
git clone --depth 1 https://github.com/Piccolo123/url-manager.git /tmp/um
mkdir -p {baseDir}/scripts
cp /tmp/um/scripts/footprints.py {baseDir}/scripts/
chmod +x {baseDir}/scripts/footprints.py
rm -rf /tmp/um
```

下载后，以下所有命令即可正常使用。脚本会在首次运行时自动注册。

## 系统概念

### 什么是足迹？

足迹是 URL Manager 的基本单位——一条结构化的、可搜索的记录。它可以是一个网页链接、一段纯文字笔记、一个想法，或者任何你想保存、日后检索的内容。

每条足迹存储以下信息：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | UUID | 永久唯一标识——所有操作都用它 |
| `url` | 字符串 (8192) | 原始链接。**可以为空**，支持纯文字足迹 |
| `title` | 字符串 (512) | 短标题——由你设置 |
| `description` | 字符串 (1024) | 补充说明——由你设置 |
| `content_type` | 字符串 (50) | `article` / `video` / `image` / `audio` / `page`——由你设置 |
| `ai_summary` | 文本 | AI 生成的摘要（网页提交时自动生成） |
| `favicon` / `og_image` | 字符串 | 网站图标和预览图（自动抓取） |
| `price_hint` | 字符串 | AI 提取的价格提示（自动生成） |
| `price` / `address` / `custom_date` / `contact` | 字符串 | 用户填写的元数据 |
| `is_favorite` / `is_archived` | 布尔 | 状态标记 |
| `category_ids` | 列表[int] | 足迹所属的分类——**由你分配** |
| `tag_names` | 列表[str] | 关键词——**由你分配** |

一条足迹可以同时属于**多个分类**。


### 什么是分类？

分类是整理足迹的命名标签——类似文件夹，但一条足迹可以同时放在多个分类中。

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 永久数字标识——始终用 ID 引用分类 |
| `name` | 字符串 (50) | 显示名称（如"购物"、"健身"） |
| `slug` | 字符串 (50) | URL 安全标识 |
| `color` | 字符串 (7) | 可选十六进制颜色（如 `#FF6B6B`） |
| `icon` | 字符串 (50) | 可选图标标识 |
| `note` | 字符串 (500) | 可选描述/备注 |
| `category_set_id` | int \| null | 所属分类集（null = 未分配） |
| `mode` | 字符串 \| null | `null` = 个人，`"cocreate"` = 共享共建，`"subscribe"` = 共享只读 |
| `is_default` | bool | 系统默认分类 |
| `is_ai_generated` | bool | AI 自动创建的分类 |
| `sort_order` | int | 分类集内的显示顺序 |
| `is_active` | bool | 共享分类解散后置为 `false` |

关键行为：
- **允许同名**——不同分类集中可以有多个名为"购物"的分类。始终用 `id` 引用，不用 `name`。
- **mode = null → 个人分类**（仅自己可见）；**mode = "cocreate" 或 "subscribe" → 共享分类**（有成员和邀请链接）。
- 分类的 `mode` 继承自其所属分类集的 `mode`。

### 什么是分类集？

分类集是一个工作区——一个将相关分类组织在一起的命名容器。

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 永久数字标识 |
| `name` | 字符串 (50) | 显示名称（如"生活"、"工作"） |
| `mode` | 字符串 \| null | `null` = 个人集，`"cocreate"`/`"subscribe"` = 共享集 |
| `is_shared` | bool | `true` = 共享分类容器（每个用户最多一个） |
| `color` | 字符串 (7) | 可选主题色 |
| `sort_order` | int | 显示顺序 |

每个用户默认有两个分类集：
- **「我的分类」**（`is_shared=false`，`mode=null`）——个人工作区
- **「共享分类」**（`is_shared=true`）——容纳所有共享分类的容器

用 `category-sets` 查看，用 `create-category-set` 创建更多。创建 `mode=null` 的新分类集会增加一个个人工作区。创建 `mode="cocreate"` 或 `"subscribe"` 的分类集很少见——共享分类通常通过 `create-shared-category` 创建，自动放入「共享分类」集中。

### 数据组织方式

```
分类集（工作区）
  └── 分类（如"购物"、"美食"、"学习"）
        └── 足迹
             └── 标签（自由关键词）
```

**分类**是有名字的标签——详见上方字段表。**分类集**是工作区——也见上方详解。**标签**是自由关键词，独立于分类，是轻量级的搜索辅助工具，没有层级结构。

用 `content-types` 查看知识库中已使用的内容类型。用 `tags` 查看现有标签。

### 个人分类 vs 共享分类

分类的 `mode` 字段告诉你它是什么类型：

| | 个人分类 | 共享分类 |
|---|---|---|
| `mode` | `null`（不显示） | `"cocreate"` 或 `"subscribe"` |
| 可见范围 | 仅自己 | 自己 + 受邀成员 |
| 谁能添加足迹 | 仅自己 | 取决于模式 |
| 有成员和邀请链接 | 否 | 是 |

执行 `categories` 查看**所有**分类——个人和共享在一起。每个分类的 `mode` 字段可以区分它们。执行 `category-sets` 查看它们如何分组为工作区。

### 共享分类模式

**共建（cocreate）**——人人贡献：
- 任何成员都可以添加/移除足迹（`add-to-shared` / `remove-from-shared`）
- 任何成员都可以生成邀请链接（`create-invite-link`）
- 只有所有者可以解散或切换模式
- 适合：团队知识库、小组旅行规划、共享研究

**订阅（subscribe）**——成员只读：
- 只有所有者可以添加/移除足迹
- 只有所有者可以生成邀请链接
- 成员可以浏览和搜索，但不能修改
- `add-to-shared` 在订阅模式下返回 403
- 适合：精选推荐列表、资源收藏

所有者可以通过网页端随时切换共建和订阅模式。

### 共享流程

1. **创建** → `create-shared-category "团队知识库" --mode cocreate`
2. **生成邀请** → `create-invite-link <sc_id>` → 获得邀请码
3. **分享**邀请码给团队成员
4. **加入** → 成员执行 `join-shared-category <code>`
5. **共建** → 所有人用 `add-to-shared <sc_id> --collection-id <id>`
6. **本地保存** → 任何人可 `copy <id> --category-ids <ids>` 将共享足迹保存到个人收藏

### 角色与权限

| 操作 | 所有者 | 管理员 | 成员 |
|------|:-----:|:-----:|:----:|
| 添加/移除足迹（共建模式） | ✅ | ✅ | ✅ |
| 添加/移除足迹（订阅模式） | ✅ | ❌ | ❌ |
| 生成邀请链接（共建模式） | ✅ | ✅ | ✅ |
| 生成邀请链接（订阅模式） | ✅ | ❌ | ❌ |
| 编辑分类名称/描述 | ✅ | ❌ | ❌ |
| 切换共建 ↔ 订阅 | ✅ | ❌ | ❌ |
| 解散共享分类 | ✅ | ❌ | ❌ |
| 管理成员 | 仅网页端 | — | — |

### 搜索原理

1. **关键词搜索**（`search <关键词>`）——匹配标题、描述、AI 摘要和提取的文本内容。用 `--category-id` 按分类过滤。

2. **URL 去重**——用 URL 搜索时自动检测并匹配 URL 哈希，完全绕过文本搜索。

### Agent 交互模型

- **零配置**：首次运行自动注册（`POST /register`），获得 Bearer Token
- **Token 持久化**：保存在 `{baseDir}/.token`（chmod 600），跨会话复用
- **魔法链接**：`agent_magic_link` 为人类用户生成可点击的卡片界面 URL——有效期 30 天，可重复使用
- **账号升级**：用户后续绑定手机号后，Agent 创建的账号无缝升级为正式账号

## Command Reference

根据用户的指令，理解用户真实需求后，调用一个或多个命令来完成。

### 收藏与搜索

| 命令 | 作用 |
|------|------|
| `python {baseDir}/scripts/footprints.py add <url> --title <title> --description <desc> --content-type <type> --category-ids <ids> --tags <tags>` | 收藏链接或纯文字内容（url 可为空） |
| `python {baseDir}/scripts/footprints.py get <id>` | 查看某条收藏的详细信息 |
| `python {baseDir}/scripts/footprints.py search <query>` | 全文搜索标题、描述、AI 摘要 |
| `python {baseDir}/scripts/footprints.py list [--category-id <id>] [--limit <n>]` | 列出收藏列表 |

### 整理

| 命令 | 作用 |
|------|------|
| `python {baseDir}/scripts/footprints.py update <id> --title <t> --description <d> --content-type <ct> --category-ids <ids> --tags <tags>` | 修改收藏的标题、分类、标签等 |
| `python {baseDir}/scripts/footprints.py batch-update <updates>` | 批量整理收藏（每次最多 50 条） |
| `python {baseDir}/scripts/footprints.py categories` | 列出所有可用分类 |
| `python {baseDir}/scripts/footprints.py create-category <name> [--category-set-id <id>]` | 创建新分类 |
| `python {baseDir}/scripts/footprints.py tags` | 列出所有已使用的标签 |
| `python {baseDir}/scripts/footprints.py content-types` | 列出已使用的内容类型（article/video/image/audio/page） |
| `python {baseDir}/scripts/footprints.py category-sets` | 列出所有分类集（工作区） |
| `python {baseDir}/scripts/footprints.py create-category-set <name>` | 创建新分类集 |

### 共享

| 命令 | 作用 |
|------|------|
| `python {baseDir}/scripts/footprints.py create-shared-category <name> --mode cocreate\|subscribe --description <desc>` | 创建共享分类 |
| `python {baseDir}/scripts/footprints.py create-invite-link <sc_id> [--duration-hours 24]` | 生成邀请链接 |
| `python {baseDir}/scripts/footprints.py join-shared-category <invite_code>` | 通过邀请码加入共享分类 |
| `python {baseDir}/scripts/footprints.py add-to-shared <sc_id> --collection-id <id>` | 将收藏添加到共享分类 |
| `python {baseDir}/scripts/footprints.py remove-from-shared <sc_id> --collection-id <id>` | 从共享分类中移除收藏 |
| `python {baseDir}/scripts/footprints.py copy <id> --category-ids <ids>` | 将共享收藏复制到个人收藏 |

### 工具

| 命令 | 作用 |
|------|------|
| `python {baseDir}/scripts/footprints.py me` | 确认当前身份 |
| `python {baseDir}/scripts/footprints.py agent_magic_link` | 生成魔法链接——整理完毕后发给用户 |
| `python {baseDir}/scripts/footprints.py agent_register` | 重新注册 / 更换凭证 ⚠️ 会创建新账号 |

## 核心工作流

### 新用户 — 零配置

```
1. 自动注册 → Token 保存到 {baseDir}/.token
2. python {baseDir}/scripts/footprints.py add "<url>" --title "<标题>" → 添加收藏
3. python {baseDir}/scripts/footprints.py categories → 了解已有结构
4. python {baseDir}/scripts/footprints.py create-category "<名称>" → 创建分类
5. python {baseDir}/scripts/footprints.py update <id> --category-ids <ids> → 归类
6. python {baseDir}/scripts/footprints.py agent_magic_link → 发链接："整理好了，点这里查看 → [链接]"
```

### 老用户 — 日常使用

```
1. python {baseDir}/scripts/footprints.py me → 确认身份
2. python {baseDir}/scripts/footprints.py categories + python {baseDir}/scripts/footprints.py tags → 了解当前结构
3. python {baseDir}/scripts/footprints.py search query → 找到目标
4. python {baseDir}/scripts/footprints.py add / python {baseDir}/scripts/footprints.py update → 操作
```

### 团队共享

```
1. python {baseDir}/scripts/footprints.py create-shared-category "团队知识库" --mode cocreate
2. python {baseDir}/scripts/footprints.py create-invite-link <sc_id> → 把邀请码发给同事
3. 同事：python {baseDir}/scripts/footprints.py join-shared-category <invite_code>
4. 所有人：python {baseDir}/scripts/footprints.py add-to-shared <sc_id> --collection-id <collection_id> → 共建知识库
```

### 批量整理

```
1. python {baseDir}/scripts/footprints.py list --limit 100 → 获取全部收藏
2. python {baseDir}/scripts/footprints.py categories → 规划目标分类
3. python {baseDir}/scripts/footprints.py batch-update '[
     {"id":"uuid1","category_ids":[1,3]},
     {"id":"uuid2","title":"新标题","category_ids":[2,5]}
   ]' → 一次性修改（每次最多 50 条）
```

## 实战范例

常见任务的具体 bash 步骤。按编号顺序执行。

### 更改收藏的分类

```bash
python {baseDir}/scripts/footprints.py get 42
# → categories: [{id: 3, name: "阅读"}, {id: 5, name: "AI"}]

# 保留 AI，去掉阅读，加上技术（7）
python {baseDir}/scripts/footprints.py update 42 --category-ids 5,7
```

### 批量归入新分类

```bash
python {baseDir}/scripts/footprints.py create-category "新主题"    # → 返回新分类 ID
python {baseDir}/scripts/footprints.py list --limit 100
# 对每一条匹配的收藏：
python {baseDir}/scripts/footprints.py update <id> --category-ids <现有ID>,<新分类ID>
```

### 合并两个分类

```bash
python {baseDir}/scripts/footprints.py categories                      # 记下源和目标 ID
python {baseDir}/scripts/footprints.py list --category-id <源分类ID>   # 列出源分类下全部收藏
# 逐条将源分类 ID 替换为目标分类 ID
python {baseDir}/scripts/footprints.py update <id> --category-ids <目标ID>,<其他ID>
# 告知用户：空分类"源"已可删除（通过网页端操作）
```

### 按域名自动归类

用户说"把 github.com 的都放到 GitHub 分类里"：

```bash
python {baseDir}/scripts/footprints.py list --limit 200
# 在内存中过滤：url 包含 "github.com" 的条目
python {baseDir}/scripts/footprints.py create-category "GitHub"
# 逐条追加：
python {baseDir}/scripts/footprints.py update <id> --category-ids <现有ID>,<GitHub分类ID>
```

### 按标签筛选并批量加分类

```bash
python {baseDir}/scripts/footprints.py search docker
# 筛选 tag_names 包含 "docker" 的结果
# 逐条追加目标分类：
python {baseDir}/scripts/footprints.py update <id> --category-ids <现有ID>,<目标分类ID>
```

### 整理未分类的收藏

```bash
python {baseDir}/scripts/footprints.py list --limit 100
# 筛选 category_ids 为空或仅默认的条目
# 列出给用户挑选分类
# 批量更新选中的条目
```

### 根据标签推荐分类

发现标签和分类之间的空白——例如 #docker 出现频繁但没有"Docker"分类：

```bash
python {baseDir}/scripts/footprints.py tags        # 高频标签
python {baseDir}/scripts/footprints.py categories  # 已有分类
# 交叉比对：有标签无对应分类 → 建议用户创建
```

### 从共享分类复制到个人

```bash
python {baseDir}/scripts/footprints.py categories  # 找到目标个人分类 ID
python {baseDir}/scripts/footprints.py copy <收藏ID> --category-ids <个人分类ID>
```

### 跨 Agent 协作

两个 Agent 共同维护一个知识库：

```
1. Agent A：python {baseDir}/scripts/footprints.py create-shared-category "团队知识库" --mode cocreate
2. Agent A：python {baseDir}/scripts/footprints.py create-invite-link <sc_id> → 把邀请码发给用户
3. 用户转发给同事
4. Agent B：python {baseDir}/scripts/footprints.py join-shared-category <code>
5. 双方都能通过 python {baseDir}/scripts/footprints.py search 看到彼此的添加
```

## 魔法链接 — 交付闭环

整理完毕后，始终通过魔法链接交付结果：

```bash
python {baseDir}/scripts/footprints.py agent_magic_link
```

将链接发给用户："整理好了，点这里查看 → [链接]"

用户点击即可看到卡片式界面，所有收藏一目了然。**有效期 30 天，可重复使用。**如果用户后续绑定手机号，Agent 创建的账号无缝升级为正式账号。

## ⚠️ 关键陷阱

### category_ids 是替换，不是追加

修改收藏时，`--category-ids` 会完全替换原有分类——不是追加。

```bash
# ❌ 错误：把收藏移到分类 7，丢掉了原有的分类 3 和 5
python {baseDir}/scripts/footprints.py update 42 --category-ids 7

# ✅ 正确：先查现有分类，再合并
python {baseDir}/scripts/footprints.py get 42  # → 现有分类 [3, 5]
python {baseDir}/scripts/footprints.py update 42 --category-ids 3,5,7
```

### Subscribe 模式只读

往 subscribe 模式的共享分类写入会返回 403。告知用户该收藏夹为只读，需创建者改为 cocreate 模式。

### 绝对不要重复调用 agent_register

每次调用都会创建全新空白账号。务必先检查是否已有保存的 Token。不确定时先调 `python {baseDir}/scripts/footprints.py me` 确认。

### 频率限制

频繁调用会触发 HTTP 429。批量操作优先用 `batch-update`，连续调用间加适当间隔，遇到限流等几秒重试。

### 成员管理需通过网页

邀请或移除共享分类成员需要通过网页端 https://ai.ocean94.com 操作，无法通过 API 完成。

## 行为准则

### 始终做到
- **静默自动注册** — 不要为账号设置中断用户
- **先搜索再列举** — 用 `python {baseDir}/scripts/footprints.py search` 精准查询，而非全量导出
- **先了解再创建** — 添加前先调 `python {baseDir}/scripts/footprints.py categories` 和 `python {baseDir}/scripts/footprints.py tags` 避免重复
- **用魔法链接交付** — 整理完毕后始终生成链接发给用户

### 操作前确认
- 取消收藏与分类的关联（不可逆）
- 清除标签
- 修改 cocreate 共享分类（影响他人）
- 从共享分类中移除收藏（其他成员失去访问权）
