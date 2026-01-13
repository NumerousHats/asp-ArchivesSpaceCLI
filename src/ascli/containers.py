import json

from asnake.client import ASnakeClient
from asnake.aspace import ASpace

# validate ASnake client
client = ASnakeClient()
client.authorize()
aspace = ASpace()

def temp(container_id, repo):
    out = client.get(f'/repositories/{repo}/archival_objects/{container_id}')
    out_json = json.loads(out.text)
    print(json.dumps(out_json, indent=2))

def view(id, repo):
    out = client.get(f'/repositories/{repo}/top_containers/{id}')
    out_json = json.loads(out.text)
    print(json.dumps(out_json, indent=2))


def create(barcode, type, indicator, profile, repo):
    top_container_json = {"type": type, "indicator": indicator, "jsonmodel_type": "top_container",
                          "active_restrictions": []}
    if barcode:
        top_container_json['barcode'] = barcode
    if profile:
        top_container_json['container_profile'] = {"ref": f"/container_profiles/{profile}"}

    out = client.post(f'/repositories/{repo}/top_containers', json=top_container_json)
    out_json = json.loads(out.text)
    print(json.dumps(out_json, indent=2))

    if out_json["status"] != "Created":
        exit(1)

    container_uri = out_json['uri']


def edit(container_id, barcode, ctype, profile, repo, indicator):
    out = client.get(f'/repositories/{repo}/top_containers/{container_id}')
    top_container_json = json.loads(out.text)
    if profile:
        top_container_json['container_profile'] = {'ref': f'/container_profiles/{profile}'}
    if barcode:
        top_container_json['barcode'] = barcode
    if ctype:
        top_container_json['type'] = ctype
    if indicator:
        top_container_json['indicator'] = indicator

    out = client.post(f'/repositories/{repo}/top_containers/{container_id}', json=top_container_json)
    out_json = json.loads(out.text)
    print(json.dumps(out_json, indent=2))
