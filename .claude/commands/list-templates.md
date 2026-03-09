---
description: List all available project templates with their commands, agents, and skills
allowed-tools: Read(*), Glob(*), Bash(*)
---

List all project templates in this repository with a summary of their Claude Code configuration.

## Process

1. **Find all templates** by looking for directories containing `CLAUDE.md` and `.claude/settings.json`

2. **For each template**, report:
   - Template name
   - Framework and purpose (from README.md first line or CLAUDE.md)
   - Number of slash commands
   - Number of agents
   - Number of skills
   - Completeness rating

3. **Display as a formatted table**:

```
Repository Templates
====================

Template            Framework    Commands  Agents  Skills  Status
------------------  -----------  --------  ------  ------  --------
django-template     Django       10        5       3       Complete
flask-template      Flask        11        6       4       Complete
react-template      React/Vite   8         5       2       Complete
...
```

4. **Show gaps** — list any planned templates (from main README.md) that don't exist yet

5. **Validate counts** — flag any template that falls below recommended minimums:
   - Commands: < 8 = warning
   - Agents: < 4 = warning
   - Skills: < 2 = warning

## Example Usage

```
/list-templates
```
