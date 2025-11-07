# Template Pattern Reference Guide

This document contains comprehensive pattern analysis extracted from the 7 existing templates in this repository.

## Quantitative Patterns

### Template Metrics Summary

| Template | Commands | Agents | Skills | Status | CLAUDE.md Lines |
|----------|----------|--------|--------|--------|-----------------|
| django | 10 | 5 | 3 | ✅ Complete | ~440 |
| react | 12 | 6 | 3 | ✅ Complete | ~850 |
| flask | 11 | 6 | 4 | ✅ Complete | ~550 |
| tkinter | 10 | 5 | 3 | ✅ Complete | ~420 |
| streamlit | 12 | 6 | 4 | ✅ Complete | ~680 |
| scrapy | 10 | 6 | 4 | ✅ Complete | ~710 |
| fastapi | 10 | 0 | 0 | ⚠️ Incomplete | ~180 |

### Average Metrics (Complete Templates Only)

- **Commands**: 10.8 average (range: 10-12)
- **Agents**: 5.7 average (range: 5-6)
- **Skills**: 3.5 average (range: 3-4)
- **CLAUDE.md**: 608 lines average (range: 420-850)

### Template Depth Guidelines

**Minimal Starter** (5-30% of standard):
- Commands: 5-6 essential operations
- Agents: 3 core roles (security, expert, test)
- Skills: 1-2 basic patterns
- CLAUDE.md: ~200-300 lines

**Standard Template** (100% - recommended):
- Commands: 10-12 comprehensive operations
- Agents: 5-6 specialized roles
- Skills: 3-4 pattern libraries
- CLAUDE.md: 400-700 lines

**Comprehensive Setup** (150-200% of standard):
- Commands: 12-15 including CI/CD and monitoring
- Agents: 6-8 with architecture and optimization
- Skills: 4-5 complete pattern libraries
- CLAUDE.md: 700-1000 lines

---

## Command Patterns

### Command Categories and Distribution

#### Category 1: Essential Operations (4-5 commands per template)

**Development Server** - Present in ALL templates
- **Names**: `dev`, `run`, `runserver`, `serve`
- **Purpose**: Start local development environment
- **Arguments**: Typically `[--port PORT]` or `[--host HOST]`
- **Tools**: `Bash(*)`
- **Examples**:
  - Django: `/runserver [port]`
  - React: `/dev`
  - Flask: `/run [--host HOST] [--port PORT]`
  - Streamlit: `/run [page_name]`

**Testing** - Present in ALL templates
- **Names**: `test`, `test-watch`, `coverage`, `test-ui`
- **Purpose**: Execute test suite
- **Arguments**: `[test_path]` or `[--watch]`
- **Tools**: `Bash(*)`
- **Examples**:
  - Django: `/test [app_name]`
  - React: `/test`, `/test-ui`, `/coverage`
  - Flask: `/test [test_pattern]`

**Linting** - Present in ALL templates
- **Names**: `lint`, `lint-fix`, `check`
- **Purpose**: Check code quality
- **Arguments**: `[--fix]` for auto-fix
- **Tools**: `Bash(*)`
- **Examples**:
  - Django: `black`, `flake8`
  - React: `eslint`
  - Flask: `ruff check`

**Formatting** - Present in ALL templates
- **Names**: `format`, `fmt`
- **Purpose**: Auto-format code
- **Arguments**: Rarely needs arguments
- **Tools**: `Bash(*)`
- **Examples**:
  - Django: `black`, `isort`
  - React: `prettier`
  - Flask: `ruff format`

**Build** - Present in production frameworks (React, Streamlit)
- **Names**: `build`, `compile`, `bundle`
- **Purpose**: Create production build
- **Arguments**: `[--mode production]`
- **Tools**: `Bash(*)`
- **Examples**:
  - React: `/build`
  - Streamlit: `/build`

#### Category 2: Code Generation (3-4 commands per template)

