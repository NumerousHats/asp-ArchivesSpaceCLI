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
@click.option('--id', required=True, help="Container ID")
@click.option('--repo', default="2", help="Repository")
def temp(id, repo):
    dum = client.get(f'/repositories/{repo}/archival_objects/{id}')
    dum_json = json.loads(dum.text)
    print(json.dumps(dum_json, indent=2))

@main.command()
@click.option('--id', required=True, help="Container ID")
@click.option('--repo', default="2", help="Repository")
def view(id, repo):
    dum = client.get(f'/repositories/{repo}/top_containers/{id}')
    dum_json = json.loads(dum.text)
    print(json.dumps(dum_json, indent=2))


@main.command()
@click.option('--barcode', help="Top container barcode string")
@click.option('--ctype', default="box", help="Container type")
@click.option('--indicator', required=True, help="Container indicator")
@click.option('--profile', help="Container profile number")
@click.option('--repo', default="2", help="Repository number")
@click.option('--resource', help="Resource ID to attach container to")
@click.option('--ao', help="Archival Object ID to attach container to")
@click.option('--itype', default="mixed_materials", help="Instance type")
def create(barcode, ctype, indicator, profile, repo, resource, ao, itype):
    if resource and ao:
        print("can't attach to both a resource and an ao")
        exit(1)

    top_container_json = {"type": ctype, "indicator": indicator, "jsonmodel_type": "top_container",
                          "active_restrictions": []}
    if barcode:
        top_container_json['barcode'] = barcode
    if profile:
        top_container_json['container_profile'] = {"ref": f"/container_profiles/{profile}"}

    dum = client.post(f'/repositories/{repo}/top_containers', json=top_container_json)
    dum_json = json.loads(dum.text)
    print(json.dumps(dum_json, indent=2))

    if dum_json["status"] != "Created":
        exit(1)

    container_uri = dum_json['uri']

    if resource or ao:
        instance_json = copy.deepcopy(instances_template)
        instance_json['sub_container']['top_container']['ref'] = container_uri
        if itype:
            instance_json['instance_type'] = itype

        if resource:
            dum = client.get(f'/repositories/{repo}/resources/{resource}')
            dum_json = json.loads(dum.text)
            if dum_json.get('instances') and type(dum_json['instances']) is list:
                dum_json['instances'].append(instance_json)
            else:
                dum_json['instances'] = [instance_json]

            dum = client.post(f'/repositories/{repo}/resources/{resource}', json=dum_json)
            dum_json = json.loads(dum.text)
            print(json.dumps(dum_json, indent=2))

        if ao:
            dum = client.get(f'/repositories/{repo}/archival_objects/{ao}')
            dum_json = json.loads(dum.text)
            if dum_json.get('instances') and type(dum_json['instances']) is list:
                dum_json['instances'].append(instance_json)
            else:
                dum_json['instances'] = [instance_json]

            dum = client.post(f'/repositories/{repo}/archival_objects/{ao}', json=dum_json)
            dum_json = json.loads(dum.text)
            print(json.dumps(dum_json, indent=2))


@main.command()
@click.argument('container_id')
@click.option('--barcode', help="Top container barcode string")
@click.option('--ctype', help="Container type")
@click.option('--profile', help="Container profile number")
@click.option('--repo', default="2", help="Repository number")
@click.option('--indicator', help="Container indicator")
def edit(container_id, barcode, ctype, profile, repo, indicator):
    dum = client.get(f'/repositories/{repo}/top_containers/{container_id}')
    top_container_json = json.loads(dum.text)
    if profile:
        top_container_json['container_profile'] = {'ref': f'/container_profiles/{profile}'}
    if barcode:
        top_container_json['barcode'] = barcode
    if ctype:
        top_container_json['type'] = ctype
    if indicator:
        top_container_json['indicator'] = indicator

    dum = client.post(f'/repositories/{repo}/top_containers/{container_id}', json=top_container_json)
    dum_json = json.loads(dum.text)
    print(json.dumps(dum_json, indent=2))


if __name__ == '__main__':
    main()
