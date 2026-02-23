# Worktree Workflow

Каждая задача = отдельный git worktree.

## Создать

```bash
git worktree add ../task_feature_x
```

## Запустить

```bash
cd ../task_feature_x
./scripts/dev-start.sh
```

- TODO: [AI] Создавать isolated instance для каждой параллельной задачи.

EXAMPLE (REPLACE ME):
- worktree для hotfix именуется `../hotfix_<issue_id>`.
