from imports import *

from generate_master_key import generate_master_key
from derive_keys import derive_keys

# Function to decrypt a file
def decrypt_file(input_file, output_file, password, hash_algorithm="sha256", iterations=100000):
    with open(input_file, 'rb') as f:
        lines = f.readlines()

    # Read the metadata from the file header
    algorithm = lines[0].decode().split(":")[1].strip()
    salt = lines[1].decode().split(":")[1].strip()
    iv = lines[2].decode().split(":")[1].strip()
    hmac_value = lines[3].decode().split(":")[1].strip()
    encrypted_data = b''.join(lines[4:])

    # Verify the HMAC
    master_key = generate_master_key(password, salt.encode(), iterations, hash_algorithm)
    encryption_key, hmac_key = derive_keys(master_key)
    h = HMAC.new(hmac_key, digestmod=SHA256)
    h.update(iv.encode())
    h.update(encrypted_data)
    if not hmac.compare_digest(h.digest(), hmac_value.encode()):
        raise ValueError("HMAC verification failed")

    # Decrypt the data
    if algorithm == "AES256":
        cipher = AES.new(encryption_key, AES.MODE_CBC, iv.encode())
    elif algorithm == "AES128":
        cipher = AES.new(encryption_key[:16], AES.MODE_CBC, iv.encode())
    elif algorithm == "3DES":
        cipher = DES3.new(encryption_key[:24], DES3.MODE_CBC, iv.encode())
    else:
        raise ValueError("Invalid algorithm")

    decrypted_data = cipher.decrypt(encrypted_data)

    # Unpad the decrypted data
    unpadded_data = unpad(decrypted_data, AES.block_size)

    with open(output_file, 'wb') as f:
        f.write(unpadded_data)