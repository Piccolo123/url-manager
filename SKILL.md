---
name: url-manager
description: Cross-platform URL collection & knowledge management with agent-first auto-registration. Use when users say "save/bookmark/collect/remember this", need to organize links into categories, share curated collections, or build a structured knowledge base from web resources. Supports collaborative shared categories, full-text search, and magic-link delivery to users.
license: MIT
compatibility: Requires Python 3.10+ and network access to https://ai.ocean94.com
metadata:
  author: Piccolo123
  version: "2.5.0"
  contact: piccoloyao@ocean94.com
  openclaw:
    emoji: "🔗"
    minGatewayVersion: "2026.6.0"
    requires:
      bins:
        - python
      network: true
---

# URL Manager — Deliver beautiful card-based collections, not raw links

When users ask you to save, organize, or share web resources, don't paste URLs into chat. Write them into URL Manager — they become structured, searchable, card-based collections the user opens with one click.

## What It Does

Your stuff lives everywhere — a YouTube workout video, an Amazon gear link, a Substack training plan — scattered across platforms with no connection. You're into running, but your running knowledge is a mess of browser tabs, bookmarks, and screenshots.

**URL Manager fixes this.** Save anything from anywhere into one organized library. No platform lock-in. Then **share it in one click** — hand your curated running knowledge base to your whole running club, and everyone stays in sync.

