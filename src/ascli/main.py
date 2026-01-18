import json

from cyclopts import App
from cyclopts import Parameter
import ascli.containers as containers
import ascli.resources as resources
import ascli.config as config

app = App(help="A command line tool for interacting with the ArchivesSpace API")
container_cmd = app.command(App(name="container", alias="cont",
                                help="Create, modify, and get info about top containers"))
resource_cmd = app.command(App(name="resource", alias="res",
                               help="Create, modify, and get info about resources"))
repo_cmd = app.command(App(name="repository", alias="repo", help="Get info about or set default repository"))


@container_cmd.command(name="get")
def container_get(id: int, repo: int = 2):
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
def container_create(barcode:str = "", ctype: str="", indicator: str="", profile: int=None, repo: int = 2,
                     json_out: bool = False):
    """Create a container. Returns the container identifier of the newly-created container, unless "--json" is specified.

    Parameters
    ----------
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
    json_out: bool
        Output container information as JSON.
    """

    # out = containers.create(barcode, type, indicator, profile, repo)

    if json_out:
        print("container create output JSON")
    else:
        print("container create output identifier")


@container_cmd.command(name="edit")
def container_edit(container_id: int, barcode:str=None, ctype: str=None, indicator: str=None, profile: int=None,
                   repo: int = 2):
    """Create a container.

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

    print("container edit")

@repo_cmd.command(name="set")
def repo_set(id: int=None):
    """Set the default repository.

    Parameters
    ----------
    id: int
        The default repository ID number you wish to set.
    """
    config.to_shelf("repo", id)


@repo_cmd.command(name="get")
def repo_get(id: int=None, verbose: bool = False):
    """Get information about the default (or specified) repository.

    Parameters
    ----------
    id: int
        The repository ID number (optional). If not specified, will report on the current default repository.
    verbose: bool
        Output detailed repository information as JSON.
    """

    if id is None:
        id = config.from_shelf('repo')
    if id is None:
        print("No repository ID specified")
        return

    out = config.get(f'/repositories/{id}')
    out_json = json.loads(out.text)
    repository_name = out_json['display_string']

    if verbose:
        print(out_json)
    else:
        print(f"repository id {id} ({repository_name}")

@repo_cmd.command(name="list")
def repo_get():
    """
    List all repositories.
    """

    out = config.get(f'/repositories')
    out_json = json.loads(out.text)
    repos = [f"{out_json[i]['uri']} {out_json[i]['display_string']}" for i in range(len(out_json))]
    print("\n".join(repos))


def main():
    app()


if __name__ == "__main__":
    main()
