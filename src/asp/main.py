import json

import asp.config as appconfig
import asp.resources as resources
import asp.containers as containers

from cyclopts import App

config = appconfig.config


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


def dispatch(spec, parameters):
    """
    Generic caller used by commands.
    """
    if spec['noun'] == 'cache':
        if spec['verb'] == 'clear':
            if spec['noun2'] == 'all':
                to_clear = ["resource", "repository", "token"]
            else:
                to_clear = [spec['noun2']]
            config.clear_state(to_clear)
        else:
            config.set_default(spec['noun2'], parameters['id'])
        return
    if spec['command'] == 'container-profile-list':
        profiles = config.client.get_paged("container_profiles")
        for profile in profiles:
            print(f'{profile["uri"]}\t{profile["display_string"]}')
        return
    if spec['command'] == 'resource-notes-add':
        resources.add_notes(**parameters)
        return
    if spec['command'] == 'resource-instance-add':
        resources.add_instance(**parameters)
        return
    if spec['endpoint'] is not None:
        if 'id' not in parameters:
            parameters['id'] = None
        if 'repo' not in parameters:
            parameters['repo'] = None
        if spec['method'] == "get":
            out_json = appconfig.simple_get(spec["endpoint"], parameters["id"], parameters["repo"])
            if spec['command'] == 'repository-get' and not parameters['verbose']:
                print(f"{out_json['uri']}\t{out_json['display_string']}")
            elif spec['command'] == 'repository-list':
                repos = [f"{out_json[i]['uri']} {out_json[i]['display_string']}" for i in range(len(out_json))]
                print("\n".join(repos))
            elif spec['command'] == 'enumeration-get':
                print("\n".join(out_json['values']))
            else:
                print(json.dumps(out_json, indent=2))
        if spec['method'] == "post":
            out_json = appconfig.simple_post(parameters["json_file"], spec["endpoint"], parameters["id"],
                                             parameters["repo"])
            print(json.dumps(out_json, indent=2))
        return


def register_command(cli, spec):
    cli_command = cli.mapping['-'.join(filter(None, [spec['noun'], spec['noun2']]))]
    spec['command'] = '-'.join(filter(None, [spec['noun'], spec['noun2'], spec['verb']]))

    match spec:
        # bespoke signatures
        case {'noun': 'resource', 'noun2': 'notes', 'verb': 'add'}:
            @cli_command.command(name=spec["verb"], help=spec["help"])
            def _cmd(note_file: str = None, id: int = None, repo: int = None, publish: bool = False):
                args = locals()
                del args['spec']
                return dispatch(spec, args)
        case {'noun': 'resource', 'noun2': 'instance', 'verb': 'add'}:
            @cli_command.command(name=spec["verb"], help=spec["help"])
            def _cmd(object_id: int, container_id: int = None, repo: int = None, itype: str = "mixed_materials",
                     to_resource: bool = False, type2: str = None, indicator2: str = None, barcode2: str = None,
                     type3: str = None, indicator3: str = None):
                args = locals()
                del args['spec']
                return dispatch(spec, args)

        # generic signatures
        case {'params': None}:
            @cli_command.command(name=spec["verb"], help=spec["help"])
            def _cmd():
                return dispatch(spec, {})
        case {'params': 'id'}:
            @cli_command.command(name=spec["verb"], help=spec["help"])
            def _cmd(id: int):
                return dispatch(spec, {'id': id})
        case {'params': 'id-o'}:
            @cli_command.command(name=spec["verb"], help=spec["help"])
            def _cmd(id: int = None):
                return dispatch(spec, {'id': id})
        case {'params': 'id-o_v'}:
            @cli_command.command(name=spec["verb"], help=spec["help"])
            def _cmd(id: int = None, verbose: bool = False):
                return dispatch(spec, {'id': id, 'verbose': verbose})
        case {'params': 'repo'}:
            @cli_command.command(name=spec["verb"], help=spec["help"])
            def _cmd(repo: int):
                return dispatch(spec, {'repo': repo})
        case {'params': 'repo-o'}:
            @cli_command.command(name=spec["verb"], help=spec["help"])
            def _cmd(repo: int = None):
                return dispatch(spec, {'repo': repo})
        case {'params': 'id-o_repo-o'}:
            @cli_command.command(name=spec["verb"], help=spec["help"])
            def _cmd(id: int = None, repo: int = None):
                return dispatch(spec, {'id': id, 'repo': repo})
        case {'params': 'id_repo-o'}:
            @cli_command.command(name=spec["verb"], help=spec["help"])
            def _cmd(id: int, repo: int = None):
                return dispatch(spec, {'id': id, 'repo': repo})
        case {'params': 'json_id-o_repo-o'}:
            @cli_command.command(name=spec["verb"], help=spec["help"])
            def _cmd(json_file: str = None, id: int = None, repo: int = None):
                return dispatch(spec, {'json_file': json_file, 'id': id, 'repo': repo})


COMMANDS = [
    {"noun": "resource", "noun2": "instance", "verb": "add",
     "params": None, "endpoint": None, "method": None, "output": None,
     "help": "Add a container instance to an archival object or resource."},
    {"noun": "resource", "noun2": "notes", "verb": "add",
     "params": None, "endpoint": None, "method": None, "output": None,
     "help": "Add note(s) to a resource from information in the provided JSON."},
    {"noun": "resource", "noun2": None, "verb": "get",
     "params": "id_repo-o", "endpoint": "repositories/{repo}/resources/{id}", "method": "get", "output": None,
     "help": "Get resource JSON."},
    {"noun": "resource", "noun2": None, "verb": "update",
     "params": "json_id-o_repo-o", "endpoint": "repositories/{repo}/resources/{id}", "method": "post", "output": None,
     "help": "Update resource from provided JSON."},
    {"noun": "repository", "noun2": None, "verb": "get",
     "params": "id-o_v", "endpoint": "repositories/{repo}", "method": "get", "output": None,
     "help": "Get information about the default or specified repository."},
    {"noun": "repository", "noun2": None, "verb": "list",
     "params": None, "endpoint": "repositories", "method": "get", "output": None,
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
     "params": "id_repo-o", "endpoint": "repositories/{repo}/top_containers/{id}", "method": "get", "output": None,
     "help": "Get container information."},
    {"noun": "container", "noun2": "profile", "verb": "list",
     "params": None, "endpoint": None, "method": None, "output": None,
     "help": "List all container profiles."},
    {"noun": "cache", "noun2": "all", "verb": "clear",
     "params": None, "endpoint": None, "method": None, "output": None,
     "help": "Clear all cached tokens and defaults."},
    {"noun": "cache", "noun2": "repository", "verb": "set",
     "params": "id", "endpoint": None, "method": None, "output": None,
     "help": "Set the default repository ID."},
    {"noun": "cache", "noun2": "repository", "verb": "clear",
     "params": None, "endpoint": None, "method": None, "output": None,
     "help": "Clear the default repository ID."},
    {"noun": "cache", "noun2": "resource", "verb": "set",
     "params": "id", "endpoint": None, "method": None, "output": None,
     "help": "Set the default resource ID."},
    {"noun": "cache", "noun2": "resource", "verb": "clear",
     "params": None, "endpoint": None, "method": None, "output": None,
     "help": "Clear the default resource ID."},
    {"noun": "cache", "noun2": "token", "verb": "clear",
     "params": None, "endpoint": None, "method": None, "output": None,
     "help": "Clear the ArchivesSpace authentication token."}
]

cli = Cli()

for spec in COMMANDS:
    register_command(cli, spec)


def main():
    cli.app()


if __name__ == "__main__":
    cli.app()
