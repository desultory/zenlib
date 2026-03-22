from importlib.util import find_spec

# Check if the cryptography library is available
if find_spec("cryptography") is None:
    def zencrypt(*args, **kwargs):
        raise ImportError("The 'cryptography' library is required for zencrypt functionality.")
    def zendecrypt(*args, **kwargs):
        raise ImportError("The 'cryptography' library is required for zendecrypt functionality.")
else:
    from zenlib.crypto.zencrypt import zencrypt, zendecrypt


__all__ = ["zencrypt", "zendecrypt"]
