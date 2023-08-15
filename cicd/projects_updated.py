import os
import requests
import json
import subprocess
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from git import Repo

META_FILE_NAME = "project.json"
LAST_COMMIT = "HEAD~1"
CICD_REPO_PATH = os.getenv("CICD_REPO_PATH", "/home/runner/work/simple-monorepo/simple-monorepo")

def get_status(repo, path, commit = LAST_COMMIT):
    changed = [item.a_path for item in repo.index.diff(commit)]
    if path in repo.untracked_files:
        return "untracked"
    elif path in changed:
        return "modified"
    else:
        return "na"

def search_meta(repo_path, path):
    meta_file = os.path.join(path, META_FILE_NAME)
    exist_meta = os.path.exists(meta_file)
    if exist_meta:
        return meta_file
    else:
        if path == repo_path:
            return None
        return search_meta(repo_path, os.path.dirname(path))

def load_json(meta_file):
    f = open(meta_file)
    data = json.load(f)
    return data

def search_in_updated_projects(repo_path, commit = LAST_COMMIT):
    repo = Repo(repo_path)
    projects = set()
    for item in repo.index.diff(commit):
        status = get_status(repo, item.a_path)
        if status == "modified":
            file_path = os.path.join(repo_path, item.a_path)
            modified_path = os.path.dirname(file_path)
            meta_file = search_meta(repo_path, modified_path)
            if meta_file is not None:
                info = load_json(meta_file)
                projects.add(info["name"])
    if len(projects) == 0:
        projects.add("empty")
    return projects

def get_project_matrix(projects):
    project_list = list(projects)
    list_str = "["
    for project in project_list:
        if len(list_str) <= 1:
            list_str += f"\"{project}\""
        else:
            list_str += f",\"{project}\""
    list_str += "]"
    return list_str

def get_current_branch(repo_path):
    repo = Repo(repo_path)
    return str(repo.active_branch)

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--commit", help="Commit or branch name", default=LAST_COMMIT)
args = vars(parser.parse_args())
commit = args["commit"]

projects = search_in_updated_projects(CICD_REPO_PATH, commit)
print(get_project_matrix(projects))
