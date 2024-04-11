from tool.imports import *

# Function to generate a master key using PBKDF2
def generate_master_key(password, salt, iterations=100000, hash_algorithm="sha256"):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )

    return kdf.derive(password.encode())