# VS Code Launch Configurations

This document owns the debugger-oriented and long-running processes exposed
through `.vscode/launch.json`.

## Launch Ownership

The available configurations are:

- `Django: Run Server`
- `Django: Shell`
- `Django: Test`
- `Django: Test All`
- `Celery: Worker`
- `Celery: Beat`

Finite management, quality, dependency, and Docker commands belong in
`.vscode/tasks.json` and are documented in `docs/vscode/tasks.md`.

## Running A Configuration

Open the **Run and Debug** view, select one configuration, and start it with
the normal VS Code debug action.

Launch configurations load `.env` through `envFile` and use the Python
interpreter selected by the Python extension.

`Django: Test` requests one target and passes it to Django's test command.
`Django: Test All` runs `python manage.py test` without labels so tests from
future installed apps are discovered automatically.

Worker and Beat remain separate configurations because they are independent
long-running processes. Start Redis before running them when the selected
environment uses Redis as broker or result backend.
