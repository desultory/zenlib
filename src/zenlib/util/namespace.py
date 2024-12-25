from multiprocessing import Event, Pipe, Process, Queue
from os import CLONE_NEWNS, CLONE_NEWUSER, chroot, getlogin, setgid, setuid, unshare
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


def new_id_map(id_type, pid, id, nsid, count=2**16):
    if id_type not in ("uid", "gid"):
        raise ValueError("id_type must be 'uid' or 'gid")
    args = [f"new{id_type}map", str(pid), str(id), str(nsid), str(count)]
    try:
        run(args, check=True)
    except CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Stderr: {e.stderr}")
        print(f"Stdout: {e.stdout}")
        raise e


class NamespaceProcess(Process):
    """Like process, but runs in a new namespace.
    Puts the target return value in a queue, and any exceptions in a pipe.
    """

    def __init__(self, target=None, args=None, kwargs=None, **ekwargs):
        self.uid = int(kwargs.pop("uid", 0))
        self.gid = int(kwargs.pop("gid", 0))
        self.target_root = kwargs.pop("target_root", "/")
        namespace_user = kwargs.pop("namespace_user", getlogin())
        self.subuid_start, self.subuid_count = get_id_map(namespace_user, "uid")
        self.subgid_start, self.subgid_count = get_id_map(namespace_user, "gid")
        self.uidmapped = Event()
        self.completed = Event()
        self.exception_recv, self.exception_send = Pipe()
        self.function_queue = Queue()
        super().__init__(target=target, args=args, kwargs=kwargs, **ekwargs)

    def map_ids(self):
        new_id_map("uid", self.pid, self.uid, self.subuid_start, self.subuid_count)
        new_id_map("gid", self.pid, self.gid, self.subgid_start, self.subgid_count)

    def map_unshare_uids(self):
        self.start()
        self.map_ids()
        self.uidmapped.set()

    def run(self):
        unshare_namespace()
        self.uidmapped.wait()
        setuid(self.uid)
        setgid(self.gid)
        chroot(self.target_root)
        try:
            self.function_queue.put(self._target(*self._args, **self._kwargs))
        except Exception as e:
            self.exception_send.send(e)
        self.completed.set()


def nschroot(target, *args, **kwargs):
    p = NamespaceProcess(target=target, args=args, kwargs=kwargs)
    try:
        p.map_unshare_uids()
    except CalledProcessError as e:
        print(f"Error: {e}")
        p.terminate()
        raise e

    p.completed.wait()
    if p.exception_recv.poll():
        p.terminate()
        raise p.exception_recv.recv()

    ret = p.function_queue.get()
    p.terminate()
    return ret


def nsexec(target, *args, **kwargs):
    p = NamespaceProcess(target=target, args=args, kwargs=kwargs)
    try:
        p.map_unshare_uids()
    except CalledProcessError as e:
        print(f"Error: {e}")
        p.terminate()
        raise e

    p.completed.wait()
    if p.exception_recv.poll():
        p.terminate()
        raise p.exception_recv.recv()

    ret = p.function_queue.get()
    p.terminate()
    return ret
