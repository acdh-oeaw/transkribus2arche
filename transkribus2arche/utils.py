import glob
import json
from datetime import datetime

def read_json(path_to_file):
    with open(path_to_file) as f:
        data = json.load(f)
        return data


def list_docs(path_to_config):
    config = read_json(path_to_config)
    docs_glob_pattern = glob.glob(f"{config['col_dir']}/col/*/*.json")
    return docs_glob_pattern


def get_md_dict(trans_doc, path_to_config):
    config = read_json(path_to_config)
    item = {}
    data = read_json(trans_doc)
    md = data['md']
    mapping = config['mapping']
    for key, value in mapping.items():
        obj = md.get(value)
        if 'Date' in key and obj is not None:
            try:
                obj = datetime.fromtimestamp(obj)
            except ValueError:
                obj = datetime.fromtimestamp(obj / 1000)  
        if 'hasExtend' in key:
            obj = config['arche_extend_pattern'].format(obj)
        if not obj:
            continue
        item[key] = f"{obj}"
    return item