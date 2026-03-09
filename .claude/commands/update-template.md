---
description: Update an existing template with latest best practices and framework changes
argument-hint: <template-name>
allowed-tools: Read(*), Write(*), Bash(*), Glob(*), Grep(*), WebSearch(*), WebFetch(*)
model: claude-sonnet-4-6
---

Update an existing project template to reflect the latest framework changes and Claude Code best practices.

## Arguments

- $1: Template directory name (e.g., "django-template", "flask-template")

## Process

### Step 1: Audit Current Template

Use the `template-validator` agent to assess the current state:
- Report current command/agent/skill counts
- Identify missing required files
- Flag outdated configurations

### Step 2: Research Latest Framework Changes

Use the `framework-researcher` agent to check for:
- New framework versions and breaking changes
- Updated recommended packages
- New security advisories
- Community best practice shifts

### Step 3: Update Model References

Update `model:` fields in all frontmatter to `claude-sonnet-4-6`:
- `.claude/settings.json`
- All command files in `.claude/commands/`
- All agent files in `.claude/agents/`

### Step 4: Fill Gaps

Based on the audit, add missing:
- Commands (target: 8-12)
- Agents (target: 4-6)
- Skills (target: 2-4)

### Step 5: Update Dependencies

Review and update:
- `requirements.txt` or `package.json` — bump versions as appropriate
- `.env.example` — add any new environment variables
- `.gitignore` — add new patterns if needed

### Step 6: Re-validate

Run a final validation with the `template-validator` agent and confirm the score improved.

## Example Usage

```
/update-template django-template
/update-template flask-template
/update-template react-template
```
