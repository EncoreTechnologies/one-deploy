Role: opennebula.deploy.repository
==================================

A role that creates various package repository configs on Debian/RedHat-like distros.

Requirements
------------

N/A

Role Variables
--------------

| Name                            | Type   | Default       | Example             | Description                                                           |
|---------------------------------|--------|---------------|---------------------|-----------------------------------------------------------------------|
| `one_version`                   | `str`  | `6.8`         | `6.8.3`             | OpenNebula version (CE/EE is decided by the presence of `one_token`). |
| `one_token`                     | `str`  | undefined     | `asd123as:123asd12` | OpenNebula Enterprise Edition subscription token.                     |
| `repos_enabled`                 | `list` | (check below) | `[frr]`             | Enable installation of specific repos.                                |
|                                 |        |               |                     |                                                                       |
| `ceph_repo_enabled`             | `bool` | `true`        | `false`             | Hard-disable Ceph repo creation (overrides `repos_enabled`).          |
| `ceph_repo_force_trusted`       | `bool` | `false`       |                     | Disable Ceph GPG / SSL repo verification.                             |
| `ceph_repo_key_path`            | `dict` |               |                     | Ceph GPG key paths for Debian/RedHat distros.                         |
| `ceph_repo_key_url`             | `dict` |               |                     | Ceph GPG key urls for Debian/RedHat distros.                          |
| `ceph_repo_path`                | `dict` |               |                     | Ceph repo definition paths for Debian/RedHat distros.                 |
| `ceph_repo_url`                 | `dict` |               |                     | Ceph repo url for Debian/RedHat distros.                              |
|                                 |        |               |                     |                                                                       |
| `frr_repo_enabled`              | `bool` | `true`        | `false`             | Hard-disable FRR repo creation (overrides `repos_enabled`).           |
| `frr_repo_force_trusted`        | `bool` | `false`       |                     | Disable FRR GPG / SSL repo verification.                             |
| `frr_repo_key_path`             | `dict` |               |                     | FRR GPG key paths for Debian/RedHat distros.                          |
| `frr_repo_key_url`              | `dict` |               |                     | FRR GPG key urls for Debian/RedHat distros.                           |
| `frr_repo_path`                 | `dict` |               |                     | FRR repo definition paths for Debian/RedHat distros.                  |
| `frr_repo_url`                  | `dict` |               |                     | FRR repo url for Debian/RedHat distros.                               |
|                                 |        |               |                     |                                                                       |
| `grafana_repo_enabled`          | `bool` | `true`        | `false`             | Hard-disable Grafana repo creation (overrides `repos_enabled`).      |
| `grafana_repo_force_trusted`    | `bool` | `false`       |                     | Disable Grafana GPG / SSL repo verification.                          |
| `grafana_repo_key_path`         | `dict` |               |                     | Grafana GPG key paths for Debian/RedHat distros.                      |
| `grafana_repo_key_url`          | `dict` |               |                     | Grafana GPG key urls for Debian/RedHat distros.                       |
| `grafana_repo_path`             | `dict` |               |                     | Grafana repo definition paths for Debian/RedHat distros.              |
| `grafana_repo_url`              | `dict` |               |                     | Grafana repo url for Debian/RedHat distros.                           |
|                                 |        |               |                     |                                                                       |
| `opennebula_repo_enabled`       | `bool` | `true`        | `false`             | Hard-disable OpenNebula repo creation (overrides `repos_enabled`).  |
| `opennebula_repo_force_trusted` | `bool` | `false`       |                     | Disable OpenNebula GPG / SSL repo verification.                       |
| `opennebula_repo_key_path`      | `dict` |               |                     | OpenNebula GPG key paths for Debian/RedHat distros.                   |
| `opennebula_repo_key_url`       | `dict` |               |                     | OpenNebula GPG key urls for Debian/RedHat distros.                    |
| `opennebula_repo_path`          | `dict` |               |                     | OpenNebula repo definition paths for Debian/RedHat distros.           |
| `opennebula_repo_url`           | `dict` |               | (check below)       | OpenNebula repo url for Debian/RedHat distros.                        |
| `opennebula_repo_pre_enable`    | `dict` |               | (check below)       | Definition of DNF repos to pre-enable in RedHat-like distros.         |

Dependencies
------------

N/A

> **NOTE on `repos_enabled`:** This list is *not* a persistent hard-disable
> switch. Each consumer role (e.g. `opennebula/server`, `gate`, `flow`,
> `provision`, `kvm`, `prometheus/*`, `gui`, `frr/common`, `ceph/repository`)
> re-includes this role with its own `repos_enabled: [<that-repo>]` via
> `include_role ... vars:`, which overrides any inventory-level value for the
> duration of the include (Ansible include params have the highest variable
> precedence). The include is guarded by `when: <name>_repo is undefined`,
> so it is triggered whenever the repo task file hasn't registered a result.
> Removing a repo from `repos_enabled` therefore only skips the *top-level*
> pass; downstream roles will re-create the repo on demand.
>
> To genuinely prevent a repo's `.list` / `.repo` file and GPG key from being
> created, set the corresponding per-repo `*_repo_enabled: false` variable.
> Gating lives inside the per-repo task file, so the skip cannot be
> overridden by a downstream re-include, and the registered result is a
> "skipped" (still defined) value which short-circuits the consumers'
> `when: <name>_repo is undefined` guards.

Example Playbook
----------------

    - hosts: frontend:node
      vars:
        repos_enabled: [ceph, frr, grafana, opennebula] # defaults

        # Don't create the OpenNebula apt/yum repo (e.g. packages are
        # already provided by a site-local mirror configured out-of-band).
        opennebula_repo_enabled: false

        # Enable OpenNebula EE repo.
        one_token: 'asd123as:123asd12'

        # Enable only 'epel' and 'crb' DNF repos in Alma Linux 9
        opennebula_repo_pre_enable:
          AlmaLinux:
            config_manager:
              '9': [epel, crb]

        # Use custom / local / insecure OpenNebula repo.
        opennebula_repo_force_trusted: true
        opennebula_repo_url:
          RedHat: http://10.11.12.13/repo/6.8/AlmaLinux/
          Ubuntu: http://10.11.12.13/repo/6.8/Ubuntu/22.04/
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.repository

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
