import hashlib

def derive_key(password):
    return hashlib.sha256(password.encode()).digest()