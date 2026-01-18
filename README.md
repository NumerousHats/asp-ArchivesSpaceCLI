# A command-line tool to work with the ArchivesSpace API

This project is not even remotely ready for prime time. Currently, only commands that have immediate usefulness for work at the Ukrainian History and Education Center are being implemented.

## Command roadmap

### Done

Repositories
- `ascli (repository|repo) get [n]` Get information about the default or specified repository
- `ascli (repository|repo) list` List all available repositories
- `ascli (repository|repo) set <n>` Set default repository number

Containers
- `ascli (container|cont) get <n>`
- `ascli (container|cont) create`
- `ascli (container|cont) edit <n>`

### In progress

Resources
- `ascli (resource|res) get <n>` Show information about the resource with the given number, or the current default resource
- `ascli (resource|res) add-instance`

Enums
- `ascli (enumeration|enum) get <n>`

### High priority

Resources
- `ascli (resource|res) use <n>` Set default resource number
- `ascli (resource|res) update [n]  <json>`

Container profiles
- `ascli profiles list`

### Low priority

Resources
- `ascli (resource|res) export --pdf [n] [outputfile]`
- `ascli (resource|res) export --ead [n] [outputfile|-]`
- `ascli (resource|res) publish [n]`

### Maybe?

API endpoint
- `ascli endpoint` Show information on current default API endpoint
- `ascli endpoint list` List all configured API endpoints
- `ascli endpoint use` Set default API endpoint
- `ascli endpoint create` Create a new API endpoint with URL and login credentials
- `ascli endpoint delete`

Resources
- Something to list/find resources?

Container profiles
- `ascli profiles create`

Enums
- `ascli (enumeration|enum) list`
- `ascli (enumeration|enum) create <name> <value>`
- `ascli (enumeration|enum) update <n> <name> <value>`

### Rejected
