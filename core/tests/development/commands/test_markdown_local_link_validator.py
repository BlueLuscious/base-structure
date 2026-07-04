"""Tests for the repository Markdown local-link validator."""

from pathlib import Path
from tempfile import TemporaryDirectory

from core.development.commands.markdown_local_link_validator import MarkdownLocalLinkValidator
from core.testing import LoggedTestCase


class TestMarkdownLocalLinkValidator(LoggedTestCase):
    """Validate local-link discovery without network requests."""

    def test_validate_reports_only_missing_local_targets(self) -> None:
        """Ignore external and fenced links while reporting missing local files."""
        with TemporaryDirectory() as temporary_directory:
            repository_root = Path(temporary_directory)
            docs_path = repository_root / "docs"
            docs_path.mkdir()
            (repository_root / "manage.py").touch()
            (repository_root / "existing.md").write_text("# Existing", encoding="utf-8")
            (repository_root / "README.md").write_text(
                "\n".join(
                    (
                        "[Existing](existing.md)",
                        "[Missing](missing.md)",
                        "[External](https://example.com)",
                        "```markdown",
                        "[Example placeholder](placeholder.md)",
                        "```",
                    )
                ),
                encoding="utf-8",
            )
            (docs_path / "guide.md").write_text("[Root](../README.md)", encoding="utf-8")

            errors = MarkdownLocalLinkValidator(repository_root).validate()

        self.assertEqual(["README.md:2: missing local target 'missing.md'"], errors)

    def test_discover_repository_root_walks_up_from_the_command_file(self) -> None:
        """Find the repository root from one nested command-module path."""
        with TemporaryDirectory() as temporary_directory:
            repository_root = Path(temporary_directory)
            command_path = repository_root / "core" / "development" / "commands" / "command.py"
            command_path.parent.mkdir(parents=True)
            command_path.touch()
            (repository_root / "manage.py").touch()
            (repository_root / "README.md").touch()

            resolved_root = MarkdownLocalLinkValidator.discover_repository_root(command_path)

        self.assertEqual(repository_root.resolve(), resolved_root)
