"""
Wrappers for the cryptography library to make it act kinda like openssl

in raw mode it does not try to be compatible with openssl

openssl compatibility here means it writes the file in a way "openssl enc" should be able to handle
such as:
    openssl enc -aes256 -pbkdf2
or:
    openssl enc -d -aes256 -pbkdf2
"""

from os import urandom
from typing import Tuple

from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.padding import PKCS7

SALT_SIZE = 8  # OpenSSL uses an 8 byte salt
# In encrypted files this is stored at the start of the file as "Salted__" followed by the salt
DEFAULT_ITERATIONS = 10000  # OpenSSL's default is 10000 iterations for PBKDF2


def derive_key_iv(password: bytes, salt: bytes, iterations: int = DEFAULT_ITERATIONS) -> Tuple[bytes, bytes]:
    """Derive a key and IV from the password and salt using PBKDF2
    The salt size should be 8bytes for compatibility with OpenSSL
    """
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=48,  # 32 bytes for key + 16 bytes for IV
        salt=salt,
        iterations=iterations,
    )
    key_iv = kdf.derive(password)
    return key_iv[:32], key_iv[32:]


def zencrypt(
    data: bytes | str,
    password: bytes | str,
    salt: bytes | None = None,
    salt_size: int = SALT_SIZE,
    iterations: int = DEFAULT_ITERATIONS,
    raw: bool = False,
) -> bytes:
    """Encrypt data using AES-256-CBC with a password
    The output format is "Salted__" + salt + ciphertext, which is compatible with OpenSSL's default format

    A salt can be provided, but if not it will be generated randomly. The salt must be 8 bytes long if provided.

    In raw mode, the salt can be any size and the output will just be the ciphertext, the caller is responsible for handling the salt and including it in the output if desired
    """
    if isinstance(data, str):
        data = data.encode()

    if isinstance(password, str):
        password = password.encode()

    if salt is None:
        salt = urandom(salt_size)
    elif not raw:  # If raw is True, we won't check the salt size since it won't be included in the output
        if len(salt) != salt_size:
            raise ValueError(f"Salt must be {salt_size} bytes long, found: {len(salt)} bytes")

    key, iv = derive_key_iv(password, salt, iterations)
    padder = PKCS7(AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(AES(key), CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return b"Salted__" + salt + ciphertext if not raw else ciphertext


def zendecrypt(
    data: bytes,
    password: bytes | str,
    salt: bytes | None = None,
    iterations: int = DEFAULT_ITERATIONS,
    raw: bool = False,
) -> bytes:
    """Decrypt data encrypted with zencrypt/OpenSSL's default format
    if raw is True, then a salt must be provided and the data is just the ciphertext, otherwise the data is expected to be in the format "Salted__" + salt + ciphertext
    """
    if not raw:
        if not data.startswith(b"Salted__"):
            raise ValueError("Data does not start with 'Salted__', cannot extract salt")
        salt = data[8:16]
        ciphertext = data[16:]
    else:
        if salt is None:
            raise ValueError("Salt must be provided when raw is True")
        ciphertext = data

    if isinstance(password, str):
        password = password.encode()

    key, iv = derive_key_iv(password, salt, iterations)
    cipher = Cipher(AES(key), CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = PKCS7(AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data
