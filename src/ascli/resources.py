import copy
import json
import ascli.config as config


def get(id, repo):
    repo = config.get_default_repo(repo)
    dum = config.get(f'/repositories/{repo}/resources/{id}')
    dum_json = json.loads(dum.text)
    print(json.dumps(dum_json, indent=2))


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


def add_instance(container_id, object_id, repo, itype, attach_to_resource, type2, indicator2, barcode2,
                 type3, indicator3):
    """Add an instance to an Archival Object or Resource.

       CONTAINER_ID is the container identifier to be added and OBJECT_ID is the identifier of the Archival Object
       to which the instance should be added, unless the 'attach_to_resource" is True. In that case, the instance
       will be added to the top level of the resource with identifier OBJECT_ID.
    """
    repo = config.get_default_repo(repo)
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

    if attach_to_resource:
        endpoint = "resources"
    else:
        endpoint = "archival_objects"

    dum = config.get(f'/repositories/{repo}/{endpoint}/{object_id}')
    dum_json = json.loads(dum.text)
    if dum_json.get('instances') and type(dum_json['instances']) is list:
        dum_json['instances'].append(instance_json)
    else:
        dum_json['instances'] = [instance_json]

    dum = config.post(f'/repositories/{repo}/{endpoint}/{object_id}', json=dum_json)
    dum_json = json.loads(dum.text)
    print(json.dumps(dum_json, indent=2))


if __name__ == '__main__':
    pass
