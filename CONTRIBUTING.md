# Contributing to Claude Code Project Templates

Thank you for your interest in contributing! This guide will help you add new templates or improve existing ones.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Creating a New Template](#creating-a-new-template)
3. [Template Standards](#template-standards)
4. [Using Template Creation Tools](#using-template-creation-tools)
5. [Validation and Testing](#validation-and-testing)
6. [Submission Process](#submission-process)
7. [Style Guidelines](#style-guidelines)

## Getting Started

### Prerequisites

- VSCode with Claude Code extension installed
- Git for version control
- Knowledge of the framework you're creating a template for
- Familiarity with Claude Code features (commands, agents, skills)

### Understanding the Repository

This repository contains:
- **Root level**: Repository documentation and metadata
- **Template directories**: Individual project templates (e.g., `django-template/`)
- **.claude/**: Root-level Claude Code configuration for template creation
- **Memories**: Saved knowledge about Claude Code best practices

### Review Existing Templates

Before creating a new template, review existing ones (especially `django-template/`) to understand:
- Directory structure
- Documentation style
- Command organization
- Agent specializations
- Skill patterns

## Creating a New Template

### Method 1: Using Claude Code Commands (Recommended)

This repository includes commands to help create templates:

```bash
# Open this repository in VSCode with Claude Code

# Create a new template
/create-template react-template React

# Follow the interactive prompts
```

The `/create-template` command will:
1. Research framework best practices
2. Create directory structure
3. Generate commands, agents, and skills
4. Create documentation
5. Validate the template

### Method 2: Manual Creation

If creating manually, follow these steps:

#### Step 1: Research

Use the `framework-researcher` agent:
```
"Research best practices for [Framework] to create a project template"
```

Gather information about:
- Current framework version
- Project structure conventions
- Popular packages and tools
- Security considerations
- Testing patterns
- Build and deployment workflows

#### Step 2: Create Structure

```bash
# Create template directory
mkdir framework-template

# Create Claude Code configuration
mkdir -p framework-template/.claude/commands
mkdir -p framework-template/.claude/agents
mkdir -p framework-template/.claude/skills

# Create root files
touch framework-template/README.md
touch framework-template/CLAUDE.md
touch framework-template/setup_instructions.md
touch framework-template/.gitignore
touch framework-template/.env.example
touch framework-template/.claude/settings.json
```

#### Step 3: Generate Commands

Create 8-12 slash commands in `.claude/commands/`:

**Essential commands**:
- Build/compile
- Test
- Development server
- Lint/format

**Development commands**:
- Create component/module
- Install dependencies
- Clean environment

**Example**: Create `.claude/commands/build.md`:
```markdown
---
description: Build the project for production
argument-hint: [--watch] [--clean]
allowed-tools: Bash(*), Read(*)
---

Build the project with optimization for production deployment.

Arguments:
- $ARGUMENTS: All build flags

Execute: `npm run build $ARGUMENTS` or equivalent

...
```

Use `/add-command` for assistance:
```
/add-command framework-template build
```

#### Step 4: Create Agents

Create 4-6 specialized agents in `.claude/agents/`:

**Required agents**:
1. Security agent (framework-specific vulnerabilities)
2. Performance agent (optimization)
3. Testing agent (test generation)
4. Framework expert (deep knowledge)

**Example**: Create `.claude/agents/framework-security.md`:
```markdown
---
name: framework-security
description: PROACTIVELY review [Framework] code for security vulnerabilities...
tools: Read, Grep, Bash
model: sonnet
---

You are a [Framework] security expert...

...
```

Use `/add-agent` for assistance:
```
/add-agent framework-template security-auditor
```

#### Step 5: Develop Skills

Create 2-4 skills in `.claude/skills/`:

**Common skills**:
1. Pattern implementation
2. Code generation
3. Validation

**Example**: Create `.claude/skills/component-generator/SKILL.md`:
```markdown
---
name: component-generator
description: Generate [Framework] components... Use when creating .ext files...
allowed-tools: Read, Write
---

You are a [Framework] component generation expert...

...
```

Use `/add-skill` for assistance:
```
/add-skill framework-template component-generator
```

#### Step 6: Write Documentation

**README.md** should include:
- Template overview
- What's included
- Quick start
- Commands table
- Agents with triggers
- Skills description
- Development workflow
- Troubleshooting
- Resources

**CLAUDE.md** should include:
- Framework overview
- Version information
- Project structure
- Common commands
- Code conventions
- Best practices
- Security considerations
- Testing strategy
- Official documentation links

**setup_instructions.md** should include:
- Prerequisites
- Step-by-step setup
- Environment configuration
- First component creation
- Running tests
- Production deployment
- Common issues

#### Step 7: Create Framework Files

Generate framework-specific files:
- Dependency file (package.json, requirements.txt, Cargo.toml, etc.)
- Configuration files (tsconfig.json, pytest.ini, etc.)
- .gitignore (framework-appropriate)
- .env.example (all environment variables)
- .claude/settings.json (Claude Code settings)

#### Step 8: Validate

Use the validation command:
```
/validate-template framework-template
```

Fix any issues reported by the validator.

## Template Standards

### Required Structure

```
template-name/
├── .claude/
│   ├── commands/         # 8-12 commands minimum
│   ├── agents/           # 4-6 agents minimum
│   ├── skills/           # 2-4 skills minimum
│   └── settings.json
├── README.md
├── CLAUDE.md
├── setup_instructions.md
├── .gitignore
├── .env.example
└── [framework files]
```

### Quality Criteria

**Commands**:
- ✅ Valid YAML frontmatter with `description`
- ✅ Clear instructions
- ✅ Usage examples
- ✅ Lowercase-with-hyphens filenames
- ✅ 8-12 commands minimum

**Agents**:
- ✅ Valid YAML with `name` and `description`
- ✅ Activation keywords (PROACTIVELY, MUST BE USED)
- ✅ Framework-specific examples
- ✅ Clear triggers
- ✅ 4-6 agents minimum

**Skills**:
- ✅ Directory structure with SKILL.md
- ✅ Description includes triggers and file extensions
- ✅ Complete code examples
- ✅ 2-4 skills minimum

**Documentation**:
- ✅ Comprehensive README.md
- ✅ Framework-specific CLAUDE.md
- ✅ Detailed setup_instructions.md
- ✅ No broken links
- ✅ Clear examples

**Configuration**:
- ✅ Valid .claude/settings.json
- ✅ Complete .env.example
- ✅ Appropriate .gitignore
- ✅ Framework dependency file

### Naming Conventions

- **Files**: lowercase-with-hyphens.md
- **Agents**: descriptive-specialty.md (e.g., `react-security.md`)
- **Commands**: verb-noun.md (e.g., `create-component.md`)
- **Skills**: capability-description (e.g., `component-generator/`)
- **Templates**: framework-template (e.g., `react-template/`)

## Using Template Creation Tools

This repository includes specialized tools to help:

### Commands

- `/create-template <name> <framework>` - Create complete template
- `/add-command <template> <command>` - Add slash command
- `/add-agent <template> <agent>` - Add subagent
- `/add-skill <template> <skill>` - Add skill
- `/validate-template <template>` - Validate structure

### Agents

- **framework-researcher**: Research framework best practices
- **template-creator**: Create template structure and files
- **template-validator**: Validate against standards

### Skills

- **template-structure**: Implement proper directory structure
- **claude-config-generator**: Generate configuration files

### Example Workflow

```bash
# 1. Create template interactively
/create-template fastapi-template FastAPI

# 2. Add additional command if needed
/add-command fastapi-template create-endpoint

# 3. Validate
/validate-template fastapi-template

# 4. Fix any issues, then validate again
/validate-template fastapi-template
```

## Validation and Testing

### Automated Validation

Run validation:
```
/validate-template your-template
```

This checks:
- Directory structure
- Required files present
- Command configuration validity
- Agent configuration validity
- Skill configuration validity
- Documentation completeness
- Configuration validity

### Manual Testing

1. **Quick Start Test**:
   - Follow your own setup_instructions.md
   - Ensure all steps work
   - Verify project runs successfully

2. **Commands Test**:
   - Try each slash command
   - Verify they execute correctly
   - Check error handling

3. **Agents Test**:
   - Trigger each agent
   - Verify they activate appropriately
   - Check output quality

4. **Skills Test**:
   - Create scenarios that should trigger skills
   - Verify auto-activation works
   - Check generated code quality

5. **Documentation Test**:
   - Read through all documentation
   - Click all links
   - Verify examples work
   - Check for typos

## Submission Process

### 1. Validate Your Template

```bash
/validate-template your-template
```

Ensure validation passes with a score of 80+.

### 2. Update Repository Documentation

Add your template to the main `README.md`:

```markdown
### Your Framework Template
**Location**: `your-template/`

Description of what it includes...

**Best For**: [use cases]
```

### 3. Create Commit

```bash
git add your-template/
git add README.md
git commit -m "Add [Framework] template with [key features]"
```

### 4. Submit Pull Request

- Fork the repository
- Push your changes
- Create pull request with:
  - Clear description
  - Validation results
  - Test results
  - Screenshots (if applicable)

### 5. Address Review Feedback

- Respond to reviewer comments
- Make requested changes
- Re-validate after changes

## Style Guidelines

### Code Style

**Python**:
- PEP 8 compliance
- Black formatting (88 char line length)
- Type hints where appropriate

**JavaScript/TypeScript**:
- Prettier formatting
- ESLint compliance
- TypeScript for new code

**Markdown**:
- One sentence per line (for easy diffs)
- Use ATX-style headers (`#` not underlines)
- Include blank lines around code blocks

### Documentation Style

**Tone**:
- Clear and concise
- Professional but friendly
- Actionable and specific

**Structure**:
- Use headings liberally
- Include table of contents for long docs
- Provide examples for all concepts
- Add troubleshooting sections

**Code Examples**:
- Complete, runnable examples
- Include comments explaining key points
- Show both good and bad patterns
- Use realistic scenarios

### Commit Messages

Format:
```
<type>: <short summary>

<detailed description if needed>
```

Types:
- `feat`: New template or major feature
- `fix`: Bug fix or correction
- `docs`: Documentation updates
- `style`: Formatting changes
- `refactor`: Code restructuring
- `test`: Testing additions
- `chore`: Maintenance tasks

Examples:
```
feat: Add React template with TypeScript support

Includes 10 commands, 5 agents, 3 skills.
Comprehensive documentation for React 18.
```

```
fix: Correct YAML syntax in django-template migrate command

Missing closing quote in description field.
```

## Questions and Support

- **Issues**: Open a GitHub issue for bugs or questions
- **Discussions**: Use GitHub Discussions for general questions
- **Claude Code Docs**: https://docs.claude.com/en/docs/claude-code

## Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [CLAUDE.md Guide](https://docs.claude.com/en/docs/claude-code/claude-md)
- [Custom Commands](https://docs.claude.com/en/docs/claude-code/custom-commands)
- [Subagents](https://docs.claude.com/en/docs/claude-code/subagents)
- [Skills](https://docs.claude.com/en/docs/claude-code/skills)
- Repository Memory: `.claude/knowledge/claude_code_best_practices`

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to Claude Code Project Templates!
