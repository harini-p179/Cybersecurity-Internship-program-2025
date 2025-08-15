from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import os
import hashlib
from config import Config

class FileEncryption:
    def __init__(self):
        self.key_size = Config.KEY_SIZE
        self.iv_size = Config.IV_SIZE
    
    def generate_key(self):
        """Generate a random AES-256 key"""
        return get_random_bytes(self.key_size)
    
    def generate_iv(self):
        """Generate a random initialization vector"""
        return get_random_bytes(self.iv_size)
    
    def encrypt_file(self, file_data, key=None):
        """
        Encrypt file data using AES-256-CBC
        Returns: (encrypted_data, key, iv)
        """
        if key is None:
            key = self.generate_key()
        
        iv = self.generate_iv()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Pad the data to be a multiple of 16 bytes
        padded_data = pad(file_data, AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        
        return encrypted_data, key, iv
    
    def decrypt_file(self, encrypted_data, key, iv):
        """
        Decrypt file data using AES-256-CBC
        Returns: decrypted_data
        """
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(encrypted_data)
        decrypted_data = unpad(decrypted_padded, AES.block_size)
        
        return decrypted_data
    
    def save_key_info(self, filename, key, iv):
        """Save key and IV information for a file"""
        key_info = {
            'key': base64.b64encode(key).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8')
        }
        
        key_filename = os.path.join(Config.KEY_FOLDER, f"{filename}.key")
        with open(key_filename, 'w') as f:
            f.write(f"KEY:{key_info['key']}\n")
            f.write(f"IV:{key_info['iv']}\n")
        
        return key_filename
    
    def load_key_info(self, filename):
        """Load key and IV information for a file"""
        key_filename = os.path.join(Config.KEY_FOLDER, f"{filename}.key")
        
        if not os.path.exists(key_filename):
            return None, None
        
        with open(key_filename, 'r') as f:
            lines = f.readlines()
            key = base64.b64decode(lines[0].split(':')[1].strip())
            iv = base64.b64decode(lines[1].split(':')[1].strip())
        
        return key, iv
    
    def calculate_file_hash(self, data):
        """Calculate SHA-256 hash of file data for integrity verification"""
        return hashlib.sha256(data).hexdigest()