**Create Component/Module** - Framework-specific
- **Names**: `create-component`, `create-model`, `create-blueprint`, `create-app`, `create-page`
- **Purpose**: Generate boilerplate code
- **Arguments**: Name of component + optional type/location
- **Tools**: `Read(*)`, `Write(*)`
- **Examples**:
  - Django: `/create-model <app> <model>`, `/create-app <app>`
  - React: `/create-component <name> [--type TYPE]`
  - Flask: `/create-blueprint <name>`, `/create-model <name>`
  - Streamlit: `/create-page <name>`, `/create-component <name>`

**Create Supporting Files** - Framework-specific
- **Names**: `create-schema`, `create-test`, `create-dialog`, `new-view`
- **Purpose**: Generate related files
- **Arguments**: Name + context
- **Tools**: `Read(*)`, `Write(*)`
- **Examples**:
  - Flask: `/create-schema <name>`
  - Tkinter: `/new-dialog <name>`, `/new-view <name>`

#### Category 3: Database Operations (2-3 commands, if applicable)

**Apply Migrations** - Backend frameworks with ORM
- **Names**: `migrate`, `db-upgrade`
- **Purpose**: Apply database schema changes
- **Arguments**: Optional migration name/version
- **Tools**: `Bash(*)`
- **Examples**:
  - Django: `/migrate [app_name]`
  - Flask: `/db-upgrade`
  - Streamlit: `/db-upgrade`

**Create Migrations** - Backend frameworks with ORM
- **Names**: `makemigrations`, `db-migrate`
- **Purpose**: Generate migration files
- **Arguments**: Optional message/description
- **Tools**: `Bash(*)`
- **Examples**:
  - Django: `/makemigrations [app_name]`
  - Flask: `/db-migrate "<message>"`
  - Streamlit: `/db-migrate "<message>"`

**Database Status** - Backend frameworks
- **Names**: `db-status`, `showmigrations`
- **Purpose**: Check migration status
- **Arguments**: None
- **Tools**: `Bash(*)`
- **Examples**:
  - Django: `/showmigrations`
  - Flask: `/db-status`

#### Category 4: Development Tools (1-2 commands per template)

**Interactive Shell** - Backend frameworks
- **Names**: `shell`, `repl`
- **Purpose**: Open interactive environment
- **Arguments**: None
- **Tools**: `Bash(*)`
- **Examples**:
  - Django: `/shell`
  - Flask: `/shell`
  - Scrapy: `/shell`

**Type Checking** - Typed languages
- **Names**: `type-check`, `typecheck`
- **Purpose**: Run static type checker
- **Arguments**: Optional file/directory
- **Tools**: `Bash(*)`
- **Examples**:
  - React: `/type-check`
  - Tkinter: `/type-check`
  - Streamlit: `/typecheck`

#### Category 5: Deployment/Production (1-2 commands per template)

**Production Build** - See Category 1 (Build)

**Collect Static** - Django-specific
- **Names**: `collectstatic`
- **Purpose**: Gather static files for deployment
- **Arguments**: Optional flags
- **Tools**: `Bash(*)`

**Deployment** - Specialized frameworks
- **Names**: `deploy`, `export-data`
- **Purpose**: Framework-specific deployment
- **Arguments**: Target environment
- **Tools**: `Bash(*)`
- **Examples**:
  - Scrapy: `/deploy`
  - Scrapy: `/export-data <format> [--output PATH]`

#### Category 6: Framework-Specific Operations (1-3 per template)

**React**:
- `/preview` - Preview production build
- `/install` - Install dependencies
- `/create-component` - Generate React component

**Django**:
- `/check` - System check
- `/create-app` - Create Django app

**Flask**:
- `/routes` - Show all API routes

**Scrapy**:
- `/run-spider <name>` - Run specific spider
- `/list-spiders` - List all spiders
- `/validate-items` - Validate scraped items
- `/check-robots` - Check robots.txt compliance
- `/benchmark <spider>` - Performance testing

**Tkinter**:
- `/validate-form <form_name>` - Validate form implementation

**Streamlit**:
- (No unique operations not covered by other categories)

---

## Agent Patterns

