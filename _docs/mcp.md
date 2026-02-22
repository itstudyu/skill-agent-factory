# Claude Code MCP (Model Context Protocol) — Reference Documentation

> Source: https://code.claude.com/docs/en/mcp
> Last fetched: 2026-02-21

---

## What Is MCP?

The Model Context Protocol (MCP) is an open standard for AI-tool integrations. MCP servers give Claude Code access to external tools, databases, and APIs.

---

## Adding MCP Servers

### Option 1: HTTP Server (Recommended)
```bash
claude mcp add --transport http <name> <url>

# Example with authentication
claude mcp add --transport http notion https://mcp.notion.com/mcp
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### Option 2: SSE Server (Deprecated — use HTTP instead)
```bash
claude mcp add --transport sse <name> <url>
```

### Option 3: Local Stdio Server
```bash
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server
```

> ⚠️ All options (`--transport`, `--env`, `--scope`) must come **before** the server name. The `--` separates server name from the command.

---

## Scope Options

```bash
# Local (default) - your project only, stored in ~/.claude.json
claude mcp add --transport http stripe https://mcp.stripe.com

# Project - shared with team via .mcp.json file
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp

# User - all your projects, stored in ~/.claude.json
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com
```

| Scope | Storage | Shareable |
|-------|---------|-----------|
| `local` (default) | `~/.claude.json` under project path | No |
| `project` | `.mcp.json` in project root | ✅ Yes (commit to VCS) |
| `user` | `~/.claude.json` globally | No |

---

## Managing MCP Servers

```bash
claude mcp list                # List all configured servers
claude mcp get github          # Get details for a server
claude mcp remove github       # Remove a server
/mcp                           # Within Claude Code: check server status + auth
```

---

## .mcp.json Format (Project Scope)

```json
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    },
    "http-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

**Environment variable expansion:**
- `${VAR}` — expands to value of `VAR`
- `${VAR:-default}` — expands to `VAR` if set, otherwise `default`

---

## OAuth Authentication

```bash
# Add server
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Authenticate in Claude Code
/mcp
# → Follow browser login flow
```

### Pre-configured OAuth credentials
```bash
claude mcp add --transport http \
  --client-id your-client-id --client-secret --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

---

## Import from Claude Desktop

```bash
claude mcp add-from-claude-desktop
# Interactive: select which servers to import
```

---

## Add from JSON

```bash
# HTTP server
claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp"}'

# Stdio server
claude mcp add-json local-tool '{"type":"stdio","command":"/path/to/tool","args":["--flag"]}'
```

---

## Claude Code as MCP Server

```bash
claude mcp serve
```

Claude Desktop config:
```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "/full/path/to/claude",
      "args": ["mcp", "serve"]
    }
  }
}
```

---

## Plugin MCP Servers

In `.mcp.json` at plugin root:
```json
{
  "database-tools": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
  }
}
```

---

## MCP Output Limits

- Default max: 25,000 tokens
- Warning shown at: 10,000 tokens
- Override: `export MAX_MCP_OUTPUT_TOKENS=50000`

---

## MCP Tool Naming Convention

MCP tools use the format: `mcp__<server>__<tool>`

Examples:
- `mcp__github__search_repositories`
- `mcp__filesystem__read_file`
- `mcp__slack__send_message`

Use in hook matchers: `mcp__github__.*` (regex)

---

## Popular MCP Servers

| Category | Server | Command/URL |
|----------|--------|-------------|
| GitHub | GitHub | `claude mcp add --transport http github https://api.githubcopilot.com/mcp/` |
| Error tracking | Sentry | `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp` |
| Database | PostgreSQL | `claude mcp add --transport stdio db -- npx -y @bytebase/dbhub --dsn "..."` |
| Filesystem | Local files | `npx -y @modelcontextprotocol/server-filesystem` |

---

## Best Practices

- Use `--scope project` for team-shared integrations (committed to repo)
- Use `--scope user` for personal developer tools
- Never commit secrets — use `${ENV_VAR}` in `.mcp.json`
- Test with `/mcp` command to verify server status
- Use `MAX_MCP_OUTPUT_TOKENS` for data-heavy integrations
