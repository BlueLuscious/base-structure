# Discord Repository Notifications

This document explains the optional Discord notification workflow defined in
`.github/workflows/discord.yaml`.

See also:

- `README.md`
- `docs/project.md`

## Purpose

The workflow sends repository lifecycle notifications to one Discord channel.
It is project-neutral and can be retained, disabled, or removed without
affecting the Django runtime.

Current notifications cover:

- commits pushed to configured branches
- branch creation and deletion
- pull requests opened, reopened, synchronized, merged, or closed
- completed `Continuous Integration` workflow runs

Pull Request actions use distinct colors so their state remains visible in the
Discord timeline. Branch creation and deletion share one lifecycle step while
preserving their own title, color, and icon.

Continuous Integration results use:

- green for success
- red for failure
- gray for cancellation
- yellow for any other conclusion

The CI notification links directly to the completed workflow run and uses the
same optional `DISCORD_WEBHOOK` secret. It runs through `workflow_run`, so
Discord delivery is not part of the CI job and cannot change the CI
conclusion.

The `workflow_run` trigger becomes active when this workflow exists on the
repository default branch.

## Setup

Create a GitHub Actions repository secret named:

```text
DISCORD_WEBHOOK
```

Set its value to the target Discord channel webhook URL. Do not store webhook
URLs in tracked files, environment examples, workflow output, or documentation.

The workflow reads repository and event data through step-level environment
variables. The webhook itself is exposed once at job level.

## Supported Branches

Push notifications currently watch:

- `master`
- `develop`
- `feature/**`
- `bugfix/**`
- `fix/**`
- `enhancement/**`
- `test/**`

Pull Request notifications currently target `master` and `develop`.

Continuous Integration notifications follow completed runs of the workflow
named `Continuous Integration`; their branch coverage comes from that
workflow's own trigger configuration.

Update these filters in `.github/workflows/discord.yaml` when a derived project
uses a different branch strategy.

## Disabling The Workflow

Use one of these approaches:

- disable the workflow from the GitHub Actions interface when notifications are
  paused temporarily
- remove `.github/workflows/discord.yaml` when the derived project will not use
  Discord notifications

Removing only the `DISCORD_WEBHOOK` secret is not the preferred disablement
strategy because workflow runs would still be scheduled.

## Maintenance

When changing the workflow:

- preserve valid Unicode icons
- keep secrets out of `run` scripts and output
- keep GitHub event values in explicit environment variables
- validate YAML, GitHub expressions, shell branches, and JQ payloads
- exercise every supported event before considering a lifecycle change complete
