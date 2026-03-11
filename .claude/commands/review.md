---
allowed-tools: Bash, Read, Grep, Glob
description: Run full pre-PR self-review (all gates + doc drift + entropy)
---

Run the full agent self-review before opening a PR.

## Steps

1. Run `make review` from the project root.
2. If any step fails, fix the issue and re-run.
3. After all checks pass, summarize results:
   - Static checks: pass/fail
   - Structural tests: pass/fail
   - Doc drift: pass/fail + any docs to verify
   - Entropy: warnings found (non-blocking)
4. If everything passes, say "Ready for PR".
