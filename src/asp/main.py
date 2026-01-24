import json
import sys
from typing import Literal

from cyclopts import App

import asp.containers as containers
import asp.resources as resources
import asp.config as appconfig

config = appconfig.config

app = App(help="A command line tool for interacting with the ArchivesSpace API")
app.register_install_completion_command()

container_cmd = app.command(App(name="container", help="Create, modify, and get info about top containers"))
resource_cmd = app.command(App(name="resource", help="Create, modify, and get info about resources"))
repo_cmd = app.command(App(name="repository", help="Get info about or set default repository"))
enum_cmd = app.command(App(name="enumeration", help="Create, modify, and get info about enumeration lists"))


def read_from_stdin(value):
    """Helper function to read a value of something from stdin."""
    if value is not None:
        return value
    # No CLI value → read from stdin
    return sys.stdin.readline().rstrip("\n")


@container_cmd.command(name="get")
def container_get(id: int, repo: int = None):
    """Get container information.

    Parameters
    ----------
    id: int
        The container ID number.
    repo: int
        The repository ID number.
    """
    print(containers.get(id, repo))


@container_cmd.command(name="create")
def container_create(indicator: str, ctype: str = None, barcode:str = None, profile: int=None, repo: int = None,
                     json_out: bool = False):
    """Create a container. Returns the container identifier of the newly-created container,
    unless "--json-out" is specified. In that case, the full JSON info is returned.

    Parameters
    ----------
    indicator: str
        The container indicator.
    ctype: str
        The container type.
    barcode: int
        The container barcode.
    profile: int
        The identifier number of the container profile.
    repo: int
        The repository ID number.
    json_out: bool
        Output container information as JSON.
    """

    out = containers.create(barcode, ctype, indicator, profile, repo)

    if out["status"] != "Created":
        print("Container could not be created", file=sys.stderr)
        sys.exit(1)

    if json_out:
        print(json.dumps(out, indent=2))
    else:
        print(out['id'])


@container_cmd.command(name="edit")
def container_edit(container_id: int, barcode:str=None, ctype: str=None, indicator: str=None, profile: int=None,
                   repo: int = None):
    """Edit a container.

    Parameters
    ----------
    container_id: int
        The container ID number.
    barcode: int
        The container barcode.
    ctype: int
        The container type.
    indicator: str
        The container indicator.
    profile: int
        The identifier number of the container profile.
    repo: int
        The repository ID number.
    """
    containers.edit(container_id, barcode, ctype, profile, repo, indicator)

@resource_cmd.command(name="set")
def resource_set(id: int=None):
    """Set the default resource.

    Parameters
    ----------
    id: int
        The default resource ID number you wish to set.
    """
    config.state["resource"] =  id

@resource_cmd.command(name="get")
def resource_get(id: int, repo: int=None):
    """Get resource JSON.

    Parameters
    ----------
    id: int
        The resource ID number.
    repo: int
        The repository ID number.
    """
    resources.get(id, repo)


@resource_cmd.command(name="update")
def resource_update(new_json: str=None, id: int=None, repo: int=None):
    """Update resource from provided JSON.

    Parameters
    ----------
    new_json: str
        The JSON that will replace the currently existing resource metadata. If not provided, read from stdin.
    id: int
        The resource ID number.
    repo: int
        The repository ID number.
    """
    if new_json is None or new_json == '-':
        new_json = json.load(sys.stdin)
    else:
        new_json = json.loads(new_json)
    resources.update(new_json, id, repo)

@resource_cmd.command
def add_instance(object_id: int, container_id: int = None, repo: int = None, itype: str = "mixed_materials",
                     to_resource: bool = False, type2: str = None, indicator2: str = None, barcode2: str = None,
                     type3: str = None, indicator3: str = None):

    """Add a container instance to an archival object or resource.

    Parameters
    ----------
    object_id: int
        The ID of the archival object (or resource, if '--attach-to-resource') where the instance should be attached.
    container_id: int
        The container ID number. If not provided, read from stdin.
    itype: str
        The instance type.
    to_resource: bool
        Attach the instance to the top level of a resource rather than an archival object. In this case, 'object-id' should be the ID of the resource.
    type2: int
        Child instance type.
    indicator2: str
        Child instance indicator.
    barcode2: str
        Child instance barcode.
    type3: int
        Grandchild instance type.
    indicator3: str
        Grandchild instance indicator.
    repo: int
        The repository ID number.
    """
    container_id = int(read_from_stdin(container_id))
    resources.add_instance(container_id, object_id, repo, itype, to_resource, type2, indicator2, barcode2,
                           type3, indicator3)

@repo_cmd.command(name="set")
def repo_set(id: int=None):
    """Set the default repository.

    Parameters
    ----------
    id: int
        The default repository ID number you wish to set.
    """
    config.state["repository"] = id


@repo_cmd.command(name="get")
def repo_get(id: int=None, verbose: bool = False):
    """Get information about the default or specified repository.

    Parameters
    ----------
    id: int
        The repository ID number (optional). If not specified, will report on the current default repository.
    verbose: bool
        Output detailed repository information as JSON.
    """
    id = config.get_default("repository", id)
    out = config.get(f'/repositories/{id}')
    out_json = json.loads(out.text)
    repository_name = out_json['display_string']
    if verbose:
        print(out_json)
    else:
        print(f"repository id {id}: {repository_name}")

@repo_cmd.command(name="list")
def repo_list():
    """
    List all repositories.
    """

    out = config.get(f'/repositories')
    out_json = json.loads(out.text)
    repos = [f"{out_json[i]['uri']} {out_json[i]['display_string']}" for i in range(len(out_json))]
    print("\n".join(repos))

@enum_cmd.command(name="get")
def enum_get(id: int):
    """
    Get enumeration values.
    """

    out = config.get(f'/config/enumerations/{id}')
    out_json = json.loads(out.text)
    print("\n".join(out_json['values']))


@app.command()
def clear_cache(cache: Literal["all", "repository", "resource", "token"]):
    """
    Clear all or selected persistent data caches.

    Parameters
    ----------
    cache: Literal["all", "repository", "resource", "token"]
        Which cache to clear.
    """
    items_to_clear = []
    if cache == "repository" or cache == "all":
        items_to_clear.append("repository")
    if cache == "resource" or cache == "all":
        items_to_clear.append("resource")
    if cache == "token" or cache == "all":
        items_to_clear.append("token")

    config.clear_state(items_to_clear)


def main():
    app()


if __name__ == "__main__":
    main()
