import os
import json
import subprocess
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

CICD_REPO_PATH = os.getenv("CICD_REPO_PATH", "/home/runner/work/simple-monorepo/simple-monorepo")
PROJECT_CONFIG_FILENAME = "configuration.json"

def load_json(meta_file):
    f = open(meta_file)
    data = json.load(f)
    return data

def get_project_config(repo_path, project_id):
    cicd_path = os.path.join(repo_path, "cicd")
    project_config_path = os.path.join(cicd_path, PROJECT_CONFIG_FILENAME)
    project_config_json = load_json(project_config_path)
    for project_config in project_config_json["projects"]:
        if project_id == project_config["id"]:
            return project_config
    return None

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-p", "--project", help="project id")
parser.add_argument("-s", "--stage", help="Stage", default=None)
parser.add_argument("-c", "--configuration", help="Configuration", default=None)
args = vars(parser.parse_args())
project_id = args["project"]
stage = args["stage"]
configuration = args["configuration"]

config = get_project_config(CICD_REPO_PATH, project_id)
if stage is None:
    print(config["path"])
else:
    print(config[stage][configuration])
