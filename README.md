# MCP Server and Client Test Scenarios

This document outlines the steps to test the MCP server setup and client-server interaction.

## Scenario 1: Test MCP Server Setup

This scenario verifies the basic functionality of the MCP server.

* **File:** `src/servers/server.py`
* **Run Command:** `mcp dev src/servers/server.py`
* After running the command, the MCP inspector will open in your web browser. Use the inspector to verify that the server is running correctly.
* **Example Inspector URL:** `http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=def336fb32f8f2b8f6be1f497ebd3c49cc0e2a9b9f0b3335ee6ae3e0db92f9ad`

---

## Scenario 2: Test Client-Server Interaction

This scenario tests the interaction between a client and a server that can execute shell commands. The `server2.py` script will run any shell command passed to the client during interaction.

* **Client Script:** `src/clients/client.py`
* **Server Script:** `src/servers/server2.py`
* **Run Command:** `python src/clients/client.py src/servers/server2.py`