### Universal Agent Roles (Required in Every Template)

#### 1. Security Agent

**Pattern**:
```yaml
---
name: {framework}-security
description: PROACTIVELY review {FRAMEWORK} code for security vulnerabilities, OWASP risks, and framework-specific security issues. MUST BE USED when reviewing authentication, permissions, user input handling, or when explicitly requested for security review.
tools: Read, Grep, Bash
model: sonnet
---

You are a {FRAMEWORK} security expert specializing in identifying and preventing security vulnerabilities.

## Your Responsibilities
1. **OWASP Top 10 Prevention**
2. **Framework-Specific Security**
3. **Authentication & Authorization Review**
4. **Input Validation & Sanitization**
5. **Dependency Security**

## Methodology
When reviewing code for security:
1. **Scan for Common Vulnerabilities**
2. **Check Authentication Implementation**
3. **Review Authorization Logic**
4. **Examine Input Handling**
5. **Verify Secret Management**

## Common Vulnerabilities

### [Framework-Specific Vulnerabilities]
**Bad Example**: [vulnerable code]
**Good Example**: [secure code]
**Explanation**: [why and how to fix]

## Best Practices
[Framework-specific security guidance]
```

**Present in**:
- ✅ django-security.md
- ✅ react-security.md
- ✅ flask-security.md
- ✅ tkinter (gui-security.md)
- ✅ streamlit-security-reviewer.md
- ✅ scrapy (security-advisor.md)

#### 2. Framework Expert Agent

**Pattern**:
```yaml
---
name: {framework}-expert
description: Expert in {FRAMEWORK} best practices, design patterns, and framework-specific solutions. PROACTIVELY suggest improvements and provide {FRAMEWORK}-specific guidance when working with {framework-specific features}.
tools: Read, Write, Grep
model: sonnet
---

You are a {FRAMEWORK} expert with deep knowledge of best practices and design patterns.

## Your Expertise
1. **Framework Architecture**
2. **Design Patterns**
3. **Performance Optimization**
4. **Best Practices**

## Common Patterns

### Pattern 1: [Pattern Name]
**When to use**: [scenario]
**Implementation**: [code example]
**Benefits**: [advantages]

[Multiple patterns]

## Best Practices
[Framework conventions and recommendations]
```

**Present in**:
- ✅ Django (no explicit django-expert, but drf-expert for DRF)
- ✅ react-expert.md
- ✅ Flask (schema-expert.md covers this role)
- ✅ tkinter-expert.md
- ✅ streamlit-expert.md
- ✅ Scrapy (spider-dev.md is the expert)

#### 3. Test Generator/Writer Agent

**Pattern**:
```yaml
---
name: test-{writer|generator|helper}
description: PROACTIVELY generate comprehensive tests with edge cases when new features are created. Expert in {FRAMEWORK} testing patterns, fixtures, and test organization.
tools: Read, Write, Bash
model: sonnet
---

You are a testing expert for {FRAMEWORK} applications.

## Your Responsibilities
1. **Test Generation** - Create comprehensive test suites
2. **Edge Case Coverage** - Identify and test edge cases
3. **Test Organization** - Structure tests properly
4. **Fixture Creation** - Set up test data

## Testing Patterns

### Unit Tests
[How to write unit tests for framework]

### Integration Tests
[How to write integration tests]

### Test Organization
[Directory structure and naming conventions]

## Best Practices
[Framework testing guidelines]
```

**Present in**:
- ✅ Django (test-writer.md)
- ✅ React (testing-expert.md)
- ✅ Flask (test-generator.md)
- ✅ Tkinter (test-helper.md)
- ✅ Streamlit (test-generator.md)
- ✅ Scrapy (testing-assistant.md)

#### 4. Performance/Optimization Agent

