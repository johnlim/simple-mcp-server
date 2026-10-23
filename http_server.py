from mcp.server.mcpserver import MCPServer

mcp = MCPServer("My-HTTP-MCP-Server")

@mcp.tool()
def calculate_square(number: float) -> str:
    """Calculates the square of a given number."""
    return f"The square of {number} is {number ** 2}."

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
