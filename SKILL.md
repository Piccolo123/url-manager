---
name: url-manager
description: Cross-platform URL collection & knowledge management with agent-first auto-registration. Use when users say "save/bookmark/collect/remember this", need to organize links into categories, share curated collections, or build a structured knowledge base from web resources. Supports collaborative shared categories, full-text search, and magic-link delivery to users.
license: MIT
compatibility: Requires Python 3.10+ and network access to https://ai.ocean94.com
metadata:
  author: Piccolo123
  version: "2.2.0"
  openclaw:
    emoji: "🔗"
    minGatewayVersion: "2026.6.0"
    requires:
      bins: ["python3"]
      network: true
---

# URL Manager — Deliver beautiful card-based collections, not raw links

When users ask you to save, organize, or share web resources, don't paste URLs into chat. Write them into URL Manager — they become structured, searchable, card-based collections the user opens with one click.

**Zero setup — token auto-management.** The `footprints.py` script handles everything: reads `{baseDir}/.token`, auto-registers on first use, stores token locally with `chmod 600`. Just run any command and it works.

All commands via `python3 {baseDir}/scripts/footprints.py <subcommand> [--json]`. Add `--json` for machine-parseable output.

If the script is missing (e.g., you only have this document but not the full skill installation), get it from the source repo:

```bash
git clone --depth 1 https://github.com/Piccolo123/url-manager.git /tmp/um
mkdir -p {baseDir}/scripts
cp /tmp/um/scripts/footprints.py {baseDir}/scripts/
chmod +x {baseDir}/scripts/footprints.py
rm -rf /tmp/um
```

After that, all commands below work as normal. The script auto-registers on first run.

## Quick Reference

### When user says... → Run this

| User says | Command |
|-----------|---------|
| "Save/bookmark/collect this link" | `python3 {baseDir}/scripts/footprints.py add <url> --title <text> [--category-ids <ids>] [--json]` |
| "Find that article about X" | `python3 {baseDir}/scripts/footprints.py search <query> [--limit <n>] [--json]` |
| "Show me my bookmarks" | `python3 {baseDir}/scripts/footprints.py list [--category-id <id>] [--limit <n>] [--json]` |
| "Show me details" | `python3 {baseDir}/scripts/footprints.py get <id> [--json]` |
| "Change title/move to category" | `python3 {baseDir}/scripts/footprints.py update <id> --title <t> --category-ids <ids> [--json]` |
| "Reorganize all bookmarks" | `python3 {baseDir}/scripts/footprints.py batch-update '<json>' [--json]` |
| "Create a new category" | `python3 {baseDir}/scripts/footprints.py create-category <name> [--json]` |
| "Create a workspace" | `python3 {baseDir}/scripts/footprints.py create-category-set <name> [--json]` |
| "Create a shared collection" | `python3 {baseDir}/scripts/footprints.py create-shared-category <name> --mode cocreate [--json]` |
| "Send invite link" | `python3 {baseDir}/scripts/footprints.py create-invite-link <sc_id> [--json]` |
| "I have an invite code" | `python3 {baseDir}/scripts/footprints.py join-shared-category <code> [--json]` |
| "Add to team collection" | `python3 {baseDir}/scripts/footprints.py add-to-shared <sc_id> --collection-id <id> [--json]` |
| "Save shared to my own" | `python3 {baseDir}/scripts/footprints.py copy <id> --category-ids <ids> [--json]` |
| Check identity | `python3 {baseDir}/scripts/footprints.py me [--json]` |
| Done organizing → deliver to user | `python3 {baseDir}/scripts/footprints.py agent_magic_link [--json]` |
| Re-authenticate (new token) | `python3 {baseDir}/scripts/footprints.py agent_register [--json]` |

## Full Command Reference

### Save & Search

| Command | Use when user says... |
|---------|----------------------|
| `python3 {baseDir}/scripts/footprints.py add <url> --title <title> --description <desc> --category-ids <ids> --tags <tags>` | "Save/bookmark/collect this link" |
| `python3 {baseDir}/scripts/footprints.py get <id>` | "Show me details of that bookmark" |
| `python3 {baseDir}/scripts/footprints.py search <query>` | "Find that article about Docker" |
| `python3 {baseDir}/scripts/footprints.py list [--category-id <id>] [--limit <n>]` | "Show me my bookmarks" |

### Organize

