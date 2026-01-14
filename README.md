# A command-line tool to work with the ArchivesSpace API

This project is not even remotely ready for prime time. Currently, only commands that have immediate usefulness for work at the UHEC are being implemented.

## Command roadmap

### Done

### In progress

Containers
- `ascli (container|cont) get <n>` (also aliased to `ascli container <n>`)
- `ascli (container|cont) create`
- `ascli (container|cont) edit <n>`

Resources
- `ascli (resource|res) get <n>` Show information about the resource with the given number, or the current default resource (also aliased to `ascli resource <n>`)
- `ascli (resource|res) add-instance`

### High priority

Repositories
- `ascli (repository|repo)` Show information on the current default repository
- `ascli (repository|repo) list` List all available repositories
- `ascli (repository|repo) use <n>` Set default repository number

Resources
- `ascli (resource|res) use <n>` Set default resource number
- `ascli (resource|res) [n] update <json>`
- `ascli (resource|res) [n] publish`

Enums
- `ascli (enumeration|enum) list`
- `ascli (enumeration|enum) create <name> <value>`
- `ascli (enumeration|enum) update <n> <name> <value>`

### Low priority

Resources
- `ascli (resource|res) export --pdf [n] [outputfile]`
- `ascli (resource|res) export --ead [n] [outputfile|-]`

### Maybe?

- `ascli endpoint` Show information on current default API endpoint
- `ascli endpoint list` List all configured API endpoints
- `ascli endpoint use` Set default API endpoint
- `ascli endpoint create` Create a new API endpoint with URL and login credentials
- `ascli endpoint delete` 
- Something to list/find resources?


### Rejected
