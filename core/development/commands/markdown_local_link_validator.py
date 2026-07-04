"""Validate local file targets in repository Markdown documents."""

import re
import sys
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import unquote


class MarkdownLocalLinkValidator:
    """Validate local Markdown links without requesting external URLs."""

    LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\((?P<target><[^>]+>|[^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
    EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#")

    def __init__(self, repository_root: Path) -> None:
        """Initialize the validator.

        Args:
            repository_root: Absolute or relative repository root path.
        """
        self.repository_root = repository_root.resolve()

    @staticmethod
    def discover_repository_root(start_path: Path) -> Path:
        """Find the project root that owns the command module.

        Args:
            start_path: File or directory located inside the repository.

        Returns:
            Path: Repository root containing `manage.py` and `README.md`.

        Raises:
            ValueError: When no repository root can be found.
        """
        resolved_path = start_path.resolve()
        search_paths = (resolved_path, *resolved_path.parents) if resolved_path.is_dir() else resolved_path.parents
        for candidate in search_paths:
            if (candidate / "manage.py").is_file() and (candidate / "README.md").is_file():
                return candidate
        raise ValueError(f"Could not find the repository root from {start_path}.")

    def validate(self) -> list[str]:
        """Validate every local Markdown target.

        Returns:
            list[str]: Human-readable validation errors.
        """
        errors: list[str] = []
        for document_path in self._iter_documents():
            for line_number, target in self._iter_local_targets(document_path):
                target_path = self._resolve_target(document_path, target)
                if not target_path.exists():
                    relative_document = document_path.relative_to(self.repository_root)
                    errors.append(f"{relative_document}:{line_number}: missing local target {target!r}")
        return errors

    def _iter_documents(self) -> Iterator[Path]:
        """Yield repository Markdown documents.

        Returns:
            Iterator[Path]: README and documentation Markdown paths.
        """
        readme_path = self.repository_root / "README.md"
        if readme_path.exists():
            yield readme_path
        yield from sorted((self.repository_root / "docs").rglob("*.md"))

    def _iter_local_targets(self, document_path: Path) -> Iterator[tuple[int, str]]:
        """Yield local link targets outside fenced code blocks.

        Args:
            document_path: Markdown document to inspect.

        Returns:
            Iterator[tuple[int, str]]: Line numbers and local targets.
        """
        inside_fence = False
        for line_number, line in enumerate(
            document_path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            stripped_line = line.lstrip()
            if stripped_line.startswith(("```", "~~~")):
                inside_fence = not inside_fence
                continue
            if inside_fence:
                continue

            for match in self.LINK_PATTERN.finditer(line):
                target = match.group("target").strip("<>")
                if not target.lower().startswith(self.EXTERNAL_PREFIXES):
                    yield line_number, target

    def _resolve_target(self, document_path: Path, target: str) -> Path:
        """Resolve one local target relative to its owning document.

        Args:
            document_path: Markdown document containing the target.
            target: Raw Markdown link target.

        Returns:
            Path: Resolved local filesystem target.
        """
        path_without_fragment = unquote(target.split("#", maxsplit=1)[0])
        return (document_path.parent / path_without_fragment).resolve()


def main() -> int:
    """Run local Markdown link validation.

    Returns:
        int: Zero when all local targets exist, otherwise one.
    """
    repository_root = MarkdownLocalLinkValidator.discover_repository_root(Path(__file__))
    validator = MarkdownLocalLinkValidator(repository_root)
    errors = validator.validate()
    if errors:
        print("\n".join(errors))
        return 1

    print("All local Markdown links are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
