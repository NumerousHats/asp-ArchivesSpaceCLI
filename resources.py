import copy
import json

from asnake.client import ASnakeClient
from asnake.aspace import ASpace
import click

# validate ASnake client
client = ASnakeClient()
client.authorize()
aspace = ASpace()

instances_template = {
      "instance_type": "mixed_materials",
      "jsonmodel_type": "instance",
      "is_representative": False,
      "sub_container": {
        "jsonmodel_type": "sub_container",
        "top_container": {
          "ref": "/repositories/3/top_containers/975"
        }
      }
    }


@click.group()
def main():
    pass


@main.command()
@click.argument('id')
@click.option('--repo', default="2", help="Repository")
def get_json(id, repo):
    """Get JSON representation of resource specified by ID."""

    dum = client.get(f'/repositories/{repo}/resources/{id}')
    dum_json = json.loads(dum.text)
    print(json.dumps(dum_json, indent=2))


@main.command()
@click.argument('container_id')
@click.argument('ao_id')
@click.option('--repo', default="2", help="Repository number")
@click.option('--itype', default="mixed_materials", help="Instance type")
@click.option('--resource', is_flag=True, help="Add to top level of resource instead of to an AO")
@click.option('--type2', help="Child instance type")
@click.option('--indicator2', help="Child instance indicator")
@click.option('--barcode2', help="Child instance barcode")
@click.option('--type3', help="Grandchild instance type")
@click.option('--indicator3', help="Grandchild instance indicator")

def add_instance(container_id, ao_id, repo, itype, resource, type2, indicator2, barcode2, type3, indicator3):
    """Add an instance to an Archival Object or Resource.

       CONTAINER_ID is the container identifier to be added and AO_ID is the identifier of the Archival Object
       to which the instance should be added, unless the '--resource' flag is present. In that case, the instance
       will be added to the top level of the resource with the identifier AO_ID.
    """
    instance_json = copy.deepcopy(instances_template)
    instance_json['sub_container']['top_container']['ref'] = f"/repositories/{repo}/top_containers/{container_id}"
    instance_json['instance_type'] = itype
    if type2:
        instance_json['type_2'] = type2
    if indicator2:
        instance_json['indicator_2'] = indicator2
    if barcode2:
        instance_json['barcode_2'] = barcode2
    if type3:
        instance_json['type_3'] = type3
    if indicator3:
        instance_json['indicator_3'] = indicator3

    if resource:
        endpoint = "resources"
    else:
        endpoint = "archival_objects"

    dum = client.get(f'/repositories/{repo}/{endpoint}/{ao_id}')
    dum_json = json.loads(dum.text)
    if dum_json.get('instances') and type(dum_json['instances']) is list:
        dum_json['instances'].append(instance_json)
    else:
        dum_json['instances'] = [instance_json]

    dum = client.post(f'/repositories/{repo}/{endpoint}/{ao_id}', json=dum_json)
    dum_json = json.loads(dum.text)
    print(json.dumps(dum_json, indent=2))


if __name__ == '__main__':
    main()
