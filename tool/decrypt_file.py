from tool.imports import *

from tool.generate_master_key import generate_master_key
from tool.derive_keys import derive_keys

# Function to decrypt a file
def decrypt_file(input_file, output_file, password, iterations=100000):   
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
    hash_algorithm = lines[0].decode().split(":")[1].strip().lower()
    encryption_algorithm = lines[1].decode().split(":")[1].strip()
    salt = base64.b64decode(lines[2].split(b":")[1].strip())                  # Reading as bytes
    iv = base64.b64decode(lines[3].split(b":")[1].strip())                    # Reading as bytes
    hmac_value = base64.b64decode(lines[4].split(b":")[1].strip())            # Reading as bytes
    encrypted_data = b''.join(lines[5:])                    # Reading as bytes

    print(hash_algorithm)

    # Verify the HMAC
    master_key = generate_master_key(password, salt, iterations, hash_algorithm)
    encryption_key, hmac_key = derive_keys(master_key)

    h = HMAC.new(hmac_key, digestmod=SHA256 if hash_algorithm == "sha256" else SHA512)

    h.update(iv)
    h.update(encrypted_data)

    if h.digest() != hmac_value:
        raise ValueError("HMAC verification failed. File cannot be decrypted!!")

    # Decrypt the data
    if encryption_algorithm == "AES256":
        cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    elif encryption_algorithm == "AES128":
        cipher = AES.new(encryption_key[:16], AES.MODE_CBC, iv)
    elif encryption_algorithm == "3DES":
        cipher = DES3.new(encryption_key[:24], DES3.MODE_CBC, iv)
    else:
        raise ValueError("Invalid algorithm")

    decrypted_data = cipher.decrypt(encrypted_data)

    # Unpad the decrypted data
    unpadded_data = unpad(decrypted_data, AES.block_size)

    # Write the decrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(unpadded_data)