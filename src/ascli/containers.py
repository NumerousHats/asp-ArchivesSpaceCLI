import json
import ascli.config as config


def get(id, repo):
    repo = config.get_default_repo(repo)
    out = config.get(f'/repositories/{repo}/top_containers/{id}')
    out_json = json.loads(out.text)
    return json.dumps(out_json, indent=2)


def create(barcode, ctype, indicator, profile, repo):
    repo = config.get_default_repo(repo)
    top_container_json = {"indicator": indicator, "jsonmodel_type": "top_container", "active_restrictions": []}
    if ctype:
        top_container_json['type'] = ctype
    if barcode:
        top_container_json['barcode'] = barcode
    if profile:
        top_container_json['container_profile'] = {"ref": f"/container_profiles/{profile}"}

    out = config.post(f'/repositories/{repo}/top_containers', json=top_container_json)
    return json.loads(out.text)


def edit(container_id, barcode, ctype, profile, repo, indicator):
    repo = config.get_default_repo(repo)
    out = config.get(f'/repositories/{repo}/top_containers/{container_id}')
    top_container_json = json.loads(out.text)
    if profile:
        top_container_json['container_profile'] = {'ref': f'/container_profiles/{profile}'}
    if barcode:
        top_container_json['barcode'] = barcode
    if ctype:
        top_container_json['type'] = ctype
    if indicator:
        top_container_json['indicator'] = indicator

    out = config.post(f'/repositories/{repo}/top_containers/{container_id}', json=top_container_json)
    out_json = json.loads(out.text)
    print(json.dumps(out_json, indent=2))

if __name__ == "__main__":
    get(111, 2)
