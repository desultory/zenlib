from getpass import getuser
from multiprocessing import Event, Pipe, Process, Queue
from os import chdir, chroot, getgid, getuid, setgid, setuid

from .namespace import get_id_map, new_id_map, unshare_namespace


class NamespaceProcess(Process):
    """Like process, but runs in a new namespace.
    Puts the target return value in a queue, and any exceptions in a pipe.
    """

    def __init__(self, target=None, args=None, kwargs=None, **ekwargs):
        self.target_root = kwargs.pop("target_root", "/")
        namespace_user = kwargs.pop("namespace_user", getuser())
        self.subuid_start, self.subuid_count = get_id_map(namespace_user, "uid")
        self.subgid_start, self.subgid_count = get_id_map(namespace_user, "gid")
        self.orig_uid = getuid()
        self.orig_gid = getgid()
        self.uidmapped = Event()
        self.unshared = Event()
        self.completed = Event()
        self.exception_recv, self.exception_send = Pipe()
        self.function_queue = Queue()
        super().__init__(target=target, args=args, kwargs=kwargs, **ekwargs)

    def map_ids(self):
        new_id_map("uid", self.pid, 0, self.orig_uid, 1, 1, self.subuid_start, self.subuid_count)
        new_id_map("gid", self.pid, 0, self.orig_gid, 1, 1, self.subgid_start, self.subgid_count)

    def map_unshare_uids(self):
        self.start()

        self.unshared.wait()
        self.map_ids()

        self.uidmapped.set()

    def run(self):
        unshare_namespace()
        self.unshared.set()
        self.uidmapped.wait()
        setuid(0)
        setgid(0)
        chroot(self.target_root)
        chdir("/")
        try:
            self.function_queue.put(self._target(*self._args, **self._kwargs))
        except Exception as e:
            self.exception_send.send(e)
        self.completed.set()
