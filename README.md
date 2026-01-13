# A command-line tool to work with the ArchivesSpace API

This project is not even remotely ready for prime time. Currently, only commands that have immediate usefulness for work at the UHEC are being implemented.

## Command roadmap

### Done

### In progress

- `ascli container get <n>`
- `ascli container create`
- `ascli container edit <n>`


- `ascli resource [n]` Show information about the resource with the given number, or the current default resource
- `ascli resource add-instance`

### High priority

- `ascli (repository|repo)` Show information on the current default repository
- `ascli (repository|repo) list` List all available repositories
- `ascli (repository|repo) use <n>` Set default repository number


- `ascli resource use <n>` Set default resource number
- `ascli resource [n] update <json>`
- `ascli resource [n] publish`


- `ascli (enumeration|enum) list`
- `ascli (enumeration|enum) create <name> <value>`
- `ascli (enumeration|enum) update <n> <name> <value>`

### Low priority

- `ascli endpoint` Show information on current default API endpoint
- `ascli endpoint list` List all configured API endpoints
- `ascli endpoint use` Set default API endpoint
- `ascli endpoint create` Create a new API endpoint with URL and login credentials
- `ascli endpoint delete` 


- `ascli resource [n] pdf [outputfile]`
- `ascli resource [n] ead [outputfile|-]`
- Need something to list/find resources?

### Rejected
