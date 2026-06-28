# Hermes Skills

Custom skills for [Hermes Agent](https://hermes-agent.nousresearch.com/) — curated workflows, tools, and automations built and battle-tested in production.

## What's a Skill?

A skill is a reusable workflow document (SKILL.md) that teaches Hermes how to handle specific tasks. Each skill includes step-by-step instructions, common pitfalls, and proven commands.

## Structure

```
hermes-skills/
├── README.md
├── devops/          # Infrastructure, deployment, server management
├── productivity/    # Feishu, Notion, Google Workspace integrations
├── frontend/        # H5, uni-app, map integrations
├── kanban/          # Multi-agent Kanban collaboration model
└── workflows/       # Project-specific workflows (e.g., ai-favorites)
```

Each skill lives in its own directory with a `SKILL.md` file.

## Usage

Copy the skill directory into your Hermes skills folder:

```bash
cp -r hermes-skills/<category>/<skill-name> ~/.hermes/skills/<category>/
```

Or symlink for auto-updates:

```bash
ln -s $(pwd)/hermes-skills/<category>/<skill-name> ~/.hermes/skills/<category>/<skill-name>
```

Then restart your gateway or start a new session.

## Contributing

These skills are battle-tested in real workflows. PRs welcome for improvements, bug fixes, and new skills.

## License

MIT
