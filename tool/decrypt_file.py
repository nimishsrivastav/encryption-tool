from tool.imports import *

from tool.generate_master_key import generate_master_key
from tool.derive_keys import derive_keys

# Function to decrypt a file
def decrypt_file(input_file, output_file, password, hash_algorithm="sha512", iterations=100000):   
    """
    Decrypt a file using a password-based key derivation and HMAC verification.

    Args:
        input_file (str)        : The path to the input file to be decrypted.
        output_file (str)       : The path to the output file where the decrypted data will be saved.
        password (str)          : The password used for key derivation.
        hash_algorithm (str)    : The hash algorithm used for key derivation (default is "sha512").
        iterations (int)        : The number of iterations for key derivation (default is 100000).
    """
    
    # Read the input file
    with open(input_file, 'rb') as f:
        lines = f.readlines()

    # Read the metadata from the file header
    algorithm = lines[0].decode().split(":")[1].strip()
    salt = lines[1].split(b":")[1].strip()                  # Reading as bytes
    iv = lines[2].split(b":")[1].strip()                    # Reading as bytes
    hmac_value = lines[3].split(b":")[1].strip()            # Reading as bytes
    encrypted_data = b''.join(lines[4:])                    # Reading as bytes

    # Verify the HMAC
    master_key = generate_master_key(password, salt, iterations, hash_algorithm)
    encryption_key, hmac_key = derive_keys(master_key)

    if hash_algorithm == "sha256":
        h = HMAC.new(hmac_key, digestmod=SHA256)
    elif hash_algorithm == "sha512":
        h = HMAC.new(hmac_key, digestmod=SHA512)

    h.update(iv)
    h.update(encrypted_data)

    if h.digest() != hmac_value:
        raise ValueError("HMAC verification failed")

    # Decrypt the data
    if algorithm == "AES256":
        cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    elif algorithm == "AES128":
        cipher = AES.new(encryption_key[:16], AES.MODE_CBC, iv)
    elif algorithm == "3DES":
        cipher = DES3.new(encryption_key[:24], DES3.MODE_CBC, iv)
    else:
        raise ValueError("Invalid algorithm")

    decrypted_data = cipher.decrypt(encrypted_data)

    # Unpad the decrypted data
    unpadded_data = unpad(decrypted_data, AES.block_size)

    # Write the decrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(unpadded_data)