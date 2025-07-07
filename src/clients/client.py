#!/usr/bin/env python
"""
MCP client that connects to an MCP server, loads tools, and runs a chat loop using gpt-4.
"""

import asyncio
import os
import sys
import json
from contextlib import AsyncExitStack
from typing import Optional, List

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv("/Users/mayurk/.env")

# Custom JSON encoder for objects with 'content' attribute
class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "content"):
            return {"type": o.__class__.__name__, "content": o.content}
        return super().default(o)

# Instantiate OpenAI LLM with deterministic output and retry logic
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    max_retries=2
)
# Require server script path as command-line argument
if len(sys.argv) < 2:
    print("Usage: python genai_bind_tools.py <path_to_server_script>")
    sys.exit(1)
server_script = sys.argv[1]

# Configure MCP server startup parameters
server_params = StdioServerParameters(
    command="python" if server_script.endswith(".py") else "node",
    args=[server_script],
)

# Global holder for the active MCP session (used by tool adapter)
mcp_client = None

# Main async function: connect, load tools, create agent, run chat loop
async def run_agent():
    global mcp_client
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_client = type("MCPClientHolder", (), {"session": session})()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(llm, tools)
            print("MCP Client Started! Type 'quit' to exit.")
            while True:
                query = input("\\nQuery: ").strip()
                if query.lower() == "quit":
                    break
                # Send user query to agent and print formatted response
                response = await agent.ainvoke({"messages": query})
                try:
                    formatted = json.dumps(response, indent=2, cls=CustomEncoder)
                except Exception:
                    formatted = str(response)
                print("\\nResponse:")
                print(formatted)
    return

# Entry point: run the async agent loop
if __name__ == "__main__":
    asyncio.run(run_agent())

