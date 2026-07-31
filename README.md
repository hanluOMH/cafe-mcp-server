# cafe-mcp-server

A minimal Python MCP server that recommends coffee from local static data.

This demo does not call external APIs and does not require an API key.

## Tools

- `list_coffee_menu`: returns the full static menu.
- `recommend_coffee`: recommends one drink from mood, milk, caffeine, and temperature preferences.
- `explain_recommendation`: explains a selected drink against the same preference inputs.

## Install

```bash
cd /Users/hanlufeng/Desktop/AI-INSIGHT-REPORT/Ceilia/cafe-mcp-server
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Run

```bash
cafe-mcp-server
```

Equivalent module form:

```bash
python -m cafe_mcp_server.server
```

## Example MCP config

```json
{
  "mcpServers": {
    "cafe-recommendation": {
      "command": "python",
      "args": [
        "-m",
        "cafe_mcp_server.server"
      ],
      "cwd": "/Users/hanlufeng/Desktop/AI-INSIGHT-REPORT/Ceilia/cafe-mcp-server"
    }
  }
}
```

If the package is installed into the same Python environment used by the MCP client, the console script can be used instead:

```json
{
  "mcpServers": {
    "cafe-recommendation": {
      "command": "cafe-mcp-server"
    }
  }
}
```

## Development

```bash
pytest
python -m compileall src tests
PYTHONPATH=src python -c "from cafe_mcp_server.recommender import recommend_coffee; print(recommend_coffee(mood='smooth iced', prefer_milk=False)['name'])"
```

## Command-line MCP tool test

After installing the project, call the MCP server through a stdio client:

```bash
python scripts/call_tool.py recommend_coffee --args '{"mood":"smooth iced","prefer_milk":false,"caffeine":"high","temperature":"cold"}'
```

Expected result includes:

```json
{
  "id": "cold_brew",
  "name": "Cold Brew"
}
```