**Pattern**:
```yaml
---
name: {performance-optimizer|api-optimizer|performance-tuner}
description: PROACTIVELY identify performance bottlenecks and suggest optimizations. Expert in {FRAMEWORK} performance patterns and optimization techniques.
tools: Read, Grep, Bash
model: sonnet
---

You are a performance optimization expert for {FRAMEWORK}.

## Your Responsibilities
1. **Identify Bottlenecks** - Find performance issues
2. **Suggest Optimizations** - Recommend improvements
3. **Profile Code** - Analyze performance metrics
4. **Optimize [Domain-Specific]** - [Queries/Rendering/etc.]

## Optimization Strategies

### Strategy 1: [Name]
**Problem**: [Performance issue]
**Solution**: [Optimization approach]
**Example**: [Code before/after]

[Multiple strategies]

## Best Practices
[Framework performance guidelines]
```

**Present in**:
- ✅ Django (orm-optimizer.md - focused on database)
- ✅ React (react-performance.md)
- ✅ Flask (api-optimizer.md)
- ✅ Tkinter (performance-optimizer.md)
- ✅ Streamlit (data-viz-optimizer.md)
- ✅ Scrapy (performance-tuner.md)

### Domain-Specific Agent Roles

#### Backend Framework Agents

**Migration Helper** (Django, Flask, Streamlit):
- Helps with database schema changes
- Reviews migrations for safety
- Suggests data migration strategies

**ORM Optimizer** (Django):
- Optimizes database queries
- Prevents N+1 problems
- Suggests indexing strategies

**API Designer** (Flask):
- Blueprint architecture
- RESTful design
- Schema validation

**DRF Expert** (Django):
- Django REST Framework patterns
- Serializer design
- ViewSet organization

#### Frontend Framework Agents

**Component Architect** (React):
- Component composition
- Props vs. state decisions
- Component reusability

**State Manager** (React):
- Zustand patterns (query-expert.md)
- Context API usage
- State optimization

**Accessibility Reviewer** (React):
- A11y compliance
- ARIA attributes
- Keyboard navigation

#### Specialized Framework Agents

**Threading Expert** (Tkinter):
- Async operations in GUI
- Background task management
- UI responsiveness

**Data Pipeline Expert** (Scrapy):
- Pipeline architecture
- Data transformation
- Storage strategies

**Database Architect** (Streamlit):
- Schema design
- Migration strategies
- Connection pooling

---

## Skill Patterns

### Universal Skills (Present in Most Templates)

#### 1. Framework Patterns Skill

**Pattern**:
```yaml
---
name: {framework}-patterns
description: Implement common {FRAMEWORK} design patterns including [pattern types]. Use when refactoring code or implementing standard {FRAMEWORK} patterns.
allowed-tools: Read, Write, Grep
---

You are a {FRAMEWORK} patterns expert. You help implement common design patterns.

## Patterns You Can Implement

### 1. Pattern Name
**Purpose**: [What problem it solves]
**When to use**: [Scenarios]
**Implementation**:
[Complete code example]

**Benefits**:
- [Advantage 1]
- [Advantage 2]

[Multiple patterns with examples]

## Best Practices
1. [Practice 1]
2. [Practice 2]

This skill helps you implement proven {FRAMEWORK} patterns.
```

**Present in**:
- ✅ django-patterns/
- ✅ flask-patterns/
- ✅ streamlit-patterns/
- ⚠️ React (component-patterns/ covers this)
- ⚠️ Tkinter (mvc-pattern/ covers this)

#### 2. Code Generator Skill

**Pattern**:
```yaml
---
name: {type}-generator
description: Generate {type} boilerplate with proper structure and best practices. Use when creating new {types} or scaffolding {domain} code.
allowed-tools: Read, Write, Grep
---

You are a {TYPE} code generator expert.

## What You Generate

### Standard {Type}
[Template/example]

### Advanced {Type}
[More complex template]

## Generation Patterns

### Pattern 1: Basic {Type}
**Usage**: When to use this pattern
**Template**:
[Code template]

[Multiple patterns]

## Best Practices
[Guidelines for generated code]
```

**Present in**:
- ✅ Django (drf-serializer/)
- ✅ Flask (rest-api-generator/)
- ✅ React (custom-hooks/)
- ✅ Tkinter (dialog-generator/)
- ✅ Scrapy (spider-generator/)

