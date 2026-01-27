import sys
from functools import partial
from typing import Annotated
from cyclopts import App


class Cli(object):
    def __init__(self):
        self.app = App(help="A command line tool for interacting with the ArchivesSpace API")
        self.app.register_install_completion_command()

        self.container_cmd = self.app.command(App(name="container",
                                                  help="Create, modify, and get info about top containers"))
        self.profile_cmd = self.container_cmd.command(App(name="profile",
                                                          help="Create, modify, and get info about container profiles"))
        self.resource_cmd = self.app.command(App(name="resource",
                                                 help="Create, modify, and get info about resources"))
        self.instance_cmd = self.resource_cmd.command(App(name="instance",
                                                          help="Create, modify, and get info about "
                                                               "a container instance of a resource"))
        self.notes_cmd = self.resource_cmd.command(App(name="notes",
                                                       help="Create, modify, and get info about notes "
                                                            "attached to a resource"))
        self.repo_cmd = self.app.command(App(name="repository", help="List or get info about repositories"))
        self.enum_cmd = self.app.command(App(name="enumeration",
                                             help="Create, modify, and get info about enumeration lists"))
        self.cache_cmd = self.app.command(App(name="cache", help="Set or clear persistent tokens and default values"))
        self.cache_all_cmd = self.cache_cmd.command(App(name="all",
                                                        help="Clear all persistent data"))
        self.cache_resource_cmd = self.cache_cmd.command(App(name="resource",
                                                             help="Set or clear default resource"))
        self.cache_repo_cmd = self.cache_cmd.command(App(name="repository",
                                                         help="Set or clear default repository"))
        self.cache_token_cmd = self.cache_cmd.command(App(name="token",
                                                          help="Clear the API authentication token"))

        self.mapping = {'container': self.container_cmd, 'resource': self.resource_cmd, 'repository': self.repo_cmd,
                        'enumeration': self.enum_cmd, 'cache': self.cache_cmd, 'resource-instance': self.instance_cmd,
                        'resource-notes': self.notes_cmd, 'container-profile': self.profile_cmd,
                        'cache-all': self.cache_all_cmd, 'cache-resource': self.cache_resource_cmd,
                        'cache-repository': self.cache_repo_cmd, 'cache-token': self.cache_token_cmd}


def dispatch(action, parameters):
    """
    Generic API caller used by many subcommands.
    """
    print(f'dispatching {action} with parameters {parameters}')


def register_command(cli, spec):
    cli_command = cli.mapping['-'.join(filter(None, [spec['noun'], spec['noun2']]))]

    match spec:
        case {'params': 'none'}:
            @cli_command.command(name=spec["verb"], help=spec["help"])
            def _cmd():
                return dispatch(spec, {})


COMMANDS = [
    {"noun": "resource", "noun2": "instance", "verb": "add", "params": "res_instance",
     "endpoint": None, "method": None, "output": None,
     "help": "Add a container instance to an archival object or resource."},
    {"noun": "resource", "noun2": "notes", "verb": "add",
     "params": "res_notes", "endpoint": None, "method": None, "output": None,
     "help": "Add note(s) to a resource from information in the provided JSON."},
    {"noun": "resource", "noun2": None, "verb": "get",
     "params": "id_repo", "endpoint": "repositories/{repo}/resources/{id}", "method": "get", "output": None,
     "help": "Get resource JSON."},
    {"noun": "resource", "noun2": None, "verb": "update",
     "params": "json_id_repo", "endpoint": "repositories/{repo}/resources/{id}", "method": "post", "output": None,
     "help": "Update resource from provided JSON."},
    {"noun": "repository", "noun2": None, "verb": "get",
     "params": "id_verbose?", "endpoint": "repositories/{repo}", "method": "get", "output": None,
     "help": "Get information about the default or specified repository."},
    {"noun": "repository", "noun2": None, "verb": "list",
     "params": "none", "endpoint": "repositories", "method": "get", "output": None,
     "help": "List all repositories."},
    {"noun": "enumeration", "noun2": None, "verb": "get",
     "params": "id", "endpoint": "config/enumerations/{id}", "method": "get", "output": None,
     "help": "Get values in an enumeration list"},
    {"noun": "container", "noun2": None, "verb": "create",
     "params": "cont_create", "endpoint": None, "method": None, "output": None,
     "help": "Create a container. Returns the container identifier of the newly-created container, "
             "unless '--verbose' is specified. In that case, the full JSON info is returned."},
    {"noun": "container", "noun2": None, "verb": "edit",
     "params": "cont_edit", "endpoint": None, "method": None, "output": None,
     "help": "Edit a container."},
    {"noun": "container", "noun2": None, "verb": "get",
     "params": "id_repo", "endpoint": "repositories/{repo}/top_containers/{id}", "method": "get", "output": None,
     "help": "Get container information."},
    {"noun": "container", "noun2": "profile", "verb": "list",
     "params": "none", "endpoint": "container_profiles", "method": "paged", "output": None,
     "help": "List all container profiles."},
    {"noun": "cache", "noun2": "all", "verb": "clear",
     "params": "none", "endpoint": None, "method": None, "output": None,
     "help": "Clear all cached tokens and defaults."},
    {"noun": "cache", "noun2": "repository", "verb": "set",
     "params": "id", "endpoint": None, "method": None, "output": None,
     "help": "Set the default repository ID."},
    {"noun": "cache", "noun2": "repository", "verb": "clear",
     "params": "none", "endpoint": None, "method": None, "output": None,
     "help": "Clear the default repository ID."},
    {"noun": "cache", "noun2": "resource", "verb": "set",
     "params": "id", "endpoint": None, "method": None, "output": None,
     "help": "Set the default resource ID."},
    {"noun": "cache", "noun2": "resource", "verb": "clear",
     "params": "none", "endpoint": None, "method": None, "output": None,
     "help": "Clear the default resource ID."},
    {"noun": "cache", "noun2": "token", "verb": "clear",
     "params": "none", "endpoint": None, "method": None, "output": None,
     "help": "Clear the ArchivesSpace authentication token."}
]

cli = Cli()

for spec in COMMANDS:
    register_command(cli, spec)

if __name__ == "__main__":
    cli.app()
