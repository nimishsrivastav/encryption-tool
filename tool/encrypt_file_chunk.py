from tool.imports import *

from tool.generate_master_key import generate_master_key
from tool.derive_keys import derive_keys

CHUNK_SIZE = 1 * 1024 * 1024 * 1024  # 1 GB
MAX_CHUNKS_PER_KEY = 64  # 64 chunks of 1 GB = 64 GB

def encrypt_chunk(data, encryption_key, hmac_key, iv, hash_algorithm):
    # Encrypt the data using the specified algorithm
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    padded_data = pad(data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)

    # Create an HMAC of the IV and the encrypted data
    h = HMAC.new(hmac_key, digestmod=SHA256 if hash_algorithm == "sha256" else SHA512)
    h.update(iv)
    h.update(encrypted_data)
    hmac_value = h.digest()

    return iv, encrypted_data, hmac_value

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
        total_chunks = 0
        key_index = 0
        
        # Generate a salt        
        salt = os.urandom(16)
        
        master_key = generate_master_key(password, salt, iterations, hash_algorithm)        # Derive master key
        
        while True:
            chunk = f.read(CHUNK_SIZE)

            if not chunk:
                break

            if total_chunks % MAX_CHUNKS_PER_KEY == 0:
                master_key = generate_master_key(password, salt, iterations, hash_algorithm)        # Derive master key
                encryption_key, hmac_key = derive_keys(master_key)                                  # Derive encryption and HMAC keys from the master key

                key_index += 1

            # Generate a random IV
            iv = get_random_bytes(16)
            iv, encrypted_data, hmac_value = encrypt_chunk(chunk, encryption_key, hmac_key, iv, hash_algorithm)

            chunk_filename = os.path.join(output_dir, f'encrypted_chunk_{key_index}_{total_chunks}.bin')
            
            with open(chunk_filename, 'wb') as chunk_file:
                chunk_file.write(b"HASHING ALGORITHM:" + hash_algorithm.encode().upper() + b"\n")
                chunk_file.write(b"ENCRYPTION ALGORITHM:" + encryption_algorithm.encode() + b"\n")
                chunk_file.write(b"SALT:" + base64.b64encode(salt) + b"\n")
                chunk_file.write(b"IV:" + base64.b64encode(iv) + b"\n")
                chunk_file.write(b"HMAC:" + base64.b64encode(hmac_value) + b"\n")
                chunk_file.write(b"ITERATIONS:" + str(iterations).encode() + b"\n")
                chunk_file.write(encrypted_data)

            total_chunks += 1
