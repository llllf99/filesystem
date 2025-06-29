# Filesystem MCP Server

Python server implementing Model Context Protocol (MCP) for filesystem operations.

## Features

- Read/write files
- Create/list/delete directories
- Move files/directories
- Search files
- Get file metadata

**Note**: The server will only allow operations within directories specified via `args`.

## API

### Resources

- `file://system`: File system operations interface

### Tools

- **read_file**
  - Read complete contents of a file
  - Input: `path` (string)
  - Reads complete file contents with UTF-8 encoding

- **read_multiple_files**
  - Read multiple files simultaneously
  - Input: `paths` (string[])
  - Failed reads won't stop the entire operation

- **write_file**
  - Create new file or overwrite existing (exercise caution with this)
  - Inputs:
    - `path` (string): File location
    - `content` (string): File content

- **edit_file**
  - Make selective edits using advanced pattern matching and formatting
  - Features:
    - Line-based and multi-line content matching
    - Whitespace normalization with indentation preservation
    - Multiple simultaneous edits with correct positioning
    - Indentation style detection and preservation
    - Git-style diff output with context
    - Preview changes with dry run mode
  - Inputs:
    - `path` (string): File to edit
    - `edits` (array): List of edit operations
      - `oldText` (string): Text to search for (can be substring)
      - `newText` (string): Text to replace with
    - `dryRun` (boolean): Preview changes without applying (default: false)
  - Returns detailed diff and match information for dry runs, otherwise applies changes
  - Best Practice: Always use dryRun first to preview changes before applying them

- **create_directory**
  - Create new directory or ensure it exists
  - Input: `path` (string)
  - Creates parent directories if needed
  - Succeeds silently if directory exists

- **list_directory**
  - List directory contents with [FILE] or [DIR] prefixes
  - Input: `path` (string)

- **move_file**
  - Move or rename files and directories
  - Inputs:
    - `source` (string)
    - `destination` (string)
  - Fails if destination exists

- **search_files**
  - Recursively search for files/directories
  - Inputs:
    - `path` (string): Starting directory
    - `pattern` (string): Search pattern
    - `excludePatterns` (string[]): Exclude any patterns. Glob formats are supported.
  - Case-insensitive matching
  - Returns full paths to matches

- **get_file_info**
  - Get detailed file/directory metadata
  - Input: `path` (string)
  - Returns:
    - Size
    - Creation time
    - Modified time
    - Access time
    - Type (file/directory)
    - Permissions

- **list_allowed_directories**
  - List all directories the server is allowed to access
  - No input required
  - Returns:
    - Directories that this server can read/write from

## Installation

### git + Python

```bash
# Clone the repository
git clone https://github.com/MarcusJellinghaus/mcp_server_filesystem
cd filesystem

# Create and activate a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies using pip with pyproject.toml
pip install -e .

```


## Running the Server

Previous instal required

```bash
# Enable virtual env 
source .venv/bin/activate 
# Run server with allowed paths (paths optional but recommended)
python ./src/main.py  /path/to/home /path/to/project
```

Alternatively, you can use uvx to run directly from GH repo
uv required https://docs.astral.sh/uv/getting-started/installation/

```bash
uvx --from git+https://github.com/javillegasna/filesystem filesystem /Users/username/Desktop
```

## Usage with Different Platforms

### Claude Desktop
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/javillegasna/filesystem",
        "filesystem",
        "/Users/username/Desktop",
        "/path/to/other/allowed/dir",
      ]
    }
  }
}

```

### vscode
```json
{
  "mcp": {
    "servers": {
      "filesystem": {
        "command": "uvx",
        "args": [
        "--from",
        "git+https://github.com/javillegasna/filesystem",
        "filesystem",
        "/Users/username/Desktop",
        "/path/to/other/allowed/dir",
      ]
      }
    }
  }
}
```

