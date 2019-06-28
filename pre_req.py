
#pip install cfn_flip
from cfn_flip import flip, to_yaml, to_json
import os,json
from pprint import pprint
from datetime import datetime


def get_list_of_resources(file_name):
    """
        considers only yaml format or yaml string
    """
    if os.path.exists(file_name):
        with open(file_name) as f:
            cloud_formation = f.read()
    else:
        cloud_formation = file_name
    AwsCloudFormationJson = json.loads(to_json(cloud_formation))
    resources_used = set()
    for resourceName, resourceDict in AwsCloudFormationJson["Resources"].items():
        resources_used.add(resourceDict['Type'])
    return resources_used
def effecitve_required_permissions(list_of_resources):
    """
        figures out list of actions required.
        as of now, we are granting all on a particular resource
    """
    actions = []
    for resource in list_of_resources:
        _, category, subcategory = resource.split("::")
        actions.append(category.lower()+":*"+subcategory)
    return actions

def get_permission_statement(file_name):
    """
        returns json string
    """
    resources = get_list_of_resources(file_name)
    actions = effecitve_required_permissions(resources)
    date = datetime.now()
    return {
        "Version": "{year}-{month}-{day}".format(year=date.year, month=date.month, day=date.day),
        "Statement": [{"Effect": "Allow","Action": [actions],"Resource": "*"}]
    }