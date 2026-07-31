#!/usr/bin/env python3
"""Call the local cafe MCP server over stdio for command-line smoke tests."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def call_tool(tool_name: str, arguments: dict[str, Any]) -> None:
    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "cafe_mcp_server.server"],
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)

    if result.isError:
        raise SystemExit(result.content[0].text if result.content else "MCP tool call failed")

    for item in result.content:
        text = getattr(item, "text", None)
        if text:
            print(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Call a cafe MCP tool over stdio.")
    parser.add_argument("tool", choices=["list_coffee_menu", "recommend_coffee", "explain_recommendation"])
    parser.add_argument("--args", default="{}", help="JSON object with tool arguments.")
    parsed = parser.parse_args()

    arguments = json.loads(parsed.args)
    if not isinstance(arguments, dict):
        raise SystemExit("--args must be a JSON object")

    asyncio.run(call_tool(parsed.tool, arguments))


if __name__ == "__main__":
    main()
