from src.servers.server import mcp
def main():
    print("Hello from letsmcp!")


if __name__ == "__main__":
    mcp.run(transport="stdio")
