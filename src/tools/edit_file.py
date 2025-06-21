import difflib
import re
from typing import Annotated

from mcp.types import TextContent
from pydantic import AfterValidator, BaseModel, Field

from core.enums import FileSystemTools
from core.formatters import normalize_line_endings
from core.types import BaseTool
from core.validations import validate_path


class EditOperation(BaseModel):
    old_text: str = Field(
        description="The text to be replaced",
        min_length=1,
        max_length=1000,
    )
    new_text: str = Field(
        description="The text to replace with",
        min_length=1,
        max_length=1000,
    )


class EditFileInput(BaseModel):
    path: Annotated[str, AfterValidator(validate_path)]
    edits: list[EditOperation]
    dry_run: bool = Field(
        description="Preview changes using git-style diff format",
        default=False,
    )


TOOL_DESCRIPTION = f"""
    Edits a file on the filesystem by replacing specified text with new text.
    @Input:
        old_text: The text to be replaced.
        new_text: The text to replace with.
        dry_run: If true, preview changes using git-style diff format.
    @Output:
        text: A string containing the diff of the changes made to the file.
    @Schema: {EditFileInput.model_json_schema()}
"""


class EditFileTool(BaseTool):
    def __init__(self):
        super().__init__(
            inputSchema=EditFileInput.model_json_schema(),
            name=FileSystemTools.EDIT_FILE.value,
            description=TOOL_DESCRIPTION,
        )

    def _entrypoint(self, input: EditFileInput) -> TextContent:
        """
        Edits a file by replacing specified text with new text.
        """
        with open(input.path, encoding="utf-8") as file:
            content = file.read()

        normalized_content = normalize_line_endings(content)

        for edit in input.edits:
            normalized_old_text = normalize_line_endings(edit.old_text)
            normalized_new_text = normalize_line_endings(edit.new_text)

            # if exact match is found, replace it
            if normalized_old_text in normalized_content:
                normalized_content = normalized_content.replace(
                    normalized_old_text,
                    normalized_new_text,
                )
            # otherwise, try line-by-line replacement
            old_lines = normalized_old_text.splitlines()
            content_lines = normalized_content.splitlines()
            match_found = False

            for i in range(len(content_lines) - len(old_lines) + 1):
                potential_match = content_lines[i : i + len(old_lines)]
                valid_match = all(
                    old_line.strip() == content_line.strip()
                    for old_line, content_line in zip(old_lines, potential_match)
                )
                if valid_match:
                    match = re.match(r"^\s*", content_lines[i])
                    original_indent = match.group(0) if match else ""
                    new_lines = [
                        (original_indent + line.lstrip()) if j == 0 else line
                        for j, line in enumerate(normalized_new_text.splitlines())
                    ]
                    content_lines[i : i + len(old_lines)] = new_lines
                    normalized_content = "\n".join(content_lines)
                    match_found = True
                    break

            if not match_found:
                raise ValueError(
                    f"Could not find exact match for edit: {edit.old_text}"
                )

        if not input.dry_run:
            with open(input.path, "w", encoding="utf-8") as file:
                file.write(normalized_content)

        diff = self._create_unified_diff(content, normalized_content, input.path)
        formattedDiff = self._format_diff_with_backticks(diff)
        return TextContent(text=formattedDiff, type="text")

    def _create_unified_diff(
        self,
        original_content: str,
        new_content: str,
        filepath: str = "file",
    ) -> str:
        """Create a unified diff between the original and new content."""
        normalized_original = normalize_line_endings(original_content)
        normalized_new = normalize_line_endings(new_content)

        diff = difflib.unified_diff(
            normalized_original.splitlines(),
            normalized_new.splitlines(),
            fromfile=f"{filepath} (original)",
            tofile=f"{filepath} (modified)",
            lineterm="",
        )
        return "\n".join(diff)

    def _format_diff_with_backticks(self, diff: str) -> str:
        """Format a diff with an appropriate number of backticks."""
        num_backticks = 3
        while "`" * num_backticks in diff:
            num_backticks += 1
        backticks = "`" * num_backticks
        return f"{backticks}diff\n{diff}\n{backticks}\n\n"
