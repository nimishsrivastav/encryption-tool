# Importing necessary modules from Cryptography library for key derivation and hashing
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend

# Importing necessary modules from Crypto library for encryption and hashing
from Crypto.Cipher import DES3, AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC, SHA256, SHA512
from Crypto.Util.Padding import pad, unpad

import os
import time
import base64