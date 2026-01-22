# asp: A command-line tool for the ArchivesSpace API

`asp` is an attempt to ease some of the pain points associated with the creation and modification of records in [ArchivesSpace](www.archivesspace.org). It currently focuses on the management of containers and resources. It is a subcommand-style CLI (like `git` and `apt-get`) that modularizes different aspects of the creation and management of ArchivesSpace data records.

This project is not quite "ready for prime time". Currently, only commands that have immediate usefulness for the author's archival work are being implemented. It has not been extensively tested, so please use with caution. Editing of existing records runs the risk of data corruption, so *please make backups* before attempting any such operations.

`asp` is built on [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake). You will need to create an `.archivessnake.yml` file as described in the ArchivesSnake documentation to store the login credentials for your ArchivesSpace instance. The ArchivesSpace API session key is cached between runs of `asp` in order to improve responsiveness and overall user experience, especially for commands that do not actually hit the API. Token expiration and re-authentication should be handled transparently. If there are authentication errors (or if you have security concerns), the stored token can be cleared using `asp clear-cache token`.

# Installation

This project is currently not available on PyPI and should be installed directly from the `main` branch of this GitHub repository. Use of `uv` is recommended and a `uv.lock` file is provided.

```commandline
uv tool install --from git+https://github.com/NumerousHats/asp-ArchivesSpaceCLI asp
asp --install-completion # If you wish to have tab-completion. This will modify your ~/.bashrc.
```

Running `asp` via `uvx` or any other mechanism has not been tested.

This project is under active development. New features and bug fixes may appear in the `main` branch without an increment in the version number. These can be pulled by running `uv tool update asp`. If a command was added or changed in an update, and it does not work with tab completion, rerun `asp --install-completion`.

# Usage

Detailed usage information for each command, including all available options and parameters, can be displayed using the `--help` flag.

The following commands are currently implemented:

#### Repositories
- `asp repository set <n>` Set default repository number
- `asp repository get [n]` Get information about the default or specified repository
- `asp repository list` List all available repositories

#### Containers
- `asp container get <n>` Get JSON representation of the specified container
- `asp container create` Create a new container
- `asp container edit <n>` Modify properties of the specified container

#### Resources and archival objects
- `asp resource set <n>` Set default resource number
- `asp resource get [n]` Get JSON representation of the default or specified resource
- `asp resource add-instance` Add an existing container as a container instance to a resource or archival object

#### Enums
- `asp enumeration get <n>` Get a list of all values in the specified enumeration

#### CLI configuration
- `asp clear-cache (all|epository|resource|token)`

# Roadmap

## In progress

#### Resources

## High priority

#### Containers
- add ability to add a container profile to a container

#### Resources
- `asp resource update [n]  <json>`
- some way of adding notes

#### Container profiles
- `asp profiles list`

## Medium priority and/or complicated to implement

#### Resources
- spawn a resource from an accession including default notes, etc.

## Low priority

#### Resources
- `asp resource export --pdf [n] [outputfile]`
- `asp resource export --ead [n] [outputfile|-]`

## Maybe?

#### Resources
- Something to list/find resources?

#### Container profiles
- `asp profiles create`

#### Enums
- `asp enumeration list`
- `asp enumeration create <name> <value>`
- `asp enumeration update <n> <name> <value>`

## Probably not

#### Manage the API endpoint
- `asp endpoint` Show information on current default API endpoint
- `asp endpoint list` List all configured API endpoints
- `asp endpoint use` Set default API endpoint
- `asp endpoint create` Create a new API endpoint with URL and login credentials
- `asp endpoint delete`

#### Resources
- `asp resource publish [n]` Easy to do from the admin GUI.