from subprocess import CalledProcessError
from typing import Any, Callable, TypeVar

from .namespace_process import NamespaceProcess

R = TypeVar("R")


def nsexec(target: Callable[..., R], *args: Any, **kwargs: Any) -> R:
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
