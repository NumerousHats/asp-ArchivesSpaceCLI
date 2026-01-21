# ascli: A command-line tool to work with the ArchivesSpace API

`ascli` is an attempt to ease some of the pain points associated with the creation and modification of records in [ArchivesSpace](www.archivesspace.org). It currently focuses on the management of containers and resources. It is a subcommand-style CLI (like `git` and `apt-get`) that modularizes different aspects of the creation and management of ArchivesSpace data records.

This project is not fully "ready for prime time". Currently, only commands that have immediate usefulness for the author's archival work are being implemented. It has not been extensively tested, so please use with caution. Editing of existing records runs the risk of data corruption, so *please make backups* before attempting any such operations.

`ascli` is built on [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake). You will need to create an `.archivessnake.yml` file as described in the ArchivesSnake documentation to store the login credentials for your ArchivesSpace instance. The ArchivesSpace API session key is cached between runs of `ascli` in order to improve responsiveness and overall user experience, especially for commands that do not actually hit the API. Token expiration and re-authentication should be handled transparently. If there are authentication errors (or if you have security concerns), the stored token can be cleared using `ascli cc token`.

# Installation

This project is currently not available on PyPI and should be installed directly from the `main` branch of this GitHub repository. Use of `uv` is recommended and a `uv.lock` file is provided.

```commandline
uv tool install --from git+https://github.com/NumerousHats/ascli-ArchivesSpaceCLI ascli
ascli --install-completion # If you wish to have tab-completion. This will modify your ~/.bashrc.
```

Running `ascli` via `uvx` or any other mechanism has not been tested.

This project is under active development. New features and fixes will appear in the `main` branch without increments in the version number and can be pulled by running `uv tool update ascli`.

# Roadmap

## Done

#### Repositories
- `ascli (repository|repo) set <n>` Set default repository number
- `ascli (repository|repo) get [n]` Get information about the default or specified repository
- `ascli (repository|repo) list` List all available repositories

#### Containers
- `ascli (container|cont) get <n>`
- `ascli (container|cont) create`
- `ascli (container|cont) edit <n>`

#### Resources
- `ascli (resource|res) set <n>` Set default resource number
- `ascli (resource|res) get <n>` Show information about the resource with the given number, or the current default resource
- `ascli (resource|res) add-instance`

#### Enums
- `ascli (enumeration|enum) get <n>`

#### CLI configuration
- `ascli (clear-cache|cc) (all|repo|repository|resource|res|token)`

## In progress

#### Resources

## High priority

#### Resources
- `ascli (resource|res) update [n]  <json>`
- some way of adding notes

#### Container profiles
- `ascli profiles list`

### Low priority

#### Resources
- `ascli (resource|res) export --pdf [n] [outputfile]`
- `ascli (resource|res) export --ead [n] [outputfile|-]`
- `ascli (resource|res) publish [n]`

## Maybe?

#### Manage the API endpoint
- `ascli endpoint` Show information on current default API endpoint
- `ascli endpoint list` List all configured API endpoints
- `ascli endpoint use` Set default API endpoint
- `ascli endpoint create` Create a new API endpoint with URL and login credentials
- `ascli endpoint delete`

#### Resources
- Something to list/find resources?

#### Container profiles
- `ascli profiles create`

#### Enums
- `ascli (enumeration|enum) list`
- `ascli (enumeration|enum) create <name> <value>`
- `ascli (enumeration|enum) update <n> <name> <value>`

## Rejected
