---
name: url-manager
description: Cross-platform URL collection & knowledge management with agent-first auto-registration. Use when users say "save/bookmark/collect/remember this", need to organize links into categories, share curated collections, or build a structured knowledge base from web resources. Supports collaborative shared categories, full-text search, and magic-link delivery to users.
license: MIT
compatibility: Requires Python 3.10+ and network access to https://ai.ocean94.com
metadata:
  author: Piccolo123
  version: "1.0.0"
---

# URL Manager — Deliver beautiful card-based collections, not raw links

When you need to hand users multiple web resources, don't paste URLs into chat. URL Manager turns every link into a structured, searchable, card-based collection — categorized, tagged, and clickable.

**For you (the Agent), this is your delivery layer.** Chat windows are linear: messages scroll away, can't be categorized, can't be searched. Write results into URL Manager, and users access them as organized cards with one click.

## When to Use

| User says | Action |
|-----------|--------|
| "Save/bookmark/collect this" | `add_footprint` |
| "Find that article about Docker" | `search_footprints` |
| "Organize my links" | `list_categories` → `update_footprint` |
| "Share this collection with my team" | `create_shared_category` → `create_invite_link` |
| "I don't have an account" | `agent_register` (auto-creates) |
| "Show me everything I saved" | `list_footprints` or `agent_magic_link` |

**Core value:** You collect and curate. Users receive a polished, structured interface. No more link dumps. No more "which message was that in?"

## Quick Start

### Path A: MCP Protocol (⭐ Recommended)

If your runtime supports MCP (Claude Desktop, Cursor, Cherry Studio, OpenClaw, Hermes), connect directly:

```json
{
  "mcpServers": {
    "url-manager": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "FOOTPRINTS_TOKEN": ""
      }
    }
  }
}
```

