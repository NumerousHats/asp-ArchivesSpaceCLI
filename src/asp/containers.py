import json
import asp.config as appconfig

config = appconfig.config


def create(barcode, ctype, indicator, profile, repo, json_out):
    repo = config.get_default("repository", repo)
    top_container_json = {"indicator": indicator, "jsonmodel_type": "top_container", "active_restrictions": []}
    if ctype:
        top_container_json['type'] = ctype
    if barcode:
        top_container_json['barcode'] = barcode
    if profile:
        top_container_json['container_profile'] = {"ref": f"/container_profiles/{profile}"}

    out = config.client.post(f'/repositories/{repo}/top_containers', json=top_container_json)
    out_json = json.loads(out.text)
    if out_json['status'] != 'Created':
        print(json.dumps(out_json, indent=2))
    if json_out:
        print(json.dumps(out_json, indent=2))
    else:
        print(out_json['id'])


def edit(container_id, barcode, ctype, profile, repo, indicator):
    repo = config.get_default("repository", repo)
    out = config.client.get(f'repositories/{repo}/top_containers/{container_id}')
    top_container_json = json.loads(out.text)
    if profile:
        top_container_json['container_profile'] = {'ref': f'/container_profiles/{profile}'}
    if barcode:
        top_container_json['barcode'] = barcode
    if ctype:
        top_container_json['type'] = ctype
    if indicator:
        top_container_json['indicator'] = indicator

    out = config.client.post(f'/repositories/{repo}/top_containers/{container_id}', json=top_container_json)
    out_json = json.loads(out.text)
    print(json.dumps(out_json, indent=2))


if __name__ == "__main__":
    pass
