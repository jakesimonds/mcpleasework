# MCP Python Demo

This repository demonstrates the use of Model Context Protocol (MCP) SDK for Python.

## Running Development Inspector

To run the development inspector:

```bash
mcp dev server.py
```

## Installing in Claude

To install this MCP plugin in Claude:

1. Run this command:

   ```bash
   mcp install server.py
   ```

2. Restart Claude

3. Troubleshooting: If you get an error, fix the uv path in the config to an absolute path:

   ```bash
   which uv
   ```

   Then update the configuration with the absolute path.

## working claude_desktop_config:

{
  "mcpServers": {
    "My App": {
      "command": "/Users/jakesimonds/Documents/mcp-python-demo/venv/bin/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli],requests,/Users/jakesimonds/Documents/mcp-python-demo/bleak-dash",
        "mcp",
        "run",
        "/Users/jakesimonds/Documents/mcp-python-demo/server.py"
      ]
    }
  }
}

