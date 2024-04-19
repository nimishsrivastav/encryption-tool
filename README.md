# File Encryption/Decryption Utility


## Introduction
This utility is created to perform encryption and decryption for different file types. Here, we are using the concept of **Password-Based Key Derivation Function 2 (PBKDF2)**. PBKDF2 is a type of **Key Derivation Function (KDF)** that reduces the vulnerability to brute-force attacks on passwords. PBKDF2 applies a pseudorandom function, such as **Hash-Based Message Authentication Code (HMAC)**, to the input password or passphrase along with a salt value and repeats the process many times to produce a derived key, which can then be used as a cryptographic key in subsequent operations. The added computational work makes password cracking much more difficult, and is known as key stretching.

The program here creates a master key using PBKDF2 function with the support for both **SHA-256 and SHA-512** hashes. The program encrypts the data using CBC chaining mode and supports **3DES, AES-128, and AES-256** algorithms. A randomly generated IV that is one block in size is used. The number of iterations are chosen to deter password cracking, and the program provides rudimentary performance numbers, such as encryption and decryption time (in seconds) to compare the performance of encryption and decryption processes under different combinations of hashing and encryption algorithms. The program verifies that its PBKDF2 implementation creates the same output as a library for the same hashing algorithm. It also derives an encryption key and an HMAC key from the master key using PBKDF2 with one iteration, using a fixed string as a 'salt' argument. The program is also able to decrypt the data, which requires it to read in the algorithms used from the metadata written out in the header (included in the encrypted file). Below combinations of hashing and encryption algorithms are used in this utility:

| Hashing Algorithm | Encryption Algirithm |
| ----------------- | -------------------- |
|       SHA-256     |        3DES          |
|                   |        AES-128       |
|                   |        AES-256       |
|       SHA-512     |        3DES          |
|                   |        AES-128       |
|                   |        AES-256       |


## Software Used
This utility is created using Python v3.11.7

## Package(s) Installation
This utility uses following Python packages:

| Packages      | Version   | Usage                                             |
| ------------- | --------- | ------------------------------------------------- |
| cryptography  | v42.0.5   | Used for KDF and Hashes                           |
| pycryptodome  | v3.20.0   | Used for Encryption and Hashing                   |
| flask         | v3.0.2    | Used for creating web app for using the utility   |

These packages can be installed by running this command present in the project: `pip install -r requirements.txt`

## Folder Structure for File Storage
Below is the folder structure for the utility:

files
  L decrypted_files
  L encrypted_files
  L uploaded_files

These folders will be created by the utility if not present. Files will be stored as below: 
![folder_structure_for_file_storage](/assets/images/folder_structure_for_file_storage.PNG)

## Working of Utility
Below is the first page which user sees when the utility is started: ![welcome_page](/assets/images/welcome_page.PNG)

Here user can upload a file from the file explorer and click on 'Upload' button to save it in the **'files/uploaded_files'** directory of this utility. The utility accepts files with extension **'txt', 'enc', 'doc', 'docx', 'xls', 'xlsx', 'json', 'xml'**. To refrain user from uploading a file of any other format, an error message will be displayed if a wrong file format is chosen. ![file_upload_error](/assets/images/file_upload_error.PNG)

