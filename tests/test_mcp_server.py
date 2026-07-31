import sys
import json

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.anyio
async def test_recommend_coffee_tool_over_stdio():
    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "cafe_mcp_server.server"],
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "recommend_coffee",
                {
                    "mood": "smooth iced",
                    "prefer_milk": False,
                    "caffeine": "high",
                    "temperature": "cold",
                },
            )

    payload = json.loads(result.content[0].text)
    assert payload["id"] == "cold_brew"
    assert payload["name"] == "Cold Brew"
