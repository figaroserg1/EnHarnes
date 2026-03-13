# Browser Automation

Agent browser automation for UI validation, screenshot comparison, and interaction testing.

## Option A: Playwright MCP Server (Recommended)

MCP server providing browser tools directly to the agent via Model Context Protocol.

### Install

```bash
claude mcp add playwright -- npx @playwright/mcp --headless --caps vision
```

Or in `.claude/settings.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp", "--headless", "--caps", "vision"]
    }
  }
}
```

### Capabilities

| Tool | Description |
|------|-------------|
| `browser_navigate` | Navigate to URL |
| `browser_screenshot` | Take screenshot (requires `--caps vision`) |
| `browser_click` | Click element |
| `browser_fill` | Fill input field |
| `browser_select` | Select dropdown option |
| `browser_evaluate` | Execute JavaScript |
| `browser_snapshot` | Get accessibility tree |
| `browser_wait` | Wait for element/condition |
| `browser_tab_*` | Tab management |
| `browser_pdf` | Generate PDF (requires `--caps pdf`) |

### Key Options

| Flag | Purpose |
|------|---------|
| `--headless` | Run without visible browser (for CI) |
| `--browser chrome` | Browser engine (chrome/firefox/webkit/msedge) |
| `--caps vision` | Enable screenshot capability |
| `--caps pdf` | Enable PDF generation |
| `--viewport-size 1280x720` | Set viewport |
| `--user-data-dir <path>` | Persistent browser profile |
| `--storage-state <path>` | Load cookies/auth state |

## Option B: agent-browser CLI

Standalone CLI tool for browser automation via shell commands.
Agent uses it via Bash tool calls (not MCP).

### Install

```bash
npm install -g agent-browser
agent-browser install  # Download Chromium
```

### Usage

```bash
agent-browser open "https://example.com"
agent-browser snapshot                    # Get accessibility tree with refs
agent-browser click @e5                   # Click by ref from snapshot
agent-browser fill @e3 "test@test.com"    # Fill input
agent-browser screenshot                  # Take screenshot
agent-browser eval "document.title"       # Run JavaScript
agent-browser close
```

### Semantic Locators

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "test@test.com"
```

## Option C: Chrome DevTools MCP (for performance profiling)

```bash
claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest
```

Best for: performance traces, network analysis, CrUX data. Complements Playwright MCP.

## Recommendation

- **Phase 1 (no UI):** Not needed. Mark as N/A until product domain is decided.
- **Phase 2 (first UI):** Start with Playwright MCP — free, local, most capable.
- **Add agent-browser** if agents need CLI-based browser control (e.g., Codex tasks).
- **Add chrome-devtools-mcp** if performance profiling is needed.
