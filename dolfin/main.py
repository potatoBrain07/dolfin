import os
import sys
import argparse
import getpass
import tarfile
import io
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64

EXTENSION = ".df"


# ── Crypto core ────────────────────────────────────────────────────────────────

def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_bytes(content: bytes, password: str) -> bytes:
    salt = os.urandom(16)
    key = generate_key(password, salt)
    ciphertext = Fernet(key).encrypt(content)
    return salt + ciphertext


def decrypt_bytes(content: bytes, password: str) -> bytes:
    salt = content[:16]
    ciphertext = content[16:]
    key = generate_key(password, salt)
    return Fernet(key).decrypt(ciphertext)  # raises InvalidToken on wrong password


# ── File operations ────────────────────────────────────────────────────────────

def encrypt_file(path: Path, password: str):
    out_path = path.with_suffix(path.suffix + EXTENSION)
    if out_path.exists():
        print(f"Error: {out_path} already exists.")
        return
    content = path.read_bytes()
    encrypted = encrypt_bytes(content, password)
    out_path.write_bytes(encrypted)
    print(f"Encrypted: {path} → {out_path}")


def decrypt_file(path: Path, password: str):
    if path.suffix != EXTENSION:
        print(f"Error: {path} doesn't have a {EXTENSION} extension.")
        return
    original_path = path.with_suffix("")  # strip .df
    if original_path.exists():
        print(f"Error: {original_path} already exists.")
        return
    try:
        content = path.read_bytes()
        decrypted = decrypt_bytes(content, password)
        original_path.write_bytes(decrypted)
        path.unlink()
        print(f"Decrypted: {path} → {original_path}")
    except InvalidToken:
        print(f"Error: Wrong password or corrupted file ({path}).")


# ── Directory operations ───────────────────────────────────────────────────────

def encrypt_dir(path: Path, password: str):
    """Encrypt each file in directory individually, in-place."""
    files = [f for f in path.rglob("*") if f.is_file() and f.suffix != EXTENSION]
    if not files:
        print("No files to encrypt.")
        return
    for f in files:
        encrypt_file(f, password)


def decrypt_dir(path: Path, password: str):
    """Decrypt each .df file in directory individually, in-place."""
    files = [f for f in path.rglob("*") if f.is_file() and f.suffix == EXTENSION]
    if not files:
        print("No encrypted files found.")
        return
    for f in files:
        decrypt_file(f, password)


def encrypt_dir_onefile(path: Path, password: str):
    """Pack directory into a tar, encrypt it, write dirname.df"""
    out_path = path.parent / (path.name + EXTENSION)
    if out_path.exists():
        print(f"Error: {out_path} already exists.")
        return
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        tar.add(path, arcname=path.name)
    encrypted = encrypt_bytes(buf.getvalue(), password)
    out_path.write_bytes(encrypted)
    print(f"Encrypted archive: {path}/ → {out_path}")


def decrypt_dir_onefile(path: Path, password: str):
    """Decrypt a .df archive and restore directory structure."""
    if path.suffix != EXTENSION:
        print(f"Error: {path} doesn't have a {EXTENSION} extension.")
        return
    try:
        content = path.read_bytes()
        decrypted = decrypt_bytes(content, password)
        buf = io.BytesIO(decrypted)
        with tarfile.open(fileobj=buf, mode="r:gz") as tar:
            tar.extractall(path=path.parent)
        path.unlink()
        print(f"Decrypted archive: {path} → {path.stem}/")
    except InvalidToken:
        print(f"Error: Wrong password or corrupted archive.")
    except tarfile.TarError:
        print(f"Error: Not a valid archive. Was this encrypted with --onefile?")


# ── CLI ────────────────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="dolfin",
        description="Dolfin — file encryption tool"
    )
    subparsers = parser.add_subparsers(dest="command")

    # shared arguments factory
    def add_common(sub):
        group = sub.add_mutually_exclusive_group(required=True)
        group.add_argument("-f", "--file", metavar="FILE", help="Target file")
        group.add_argument("-d", "--dir", metavar="DIR", help="Target directory")
        sub.add_argument("-p", "--password", action="store_true",
                         help="Prompt for password (always silent)")

    enc = subparsers.add_parser("enc", help="Encrypt a file or directory")
    add_common(enc)
    enc.add_argument("--onefile", action="store_true",
                     help="Pack directory into a single .df archive (requires -d)")

    dec = subparsers.add_parser("dec", help="Decrypt a file or directory")
    add_common(dec)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    password = getpass.getpass("Password: ")

    if args.command == "enc":
        if args.file:
            encrypt_file(Path(args.file), password)
        elif args.dir:
            if args.onefile:
                encrypt_dir_onefile(Path(args.dir), password)
            else:
                encrypt_dir(Path(args.dir), password)

    elif args.command == "dec":
        if args.file:
            # could be a single file or a onefile archive — handled by extension check
            decrypt_file(Path(args.file), password)
        elif args.dir:
            decrypt_dir(Path(args.dir), password)


if __name__ == "__main__":
    main()
