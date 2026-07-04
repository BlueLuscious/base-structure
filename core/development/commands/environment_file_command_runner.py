"""Run one project command with environment values loaded from a file."""

import argparse
import os
import subprocess
from pathlib import Path
from typing import Sequence


class EnvironmentFileCommandRunner:
    """Load a simple dotenv file and execute one child command."""

    def __init__(self, env_file: Path) -> None:
        """Initialize the runner.

        Args:
            env_file: Dotenv-style file to load before executing the command.
        """
        self.env_file = env_file

    def run(self, command: Sequence[str]) -> int:
        """Execute a command with the merged local environment.

        Args:
            command: Executable and arguments to run.

        Returns:
            int: Child-process exit code.
        """
        environment = os.environ.copy()
        environment.update(self._read_environment())
        completed_process = subprocess.run(command, env=environment, check=False)
        return completed_process.returncode

    def _read_environment(self) -> dict[str, str]:
        """Read environment entries from the configured file.

        Returns:
            dict[str, str]: Parsed environment names and values.

        Raises:
            ValueError: When a non-comment line does not contain a valid assignment.
        """
        environment: dict[str, str] = {}
        for line_number, raw_line in enumerate(
            self.env_file.read_text(encoding="utf-8-sig").splitlines(),
            start=1,
        ):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("export "):
                line = line.removeprefix("export ").lstrip()

            if "=" not in line:
                raise ValueError(f"{self.env_file}:{line_number}: expected NAME=VALUE.")

            name, raw_value = line.split("=", maxsplit=1)
            name = name.strip()
            if not name or not name.replace("_", "").isalnum() or name[0].isdigit():
                raise ValueError(f"{self.env_file}:{line_number}: invalid environment name {name!r}.")

            value = raw_value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            environment[name] = value

        return environment


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser.

    Returns:
        argparse.ArgumentParser: Configured parser.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    return parser


def main() -> int:
    """Load the selected environment and execute the requested command.

    Returns:
        int: Child-process exit code.
    """
    arguments = build_argument_parser().parse_args()
    command = arguments.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        raise ValueError("A command is required after --.")

    return EnvironmentFileCommandRunner(arguments.env_file).run(command)


if __name__ == "__main__":
    raise SystemExit(main())
