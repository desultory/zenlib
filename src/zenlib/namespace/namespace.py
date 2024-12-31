from os import CLONE_NEWNS, CLONE_NEWUSER, getlogin, unshare, getuid
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


def write_id_map(id_type, pid, *args, failures=0):
    if id_type not in ("uid", "gid"):
        raise ValueError("id_type must be 'uid' or 'gid")

    map_file = f"/proc/{pid}/uid_map" if id_type == "uid" else f"/proc/{pid}/gid_map"

    # Get id, nsid, count tuples from args
    map_contents = [f"{id} {nsid} {count}" for id, nsid, count in zip(*[iter(args)] * 3)]

    try:
        with open(map_file, "w") as f:
            f.write("\n".join(map_contents))
    except PermissionError as e:
        if failures > 5:
            raise e
        new_id_map(id_type, pid, *args, failures=failures + 1)

def new_id_map(id_type, pid, id, nsid, count=1, *args, failures=0):
    if id_type not in ("uid", "gid"):
        raise ValueError("id_type must be 'uid' or 'gid")

    if getuid() == 0:
        return write_id_map(id_type, pid, id, nsid, count, *args)

    try:
        cmd_args = [f"new{id_type}map", str(pid), str(id), str(nsid), str(count), *map(str, args)]
        return run(cmd_args, check=True, capture_output=True)
    except CalledProcessError as e:
        if failures > 5:
            raise e
    new_id_map(id_type, pid, id, nsid, count, *args, failures=failures + 1)
