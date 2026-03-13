# Plan: Harness CLI Installer + Multi-Agent Support

**Status**: Planning (not started)
**Priority**: Medium — enables distribution, but manual copy works for now

## Goal

Create a CLI tool that bootstraps any project with EnHarnes skills, policies, and Makefile. Similar to `specify init` from GitHub Spec Kit.

## Installation Modes

### Mode 1: CLI (pip install)
```bash
pip install enharness
harness init --ai claude
harness init --ai cursor
harness init . --ai claude --with-agents
```

### Mode 2: Template copy (no CLI)
User copies the template project directory into their repo root. Agent reads `harness.core/SKILL.md` and scaffolds the rest.

## CLI Commands

| Command | What it does |
|---------|-------------|
| `harness init [dir] --ai <agent>` | Bootstrap project with skills + policies + Makefile |
| `harness init --with-agents` | Also create `.claude/agents/harness/*.md` (optional) |
| `harness check` | Run `make test` equivalent |
| `harness upgrade` | Pull latest skills from registry/repo |

## What `harness init --ai claude` Creates

```
.claude/
├── skills/
│   ├── harness.core/       (docs, templates, example)
│   ├── harness.linters/    (static analysis scripts)
│   ├── harness.generators/ (doc generators)
│   ├── harness.ci/         (CI orchestration)
│   ├── harness.planner/    (ExecPlan creation)
│   ├── harness.anti-overengineering/ (optional)
│   ├── harness.smoke/      (slash command)
│   ├── harness.test/       (slash command)
│   ├── harness.review/     (slash command)
│   ├── harness.entropy/    (slash command)
│   └── harness.plan/       (slash command)
policies/
├── architecture.yaml       (empty template)
├── doc-indexes.yaml        (empty template)
├── control-loop-metrics.yaml
└── risk-policy.json
Makefile                    (includes harness.core/templates/Makefile.inc)
AGENTS.md                   (from harness.core/templates/AGENTS.md.template)
```

## Multi-Agent Support (AGENT_CONFIG)

Inspired by Spec Kit's 18-agent support via a single config dictionary.

```python
AGENT_CONFIG = {
    "claude": {
        "name": "Claude Code",
        "skills_dir": ".claude/skills",
        "commands_dir": ".claude/commands",   # if slash commands needed
        "agents_dir": ".claude/agents",
        "format": "markdown",
    },
    "cursor": {
        "name": "Cursor",
        "skills_dir": ".cursor/rules",
        "commands_dir": ".cursor/commands",
        "format": "markdown",
    },
    "copilot": {
        "name": "GitHub Copilot",
        "skills_dir": ".github/instructions",
        "commands_dir": ".github/agents",
        "format": "markdown",
    },
    "gemini": {
        "name": "Gemini CLI",
        "skills_dir": ".gemini/skills",
        "commands_dir": ".gemini/commands",
        "format": "toml",
    },
}
```

### What changes per agent:
- **Directory paths** — `.claude/skills/` vs `.cursor/rules/` vs `.github/instructions/`
- **Frontmatter format** — YAML (Claude, Cursor) vs TOML (Gemini)
- **Skill invocation** — `/harness.test` vs different patterns
- **Agent definitions** — `.claude/agents/` vs not supported

### What stays the same:
- `policies/` — universal, agent-agnostic
- `scripts/` — Python, runs everywhere
- `Makefile` — universal
- `AGENTS.md` — universal control panel
- `docs/` — universal

## Tech Stack

- Python 3.11+
- `typer` for CLI
- `rich` for output formatting
- No other deps (keep it minimal)
- Distribute via PyPI: `pip install enharness`

## Milestones

1. **M1: Core init** — `harness init --ai claude` creates full structure
2. **M2: Template mode** — `harness init --template-only` copies without CLI
3. **M3: Multi-agent** — Add cursor, copilot, gemini support
4. **M4: Upgrade** — `harness upgrade` pulls latest skills
5. **M5: Registry** — Central skill registry for community extensions

## Open Questions

- Should this be a separate repo (`enharness-cli`) or part of EnHarnes?
- Package name: `enharness`? `harness-cli`? `harness-init`?
- Should skills be bundled in the package or fetched from a registry?
