import pyotp
import json
import os
from cryptography.fernet import Fernet

class SecurityUtils:
    """
    Utility class for security-related functionality, including:
    - Two-factor authentication
    - Secret management
    - Encryption/decryption for sensitive test data
    """
    
    def __init__(self):
        self.config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config',
            'security_config.json'
        )
        self._load_config()
        self._setup_encryption()
    
    def _load_config(self):
        """
        Load security configuration
        """
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            # Create default config
            self.config = {
                "totp_secrets": {
                    "2fauser": "BASE32SECRET3232",  # Test secret for automation
                    "testuser": "BASE32SECRET3233"
                },
                "encryption_key": Fernet.generate_key().decode('utf-8')
            }
            # Ensure config directory exists
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            # Save default config
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
    
    def _setup_encryption(self):
        """
        Set up encryption for sensitive data
        """
        key = self.config.get("encryption_key", "").encode('utf-8')
        if not key:
            key = Fernet.generate_key()
            self.config["encryption_key"] = key.decode('utf-8')
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
        
        self.cipher = Fernet(key)
    
    def get_totp_secret_for_user(self, username):
        """
        Get the TOTP secret for a specific user
        
        :param username: Username to get the secret for
        :return: TOTP secret
        """
        return self.config.get("totp_secrets", {}).get(username, "")
    
    def generate_totp_code(self, secret):
        """
        Generate a TOTP code for a given secret
        
        :param secret: TOTP secret
        :return: Generated TOTP code
        """
        totp = pyotp.TOTP(secret)
        return totp.now()
    
    def encrypt_data(self, data):
        """
        Encrypt sensitive data
        
        :param data: Data to encrypt (string)
        :return: Encrypted data
        """
        return self.cipher.encrypt(data.encode('utf-8')).decode('utf-8')
    
    def decrypt_data(self, encrypted_data):
        """
        Decrypt sensitive data
        
        :param encrypted_data: Encrypted data to decrypt
        :return: Decrypted data
        """
        return self.cipher.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')
    
    def store_sensitive_credential(self, key, value):
        """
        Store a sensitive credential in the encrypted storage
        
        :param key: Key for the credential
        :param value: Value to store (will be encrypted)
        """
        if "encrypted_credentials" not in self.config:
            self.config["encrypted_credentials"] = {}
        
        self.config["encrypted_credentials"][key] = self.encrypt_data(value)
        
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def get_sensitive_credential(self, key):
        """
        Retrieve a sensitive credential from the encrypted storage
        
        :param key: Key for the credential
        :return: Decrypted credential value
        """
        encrypted_value = self.config.get("encrypted_credentials", {}).get(key, "")
        if not encrypted_value:
            return ""
        
        return self.decrypt_data(encrypted_value)
    
    def generate_secure_password(self, length=12):
        """
        Generate a secure password for test users
        
        :param length: Length of the password
        :return: Generated password
        """
        import random
        import string
        
        # Ensure the password contains at least one of each required character type
        lowercase = random.choice(string.ascii_lowercase)
        uppercase = random.choice(string.ascii_uppercase)
        digit = random.choice(string.digits)
        special = random.choice('!@#$%^&*()-_=+[]{}|;:,.<>?')
        
        # Generate the remaining characters
        remaining_length = length - 4
        all_chars = string.ascii_letters + string.digits + '!@#$%^&*()-_=+[]{}|;:,.<>?'
        remaining_chars = ''.join(random.choice(all_chars) for _ in range(remaining_length))
        
        # Combine all characters and shuffle
        password_chars = lowercase + uppercase + digit + special + remaining_chars
        password_list = list(password_chars)
        random.shuffle(password_list)
        
        return ''.join(password_list)