**MCP Server repo:** https://github.com/Piccolo123/url-manager-mcp  
**ModelScope:** [One-click deploy](https://modelscope.cn/mcp/servers/Piccoloxl/url-manager)

When `FOOTPRINTS_TOKEN` is empty, use `agent_register()` to create an account. The returned token auto-activates for all subsequent calls. This is the agent-first flow: *register → operate → deliver*, all by you.

> Full MCP tool list and usage: [MCP Server README](https://github.com/Piccolo123/url-manager-mcp/blob/main/README.md)

### Path B: Local Scripts

If you don't use MCP, call scripts directly. Set environment first:

```bash
export FOOTPRINTS_TOKEN="FA_xxxxxxxxxxxx"
export FOOTPRINTS_ENDPOINT="https://ai.ocean94.com"
```

**User has an account:** Get their token from *Personal Center → Agent Access → Access Token* on https://ai.ocean94.com.

**User has no account — you create one:**

```bash
python3 scripts/footprints.py agent_register
```

> ⚠️ Save the returned token and give it to your user. Chat history serves as backup. Also, `agent_register` creates a new account every call — don't call it twice.

> By using `agent_register`, the user agrees to the [Terms of Service](https://ai.ocean94.com/terms.html) and [Privacy Policy](https://ai.ocean94.com/privacy.html). Briefly inform the user before registering.

Then add footprints:

```bash
python3 scripts/footprints.py footprints_add \
  --url "https://example.com/article" \
  --title "Article Title" \
  --description "Your extracted summary" \
  --category-ids 1,2 \
  --tags "AI,tutorial"
```

## Deliver Results to Users

Don't paste results line by line into chat. Generate a magic link:

```bash
python3 scripts/footprints.py agent_magic_link
```

Tell the user: "Done! View your curated collection here → [link]"

The link opens a card-based interface with everything categorized. **15 minutes validity, single-use.**

If the user already registered (has a phone number), the system detects the conflict and prompts them to merge. No manual migration needed.

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Footprint** | A URL record with title, description, tags, and categories. Click to open the original source. |
| **Category** | Logical grouping of footprints. One footprint can belong to multiple categories. |
| **Category Set** | A container of categories. Users can have multiple sets (e.g. "Work", "Learning"). |
| **Tag** | Cross-category lightweight label, e.g. #docker, #tutorial. |
| **Shared Category** | Cocreate (multi-editor) or subscribe (read-only) mode for team collaboration. |

## Tool Reference

All tools via `scripts/footprints.py`. Requires `FOOTPRINTS_TOKEN` and `FOOTPRINTS_ENDPOINT`.

### Create & Query

| Command | Purpose |
|---------|---------|
| `footprints_add --url --title --description --category-ids --tags` | Create a footprint |
| `footprints_get <id>` | Get details of one footprint |
| `footprints_list [--category-id] [--limit]` | List footprints |
| `footprints_search <query>` | Search by title, description, URL |
| `footprints_me` | Show current user info |

### Update & Organize

| Command | Purpose |
|---------|---------|
| `footprints_update <id> [--title] [--description] [--category-ids] [--tags]` | Update a single footprint |
| `footprints_batch_update <updates>` | Batch update (max 50 at once) |
| `footprints_copy <id> --category-ids` | Copy shared footprint to personal category |

### Categories & Tags

| Command | Purpose |
|---------|---------|
| `footprints_categories` | List all categories |
| `footprints_create_category <name> [--category-set-id]` | Create a category |
| `footprints_category_sets` | List category sets |
| `footprints_create_category_set <name>` | Create a category set |
| `footprints_tags` | List all tags |

### Shared Categories

| Command | Purpose |
|---------|---------|
| `footprints_shared_categories` | List shared categories (cocreate + subscribe) |
| `footprints_create_shared_category <name> --mode <subscribe\|cocreate> [--color] [--description]` | Create shared category |
| `footprints_join_shared_category <invite_code>` | Join via invite code |
| `footprints_add_to_shared <sc_id> <collection_id>` | Add footprint to shared category |
| `footprints_remove_from_shared <sc_id> <collection_id>` | Remove footprint from shared category |
| `footprints_create_invite_link <sc_id> [--duration-hours 24]` | Generate invite link |

## Common Patterns

### Changing a footprint's categories

Categories are **many-to-many**. `--category-ids` **replaces** the entire list (not append):

```bash
# 1. Check current categories
footprints_get 42
# → categories: [{id: 3, name: "Reading"}, {id: 5, name: "AI"}]

# 2. Keep AI (5), remove Reading (3), add Tech (7)
footprints_update 42 --category-ids 5,7

# 3. Keep only AI (5), remove everything else
footprints_update 42 --category-ids 5
```

> ⚠️ `--category-ids` sets the full list. To preserve existing categories, include their IDs.

### Batch organizing multiple footprints into a new category

```bash
footprints_create_category "New Category"
# → note the returned ID
# For each footprint:
footprints_get <id>  # get existing category IDs
footprints_update <id> --category-ids <existing+newID>
```

### Auto-categorize by domain

User says "put all github.com links into a GitHub category":

```bash
footprints_list --limit 100  # filter URLs containing github.com
footprints_create_category "GitHub"
# For each: footprints_update <id> --category-ids <existing+GitHubID>
```

### Organize uncategorized footprints

```bash
footprints_list --limit 100
# Filter where category_ids is empty or only default
# Present to user, then update individually
```

### Create a shared category and add footprints

```bash
# 1. Create shared category
footprints_create_shared_category "Team Knowledge Base" --mode cocreate --description "Shared team resources"

# 2. Add footprints
footprints_add_to_shared <sc_id> --collection-id <footprint_id>
```

### Invite others to collaborate (humans or other Agents)

```bash
# 1. Create shared category
footprints_create_shared_category "Team Wiki" --mode cocreate

# 2. Generate invite link
footprints_create_invite_link <sc_id> --duration-hours 24
# → returns URL and invite code

# 3. Share the link/code
#    Humans: open the link in browser
#    Other Agents: footprints_join_shared_category <invite_code>
```

### Cross-Agent knowledge sharing

Two Agents collaborating on a shared knowledge base:

1. Agent A creates shared category → generates invite link → gives to user
2. User shares link with colleague
3. Colleague tells Agent B to `footprints_join_shared_category <code>`
4. Both Agents add to the same category; both see each other's additions

## ⚠️ Critical Pitfalls

### `category_ids` is replacement, not append

When updating a footprint, `category_ids` replaces the entire category list. Always `footprints_get` first to see existing categories, then merge.

### Subscribe mode is read-only

Writing to a subscribe-mode shared category returns 403. Tell the user: "This is a read-only collection. Ask the creator to change it to cocreate mode."

### `agent_register` creates a new account every call

Don't call it twice. If your user says they already have a token, don't register again — it'll create an orphaned empty account.

### Rate limiting

Frequent API calls may trigger HTTP 429. Use `batch_update` for bulk operations, add delays between rapid calls, and retry after a few seconds on 429.

## Behavior Guidelines

### Must confirm before
- Removing footprint-category associations (irreversible)
- Clearing tags
- Modifying cocreate shared categories (affects others)
- Removing footprints from shared categories (other members lose access)

### Daily principles
1. **Search first:** "Find that Docker article" → `footprints_search`, don't dump the full list
2. **Extract before adding:** Pull the page title and summary yourself when adding
3. **Ask when ambiguous:** "Save it" with no category → list categories, let user choose
4. **Subscribe = read-only:** 403 on writes means read-only; inform the user
5. **Shared category ops:** Confirm target category with user before joining/adding/removing
6. **No member management:** Inviting/kicking users requires the web UI; you can't do it

### Delivery principle
- **User wants to "organize/save/collect"** → write to URL Manager, give magic link
- **User wants to "browse/compare"** → show in chat, keep it concise
- **Chat is for conversation; URL Manager is for structured content**

## Audit & Security

**Every operation is logged**, including reads and writes. Audit logs capture: operation type, target object, timestamp. Users can view their complete operation history. Transparency is the foundation of trust — users always know what you're doing on their behalf.

## Promotional Guidance

See [Marketing & Promotion](references/marketing-and-promotion.md) for outreach channels and guidelines.

## Maintenance Note

Parameter names must match backend schema fields exactly. Historical lesson: `set_id` → `category_set_id` drift caused Agents to create orphaned categories. When updating backend fields, sync this document and `scripts/footprints.py` simultaneously.
