from tool.imports import *

# Function to derive an encryption key and an HMAC key from the master key using PBKDF2 with one iteration
def derive_keys(master_key, hash_algorithm="sha256"):
    """
    Derive an encryption key and an HMAC key from the master key using PBKDF2 with one iteration.

    Args:
        master_key (bytes)  : The master key to derive the keys from.

    Returns:
        tuple               : A tuple containing the derived encryption key and HMAC key.
    """
    
    # Deriving encryption key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256() if hash_algorithm == "sha256" else hashes.SHA512(),       # Selecting appropriate hashing algorithm based on user input
        length=32,                                                                          # Length of derived key
        salt=b"encryption_salt",
        iterations=1,
        backend=default_backend()
    )
    encryption_key = kdf.derive(master_key)

    # Deriving HMAC key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256() if hash_algorithm == "sha256" else hashes.SHA512(),       # Selecting appropriate hashing algorithm based on user input
        length=32,                                                                          # Length of derived key
        salt=b"hmac_salt",
        iterations=1,
        backend=default_backend()
    )
    hmac_key = kdf.derive(master_key)

    return encryption_key, hmac_key