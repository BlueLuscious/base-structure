"""Tests for the local environment-file command runner."""

import os
from pathlib import Path
from subprocess import CompletedProcess
from tempfile import TemporaryDirectory
from unittest.mock import patch

from core.development.commands.environment_file_command_runner import EnvironmentFileCommandRunner
from core.testing import LoggedTestCase


class TestEnvironmentFileCommandRunner(LoggedTestCase):
    """Validate portable environment loading for local project tasks."""

    def test_run_merges_environment_values_and_preserves_command_arguments(self) -> None:
        """Load comments, exports, quoted values, and literal hash characters."""
        with TemporaryDirectory() as temporary_directory:
            env_file = Path(temporary_directory) / ".env"
            env_file.write_text(
                "\n".join(
                    (
                        "# Local environment",
                        "PLAIN=value",
                        'QUOTED="value with spaces"',
                        "export EXPORTED=available",
                        "SECRET=value#fragment",
                    )
                ),
                encoding="utf-8",
            )

            with patch(
                "core.development.commands.environment_file_command_runner.subprocess.run",
                return_value=CompletedProcess(args=[], returncode=7),
            ) as run_mock:
                with patch.dict(os.environ, {"INHERITED": "present"}, clear=True):
                    return_code = EnvironmentFileCommandRunner(env_file).run(("python", "manage.py", "check"))

        self.assertEqual(7, return_code)
        run_mock.assert_called_once()
        self.assertEqual(("python", "manage.py", "check"), run_mock.call_args.args[0])
        child_environment = run_mock.call_args.kwargs["env"]
        self.assertEqual("present", child_environment["INHERITED"])
        self.assertEqual("value", child_environment["PLAIN"])
        self.assertEqual("value with spaces", child_environment["QUOTED"])
        self.assertEqual("available", child_environment["EXPORTED"])
        self.assertEqual("value#fragment", child_environment["SECRET"])
        self.assertFalse(run_mock.call_args.kwargs["check"])

    def test_run_rejects_invalid_environment_assignments(self) -> None:
        """Reject malformed non-comment lines with an actionable error."""
        with TemporaryDirectory() as temporary_directory:
            env_file = Path(temporary_directory) / ".env"
            env_file.write_text("INVALID LINE", encoding="utf-8")

            with self.assertRaisesMessage(ValueError, f"{env_file}:1: expected NAME=VALUE."):
                EnvironmentFileCommandRunner(env_file).run(("python", "--version"))
