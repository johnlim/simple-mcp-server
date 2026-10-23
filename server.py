import datetime
from mcp.server.mcpserver import MCPServer 

# 1. Initialize the MCP Server
mcp = MCPServer("QuickStart-Server")

# 2. Expose the data as a TOOL instead of a resource
@mcp.tool()
def get_server_status() -> str:
    """
    Provides a quick operational status update on this specific server instance.
    Use this when the user asks for the status or condition of the server.
    """
    return "The local Python MCP server is online, secure, and ready to assist."

# 3. Expose your existing Time Tool
@mcp.tool()
def get_current_time(city: str) -> str:
    """
    Fetches the current local system time. Use this when the user asks for the time.
    
    Args:
        city: The name of the city the user is asking about.
    """
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time in {city} is {now} (based on server system clock)."

# 4. Run the server using default v2 pipelines
if __name__ == "__main__":
    mcp.run()

