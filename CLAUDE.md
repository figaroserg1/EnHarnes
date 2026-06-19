# CLAUDE.md — Claude Code CLI Bootstrap

**Read [AGENTS.md](AGENTS.md) fully before any work.** It is your control panel —
the task loop, autonomy tiers, skills, hooks, and reference table all live there.
This file only adds what is specific to an interactive Claude Code session.

## Language in responses

- Reply in the language the user wrote in. Match it consistently — no
  spontaneous code-switching mid-reply.
- Use established technical terms in their canonical form. Don't invent
  translations or local variants for terms that have a standard spelling.
- Do not mangle words. Do not merge characters from different keyboard
  layouts into a single token.
- Mixing languages within a reply is acceptable only for quoting code,
  identifiers, file paths, or established terms — never inside a single word.

## Do NOT

- Push without explicit user permission.
