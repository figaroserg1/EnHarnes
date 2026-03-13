# Worktree Workflow

Each agent task runs in an isolated git worktree. No shared state between tasks.

## Create and Boot

```bash
# One command: creates worktree, installs deps, runs smoke
python scripts/harness/worktree_boot.py feature-x
```

This creates `../worktree_feature-x` on branch `task/feature-x`.

## Manual Steps

```bash
# Create worktree manually
git worktree add ../worktree_feature-x -b task/feature-x

# Enter and work
cd ../worktree_feature-x
make lint-docs

# When done
cd -
git worktree remove ../worktree_feature-x
```

## Naming Convention

| Task type | Worktree path | Branch |
|-----------|---------------|--------|
| Feature | `../worktree_feature-x` | `task/feature-x` |
| Hotfix | `../worktree_hotfix-123` | `task/hotfix-123` |
| Entropy cleanup | `../worktree_entropy-2026-02` | `task/entropy-2026-02` |

## Rules

- Each parallel agent task gets its own worktree.
- Never share a worktree between concurrent tasks.
- Clean up worktrees after merge: `git worktree remove <path>`.
- The boot script auto-detects runtime and installs dependencies.
