from os import CLONE_NEWNS, CLONE_NEWUSER, getlogin, unshare
from subprocess import CalledProcessError, run


def unshare_namespace():
    unshare(CLONE_NEWNS | CLONE_NEWUSER)


def get_id_map(username=None, id_type="uid"):
    username = username or getlogin()
    if id_type not in ("uid", "gid"):
        raise ValueError("id_type must be 'uid' or 'gid'")

    with open(f"/etc/sub{id_type}") as f:
        for line in f:
            if line.startswith(f"{username}:"):
                start, count = line.strip().split(":")[1:]
                return int(start), int(count)
    raise ValueError(f"User {username} not found in /etc/sub{id_type}")


def new_id_map(id_type, pid, id, nsid, count=1, *args, failures=0):
    if id_type not in ("uid", "gid"):
        raise ValueError("id_type must be 'uid' or 'gid")
    cmd_args = [f"new{id_type}map", str(pid), str(id), str(nsid), str(count), *map(str, args)]
    try:
        return run(cmd_args, check=True)
    except CalledProcessError as e:
        if failures > 5:
            raise e
    new_id_map(id_type, pid, id, nsid, count, *args, failures=failures + 1)
