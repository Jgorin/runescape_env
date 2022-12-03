import pathlib

def resolve_path(path, dir):
    res = pathlib.Path(path).resolve()
    while res != None and res.name != dir and res.name != '':
        res = res.parent
    return res