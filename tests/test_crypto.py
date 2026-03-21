from os import urandom
from subprocess import run
from tempfile import NamedTemporaryFile
from unittest import TestCase, main

from zenlib.crypto import zencrypt, zendecrypt

if zencrypt is None or zendecrypt is None:
    print("cryptography library is not installed, skipping crypto tests")


class TestCrypto(TestCase):
    """Tests that zencrypt/zendecrypt are compatible with openssl"""

    def test_zencrypt(self):
        """Tests that zencrypt produces output which openssl can decrypt"""
        with NamedTemporaryFile() as enc_file:
            key = urandom(64).hex()
            plaintext = urandom(128).hex()
            enc_file.write(zencrypt(plaintext, key))
            enc_file.flush()

            res = run(
                ["openssl", "enc", "-d", "-aes256", "-pbkdf2", "-in", enc_file.name, "-k", key],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0)
            self.assertEqual(res.stdout, plaintext)

    def test_zencrypt_iterations(self):
        """Tests that iterations work properly"""
        with NamedTemporaryFile() as enc_file:
            key = urandom(64).hex()
            plaintext = urandom(128).hex()
            enc_file.write(zencrypt(plaintext, key, iterations=100))
            enc_file.flush()

            res = run(
                [
                    "openssl",
                    "enc",
                    "-d",
                    "-aes256",
                    "-pbkdf2",
                    "-in",
                    enc_file.name,
                    "-k",
                    key,
                    "-pbkdf2",
                    "-iter",
                    "100",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0)
            self.assertEqual(res.stdout, plaintext)

    def test_zendecrypt(self):
        """Tests that zendecrypt can decrypt output from openssl"""
        with NamedTemporaryFile() as enc_file:
            key = urandom(64).hex()
            plaintext = urandom(128).hex()
            run(
                ["openssl", "enc", "-aes256", "-pbkdf2", "-in", "-", "-out", enc_file.name, "-k", key],
                input=plaintext,
                text=True,
            )
            enc_file.flush()

            decrypted = zendecrypt(enc_file.read(), key)
            self.assertEqual(decrypted, plaintext.encode())

    def test_zendecrypt_iterations(self):
        """Tests that zendecrypt can decrypt output from openssl with iterations"""
        with NamedTemporaryFile() as enc_file:
            key = urandom(64).hex()
            plaintext = urandom(128).hex()
            run(
                [
                    "openssl",
                    "enc",
                    "-aes256",
                    "-pbkdf2",
                    "-in",
                    "-",
                    "-out",
                    enc_file.name,
                    "-k",
                    key,
                    "-pbkdf2",
                    "-iter",
                    "100",
                ],
                input=plaintext,
                text=True,
            )
            enc_file.flush()

            decrypted = zendecrypt(enc_file.read(), key, iterations=100)
            self.assertEqual(decrypted, plaintext.encode())

    def test_zencrypt_loop(self):
        """Tests that zencrypt -> zendecrypt works properly"""
        key = urandom(64).hex()
        plaintext = urandom(128).hex()
        ciphertext = zencrypt(plaintext, key)
        decrypted = zendecrypt(ciphertext, key)
        self.assertEqual(decrypted, plaintext.encode())

    def test_zencrypt_raw(self):
        """Tests that raw mode works properly (with larger salt)"""
        key = urandom(64).hex()
        salt = urandom(64)
        plaintext = urandom(128).hex()
        ciphertext = zencrypt(plaintext, key, salt=salt, raw=True)
        decrypted = zendecrypt(ciphertext, key, salt=salt, raw=True)
        self.assertEqual(decrypted, plaintext.encode())


if __name__ == "__main__":
    main()
