from tool.imports import *

from tool.generate_master_key import generate_master_key
from tool.derive_keys import derive_keys

# Function to encrypt a file
def encrypt_file(input_file, output_file, password, hash_algorithm="sha512", encryption_algorithm="AES256", iterations=100000):
    """
    Encrypt a file using a password-based key derivation, encryption, and HMAC process.

    Args:
        input_file (str)        : The path to the input file to be encrypted.
        output_file (str)       : The path to the output file where the encrypted data will be saved.
        password (str)          : The password used for key derivation.
        hash_algorithm (str)    : The hash algorithm used for key derivation (default is "sha512").
        algorithm (str)         : The encryption algorithm to use (default is "AES256").
        iterations (int)        : The number of iterations for key derivation (default is 100000).
    """
    
    # Read the input file
    with open(input_file, 'rb') as f:
        data = f.read()

    salt = os.urandom(16)                                                               # Generate a salt
    master_key = generate_master_key(password, salt, iterations, hash_algorithm)        # Derive master key

    # Derive encryption and HMAC keys from the master key
    encryption_key, hmac_key = derive_keys(master_key)

    # Generate a random IV
    iv = get_random_bytes(16)

    # Encrypt the data using the specified algorithm
    if encryption_algorithm == "AES256":
        cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    elif encryption_algorithm == "AES128":
        cipher = AES.new(encryption_key[:16], AES.MODE_CBC, iv)
    elif encryption_algorithm == "3DES":
        iv = get_random_bytes(8)                                                        # Generate an 8-byte IV for 3DES
        cipher = DES3.new(encryption_key[:24], DES3.MODE_CBC, iv)
    else:
        raise ValueError("Invalid algorithm")

    # Padding data and encrypting it
    padded_data = pad(data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)

    # Create an HMAC of the IV and the encrypted data
    h = HMAC.new(hmac_key, digestmod=SHA256 if hash_algorithm == "sha256" else SHA512)

    h.update(iv)
    h.update(encrypted_data)
    hmac_value = h.digest()

    # Write the metadata and encrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(b"HASHING ALGORITHM:" + hash_algorithm.encode().upper() + b"\n")
        f.write(b"ENCRYPTION ALGORITHM:" + encryption_algorithm.encode() + b"\n")
        f.write(b"SALT:" + base64.b64encode(salt) + b"\n")
        f.write(b"IV:" + base64.b64encode(iv) + b"\n")
        f.write(b"HMAC:" + base64.b64encode(hmac_value) + b"\n")
        f.write(encrypted_data)