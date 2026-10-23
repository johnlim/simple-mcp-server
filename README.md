# MCP Servers for Claude Desktop

This repository contains two MCP servers that connect to Claude Desktop in different ways. Both are registered in `claude_desktop_config.json`.

## The role of the config file

Each entry under `mcpServers` tells Claude Desktop **which local process to start**: it runs `command` with `args`. On startup, Claude Desktop launches every entry as a child process and communicates with it over **stdio** (stdin/stdout), using JSON-RPC messages. When Claude Desktop quits, these processes are stopped. Config changes take effect only after a full restart of Claude Desktop.

The config never describes a network connection directly. For a command-based entry, stdio is the only transport. Reaching an HTTP server requires a bridge process.

## Server 1: `my-custom-server` (stdio)

```json
"my-custom-server": {
  "command": "/full/path/to/.venv/bin/python",
  "args": ["/full/path/to/<stdio_server>.py"]
}
```

- Claude Desktop **starts the Python server itself**.
- `mcp.run()` defaults to the stdio transport, so the server reads requests from stdin and writes responses to stdout.
- Tools: `get_server_status`, `get_current_time`.

```
Claude Desktop ──stdio──▶ Python server (started by Claude)
```

## Server 2: `my-http-server` (HTTP via `mcp-remote`)

```json
"my-http-server": {
  "command": "npx",
  "args": ["-y", "mcp-remote@latest", "http://127.0.0.1:8000/mcp", "--allow-http"]
}
```

- Claude Desktop starts **`mcp-remote`**, a bridge that speaks stdio to Claude and HTTP to the server.
- Claude Desktop **does not start the Python server**. It must already be running (`python <http_server>.py`), serving streamable HTTP at `http://127.0.0.1:8000/mcp` via `mcp.run(transport="streamable-http")`.
- Tools: `calculate_square`.

```
Claude Desktop ──stdio──▶ mcp-remote ──HTTP──▶ Python server (started manually)
```

## Notes

- **Use full paths** in the config. Claude Desktop does not inherit your shell's `PATH` or an activated virtual environment (this includes `npx` installed via nvm).
- **Never print to stdout in a stdio server.** stdout is the protocol channel; log to stderr instead.
- `.venv/` is not committed. Recreate it from the dependency file (for example, `pip install -r requirements.txt`).
- MCPServer SDK handles the handshake and MCP communications
