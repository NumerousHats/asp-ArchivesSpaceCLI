from cyclopts import App
import ascli.containers as containers
import ascli.resources as resources

app = App()
container = app.command(App(name="container"))
resource = app.command(App(name="resource"))

@container.command(name="view")
def container_view(id: int, repo: int = 2):
    """Get container information.

    Parameters
    ----------
    id: int
        The container ID number.
    repo: int
        The repository ID number.
    """
    print(f"viewing container {id}")

@container.command(name="create")
def container_create(barcode:str, ctype: str, indicator: str, profile: int, repo: int = 2):
    """Create a container.

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
    """

    print("container create")

@container.command(name="edit")
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


def main():
    app()

if __name__ == "__main__":
    main()
