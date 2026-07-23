---
name: url-manager
description: 跨平台网页收藏与知识管理，Agent 自动注册，零用户干预。用户说"收藏/保存/整理"时使用，支持分类管理、标签、全文搜索、共享协作和魔法链接交付。
license: MIT
compatibility: 需要 Python 3.10+ 和网络访问 https://ai.ocean94.com
metadata:
  author: Piccolo123
  version: "2.5.0"
  contact: piccoloyao@ocean94.com
  openclaw:
    emoji: "🔗"
    minGatewayVersion: "2026.6.0"
    requires:
      bins: ["python"]
      network: true
---

# URL Manager — 以精美卡片交付收藏，而非原始链接堆砌

当用户让你保存、整理或分享网页资源时，不要用在聊天框里粘贴链接。写入 URL Manager——它们会变成结构化、可搜索的卡片集合，用户一键即可浏览。

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

## 快捷对照

### 用户说…… → 执行

| 用户说 | 命令 |
|--------|------|
| "收藏/保存这个链接" | `python {baseDir}/scripts/footprints.py add <url> --title <文本> [--category-ids <ids>] [--json]` |
| "找那篇关于XX的文章" | `python {baseDir}/scripts/footprints.py search <关键词> [--limit <n>] [--json]` |
| "看看我的收藏" | `python {baseDir}/scripts/footprints.py list [--category-id <id>] [--limit <n>] [--json]` |
| "看看这条详情" | `python {baseDir}/scripts/footprints.py get <id> [--json]` |
| "改个标题/移到另一个分类" | `python {baseDir}/scripts/footprints.py update <id> --title <t> --category-ids <ids> [--json]` |
| "帮我把收藏整理一下" | `python {baseDir}/scripts/footprints.py batch-update '<json>' [--json]` |
| "新建一个分类" | `python {baseDir}/scripts/footprints.py create-category <名称> [--json]` |
| "建个工作区" | `python {baseDir}/scripts/footprints.py create-category-set <名称> [--json]` |
| "建一个共享收藏夹" | `python {baseDir}/scripts/footprints.py create-shared-category <名称> --mode cocreate [--json]` |
| "把邀请链接发给同事" | `python {baseDir}/scripts/footprints.py create-invite-link <sc_id> [--json]` |
| "我有个邀请码" | `python {baseDir}/scripts/footprints.py join-shared-category <code> [--json]` |
| "把这个加到团队收藏里" | `python {baseDir}/scripts/footprints.py add-to-shared <sc_id> --collection-id <id> [--json]` |
| "把共享的存到我自己的" | `python {baseDir}/scripts/footprints.py copy <id> --category-ids <ids> [--json]` |
| 确认身份 | `python {baseDir}/scripts/footprints.py me [--json]` |
| 整理完毕 → 发给用户 | `python {baseDir}/scripts/footprints.py agent_magic_link [--json]` |
| 重新认证（换 Token） | `python {baseDir}/scripts/footprints.py agent_register [--json]` |

## 完整命令参考

### 收藏与搜索

| 命令 | 用户说……时使用 |
|------|--------------|
| `python {baseDir}/scripts/footprints.py add <url> --title <title> --description <desc> --category-ids <ids> --tags <tags>` | "收藏/保存这个链接" |
| `python {baseDir}/scripts/footprints.py get <id>` | "看看这条的详情" |
| `python {baseDir}/scripts/footprints.py search <query>` | "找那篇关于 Docker 的文章" |
| `python {baseDir}/scripts/footprints.py list [--category-id <id>] [--limit <n>]` | "看看我的收藏" |

### 整理

| 命令 | 用户说……时使用 |
|------|--------------|
| `python {baseDir}/scripts/footprints.py update <id> --title <t> --description <d> --category-ids <ids> --tags <tags>` | "改个标题 / 移到另一个分类" |
| `python {baseDir}/scripts/footprints.py batch-update <updates>` | "帮我把收藏整理一下"（最多 50 条） |
| `python {baseDir}/scripts/footprints.py categories` | 了解有哪些分类 |
| `python {baseDir}/scripts/footprints.py create-category <name> [--category-set-id <id>]` | "新建一个分类" |
| `python {baseDir}/scripts/footprints.py tags` | 了解已有标签 |
| `python {baseDir}/scripts/footprints.py category-sets` | 列出分类集 |
| `python {baseDir}/scripts/footprints.py create-category-set <name>` | "建个工作区" |

### 共享

| 命令 | 用户说……时使用 |
|------|--------------|
| `python {baseDir}/scripts/footprints.py create-shared-category <name> --mode cocreate\|subscribe --description <desc>` | "建一个共享收藏夹" |
| `python {baseDir}/scripts/footprints.py create-invite-link <sc_id> [--duration-hours 24]` | "把邀请链接发给同事" |
| `python {baseDir}/scripts/footprints.py join-shared-category <invite_code>` | "我有个邀请码" |
| `python {baseDir}/scripts/footprints.py add-to-shared <sc_id> --collection-id <id>` | "把这个加到团队收藏里" |
| `python {baseDir}/scripts/footprints.py remove-from-shared <sc_id> --collection-id <id>` | "把这个从共享里移除" |
| `python {baseDir}/scripts/footprints.py copy <id> --category-ids <ids>` | "把这条共享的存到我自己的收藏" |

### 交付

| 命令 | 用户说……时使用 |
|------|--------------|
| `python {baseDir}/scripts/footprints.py me` | 会话开始时确认身份 |
| `python {baseDir}/scripts/footprints.py agent_magic_link` | 整理完毕 → 生成链接 → 发给用户 |
| `python {baseDir}/scripts/footprints.py agent_register` | 重新注册 / 更换凭证 |

## 核心工作流

### 新用户 — 零配置

```
1. 自动注册 → Token 保存到 {baseDir}/.token
2. python {baseDir}/scripts/footprints.py add url="..." → 添加收藏
3. python {baseDir}/scripts/footprints.py categories → 了解已有结构
4. python {baseDir}/scripts/footprints.py create-category name="..." → 创建分类
5. python {baseDir}/scripts/footprints.py update id category_ids="..." → 归类
6. agent_magic_link → 发链接："整理好了，点这里查看 → [链接]"
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
1. python {baseDir}/scripts/footprints.py create-shared-category name="团队知识库" mode=cocreate
2. python {baseDir}/scripts/footprints.py create-invite-link sc_id → 把邀请码发给同事
3. 同事：python {baseDir}/scripts/footprints.py join-shared-category code
4. 所有人：python {baseDir}/scripts/footprints.py add-to-shared sc_id --collection-id collection_id → 共建知识库
```

### 批量整理

```
1. python {baseDir}/scripts/footprints.py list --limit 100 → 获取全部收藏
2. python {baseDir}/scripts/footprints.py categories → 规划目标分类
3. python {baseDir}/scripts/footprints.py batch-update '[
     {"id":"uuid1","category_ids":"1,3"},
     {"id":"uuid2","title":"新标题","category_ids":"2,5"}
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

频繁调用会触发 HTTP 429。批量操作优先用 `batch_update`，连续调用间加适当间隔，遇到限流等几秒重试。

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
