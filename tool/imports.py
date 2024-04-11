from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend

import os
import time

from Crypto.Cipher import DES3, AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC, SHA256, SHA512
from Crypto.Util.Padding import pad, unpad