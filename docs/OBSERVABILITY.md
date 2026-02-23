# OBSERVABILITY

Цель:
сделать систему проверяемой агентом без участия человека.

- TODO: [AI->HUMAN] Уточнить, какие метрики считаются критичными.
- TODO: [AI->HUMAN] Уточнить, какие user journeys критичны для smoke/regression.

## Agent Capabilities

Агент обязан уметь:

- запускать локальный observability stack;
- читать логи;
- читать метрики;
- проверять latency budget.

## Commands

```bash
./scripts/obs_up.sh
./scripts/obs_down.sh
```

## Acceptance Checks

- startup < 800ms;
- no error logs during smoke test.

EXAMPLE (REPLACE ME):
- p95 latency `/health` < 100ms при локальном запуске.
