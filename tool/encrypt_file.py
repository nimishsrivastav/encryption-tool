from tool.imports import *

from tool.generate_master_key import generate_master_key
from tool.derive_keys import derive_keys

# Function to encrypt a file
def encrypt_file(input_file, output_file, password, hash_algorithm="sha256", iterations=100000, algorithm="AES256"):
    with open(input_file, 'rb') as f:
        data = f.read()

    salt = os.urandom(16)
    master_key = generate_master_key(password, salt, iterations, hash_algorithm)

    encryption_key, hmac_key = derive_keys(master_key)

    # Generate a random IV
    iv = get_random_bytes(16)

    # Encrypt the data using the specified algorithm
    if algorithm == "AES256":
        cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    elif algorithm == "AES128":
        cipher = AES.new(encryption_key[:16], AES.MODE_CBC, iv)
    elif algorithm == "3DES":
        cipher = DES3.new(encryption_key[:24], DES3.MODE_CBC, iv)
    else:
        raise ValueError("Invalid algorithm")

    padded_data = pad(data, AES.block_size)

    encrypted_data = cipher.encrypt(padded_data)

    # Create an HMAC of the IV and the encrypted data
    h = HMAC.new(hmac_key, digestmod=SHA256)
    h.update(iv)
    h.update(encrypted_data)
    hmac_value = h.digest()

    # Write the metadata and encrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(b"ALGORITHM:" + algorithm.encode() + b"\n")
        f.write(b"SALT:" + salt + b"\n")
        f.write(b"IV:" + iv + b"\n")
        f.write(b"HMAC:" + hmac_value + b"\n")
        f.write(encrypted_data)