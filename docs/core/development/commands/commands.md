# Core Development Commands

The modules under `core/development/commands/` support repository-owned local
tooling and CI.

They are not Django management commands. Django management commands belong
under an installed app's `management/commands/` package and are invoked through
`manage.py`.

## Environment File Command Runner

`EnvironmentFileCommandRunner` loads one selected environment file and starts
one child process without evaluating values through a shell.

Supported environment-file syntax:

- empty lines
- full-line comments
- `NAME=VALUE`
- `export NAME=VALUE`
- complete values wrapped in matching single or double quotes

Shell interpolation and inline expression execution are intentionally not
supported.

VS Code Django tasks use this command because `tasks.json` has no portable
equivalent to the debugger's `envFile` property. See `docs/vscode/tasks.md` for
the user-facing task contract.

## Markdown Local-Link Validator

`MarkdownLocalLinkValidator` discovers the repository root from `manage.py`
and `README.md`, then checks local file targets in:

- the root `README.md`
- Markdown documents under `docs/`

External URLs, document-only anchors, and links inside fenced code examples do
not require filesystem targets. The validator performs no network requests.

CI runs this command as part of the `Python quality` job.
