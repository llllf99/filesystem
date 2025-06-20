

from mcp.server.fastmcp import FastMCP

import tools
from core.types import BaseTool

# Define the MCP server
server = FastMCP(name="file-reader-server", version="1.0.0")

def register_tools():
    tools_list: list[BaseTool]   = [
        tools.ReadFileTool(),
        tools.ReadMultipleFilesTool(),
        tools.WriteFileTool(),
        tools.EditFileTool(),
        tools.CreateDirectoryTool(),
        tools.ListDirectoryTool(),
        tools.ListDirectoryWithSizeTool(),
        tools.DirectoryTreeTool(),
    ]
    for tool in tools_list:
        server.add_tool(
            fn=tool.callback(),
            name=tool.name,
            description=tool.description,
        )



if __name__ == "__main__":
    # Register tools
    register_tools()
    server.run()