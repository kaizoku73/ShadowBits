import hashlib
from Crypto.Cipher import AES

def derive_key(password):
    return hashlib.sha256(password.encode()).digest()

def to_seed(password: str) -> int:
    digest = hashlib.sha256(password.encode()).digest()
    return int.from_bytes(digest, 'big')

def encryption(payload, key):
    cipher = AES.new(derive_key(key), AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(payload)
    payload = cipher.nonce + tag + ciphertext
    return payload

def decryption(payload, key):
    if len(payload) < 32:
        raise ValueError("Encrypted payload too short")
    nonce = payload[:16]
    tag = payload[16:32]
    ciphertext = payload[32:]
    cipher = AES.new(derive_key(key), AES.MODE_EAX, nonce=nonce)
    try:
        payload = cipher.decrypt_and_verify(ciphertext, tag)
        return payload
    except ValueError as e:
        raise ValueError("Decryption failed - wrong key or corrupted data")