| Command | Use when user says... |
|---------|----------------------|
| `python3 {baseDir}/scripts/footprints.py update <id> --title <t> --description <d> --category-ids <ids> --tags <tags>` | "Change the title / move to another category" |
| `python3 {baseDir}/scripts/footprints.py batch-update <updates>` | "Reorganize all my bookmarks" (max 50) |
| `python3 {baseDir}/scripts/footprints.py categories` | Discover available categories |
| `python3 {baseDir}/scripts/footprints.py create-category <name> [--category-set-id <id>]` | "Create a new category" |
| `python3 {baseDir}/scripts/footprints.py tags` | Discover existing tags |
| `python3 {baseDir}/scripts/footprints.py category-sets` | List category sets |
| `python3 {baseDir}/scripts/footprints.py create-category-set <name>` | "Create a workspace" |

### Share

| Command | Use when user says... |
|---------|----------------------|
| `python3 {baseDir}/scripts/footprints.py create-shared-category <name> --mode cocreate\|subscribe --description <desc>` | "Create a shared collection" |
| `python3 {baseDir}/scripts/footprints.py create-invite-link <sc_id> [--duration-hours 24]` | "Send invite link to my team" |
| `python3 {baseDir}/scripts/footprints.py join-shared-category <invite_code>` | "I have an invite code" |
| `python3 {baseDir}/scripts/footprints.py add-to-shared <sc_id> --collection-id <id>` | "Add this to team collection" |
| `python3 {baseDir}/scripts/footprints.py remove-from-shared <sc_id> --collection-id <id>` | "Remove this from shared" |
| `python3 {baseDir}/scripts/footprints.py copy <id> --category-ids <ids>` | "Save that shared bookmark to my own" |

### Deliver

| Command | Use when user says... |
|---------|----------------------|
| `python3 {baseDir}/scripts/footprints.py me` | Confirm identity at session start |
| `python3 {baseDir}/scripts/footprints.py agent_magic_link` | Done organizing → generate link → send to user |

## Core Workflows

### New User — Zero Setup

```
1. Token check → auto-register (save to {baseDir}/.token)
2. python3 {baseDir}/scripts/footprints.py add url="..." → save bookmarks
3. python3 {baseDir}/scripts/footprints.py categories → discover structure
4. python3 {baseDir}/scripts/footprints.py create-category name="..." → create categories
5. python3 {baseDir}/scripts/footprints.py update id category_ids="..." → categorize
6. agent_magic_link → send link: "Done! View here → [link]"
```

### Returning User — Daily Use

```
1. python3 {baseDir}/scripts/footprints.py me → confirm identity
2. python3 {baseDir}/scripts/footprints.py categories + python3 {baseDir}/scripts/footprints.py tags → understand structure
3. python3 {baseDir}/scripts/footprints.py search query → find what's needed
4. python3 {baseDir}/scripts/footprints.py add / python3 {baseDir}/scripts/footprints.py update → operate
```

### Team Sharing

```
1. python3 {baseDir}/scripts/footprints.py create-shared-category name="Team KB" mode=cocreate
2. python3 {baseDir}/scripts/footprints.py create-invite-link sc_id → share code with team
3. Teammates: python3 {baseDir}/scripts/footprints.py join-shared-category code
4. Everyone: python3 {baseDir}/scripts/footprints.py add-to-shared sc_id --collection-id collection_id → build together
```

### Batch Reorganization

```
1. python3 {baseDir}/scripts/footprints.py list --limit 100 → get all bookmarks
2. python3 {baseDir}/scripts/footprints.py categories → map target categories
3. python3 {baseDir}/scripts/footprints.py batch-update '[
     {"id":"uuid1","category_ids":"1,3"},
     {"id":"uuid2","title":"New Title","category_ids":"2,5"}
   ]' → bulk edit (max 50 per call)
```

## Recipes

Concrete bash patterns for common tasks. Follow the numbered steps.

### Change a footprint's categories

```bash
python3 {baseDir}/scripts/footprints.py get 42
# → categories: [{id: 3, name: "Reading"}, {id: 5, name: "AI"}]

# Keep AI, drop Reading, add Tech (7)
python3 {baseDir}/scripts/footprints.py update 42 --category-ids 5,7
```

### Batch move to a new category

```bash
python3 {baseDir}/scripts/footprints.py create-category "New Topic"    # → returns new ID
python3 {baseDir}/scripts/footprints.py list --limit 100
# For each matching footprint:
python3 {baseDir}/scripts/footprints.py update <id> --category-ids <existing_ids>,<new_id>
```

### Merge two categories