#### 3. Validator/Helper Skill

**Pattern**:
```yaml
---
name: {domain}-validator
description: Validate {domain} code against best practices and {FRAMEWORK} conventions. Use when reviewing {domain} implementations or before commits.
allowed-tools: Read, Grep
---

You are a {DOMAIN} validation expert.

## What You Validate

1. **Structural Validation**
   - [Checks for structure]
2. **Convention Compliance**
   - [Checks for conventions]
3. **Best Practices**
   - [Checks for practices]

## Validation Rules

### Rule 1: [Name]
**Check**: [What to verify]
**Bad Example**: [Anti-pattern]
**Good Example**: [Best practice]

[Multiple rules]

## Common Issues
[Typical problems and solutions]
```

**Present in**:
- ✅ Django (model-validator/)
- ✅ Flask (database-validator/)
- ✅ Tkinter (form-validation/)
- ✅ Streamlit (database-operations/)
- ✅ Scrapy (test-coverage/)

### Specialized Skills by Framework Type

**Backend Frameworks**:
- Authentication systems (flask/auth-system/, streamlit/auth-system/)
- Database operations (streamlit/database-operations/)
- API generation (flask/rest-api-generator/)
- Data pipelines (scrapy/data-pipeline/)

**Frontend Frameworks**:
- Component patterns (react/component-patterns/)
- Custom hooks (react/custom-hooks/)
- Query patterns (react/query-patterns/)
- State management patterns

**Desktop/GUI**:
- MVC patterns (tkinter/mvc-pattern/)
- Dialog generation (tkinter/dialog-generator/)
- Form validation (tkinter/form-validation/)

**Data/Specialized**:
- Caching optimization (streamlit/caching-optimizer/)
- Spider generation (scrapy/spider-generator/)
- Docker deployment (scrapy/docker-deploy/)

---

## Documentation Structure Patterns

### README.md Structure (All Templates Follow)

```markdown
# {Framework} Project Template

Brief description of template.

## What's Included

- ✅ Feature 1
- ✅ Feature 2
[8-12 bullet points]

## Quick Start

### Prerequisites
- Requirement 1
- Requirement 2

### Installation
1. Step 1
2. Step 2
[5-8 steps]

### First Run
[How to verify it works]

## Project Structure

[Directory tree with descriptions]

## Available Scripts / Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| /command1 | Description | args |

[Table of 10-12 commands]

## Subagents

This template includes specialized subagents:

### Agent 1
**Trigger**: When to activate
**Purpose**: What it does

[5-6 agent descriptions]

## Skills

### Skill 1
**Purpose**: What it provides
**When to use**: Scenarios

[3-4 skill descriptions]

## Development Workflow

[Typical development process]

## Testing

[How to run tests]

## Deployment

[How to deploy]

## Customization

[How to customize]

## Troubleshooting

[Common issues]

## Resources

- [Link 1]
- [Link 2]
[5-10 external resources]

## License

MIT License
```

**Typical Length**: 300-600 lines

### CLAUDE.md Structure (All Templates Follow)

