from subprocess import CalledProcessError
from .namespace_process import NamespaceProcess


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
