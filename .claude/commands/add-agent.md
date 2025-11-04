---
description: Add a specialized subagent to an existing template
argument-hint: <template-name> <agent-name>
allowed-tools: Read(*), Write(*), Grep(*)
---

Add a new specialized subagent to an existing project template.

## Arguments

- $1: Template directory name (e.g., "django-template", "react-template")
- $2: Agent name in lowercase-with-hyphens (e.g., "security-auditor", "performance-optimizer")

## Process

1. **Verify Template Exists**

Check that `$1/.claude/agents/` directory exists.

2. **Gather Agent Details**

Ask the user:
- What is the agent's specialty/expertise?
- When should it activate? (triggers/keywords)
- What tasks should it handle?
- What tools does it need access to?
- Should it activate proactively or only when invoked?
- What model should it use?

3. **Research Agent Domain**

If creating a specialist agent (e.g., security, performance):
- Research best practices in that domain for the framework
- Identify common issues and solutions
- Find patterns and anti-patterns
- Gather examples

4. **Create Agent File**

Generate `$1/.claude/agents/$2.md` with proper structure, detailed system prompt, framework-specific examples, and clear activation criteria.

5. **Update Documentation**

Add the agent to `$1/README.md` in the subagents section with activation triggers and example invocation.

## Example Usage

```
/add-agent react-template accessibility-checker
```

Then answer prompts about the agent's purpose and capabilities.

## Best Practices for Agents

- **Single responsibility**: Each agent should have one clear purpose
- **Detailed instructions**: Include step-by-step processes
- **Code examples**: Show framework-specific patterns
- **Clear triggers**: Use PROACTIVELY and MUST BE USED keywords
- **Tool restrictions**: Only grant necessary tools
- **Framework-specific**: Tailor to the template's technology
