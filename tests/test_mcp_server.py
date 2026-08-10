import sys
import json

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from cafe_mcp_server.server import (
    MCP_ACCEPT_HEADER,
    _default_transport,
    _ensure_mcp_accept_header,
    _host,
    _port,
    mcp,
)


def test_defaults_to_stdio_without_port(monkeypatch):
    monkeypatch.delenv("MCP_TRANSPORT", raising=False)
    monkeypatch.delenv("PORT", raising=False)
    monkeypatch.delenv("HOST", raising=False)

    assert _default_transport() == "stdio"
    assert _host() == "127.0.0.1"
    assert _port() == 8000


def test_port_switches_default_to_streamable_http(monkeypatch):
    monkeypatch.delenv("MCP_TRANSPORT", raising=False)
    monkeypatch.setenv("PORT", "9090")
    monkeypatch.delenv("HOST", raising=False)

    assert _default_transport() == "streamable-http"
    assert _host() == "0.0.0.0"
    assert _port() == 9090


def test_explicit_transport_overrides_port(monkeypatch):
    monkeypatch.setenv("MCP_TRANSPORT", "stdio")
    monkeypatch.setenv("PORT", "9090")

    assert _default_transport() == "stdio"


def test_invalid_transport_fails(monkeypatch):
    monkeypatch.setenv("MCP_TRANSPORT", "http")

    with pytest.raises(ValueError, match="MCP_TRANSPORT"):
        _default_transport()


def test_adds_required_accept_header_when_missing():
    assert _ensure_mcp_accept_header([]) == [(b"accept", MCP_ACCEPT_HEADER)]


def test_replaces_incompatible_accept_header():
    headers = [(b"host", b"example.test"), (b"accept", b"application/json")]

    assert _ensure_mcp_accept_header(headers) == [
        (b"host", b"example.test"),
        (b"accept", MCP_ACCEPT_HEADER),
    ]


@pytest.mark.anyio
async def test_all_tools_publish_output_schemas():
    tools = await mcp.list_tools()

    assert {tool.name for tool in tools} == {
        "list_coffee_menu",
        "recommend_coffee",
        "explain_recommendation",
    }
    assert all(tool.outputSchema is not None for tool in tools)

    for tool in tools:
        assert "anyOf" not in str(tool.inputSchema)


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
