---
name: cafe-recommendation-skill
description: Coffee recommendation skill that calls the deployed cafe MCP server. Use when the user asks for coffee menu exploration, drink recommendations, caffeine preference matching, hot or cold coffee choices, milk preference matching, or explanation of why a coffee fits the user's mood and preferences.
---

# Cafe Recommendation Skill

Use this skill when the user wants coffee menu exploration or a coffee recommendation through the deployed `cafe-mcp-server` MCP demo.

## What This Skill Does

- Lists the available demo coffee menu.
- Recommends one coffee based on mood, milk preference, caffeine level, and hot/cold preference.
- Explains why a coffee fits or does not fit the provided preferences.

## MCP Server

Use the deployed Streamable HTTP/SSE MCP endpoint:

`https://cafe-mcp-server-git-695741304915.us-west1.run.app/mcp`

Local source code lives at:

`/Users/hanlufeng/Desktop/AI-INSIGHT-REPORT/Ceilia/cafe-mcp-server`

It exposes these tools:

- `list_coffee_menu`
- `recommend_coffee`
- `explain_recommendation`

## Input Guidance

Ask for missing preferences only when needed. The server works with partial input, so it is usually better to call `recommend_coffee` with what the user already said.

Supported structured preferences:

- `prefer_milk`: `true`, `false`, or omitted
- `caffeine`: `low`, `medium`, or `high`
- `temperature`: `hot` or `cold`
- `mood`: any short text, such as `smooth iced`, `quick energy`, `creamy`, or `evening`

## Response Style

Return the recommendation directly, then briefly explain the strongest matching signals. Keep the response practical and do not mention external APIs or API keys unless the user asks about setup.

## MCP Connection

Configure the platform MCP plugin/client to use:

- URL: `https://cafe-mcp-server-git-695741304915.us-west1.run.app/mcp`
- Transport: Streamable HTTP/SSE
- Authentication: none for this demo
- Accept header: `application/json, text/event-stream`

Use `mcp-config.example.json` in this skill directory as a starting point for client configuration.

For local development only, see `mcp-config.local.example.json`.