```bash
python3 {baseDir}/scripts/footprints.py categories                      # note source and target IDs
python3 {baseDir}/scripts/footprints.py list --category-id <source_id>  # list all in source
# For each, replace source_id with target_id:
python3 {baseDir}/scripts/footprints.py update <id> --category-ids <target_id>,<other_ids>
# Tell user: empty category "source" is ready to delete via the web UI
```

### Auto-categorize by domain

User says "put all github.com links into a GitHub category":

```bash
python3 {baseDir}/scripts/footprints.py list --limit 200
# Filter in-memory: items where url contains "github.com"
python3 {baseDir}/scripts/footprints.py create-category "GitHub"
# For each match:
python3 {baseDir}/scripts/footprints.py update <id> --category-ids <existing_ids>,<github_id>
```

### Filter by tag and batch categorize

```bash
python3 {baseDir}/scripts/footprints.py search docker
# Filter results where tag_names includes "docker"
# For each, append target category:
python3 {baseDir}/scripts/footprints.py update <id> --category-ids <existing_ids>,<target_id>
```

### Organize uncategorized footprints

```bash
python3 {baseDir}/scripts/footprints.py list --limit 100
# Filter where category_ids is empty or only the default
# Present to user, let them pick categories
# Batch update selected items
```

### Recommend categories from tags

Spot gaps between tags and categories — e.g., #docker is common but no "Docker" category:

```bash
python3 {baseDir}/scripts/footprints.py tags        # most-used tags
python3 {baseDir}/scripts/footprints.py categories  # existing categories
# Cross-reference: tag without matching category → suggest creating one
```

### Copy from shared to personal

```bash
python3 {baseDir}/scripts/footprints.py categories  # find target personal category ID
python3 {baseDir}/scripts/footprints.py copy <footprint_id> --category-ids <personal_category_id>
```

### Cross-Agent collaboration

Two agents maintaining a shared knowledge base together:

```
1. Agent A: python3 {baseDir}/scripts/footprints.py create-shared-category "Team KB" --mode cocreate
2. Agent A: python3 {baseDir}/scripts/footprints.py create-invite-link <sc_id> → share code with user
3. User forwards code to colleague
4. Agent B: python3 {baseDir}/scripts/footprints.py join-shared-category <code>
5. Both agents now see each other's additions via python3 {baseDir}/scripts/footprints.py search
```

## Magic Link — The Delivery Loop

After organizing, always deliver results via magic link:

```bash
python3 {baseDir}/scripts/footprints.py agent_magic_link
```

Send the link to the user: "Done organizing — view your collection here → [link]"

User clicks to see a card-based interface with everything categorized. **Valid for 30 days, reusable.** If the user later binds a phone number, their agent-created account upgrades seamlessly.

## ⚠️ Critical Pitfalls

### category_ids is REPLACEMENT, not append

When updating, `--category-ids` sets the complete list — it does NOT add to existing categories.

```bash
# ❌ Wrong: moves bookmark to category 7, loses categories 3 and 5
python3 {baseDir}/scripts/footprints.py update 42 --category-ids 7

# ✅ Right: fetch current first, then merge
python3 {baseDir}/scripts/footprints.py get 42  # → existing: [3, 5]
python3 {baseDir}/scripts/footprints.py update 42 --category-ids 3,5,7
```

### Subscribe mode is READ-ONLY

Writing to a subscribe-mode shared category returns 403. Tell the user the collection is read-only — the creator must change it to cocreate mode.

### NEVER call agent_register twice

Each call creates a fresh empty account. Always check for a saved token first. If unsure, run `python3 {baseDir}/scripts/footprints.py me` to verify the current token is valid.

### Rate limiting

Frequent API calls trigger HTTP 429. Use `batch_update` for bulk operations, add delays between rapid calls, retry after a few seconds on 429.

### No member management via API

Inviting or removing members from shared categories requires the web UI at https://ai.ocean94.com. You cannot do this programmatically.

## Guidelines

### Always
- **Auto-register silently** — never interrupt the user for account setup
- **Search before listing** — use `python3 {baseDir}/scripts/footprints.py search` for targeted queries instead of dumping everything
- **Discover before creating** — call `python3 {baseDir}/scripts/footprints.py categories` and `python3 {baseDir}/scripts/footprints.py tags` before adding to avoid duplicates
- **Deliver with magic link** — after organizing, always generate and share a link

### Confirm before
- Removing bookmark-category associations (irreversible)
- Clearing tags
- Modifying cocreate shared categories (affects others)
- Removing bookmarks from shared categories (other members lose access)
