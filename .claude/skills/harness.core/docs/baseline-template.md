# Baseline Recording Template

Use this template before starting harness integration on a new project or when resetting baseline after major changes.

## Current State

| Item | Value |
|------|-------|
| **Date** | TODO: [HUMAN] YYYY-MM-DD |
| **Project** | TODO: [HUMAN] project name |
| **Primary language** | TODO: [HUMAN] |
| **Framework** | TODO: [HUMAN] |
| **Package manager** | TODO: [HUMAN] |

## Existing Entrypoints

| Action | Command | Works? |
|--------|---------|--------|
| Build | TODO: [HUMAN] | Y/N |
| Test | TODO: [HUMAN] | Y/N |
| Lint | TODO: [HUMAN] | Y/N |
| Typecheck | TODO: [HUMAN] | Y/N |
| Start dev server | TODO: [HUMAN] | Y/N |

## Known Issues

| Issue | Severity | Notes |
|-------|----------|-------|
| Flaky tests | TODO: [HUMAN] | which tests, how often |
| Long-running checks | TODO: [HUMAN] | which, how long |
| Missing CI gates | TODO: [HUMAN] | what's not covered |

## Required Environments

| Environment | Status | Access |
|-------------|--------|--------|
| Local dev | TODO: [HUMAN] | |
| CI (GitHub Actions) | TODO: [HUMAN] | |
| Staging | TODO: [HUMAN] | |
| Production | TODO: [HUMAN] | |

## Agent Readiness Snapshot

Run `make ci` and record:

```
make ci exit code: TODO
make lint-todos time: TODO
make lint time: TODO
make test time: TODO
Total CI time: TODO
```

## Harness Maturity Before Integration

| Category | Score (0-3) | Notes |
|----------|-------------|-------|
| Repository knowledge (AGENTS.md, docs/) | | |
| Architecture enforcement (linters, tests) | | |
| Agent legibility (bootable, observable) | | |
| Golden principles (documented, enforced) | | |
| Agent workflow (CI gates, PR templates) | | |
| Garbage collection (debt tracking, gardening) | | |

**Total: __ / 18**
