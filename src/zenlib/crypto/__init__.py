from importlib.util import find_spec
from typing import Callable

# Check if the cryptography library is available

zencrypt: Callable | None
zendecrypt: Callable | None

if find_spec("cryptography") is None:
    zencrypt, zendecrypt = None, None
else:
    from zenlib.crypto.zencrypt import zencrypt, zendecrypt


__all__ = ["zencrypt", "zendecrypt"]
