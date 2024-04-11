from imports import *

# Function to derive an encryption key and an HMAC key from the master key using PBKDF2 with one iteration
def derive_keys(master_key):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"encryption_salt",
        iterations=1,
        backend=default_backend()
    )
    encryption_key = kdf.derive(master_key)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"hmac_salt",
        iterations=1,
        backend=default_backend()
    )
    hmac_key = kdf.derive(master_key)

    return encryption_key, hmac_key