```markdown
# {Framework} {Project Type}

## Project Type

This is a {FRAMEWORK} {version} project for {purpose}.

## Technology Stack

- **{Framework}**: {version} - {purpose}
- **{Tool 1}**: {version} - {purpose}
[5-10 key dependencies]

## Project Structure

[Detailed directory tree with explanations]

## Common Commands

| Command | Description | Usage |
|---------|-------------|-------|
| /command | What it does | Example |

[Table of all commands]

## Code Style & Conventions

### {Language} Style
- Convention 1
- Convention 2
[10-15 conventions]

### {Framework} Conventions
- Pattern 1
- Pattern 2
[Framework-specific rules]

## {Framework-Specific Patterns}

### Pattern Category 1 (e.g., Models, Components, Views)

**Good Example**:
[Code example]

**Bad Example**:
[Anti-pattern]

**Explanation**: Why good is better

[3-5 categories with examples]

## {Domain} Patterns (e.g., State Management, ORM, Routing)

### Pattern 1
[Detailed explanation with code]

### Pattern 2
[Detailed explanation with code]

[5-8 patterns]

## Testing Strategy

### Unit Tests
[How to write unit tests]

### Integration Tests
[How to write integration tests]

### Running Tests
[Commands and patterns]

## Security Best Practices

1. **Security Area 1** (e.g., Authentication)
   - Practice 1
   - Practice 2
   [5-8 areas with practices]

## Performance Considerations

1. **Performance Area 1** (e.g., Database Queries)
   - Optimization 1
   - Optimization 2
   [4-6 areas with optimizations]

## Common Packages & Their Uses

- **Package 1**: Purpose and common usage
- **Package 2**: Purpose and common usage
[10-20 packages]

## Helpful Documentation

- [Official Docs]
- [Tool Docs]
[8-12 links]

## Notes

[Additional framework-specific guidance]
```

**Typical Length**: 400-850 lines

### setup_instructions.md Structure (Some Templates)

```markdown
# {Framework} Project Setup Instructions

## Prerequisites

- Software 1: version, installation link
- Software 2: version, installation link
[3-5 prerequisites]

## Quick Start

1. **Step 1 Title**
   ```bash
   command
   ```
   Explanation

2. **Step 2 Title**
   [Detailed step]

[8-12 steps]

## Configuration

### Database Setup
[If applicable]

### Environment Variables
[List of variables with descriptions]

### Framework Configuration
[Framework-specific config]

## First Component/Module

[How to create your first {component/model/view}]

## Running Tests

[Test execution details]

## Production Deployment

[Deployment guidance]

## Common Issues

### Issue 1
**Problem**: Description
**Solution**: How to fix

[5-8 common issues]

## Resources

- [Link 1]
- [Link 2]
```

**Typical Length**: 200-400 lines

---

## Configuration File Patterns

### .claude/settings.json

**Minimal Pattern** (React):
```json
{
  "model": "sonnet",
  "permissions": {
    "allow": ["*"],
    "deny": [".env", "*.key", "*.pem", "secrets.*"]
  },
  "outputStyle": "markdown",
  "cleanupPeriodDays": 30
}
```

**With Environment** (Django):
```json
{
  "model": "sonnet",
  "env": {
    "DJANGO_SETTINGS_MODULE": "project_name.settings"
  },
  "permissions": {
    "allow": ["*"],
    "deny": [".env", "*.key", "*.pem", "secrets.*"]
  },
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "if echo $FILE | grep -E '\\.py$'; then black $FILE 2>/dev/null || true; fi"
      }]
    }]
  }
}
```

**Common Elements**:
- ✅ Model selection (always "sonnet")
- ✅ Permissions with sensitive file denial
- ✅ Optional environment variables
- ✅ Optional auto-format hooks
- ✅ Optional output style
- ✅ Optional cleanup period

### Auto-Format Hook Patterns

**Python**:
```bash
if echo $FILE | grep -E '\\.py$'; then black $FILE 2>/dev/null || true; fi
```

**JavaScript/TypeScript**:
```bash
if echo $FILE | grep -E '\\.(js|jsx|ts|tsx)$'; then prettier --write $FILE 2>/dev/null || true; fi
```

**Rust**:
```bash
if echo $FILE | grep -E '\\.rs$'; then rustfmt $FILE 2>/dev/null || true; fi
```

**Go**:
```bash
if echo $FILE | grep -E '\\.go$'; then gofmt -w $FILE 2>/dev/null || true; fi
```

### .env.example Pattern

```bash
# {Framework} Settings
{FRAMEWORK}_SETTING_1=value
{FRAMEWORK}_SETTING_2=value

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# DATABASE_URL=mysql://user:password@localhost:3306/dbname
# DATABASE_URL=sqlite:///./database.db

# Security Settings
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET=your-jwt-secret-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# API Keys (if needed)
EXTERNAL_API_KEY=your-api-key-here
EXTERNAL_API_SECRET=your-api-secret-here

# Feature Flags (if applicable)
DEBUG=True
TESTING=False

# IMPORTANT: Never commit the actual .env file!
# Copy this to .env and update with real values.
```

