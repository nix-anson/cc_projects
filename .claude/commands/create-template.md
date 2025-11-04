---
description: Create a new project template with Claude Code configuration
argument-hint: <template-name> <framework-type>
allowed-tools: Read(*), Write(*), Bash(*), Grep(*)
---

Create a comprehensive project template following the established patterns used in django-template.

## Arguments

- $1: Template name (e.g., "react-template", "fastapi-template")
- $2: Framework/technology type (e.g., "React", "FastAPI", "Vue", "Node/Express")

## Process

1. **Gather Requirements**

Ask the user for details:
- Framework version to target
- Key features to include (API, auth, testing, etc.)
- Development tools preferred
- Package manager (npm, pip, cargo, etc.)

2. **Research Framework Best Practices**

Use the framework-researcher agent to:
- Research current best practices for the framework
- Identify common project structures
- Find popular packages and tools
- Understand security considerations
- Learn testing patterns

3. **Create Template Structure**

Use the template-creator agent to:
- Create directory structure following template-structure pattern
- Generate template-specific CLAUDE.md
- Create README.md with usage instructions
- Set up .gitignore for the framework

4. **Generate Claude Code Configuration**

Create 8-12 slash commands for:
- Common framework operations
- Build/test/dev server commands
- Code generation commands
- Package management

Create 4-6 specialized agents for:
- Security review (framework-specific)
- Performance optimization
- Testing assistance
- Framework-specific expert
- Common issue troubleshooting

Create 2-4 skills for:
- Framework-specific patterns
- Code generation
- Configuration best practices

5. **Create Framework Files**

Generate:
- Package/dependency file (package.json, requirements.txt, etc.)
- Environment variable template (.env.example)
- Configuration files (tsconfig.json, pytest.ini, etc.)
- Setup instructions (setup_instructions.md)

6. **Validate Template**

Use template-validator agent to ensure:
- All required files present
- Claude Code configuration valid
- Documentation complete
- Structure follows standards

7. **Update Repository**

- Add template to main README.md
- Update CLAUDE.md if needed
- Create pull request (if applicable)

## Example Usage

```
/create-template react-template React
```

This will interactively guide you through creating a comprehensive React project template.

## Notes

- Reference claude_code_best_practices memory for Claude Code configuration
- Follow the structure established in django-template
- Ensure comprehensive documentation
- Test all commands and agents work correctly