Once the file is successfully uploaded, user will be provided with two options: to **Encrypt** the file or to **Decrypt** the file. User can click of either of the buttons to choose the action to be performed on the uploaded file. ![encrypt_decrypt_buttons](/assets/images/encrypt_decrypt_buttons.PNG) The uploaded file will also be saved in the **uploaded_files** directory as displayed in the [Folder Structure for File Storage](#folder-structure-for-file-storage) section. For example, below are the contents of the original file:
![original_file](/assets/images/original_file.PNG)

If user clicks on **Encryption** button, page will be redirected to **/encrypt/<filename>** route. There, user will select the **Hashing Algorithm**, **Encryption Algorithm**, **No. of Iterations**, and **Password** to perform file encryption. File will be encrypted and stored in the **'files/encrypted_files'** directory with **.enc** extension as displayed in the [Folder Structure for File Storage](#folder-structure-for-file-storage) section. Encryption time (in seconds) is also calculated for the encrypted file. ![encrypt_file](/assets/images/encrypt_file.PNG)

The contents of encrypted file includes following metadata alongwith the encrypted data:
* Hashing Algorithm
* Encryption Algorithm
* Salt
* Initialization Vector (IV)
* HMAC
* Iterations

The metadata stored is used during file decryption process. The Hashing Algorithm, Encryption Algorithm, and Iterations are stored as string. The Salt, IV, and the HMAC are stored in Base 64 encoding. And the Encrypted data is stored in binary format. ![encrypted_file_contents](/assets/images/encrypted_file_contents.PNG)

The encrypted file is now the input file for the decryption process, which is initiated when user clicks on **Decryption** button, redirecting to **/decrypt/<encrypted_file>** route. In decryption function, the file is read line by line to read the metadata and proceed with decryption. Once all the requirements are satisfied, the file will be decrypted and stored in **decrypted_files** folder with filename same as the original file as displayed in the [Folder Structure for File Storage](#folder-structure-for-file-storage) section. Decryption time (in seconds) is also calculated for the decrypted file. ![decrypt_file](/assets/images/decrypt_file.PNG) ![decrypted_file](/assets/images/decrypted_file.PNG)

The utility will not allow user to decrypt file if file contents are tampered with or password entered is incorrect. ![decrypt_file](/assets/images/decrypt_file_error.PNG) Server error will be displayed if any un-encrypted file is uploaded in the utility for decryption.


## About the Hashing and Encryption Algorithms Used
Below is the list of hashing and encryption algorithms used in this utility:

| Algorithm | Used For 		| Description | Output Size | Block Size | Key Length |
| --------- | ------------- | ----------- | ----------- | ---------- | ---------- |
| SHA-256	| Hashing  		| SHA-256 is part of the SHA-2 family of hash functions. It is designed to take an input message and produce a fixed-size output hash value, which is typically used for verifying data integrity. SHA-256 is widely used in various security applications and protocols, including TLS, SSL, PGP, and Bitcoin. | 256 bits (32 bytes) | - | - |
| SHA-512	| Hashing  		| SHA-512 is another member of the SHA-2 family of hash functions. It is similar to SHA-256 but produces a larger hash value for increased security. SHA-512 is often used in situations where stronger security guarantees are required, such as in cryptographic applications and protocols. | 512 bits (64 bytes) | - | - |
| 3-DES		| Encryption 	| 3-DES is a symmetric key encryption algorithm that applies the DES encryption algorithm three times to each data block. It was designed to provide increased security over the original DES algorithm by using multiple encryption rounds. However, due to advances in cryptography, 3-DES is now considered relatively insecure and has been largely replaced by more modern encryption algorithms such as AES. | - | 64 bits (8 bytes) | 168 bits (21 bytes) |
| AES-128	| Encryption 	| AES-128 is a variant of the AES encryption standard with a key size of 128 bits. It is widely used for encrypting sensitive data in various security applications. AES-128 provides a good balance between security and performance, making it suitable for many encryption tasks. | - | 128 bits (16 bytes) | 128 bits (16 bytes) |
| AES-256	| Encryption 	| AES-256 is a variant of the AES encryption standard with a key size of 256 bits. It is considered more secure than AES-128 due to its larger key size, which provides stronger security against brute-force attacks. AES-256 is often used in situations where stronger security guarantees are required, such as in government and military applications. | - | 128 bits (16 bytes) | 256 bits (32 bytes) |


## Functions created
1. Generation of master key [tool/generate_master_key.py](tool/generate_master_key.py)
2. Key Derivation Function [tool/derive_keys.py](tool/derive_keys.py)
3. File Encryption [tool/encrypt.py](tool/encrypt.py)
4. File Decryption [tool/decrypt.py](tool/decrypt.py)
5. The Flask Web App [app.py](app.py)

## Result
The file is encrypted and decrypted successfully using the combinations of hashing and encryption algorithms mentioned in [Introduction](#introduction) section. As of 2023[^1], OWASP recommended to use **600,000 iterations** for PBKDF2-HMAC-SHA256 and **210,000 iterations** for PBKDF2-HMAC-SHA512. Below are the times calculated for encryption and decryption for different iteration rounds while file size is 1.97 KB :

| Cipher Suite Used | No. of Iterations | Encryption Time (in seconds) | Decryption Time (in seconds) |
| ----------------- | ----------------- | ---------------------------- | ---------------------------- |
| SHA256_3DES       | 100,000           | 0.7951                       | 0.4696                       |
| SHA256_AES128     | 100,000           | 0.6210                       | 0.3772                       |
| SHA256_AES256     | 100,000           | 0.3182                       | 0.2571                       |
|                   |                   |                              |                              |
| SHA512_3DES       | 50,000            | 0.4448                       | 0.3063                       |
| SHA512_AES128     | 50,000            | 0.2514                       | 0.1947                       |
| SHA512_AES256     | 50,000            | 0.2128                       | 0.1916                       |
|                   |                   |                              |                              |
| SHA256_3DES       | 500,000           | 0.9001                       | 0.9489                       |
| SHA256_AES128     | 500,000           | 1.3190                       | 1.3322                       |
| SHA256_AES256     | 500,000           | 1.0780                       | 1.2834                       |
|                   |                   |                              |                              |
| SHA512_3DES       | 210,000           | 1.3027                       | 1.3033                       |
| SHA512_AES128     | 210,000           | 0.8219                       | 0.6413                       |
| SHA512_AES256     | 210,000           | 0.4980                       | 0.3047                       |
|                   |                   |                              |                              |
| SHA256_3DES       | 600,000           | 0.8911                       | 0.8411                       |
| SHA256_AES128     | 600,000           | 1.2477                       | 1.5400                       |
| SHA256_AES256     | 600,000           | 1.2155                       | 1.2852                       |

From the above table, we can observe that as the number of iterations increase, the encryption/decryption time also increase. The time calculated here would also depend on the file contents, type, and size. The higher the number of iterations, more secure the file will be as brute forcing the password would be difficult.

[^1]: [Wikipedia | PBKDF2](https://en.wikipedia.org/wiki/PBKDF2)