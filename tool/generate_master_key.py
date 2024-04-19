from tool.imports import *

# Function to generate a master key using PBKDF2
def generate_master_key(password, salt, iterations=100000, hash_algorithm="sha256"):
    """
    Generate a master key using PBKDF2.

    Args:
        password (str)          : The password to derive the key from.
        salt (bytes)            : The salt value for key derivation.
        iterations (int)        : The number of iterations for key derivation (default is 100000).
        hash_algorithm (str)    : The hash algorithm to use (default is "sha256").

    Returns:
        bytes                   : The derived master key.
    """
    
    # Creation of PBKDF2HMAC key derivation function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256() if hash_algorithm == "sha256" else hashes.SHA512(),           # Selecting appropriate hashing algorithm based on user input
        length=32,                                                                              # Length of derived key
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )

    # Deriving master key from the password set by the user
    return kdf.derive(password.encode())
