"""FastMCP server exposing local coffee recommendation tools."""

from __future__ import annotations

import os
from typing import Any, Literal

from mcp.server.fastmcp import FastMCP
from starlette.types import ASGIApp, Receive, Scope, Send
import uvicorn

from .recommender import explain_recommendation as build_explanation
from .recommender import list_menu, recommend_coffee as choose_coffee

Transport = Literal["stdio", "sse", "streamable-http"]
MCP_ACCEPT_HEADER = b"application/json, text/event-stream"


def _ensure_mcp_accept_header(headers: list[tuple[bytes, bytes]]) -> list[tuple[bytes, bytes]]:
    """Make Streamable MCP discovery compatible with XiaoYi's HTTP client."""
    return [
        (key, MCP_ACCEPT_HEADER) if key.lower() == b"accept" else (key, value)
        for key, value in headers
    ] or [(b"accept", MCP_ACCEPT_HEADER)]


class XiaoYiAcceptCompatibilityMiddleware:
    """Supply the Streamable MCP media types XiaoYi omits during tool discovery."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http" and scope["path"] == "/mcp":
            scope = {**scope, "headers": _ensure_mcp_accept_header(list(scope["headers"]))}
        await self.app(scope, receive, send)


def _default_transport() -> Transport:
    transport = os.getenv("MCP_TRANSPORT")
    if transport:
        if transport not in {"stdio", "sse", "streamable-http"}:
            raise ValueError("MCP_TRANSPORT must be one of: stdio, sse, streamable-http")
        return transport  # type: ignore[return-value]

    if os.getenv("PORT"):
        return "streamable-http"

    return "stdio"


def _host() -> str:
    return os.getenv("HOST", "0.0.0.0" if os.getenv("PORT") else "127.0.0.1")


def _port() -> int:
    return int(os.getenv("PORT", "8000"))


mcp = FastMCP(
    "cafe-recommendation",
    host=_host(),
    port=_port(),
    streamable_http_path=os.getenv("MCP_PATH", "/mcp"),
)


@mcp.tool()
def list_coffee_menu() -> list[dict]:
    """List all available coffee menu items."""
    return list_menu()


@mcp.tool()
def recommend_coffee(
    mood: str = "",
    prefer_milk: bool | None = None,
    caffeine: str | None = None,
    temperature: str | None = None,
) -> dict[str, Any]:
    """Recommend a coffee from mood and simple preferences.

    Args:
        mood: Free-text preference such as "smooth iced" or "quick energy".
        prefer_milk: True for milk drinks, False for black coffee, None for either.
        caffeine: Optional caffeine level: low, medium, or high.
        temperature: Optional drink style: hot or cold.
    """
    return choose_coffee(
        mood=mood,
        prefer_milk=prefer_milk,
        caffeine=caffeine,
        temperature=temperature,
    )


@mcp.tool()
def explain_recommendation(
    coffee_id: str,
    mood: str = "",
    prefer_milk: bool | None = None,
    caffeine: str | None = None,
    temperature: str | None = None,
) -> str:
    """Explain a coffee choice against the same preference inputs."""
    return build_explanation(
        coffee_id=coffee_id,
        mood=mood,
        prefer_milk=prefer_milk,
        caffeine=caffeine,
        temperature=temperature,
    )


def main() -> None:
    """Run stdio locally, or Streamable HTTP on Cloud Run when PORT is set."""
    transport = _default_transport()
    if transport == "streamable-http":
        app = XiaoYiAcceptCompatibilityMiddleware(mcp.streamable_http_app())
        uvicorn.run(app, host=_host(), port=_port())
        return

    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
