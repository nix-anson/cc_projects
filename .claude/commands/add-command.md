---
description: Add a slash command to an existing template
argument-hint: <template-name> <command-name>
allowed-tools: Read(*), Write(*), Grep(*)
---

Add a new slash command to an existing project template.

## Arguments

- $1: Template directory name (e.g., "django-template", "react-template")
- $2: Command name (without slash, e.g., "build", "deploy")

## Process

1. **Verify Template Exists**

Check that `$1/.claude/commands/` directory exists.

2. **Gather Command Details**

Ask the user:
- What should this command do?
- What arguments should it accept?
- What tools does it need? (Bash, Read, Write, etc.)
- Should it be restricted in any way?
- What model should it use? (sonnet, opus, haiku)

3. **Create Command File**

Generate `$1/.claude/commands/$2.md` with:
- Proper YAML frontmatter (description, argument-hint, allowed-tools, model)
- Clear instructions for what the command does
- Parameter handling ($ARGUMENTS, $1, $2, etc.)
- Common usage patterns
- Error handling guidance
- Related commands or workflows

4. **Update Documentation**

Add the new command to:
- `$1/README.md` in the commands table
- `$1/setup_instructions.md` if relevant

5. **Validation**

Check that:
- YAML frontmatter is valid
- Description is clear and concise
- Arguments are documented
- File follows naming convention

## Example Usage

```
/add-command django-template deploy
```

Then answer prompts about what the deploy command should do.

## Best Practices

- Keep commands focused on single tasks
- Provide clear examples
- Document expected arguments
- Include error handling guidance
- Reference related commands
- Use appropriate tool restrictions
