# Admin Sites

This document explains the purpose and structure of `core/adminsites/`.

## Goal

`core/adminsites/` contains project-level admin infrastructure shared across apps.

It exists to define:

- custom `AdminSite` classes
- admin site namespaces
- shared admin site instances
- the Unfold integration layer used by those sites

The package should stay focused on project-wide admin infrastructure, not domain-specific admin implementations.

## Current Structure

Current contents:

- `admin_namespace.py`
- `registry.py`
- `site_instances.py`
- `sites/`
- `unfold/`

## Responsibilities

### `admin_namespace.py`

Defines the project admin namespaces used for routing and site resolution.

Current namespaces:

- `master_admin`
- `owner_admin`

### `registry.py`

Maps each admin namespace to its corresponding admin site class.

This registry is project admin infrastructure. It should not contain Unfold-specific behavior.

### `site_instances.py`

Creates the concrete shared admin site instances used by:

- `core/urls.py`
- admin registration modules

These instances are the actual Django admin site objects exposed by the project.

### `sites/`

Contains the admin site class hierarchy.

Current site classes:

- `BaseAdminSite`
- `MasterAdminSite`
- `OwnerAdminSite`

Rules:

- keep one principal class per file
- keep shared default behavior in the base site
- let concrete sites override hooks rather than duplicating wiring

### `unfold/`

Contains the adapter layer between the custom admin sites and Unfold settings.

This package should translate site metadata and hooks into the settings format expected by Unfold.

It should not become a second source of truth for site identity.

## Design Rules

The source of truth for site identity should remain the site classes themselves.

Examples:

- `site_title`
- `site_header`
- `site_symbol`
- `site_url`
- per-site sidebar hooks

The Unfold layer should adapt those values, not redefine them independently.

## Relationship With App Admins

`core/adminsites/` should define the shared admin infrastructure only.

App-specific admin implementations should live in their respective apps.

Recommended structure:

```text
<app>/admin/
  master/
  owner/
```

Examples:

- `accounts/admin/master/`
- `catalog/admin/owner/`

This keeps:

- site infrastructure in `core`
- domain admin logic close to each app

## Current Behavior

### `MasterAdminSite`

Intended for technical platform administrators.

Characteristics:

- active superusers only
- full Django-style admin visibility
- custom master sidebar navigation

### `OwnerAdminSite`

Intended for business owners and operators.

Characteristics:

- active staff users
- guided domain-specific admin experience
- simpler navigation than the master site

## Maintenance Rule

If a concern is shared by all admin sites, place it in:

- `sites/base_admin_site.py`
- or the `unfold/` adapter layer when it is Unfold-specific

If a concern is specific to one domain app, keep it inside that app instead of growing `core/adminsites/`.
