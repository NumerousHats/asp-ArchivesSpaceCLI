import copy
import json
import sys

import asp.config as appconfig

config = appconfig.config


note_singlepart_template = {"jsonmodel_type": "note_singlepart", "label": None, "type": None,
                            "content": None, "publish": False}
note_multipart_template = {"jsonmodel_type": "note_multipart", "label": None, "type": None,
                           "subnotes": [{"jsonmodel_type": "note_text", "content": None, "publish": False}],
                           "publish": False}


def add_notes(note_file, id, repo, publish):
    if note_file is None or note_file == '-':
        input_json = json.load(sys.stdin)
    else:
        try:
            with open(note_file, 'r') as f:
                input_json = json.load(f)

        except FileNotFoundError:
            print("Note JSON file not found", file=sys.stderr)
            exit(1)
        except json.JSONDecodeError:
            print("Error decoding JSON from file. File might be corrupted.", file=sys.stderr)
            exit(1)

    repo = config.get_default("repository", repo)
    id = config.get_default("resource", id)

    resource = config.client.get(f'repositories/{repo}/resources/{id}')
    resource_json = json.loads(resource.text)

    for note_info in input_json:
        if "jsonmodel_type" not in note_info:
            print("jsonmodel_type cannot be empty", file=sys.stderr)
            exit(1)
        if note_info["jsonmodel_type"] == "note_singlepart":
            note_json = copy.deepcopy(note_singlepart_template)
            note_json["content"] = note_info["note_contents"]
        elif note_info["jsonmodel_type"] == "note_multipart":
            note_json = copy.deepcopy(note_multipart_template)
            note_json["subnotes"][0]["content"] = note_info["note_contents"]
            if publish:
                note_json["subnotes"][0]["publish"] = True
        else:
            print(f"Invalid jsonmodel_type '{note_info["jsonmodel_type"]}'", file=sys.stderr)
            exit(1)
        if publish:
            note_json["publish"] = True
        if "note_type" in note_info:
            note_json["type"] = note_info["note_type"]
        else:
            print("note_type cannot be empty", file=sys.stderr)
            exit(1)
        if "label" in note_info:
            note_json["label"] = note_info["label"]
        else:
            del note_json["label"]

        resource_json["notes"].append(note_json)

    out = config.client.post(f'repositories/{repo}/resources/{id}', json=resource_json)
    out_json = json.loads(out.text)
    print(json.dumps(out_json, indent=2))


instance_template = {
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


def add_instance(container_id, object_id, repo, itype, to_resource, type2, indicator2, barcode2,
                 type3, indicator3):
    """Add an instance to an Archival Object or Resource.

       CONTAINER_ID is the container identifier to be added and OBJECT_ID is the identifier of the Archival Object
       to which the instance should be added, unless the 'attach_to_resource' is True. In that case, the instance
       will be added to the top level of the resource with identifier OBJECT_ID.
    """
    repo = config.get_default("repository", repo)
    if container_id is None:
        container_id = int(sys.stdin.readline().rstrip("\n"))

    instance_json = copy.deepcopy(instance_template)
    instance_json['sub_container']['top_container']['ref'] = f"/repositories/{repo}/top_containers/{container_id}"
    instance_json['instance_type'] = itype
    if type2:
        instance_json['sub_container']['type_2'] = type2
    if indicator2:
        instance_json['sub_container']['indicator_2'] = indicator2
    if barcode2:
        instance_json['sub_container']['barcode_2'] = barcode2
    if type3:
        instance_json['sub_container']['type_3'] = type3
    if indicator3:
        instance_json['sub_container']['indicator_3'] = indicator3

    if to_resource:
        endpoint = "resources"
    else:
        endpoint = "archival_objects"

    out = config.client.get(f'repositories/{repo}/{endpoint}/{object_id}')
    out_json = json.loads(out.text)
    if out_json.get('instances') and type(out_json['instances']) is list:
        out_json['instances'].append(instance_json)
    else:
        out_json['instances'] = [instance_json]

    out = config.client.post(f'/repositories/{repo}/{endpoint}/{object_id}', json=out_json)
    out_json = json.loads(out.text)
    print(json.dumps(out_json, indent=2))


if __name__ == '__main__':
    pass
