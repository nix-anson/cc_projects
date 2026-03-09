---
allowed-tools: Bash, Write
description: Generate commit message from staged changes
---

# commit-msg

Analyzes staged git changes and generates a formatted `COMMIT_MESSAGE.md` file for easy copy-paste during commits.

## Usage

```
/commit-msg
```

No arguments needed. The command reads staged changes automatically.

## Core Instructions

### Phase 1: Gather Staged Changes

1. **Get staged file summary**:
   - Run `git diff --cached --stat` to see which files are staged
   - If no files are staged, inform the user and stop

2. **Get full diff**:
   - Run `git diff --cached` to get the complete changes

### Phase 2: Analyze Changes

Analyze the diff to understand:

1. **Change categories**:
   - New files added
   - Files modified
   - Files deleted
   - Version bumps

2. **Change types**:
   - Feature additions
   - Bug fixes
   - Refactoring
   - Documentation updates
   - Configuration changes
   - Test updates

3. **Key details**:
   - What functionality was added/changed
   - Why the change was made (infer from context)
   - Breaking changes or important notes

### Phase 3: Generate Commit Message

Create a structured commit message following conventional commit style:

**Subject Line Guidelines**:
- Max 50 characters
- Imperative mood ("Add" not "Added")
- No period at end
- Format: `<type>: <description>`
- Types: feat, fix, docs, refactor, test, chore, style

**Body Guidelines**:
- Wrap at 72 characters
- Explain what and why, not how
- Use bullet points for multiple changes
- Include version bumps if relevant

### Phase 4: Write COMMIT_MESSAGE.md

Write the file to the repository root with this structure:

```markdown
# Commit Message

## Subject
<subject line here>

## Body
<detailed body here>

## Files Changed
- `file1.py` - brief description
- `file2.py` - brief description

---
*Copy the subject and body sections above for your git commit.*
```

## Output Format

The generated `COMMIT_MESSAGE.md` should be:
- Clear and scannable
- Ready to copy-paste into a git commit
- Include all relevant context from the staged changes

## Examples

### Example 1: Feature Addition

```markdown
# Commit Message

## Subject
feat: Add Teams notification support for script failures

## Body
Integrate Microsoft Teams notifications using Workflows webhooks with Adaptive Cards.

- Add send_teams.py utility with failure and success alert functions
- Update script_wrapper to optionally send Teams alerts on failure
- Add notify_teams_on_failure option to CHANGEABLES dict
- Update CLAUDE.md with Teams notification documentation

Version bumps:
- script_template.py: 3.5.0 -> 3.6.0
- logging_config.py: 1.0.5 -> 1.1.0

## Files Changed
- `utils/send_teams.py` - NEW: Teams notification utility
- `utils/script_template.py` - Add Teams integration
- `utils/logging_config.py` - Auto-detect script name
- `CLAUDE.md` - Document Teams notifications
- `src/inscope_ondemand/1_test_basic.py` - Add Teams support

---
*Copy the subject and body sections above for your git commit.*
```

### Example 2: Bug Fix

```markdown
# Commit Message

## Subject
fix: Resolve connection timeout in data sync

## Body
Fix database connection timeout that occurred during large data transfers.

- Increase connection timeout from 30s to 120s
- Add retry logic with exponential backoff
- Improve error messages for timeout scenarios

## Files Changed
- `utils/connectors.py` - Adjust timeout settings
- `src/inscope_scheduled_tasks/sync_data.py` - Add retry logic

---
*Copy the subject and body sections above for your git commit.*
```

## Error Handling

- **No staged changes**: Inform user "No staged changes found. Stage files with `git add` first."
- **Git not available**: Inform user "Git command failed. Ensure you're in a git repository."

## Notes

- This command is READ-ONLY for git operations
- Only writes to `COMMIT_MESSAGE.md` (gitignored)
- Does not perform any git actions (add, commit, push)
