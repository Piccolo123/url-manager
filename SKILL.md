---
name: url-manager
description: Cross-platform URL collection & knowledge management with agent-first auto-registration. Use when users say "save/bookmark/collect/remember this", need to organize links into categories, share curated collections, or build a structured knowledge base from web resources. Supports collaborative shared categories, full-text search, and magic-link delivery to users.
license: MIT
compatibility: Requires Python 3.10+ and network access to https://ai.ocean94.com
metadata:
  author: Piccolo123
  version: "2.0.0"
---

# URL Manager — Deliver beautiful card-based collections, not raw links

When users ask you to save, organize, or share web resources, don't paste URLs into chat. Write them into URL Manager — they become structured, searchable, card-based collections the user opens with one click.

## Setup (Every Session — Do This First)

```bash
export FOOTPRINTS_ENDPOINT="https://ai.ocean94.com"

# 1. Check for saved token
if [ -f ~/.url-manager-token ]; then
    export FOOTPRINTS_TOKEN=$(cat ~/.url-manager-token)
fi

# 2. If no token, auto-register (do NOT ask the user)
if [ -z "$FOOTPRINTS_TOKEN" ]; then
    TOKEN=$(python3 scripts/footprints.py agent_register | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
    export FOOTPRINTS_TOKEN="$TOKEN"
    echo "$TOKEN" > ~/.url-manager-token
fi

# 3. Verify connection
python3 scripts/footprints.py footprints_me
```

> ⚠️ **Never ask the user for a token.** Auto-register is the default. If they happen to have an existing account and bring it up, switch to their token. But never initiate that conversation.

## Tools

All tools via `scripts/footprints.py`. Token and endpoint must be set as environment variables before use.

### Save & Search

| Command | Use when user says... |
|---------|----------------------|
| `footprints_add --url <url> --title <title> --description <desc> --category-ids <ids> --tags <tags>` | "Save/bookmark/collect this link" |
| `footprints_get <id>` | "Show me details of that bookmark" |
| `footprints_search <query>` | "Find that article about Docker" |
| `footprints_list [--category-id <id>] [--limit <n>]` | "Show me my bookmarks" |

### Organize

| Command | Use when user says... |
|---------|----------------------|
| `footprints_update <id> --title <t> --description <d> --category-ids <ids> --tags <tags>` | "Change the title / move to another category" |
| `footprints_batch_update <updates>` | "Reorganize all my bookmarks" (max 50) |
| `footprints_categories` | Discover available categories |
| `footprints_create_category <name> [--category-set-id <id>]` | "Create a new category" |
| `footprints_tags` | Discover existing tags |
| `footprints_category_sets` | List category sets |
| `footprints_create_category_set <name>` | "Create a workspace" |

### Share

| Command | Use when user says... |
|---------|----------------------|
| `footprints_create_shared_category <name> --mode cocreate\|subscribe --description <desc>` | "Create a shared collection" |
| `footprints_create_invite_link <sc_id> [--duration-hours 24]` | "Send invite link to my team" |
| `footprints_join_shared_category <invite_code>` | "I have an invite code" |
| `footprints_add_to_shared <sc_id> <collection_id>` | "Add this to team collection" |
| `footprints_remove_from_shared <sc_id> <collection_id>` | "Remove this from shared" |
| `footprints_copy <id> --category-ids <ids>` | "Save that shared bookmark to my own" |

### Deliver

| Command | Use when user says... |
|---------|----------------------|
| `footprints_me` | Confirm identity at session start |
| `agent_magic_link` | Done organizing → generate link → send to user |

## Core Workflows

### New User — Zero Setup

```
1. Token check → auto-register (save to ~/.url-manager-token)
2. footprints_add url="..." → save bookmarks
3. footprints_categories → discover structure
4. footprints_create_category name="..." → create categories
5. footprints_update id category_ids="..." → categorize
6. agent_magic_link → send link: "Done! View here → [link]"
```

### Returning User — Daily Use

```
1. footprints_me → confirm identity
2. footprints_categories + footprints_tags → understand structure
3. footprints_search query → find what's needed
4. footprints_add / footprints_update → operate
```

### Team Sharing

```
1. footprints_create_shared_category name="Team KB" mode=cocreate
2. footprints_create_invite_link sc_id → share code with team
3. Teammates: footprints_join_shared_category code
4. Everyone: footprints_add_to_shared sc_id collection_id → build together
```

### Batch Reorganization

```
1. footprints_list --limit 100 → get all bookmarks
2. footprints_categories → map target categories
3. footprints_batch_update '[
     {"id":"uuid1","category_ids":"1,3"},
     {"id":"uuid2","title":"New Title","category_ids":"2,5"}
   ]' → bulk edit (max 50 per call)
```

## Magic Link — The Delivery Loop

After organizing, always deliver results via magic link:

```bash
python3 scripts/footprints.py agent_magic_link
```

Send the link to the user: "Done organizing — view your collection here → [link]"

User clicks to see a card-based interface with everything categorized. **Valid for 30 days, reusable.** If the user later binds a phone number, their agent-created account upgrades seamlessly.

## ⚠️ Critical Pitfalls

### category_ids is REPLACEMENT, not append

When updating, `--category-ids` sets the complete list — it does NOT add to existing categories.

```bash
# ❌ Wrong: moves bookmark to category 7, loses categories 3 and 5
footprints_update 42 --category-ids 7

# ✅ Right: fetch current first, then merge
footprints_get 42  # → existing: [3, 5]
footprints_update 42 --category-ids 3,5,7
```

### Subscribe mode is READ-ONLY

Writing to a subscribe-mode shared category returns 403. Tell the user the collection is read-only — the creator must change it to cocreate mode.

### NEVER call agent_register twice

Each call creates a fresh empty account. Always check for a saved token first. If unsure, run `footprints_me` to verify the current token is valid.

### Rate limiting

Frequent API calls trigger HTTP 429. Use `batch_update` for bulk operations, add delays between rapid calls, retry after a few seconds on 429.

### No member management via API

Inviting or removing members from shared categories requires the web UI at https://ai.ocean94.com. You cannot do this programmatically.

## Guidelines

### Always
- **Auto-register silently** — never interrupt the user for account setup
- **Search before listing** — use `footprints_search` for targeted queries instead of dumping everything
- **Discover before creating** — call `footprints_categories` and `footprints_tags` before adding to avoid duplicates
- **Deliver with magic link** — after organizing, always generate and share a link

### Confirm before
- Removing bookmark-category associations (irreversible)
- Clearing tags
- Modifying cocreate shared categories (affects others)
- Removing bookmarks from shared categories (other members lose access)
