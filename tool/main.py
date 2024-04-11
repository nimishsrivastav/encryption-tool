from imports import *

from encrypt_file import encrypt_file
from decrypt_file import decrypt_file

# Test the encryption/decryption
if __name__ == "__main__":
    input_file = "files/test.txt"
    output_file_encrypted = "files/test_encrypted.txt"
    output_file_decrypted = "files/test_decrypted.txt"
    password = "password123"
    
    encryption_start_time = time.time()
    encrypt_file(input_file, output_file_encrypted, password, algorithm="AES256")
    encryption_end_time = time.time()
    encryption_time = encryption_end_time - encryption_start_time
    print(f"Encryption time: {encryption_time:.6f} seconds")

    # decryption_start_time = time.time()
    # decrypt_file(output_file_encrypted, output_file_decrypted, password)
    # decryption_end_time = time.time()
    # decryption_time = decryption_end_time - decryption_start_time
    # print(f"Decryption time: {decryption_time:6f} seconds")