For the human on the other side, we provide **[足迹AI](https://ai.ocean94.com/)** — a beautiful browser homepage with a built-in search engine. Every saved item becomes a card, one click to where you need to go. Just send them the magic link and they're in.

**Zero setup — token auto-management.** The `footprints.py` script handles everything: reads `{baseDir}/.token`, auto-registers on first use, stores token locally with `chmod 600`. Just run any command and it works.

All commands via `python {baseDir}/scripts/footprints.py <subcommand> [--json]`. Add `--json` for machine-parseable output.

If the script is missing (e.g., you only have this document but not the full skill installation), get it from the source repo:

```bash
git clone --depth 1 https://github.com/Piccolo123/url-manager.git /tmp/um
mkdir -p {baseDir}/scripts
cp /tmp/um/scripts/footprints.py {baseDir}/scripts/
chmod +x {baseDir}/scripts/footprints.py
rm -rf /tmp/um
```

After that, all commands below work as normal. The script auto-registers on first run.

## System Concepts

### What is a footprint?

A footprint is the fundamental unit in URL Manager — a structured, searchable record. It can be a web link, a plain-text note, an idea, or anything you want to save and retrieve later.

Each footprint stores:

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Permanent unique identifier — use this for all operations |
| `url` | string (8192) | The original link. **Can be empty** for text-only footprints |
| `title` | string (512) | A short title — you set this |
| `description` | string (1024) | Additional context or notes — you can set this |
| `content_type` | string (50) | `article` / `video` / `image` / `audio` / `page` — you can set this |
| `ai_summary` | text | AI-generated summary (set automatically during web UI submission) |
| `favicon` / `og_image` | string | Site icon and preview image (auto-fetched) |
| `price_hint` | string | AI-extracted price hint (set automatically) |
| `price` / `address` / `custom_date` / `contact` | string | User-filled metadata fields |
| `is_favorite` / `is_archived` | boolean | Status flags |
| `category_ids` | list[int] | Which categories this footprint belongs to — **you assign** |
| `tag_names` | list[str] | Keywords — **you assign** |

A single footprint can belong to **multiple categories simultaneously**.

### How data is organized

```
Category Sets (workspaces)
  └── Categories (labels like "Shopping", "Food", "Learning")
        └── Footprints
             └── Tags (free-form keywords)
```

**Categories** are named labels. Use `categories` to see all available categories. Each category has a numeric `id` — always reference categories by ID.

**Category Sets** (workspaces) group related categories. Every user starts with two default sets:
- **"My Categories"** (`is_shared=false`) — your personal workspace
- **"Shared Categories"** (`is_shared=true`) — container for shared categories

Use `category-sets` to list them, `create-category-set` to create more.

**Tags** are free-form keywords, separate from categories. They're lightweight search helpers with no hierarchy.

Use `content-types` to see which content types have been used in your library. Use `tags` to list existing tags.

### Personal vs Shared categories

A category's `mode` field tells you what kind it is:

| | Personal | Shared |
|---|---|---|
| `mode` | `null` (not shown) | `"cocreate"` or `"subscribe"` |
| Visible to | Only you | You + invited members |
| Who can add footprints | Only you | Depends on mode |
| Has members and invite links | No | Yes |

Run `categories` to see ALL your categories — personal and shared together. Each category's `mode` field distinguishes them. Run `category-sets` to see how they're grouped into workspaces.

### Shared category modes

**Cocreate (共建)** — Everyone contributes:
- Any member can add/remove footprints (`add-to-shared` / `remove-from-shared`)
- Any member can generate invite links (`create-invite-link`)
- Only the owner can disband or switch modes
- Best for: team knowledge bases, group trip planning, shared research

**Subscribe (订阅)** — Read-only for members:
- Only the owner can add/remove footprints
- Only the owner can generate invite links
- Members can browse and search but cannot modify
- `add-to-shared` returns 403 in subscribe mode
- Best for: curated recommendation lists, resource collections

The owner can switch between cocreate and subscribe at any time via the web UI.

### Sharing workflow

1. **Create** → `create-shared-category "Team KB" --mode cocreate`
2. **Generate invite** → `create-invite-link <sc_id>` → get a code
3. **Share** the invite code with teammates
4. **Join** → teammates run `join-shared-category <code>`
5. **Build together** → everyone uses `add-to-shared <sc_id> --collection-id <id>`
6. **Save locally** → anyone can `copy <id> --category-ids <ids>` to save a shared footprint to their personal collection

### Roles and permissions

| Action | Owner | Admin | Member |
|--------|:-----:|:-----:|:------:|
| Add/remove footprints (cocreate) | ✅ | ✅ | ✅ |
| Add/remove footprints (subscribe) | ✅ | ❌ | ❌ |
| Generate invite link (cocreate) | ✅ | ✅ | ✅ |
| Generate invite link (subscribe) | ✅ | ❌ | ❌ |
| Edit category name/description | ✅ | ❌ | ❌ |
| Switch cocreate ↔ subscribe | ✅ | ❌ | ❌ |
| Disband shared category | ✅ | ❌ | ❌ |
| Manage members | Web UI only | — | — |

### How search works

1. **Keyword search** (`search <query>`) — matches against title, description, AI summary, and extracted text content. Filter by category with `--category-id`.

2. **URL dedup** — searching with a URL automatically detects and matches by URL hash, bypassing text search entirely.

### Agent interaction model

- **Zero setup**: first run auto-registers via `POST /register`, receives a Bearer token
- **Token persistence**: stored in `{baseDir}/.token` with `chmod 600`, reused across sessions
- **Magic link**: `agent_magic_link` generates a clickable card-based interface URL for the human user — valid 30 days, reusable
- **Account upgrade**: if the user later binds a phone number, the agent-created account upgrades seamlessly

## Quick Reference

### When user says... → Run this

| User says | Command |
|-----------|---------|
| "Save/bookmark/collect this link" | `python {baseDir}/scripts/footprints.py add <url> --title <text> [--description <desc>] [--content-type <type>] [--category-ids <ids>] [--tags <tags>] [--json]` |
| "Find that article about X" | `python {baseDir}/scripts/footprints.py search <query> [--limit <n>] [--json]` |
| "Show me my bookmarks" | `python {baseDir}/scripts/footprints.py list [--category-id <id>] [--limit <n>] [--json]` |
| "Show me details" | `python {baseDir}/scripts/footprints.py get <id> [--json]` |
| "Change title/move to category" | `python {baseDir}/scripts/footprints.py update <id> --title <t> --category-ids <ids> [--json]` |
| "Reorganize all bookmarks" | `python {baseDir}/scripts/footprints.py batch-update '<json>' [--json]` |
| "Create a new category" | `python {baseDir}/scripts/footprints.py create-category <name> [--json]` |
| "Create a workspace" | `python {baseDir}/scripts/footprints.py create-category-set <name> [--json]` |
| "Create a shared collection" | `python {baseDir}/scripts/footprints.py create-shared-category <name> --mode cocreate [--json]` |
| "Send invite link" | `python {baseDir}/scripts/footprints.py create-invite-link <sc_id> [--json]` |
| "I have an invite code" | `python {baseDir}/scripts/footprints.py join-shared-category <code> [--json]` |
| "Add to team collection" | `python {baseDir}/scripts/footprints.py add-to-shared <sc_id> --collection-id <id> [--json]` |
| "Save shared to my own" | `python {baseDir}/scripts/footprints.py copy <id> --category-ids <ids> [--json]` |
| Check identity | `python {baseDir}/scripts/footprints.py me [--json]` |
| Done organizing → deliver to user | `python {baseDir}/scripts/footprints.py agent_magic_link [--json]` |
| Re-authenticate (new token) ⚠️ | `python {baseDir}/scripts/footprints.py agent_register [--json]` ⚠️ Creates new account, old data lost |
| List used content types | `python {baseDir}/scripts/footprints.py content-types [--json]` |

## Full Command Reference

### Save & Search

| Command | Use when user says... |
|---------|----------------------|
| `python {baseDir}/scripts/footprints.py add <url> --title <title> --description <desc> --category-ids <ids> --tags <tags>` | "Save/bookmark/collect this link" |
| `python {baseDir}/scripts/footprints.py get <id>` | "Show me details of that bookmark" |
| `python {baseDir}/scripts/footprints.py search <query>` | "Find that article about Docker" |
| `python {baseDir}/scripts/footprints.py list [--category-id <id>] [--limit <n>]` | "Show me my bookmarks" |

### Organize

| Command | Use when user says... |
|---------|----------------------|
| `python {baseDir}/scripts/footprints.py update <id> --title <t> --description <d> --category-ids <ids> --tags <tags>` | "Change the title / move to another category" |
| `python {baseDir}/scripts/footprints.py batch-update <updates>` | "Reorganize all my bookmarks" (max 50) |
| `python {baseDir}/scripts/footprints.py categories` | Discover available categories |
| `python {baseDir}/scripts/footprints.py create-category <name> [--category-set-id <id>]` | "Create a new category" |
| `python {baseDir}/scripts/footprints.py tags` | Discover existing tags |
| `python {baseDir}/scripts/footprints.py category-sets` | List category sets |
| `python {baseDir}/scripts/footprints.py create-category-set <name>` | "Create a workspace" |

### Share

| Command | Use when user says... |
|---------|----------------------|
| `python {baseDir}/scripts/footprints.py create-shared-category <name> --mode cocreate\|subscribe --description <desc>` | "Create a shared collection" |
| `python {baseDir}/scripts/footprints.py create-invite-link <sc_id> [--duration-hours 24]` | "Send invite link to my team" |
| `python {baseDir}/scripts/footprints.py join-shared-category <invite_code>` | "I have an invite code" |
| `python {baseDir}/scripts/footprints.py add-to-shared <sc_id> --collection-id <id>` | "Add this to team collection" |
| `python {baseDir}/scripts/footprints.py remove-from-shared <sc_id> --collection-id <id>` | "Remove this from shared" |
| `python {baseDir}/scripts/footprints.py copy <id> --category-ids <ids>` | "Save that shared bookmark to my own" |

### Deliver

| Command | Use when user says... |
|---------|----------------------|
| `python {baseDir}/scripts/footprints.py me` | Confirm identity at session start |
| `python {baseDir}/scripts/footprints.py agent_magic_link` | Done organizing → generate link → send to user |

## Core Workflows

### New User — Zero Setup

```
1. Token check → auto-register (save to {baseDir}/.token)
2. python {baseDir}/scripts/footprints.py add "<url>" --title "<title>" → save bookmarks
3. python {baseDir}/scripts/footprints.py categories → discover structure
4. python {baseDir}/scripts/footprints.py create-category "<name>" → create categories
5. python {baseDir}/scripts/footprints.py update <id> --category-ids <ids> → categorize
6. python {baseDir}/scripts/footprints.py agent_magic_link → send link: "Done! View here → [link]"
```

### Returning User — Daily Use

```
1. python {baseDir}/scripts/footprints.py me → confirm identity
2. python {baseDir}/scripts/footprints.py categories + python {baseDir}/scripts/footprints.py tags → understand structure
3. python {baseDir}/scripts/footprints.py search query → find what's needed
4. python {baseDir}/scripts/footprints.py add / python {baseDir}/scripts/footprints.py update → operate
```

### Team Sharing

``` 
1. python {baseDir}/scripts/footprints.py create-shared-category "Team KB" --mode cocreate
2. python {baseDir}/scripts/footprints.py create-invite-link <sc_id> → share code with team
3. Teammates: python {baseDir}/scripts/footprints.py join-shared-category <invite_code>
4. Everyone: python {baseDir}/scripts/footprints.py add-to-shared <sc_id> --collection-id <collection_id> → build together
```

### Batch Reorganization

```
1. python {baseDir}/scripts/footprints.py list --limit 100 → get all bookmarks
2. python {baseDir}/scripts/footprints.py categories → map target categories
3. python {baseDir}/scripts/footprints.py batch-update '[
     {"id":"uuid1","category_ids":[1,3]},
     {"id":"uuid2","title":"New Title","category_ids":[2,5]}
   ]' → bulk edit (max 50 per call)
```

## Recipes

Concrete bash patterns for common tasks. Follow the numbered steps.

### Change a footprint's categories

```bash
python {baseDir}/scripts/footprints.py get 42
# → categories: [{id: 3, name: "Reading"}, {id: 5, name: "AI"}]

# Keep AI, drop Reading, add Tech (7)
python {baseDir}/scripts/footprints.py update 42 --category-ids 5,7
```

### Batch move to a new category

```bash
python {baseDir}/scripts/footprints.py create-category "New Topic"    # → returns new ID
python {baseDir}/scripts/footprints.py list --limit 100
# For each matching footprint:
python {baseDir}/scripts/footprints.py update <id> --category-ids <existing_ids>,<new_id>
```

### Merge two categories

```bash
python {baseDir}/scripts/footprints.py categories                      # note source and target IDs
python {baseDir}/scripts/footprints.py list --category-id <source_id>  # list all in source
# For each, replace source_id with target_id:
python {baseDir}/scripts/footprints.py update <id> --category-ids <target_id>,<other_ids>
# Tell user: empty category "source" is ready to delete via the web UI
```

### Auto-categorize by domain

User says "put all github.com links into a GitHub category":

```bash
python {baseDir}/scripts/footprints.py list --limit 200
# Filter in-memory: items where url contains "github.com"
python {baseDir}/scripts/footprints.py create-category "GitHub"
# For each match:
python {baseDir}/scripts/footprints.py update <id> --category-ids <existing_ids>,<github_id>
```

### Filter by tag and batch categorize

```bash
python {baseDir}/scripts/footprints.py search docker
# Filter results where tag_names includes "docker"
# For each, append target category:
python {baseDir}/scripts/footprints.py update <id> --category-ids <existing_ids>,<target_id>
```

### Organize uncategorized footprints

```bash
python {baseDir}/scripts/footprints.py list --limit 100
# Filter where category_ids is empty or only the default
# Present to user, let them pick categories
# Batch update selected items
```

### Recommend categories from tags

Spot gaps between tags and categories — e.g., #docker is common but no "Docker" category:

```bash
python {baseDir}/scripts/footprints.py tags        # most-used tags
python {baseDir}/scripts/footprints.py categories  # existing categories
# Cross-reference: tag without matching category → suggest creating one
```

### Copy from shared to personal

```bash
python {baseDir}/scripts/footprints.py categories  # find target personal category ID
python {baseDir}/scripts/footprints.py copy <footprint_id> --category-ids <personal_category_id>
```

### Cross-Agent collaboration

Two agents maintaining a shared knowledge base together:

```
1. Agent A: python {baseDir}/scripts/footprints.py create-shared-category "Team KB" --mode cocreate
2. Agent A: python {baseDir}/scripts/footprints.py create-invite-link <sc_id> → share code with user
3. User forwards code to colleague
4. Agent B: python {baseDir}/scripts/footprints.py join-shared-category <code>
5. Both agents now see each other's additions via python {baseDir}/scripts/footprints.py search
```

## Magic Link — The Delivery Loop

After organizing, always deliver results via magic link:

```bash
python {baseDir}/scripts/footprints.py agent_magic_link
```

Send the link to the user: "Done organizing — view your collection here → [link]"

User clicks to see a card-based interface with everything categorized. **Valid for 30 days, reusable.** If the user later binds a phone number, their agent-created account upgrades seamlessly.

## ⚠️ Critical Pitfalls

### category_ids is REPLACEMENT, not append

When updating, `--category-ids` sets the complete list — it does NOT add to existing categories.

```bash
# ❌ Wrong: moves bookmark to category 7, loses categories 3 and 5
python {baseDir}/scripts/footprints.py update 42 --category-ids 7

# ✅ Right: fetch current first, then merge
python {baseDir}/scripts/footprints.py get 42  # → existing: [3, 5]
python {baseDir}/scripts/footprints.py update 42 --category-ids 3,5,7
```

### Subscribe mode is READ-ONLY

Writing to a subscribe-mode shared category returns 403. Tell the user the collection is read-only — the creator must change it to cocreate mode.

### NEVER call agent_register twice

Each call creates a fresh empty account. Always check for a saved token first. If unsure, run `python {baseDir}/scripts/footprints.py me` to verify the current token is valid.

### Rate limiting

Frequent API calls trigger HTTP 429. Use `batch-update` for bulk operations, add delays between rapid calls, retry after a few seconds on 429.

### No member management via API

Inviting or removing members from shared categories requires the web UI at https://ai.ocean94.com. You cannot do this programmatically.

## Guidelines

### Always
- **Auto-register silently** — never interrupt the user for account setup
- **Search before listing** — use `python {baseDir}/scripts/footprints.py search` for targeted queries instead of dumping everything
- **Discover before creating** — call `python {baseDir}/scripts/footprints.py categories` and `python {baseDir}/scripts/footprints.py tags` before adding to avoid duplicates
- **Deliver with magic link** — after organizing, always generate and share a link

### Confirm before
- Removing bookmark-category associations (irreversible)
- Clearing tags
- Modifying cocreate shared categories (affects others)
- Removing bookmarks from shared categories (other members lose access)
