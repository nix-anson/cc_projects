---
description: Validate a template follows proper structure and standards
argument-hint: <template-name>
allowed-tools: Read(*), Grep(*), Bash(*)
---

Validate that a project template follows the proper structure and standards established for this repository.

## Arguments

- $1: Template directory name (e.g., "django-template", "react-template")

## Validation Process

Use the template-validator agent to perform comprehensive validation.

The agent will check:

### Required Structure
- Directory structure (.claude/commands/, agents/, skills/)
- Required files (README.md, CLAUDE.md, .gitignore, .env.example, setup_instructions.md)
- Claude Code configuration files

### Commands Validation
- Valid YAML frontmatter
- Has description field
- Clear instructions
- Minimum 8-10 commands

### Agents Validation
- Valid frontmatter with name, description, tools
- Activation keywords (PROACTIVELY, MUST BE USED)
- Framework-specific examples
- Minimum 4-6 agents

### Skills Validation
- Proper directory structure
- Valid SKILL.md with triggers
- Complete instructions
- Minimum 2-4 skills

### Documentation Validation
- Comprehensive README.md
- Complete CLAUDE.md with framework conventions
- Detailed setup_instructions.md

### Configuration Validation
- Valid .claude/settings.json
- Appropriate .gitignore
- Complete .env.example

## Example Usage

```
/validate-template django-template
```

## Success Criteria

A valid template should:
- Be comprehensive (8-10 commands, 4-6 agents, 2-4 skills)
- Be well-documented
- Follow established patterns
- Be immediately usable