**Pattern Notes**:
- Group by category with comments
- Provide example values
- Comment alternative options
- Include security warnings
- Explain how to use

### .gitignore Pattern

```gitignore
# Language-specific
{python: __pycache__, *.py[cod], *.so, .Python}
{node: node_modules/, npm-debug.log, yarn-error.log}
{rust: target/, Cargo.lock}

# Virtual Environments / Dependencies
{python: venv/, env/, .env/}
{node: node_modules/}
{ruby: vendor/bundle/}

# Framework-specific
{django: *.log, db.sqlite3, media/}
{react: build/, dist/, .vite/}
{flask: instance/, .webassets-cache}

# Environment Variables
.env
.env.local
.env.production
.env.*.local

# IDE Files
.vscode/
.idea/
*.swp
*.swo
*~

# Testing Artifacts
.coverage
htmlcov/
.pytest_cache/
.tox/

# Build Outputs
dist/
build/
*.egg-info/

# Claude Code Local Settings
.claude/*.local.*

# OS Files
.DS_Store
Thumbs.db
```

---

## Key Insights for Template Creation

### 1. Consistency is Critical

Every complete template follows the same patterns:
- 10-12 commands covering 5 categories
- 5-6 agents with 4 universal roles + domain-specific
- 3-4 skills with patterns/generator/validator structure
- Documentation with identical section structures

### 2. Universal Components Are Reusable

These components work across ALL frameworks with minor customization:
- Security agent (just change vulnerabilities)
- Test generator (just change testing framework)
- Performance optimizer (just change optimization strategies)
- Framework patterns skill (just change patterns)

### 3. Framework Files Vary Significantly

While Claude Code configs are highly consistent, framework files differ greatly:
- Python: requirements.txt, setup.py, pyproject.toml
- Node: package.json, tsconfig.json, vite.config.ts
- Rust: Cargo.toml
- Go: go.mod, go.sum

Research these per-framework!

### 4. Documentation Quality Matters

Complete templates have:
- Comprehensive CLAUDE.md (400+ lines) with examples
- User-friendly README.md (300+ lines) with setup
- Clear setup_instructions.md for beginners
- All three docs work together but serve different audiences

### 5. Incomplete Templates Stand Out

FastAPI has commands but no agents/skills - it immediately feels incomplete compared to others. Don't skip components!

---

## Quick Reference Checklist

When creating a new template, ensure you have:

### File Structure
- [ ] README.md (300-600 lines)
- [ ] CLAUDE.md (400-700 lines)
- [ ] setup_instructions.md (optional, 200-400 lines)
- [ ] .claude/settings.json
- [ ] .env.example
- [ ] .gitignore

### Commands (10-12 total)
- [ ] Development server
- [ ] Testing (including coverage)
- [ ] Linting
- [ ] Formatting
- [ ] Type checking (if typed language)
- [ ] Build (if applicable)
- [ ] Create component/model (3-4 variants)
- [ ] Database operations (if applicable)
- [ ] Shell/REPL (if applicable)
- [ ] Framework-specific operations (1-3)

### Agents (5-6 total)
- [ ] Security agent ({framework}-security)
- [ ] Framework expert
- [ ] Test generator
- [ ] Performance optimizer
- [ ] Domain-specific agent 1
- [ ] Domain-specific agent 2 (optional)

### Skills (3-4 total)
- [ ] Framework patterns
- [ ] Code generator (component/model/etc.)
- [ ] Validator or helper
- [ ] Domain-specific skill (optional)

### Quality Checks
- [ ] All commands have descriptions
- [ ] All agents have PROACTIVELY or MUST BE USED
- [ ] All skills have clear descriptions
- [ ] Documentation is comprehensive
- [ ] Examples are included
- [ ] Framework files are present

---

This reference guide ensures new templates maintain the high quality standards established by the existing templates.
