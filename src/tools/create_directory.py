import os

from mcp.types import TextContent
from pydantic import BaseModel

from core.enums import FileSystemTools
from core.types import BaseTool


class CreateDirectoryinput(BaseModel):
    path: str

TOOL_DESCRIPTION = f"""
    Create a new directory or ensure a directory exists. Can create multiple
    directories at once. If the directory already exists, this operation will succeed 
    silently. Perfect for setting up directory structures for projects or ensuring
    that required directories are present before performing other operations.
    @Input:
        input: The path to the file to read.
    @Output:
        text: The content of the file.
    @Schema: {CreateDirectoryinput.model_json_schema()}
"""

class CreateDirectoryTool(BaseTool):
    def __init__(self):
        super().__init__(
            inputSchema=CreateDirectoryinput.model_json_schema(),
            name=FileSystemTools.CREATE_DIRECTORY.value,
            description=TOOL_DESCRIPTION,
        )

    def _entrypoint(self, input: CreateDirectoryinput) -> TextContent:
        os.makedirs(input.path, exist_ok=True)
        return TextContent(
            type="text", 
            text=f"Directory created successfully at {input.path}",
        )
