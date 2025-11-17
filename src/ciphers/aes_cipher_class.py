"""
AES Cipher Class Implementation
Authors: Salah, Fares, Ziad, Zeiad
Description: AES encryption implementation with step visualization.
"""

from typing import List, Tuple
from cipher_base import CipherBase
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


class AESCipher(CipherBase):
    """AES cipher implementation with visual step tracking."""
    
    def __init__(self, key_size: int = 256):
        """
        Initialize the AES cipher.
        
        Args:
            key_size (int): Key size in bits (128, 192, or 256)
        """
        self.name = f"AES-{key_size}"
        self.key_size = key_size // 8  # Convert bits to bytes
        
    def _generate_key(self, password: str) -> bytes:
        """
        Generate a fixed-size key from a password.
        
        Args:
            password (str): User-provided password
            
        Returns:
            bytes: Fixed-size encryption key
        """
        from hashlib import sha256
        # Use SHA-256 to create a consistent key from password
        key = sha256(password.encode()).digest()
        return key[:self.key_size]
    
    def encrypt(self, plaintext: str, key: str) -> Tuple[str, List[dict]]:
        """
        Encrypt plaintext using AES.
        
        Args:
            plaintext (str): The text to encrypt
            key (str): The password/key string
            
        Returns:
            Tuple[str, List[dict]]: (ciphertext in base64, visualization steps)
        """
        steps = []
        
        # Step 1: Initialize
        steps.append({
            'step_number': 1,
            'title': 'Initialize AES Encryption',
            'description': f'Using {self.name} encryption mode',
            'details': f'Input length: {len(plaintext)} characters'
        })
        
        # Step 2: Generate key
        encryption_key = self._generate_key(key)
        steps.append({
            'step_number': 2,
            'title': 'Key Derivation',
            'description': 'Generate encryption key from password',
            'details': f'Using SHA-256 hash → {self.key_size * 8}-bit key'
        })
        
        # Step 3: Convert to bytes
        plaintext_bytes = plaintext.encode('utf-8')
        steps.append({
            'step_number': 3,
            'title': 'Encode Plaintext',
            'description': 'Convert text to bytes',
            'details': f'{len(plaintext)} chars → {len(plaintext_bytes)} bytes'
        })
        
        # Step 4: Apply padding
        padded_data = pad(plaintext_bytes, AES.block_size)
        padding_added = len(padded_data) - len(plaintext_bytes)
        steps.append({
            'step_number': 4,
            'title': 'Apply PKCS7 Padding',
            'description': f'Pad to {AES.block_size}-byte blocks',
            'details': f'Added {padding_added} bytes of padding'
        })
        
        # Step 5: Generate IV
        iv = get_random_bytes(AES.block_size)
        steps.append({
            'step_number': 5,
            'title': 'Generate IV',
            'description': 'Create random initialization vector',
            'details': f'IV size: {len(iv)} bytes (for CBC mode)'
        })
        
        # Step 6: Create cipher and encrypt
        cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
        ciphertext_bytes = cipher.encrypt(padded_data)
        steps.append({
            'step_number': 6,
            'title': 'AES Encryption',
            'description': 'Encrypt padded data using AES-CBC',
            'details': f'Processed {len(padded_data)} bytes → {len(ciphertext_bytes)} bytes'
        })
        
        # Step 7: Combine IV and ciphertext
        combined = iv + ciphertext_bytes
        steps.append({
            'step_number': 7,
            'title': 'Combine IV and Ciphertext',
            'description': 'Prepend IV to encrypted data',
            'details': f'Total size: {len(combined)} bytes'
        })
        
        # Step 8: Base64 encode
        ciphertext_b64 = base64.b64encode(combined).decode('utf-8')
        steps.append({
            'step_number': 8,
            'title': 'Base64 Encoding',
            'description': 'Encode binary data to text format',
            'details': f'Output length: {len(ciphertext_b64)} characters'
        })
        
        # Step 9: Complete
        steps.append({
            'step_number': 9,
            'title': 'Encryption Complete',
            'description': '✓ Data encrypted successfully!',
            'details': f'Result: {ciphertext_b64[:50]}{"..." if len(ciphertext_b64) > 50 else ""}'
        })
        
        return ciphertext_b64, steps
    
    def decrypt(self, ciphertext: str, key: str) -> Tuple[str, List[dict]]:
        """
        Decrypt ciphertext using AES.
        
        Args:
            ciphertext (str): The base64-encoded ciphertext
            key (str): The password/key string
            
        Returns:
            Tuple[str, List[dict]]: (plaintext, visualization steps)
        """
        steps = []
        
        try:
            # Step 1: Initialize
            steps.append({
                'step_number': 1,
                'title': 'Initialize AES Decryption',
                'description': f'Using {self.name} decryption mode',
                'details': f'Input length: {len(ciphertext)} characters'
            })
            
            # Step 2: Generate key
            decryption_key = self._generate_key(key)
            steps.append({
                'step_number': 2,
                'title': 'Key Derivation',
                'description': 'Generate decryption key from password',
                'details': f'Using SHA-256 hash → {self.key_size * 8}-bit key'
            })
            
            # Step 3: Base64 decode
            combined = base64.b64decode(ciphertext)
            steps.append({
                'step_number': 3,
                'title': 'Base64 Decoding',
                'description': 'Decode text to binary data',
                'details': f'{len(ciphertext)} chars → {len(combined)} bytes'
            })
            
            # Step 4: Extract IV
            iv = combined[:AES.block_size]
            ciphertext_bytes = combined[AES.block_size:]
            steps.append({
                'step_number': 4,
                'title': 'Extract IV',
                'description': 'Separate IV from ciphertext',
                'details': f'IV: {len(iv)} bytes, Ciphertext: {len(ciphertext_bytes)} bytes'
            })
            
            # Step 5: Create cipher and decrypt
            cipher = AES.new(decryption_key, AES.MODE_CBC, iv)
            padded_plaintext = cipher.decrypt(ciphertext_bytes)
            steps.append({
                'step_number': 5,
                'title': 'AES Decryption',
                'description': 'Decrypt data using AES-CBC',
                'details': f'Processed {len(ciphertext_bytes)} bytes'
            })
            
            # Step 6: Remove padding
            plaintext_bytes = unpad(padded_plaintext, AES.block_size)
            padding_removed = len(padded_plaintext) - len(plaintext_bytes)
            steps.append({
                'step_number': 6,
                'title': 'Remove PKCS7 Padding',
                'description': 'Strip padding from decrypted data',
                'details': f'Removed {padding_removed} bytes of padding'
            })
            
            # Step 7: Decode to string
            plaintext = plaintext_bytes.decode('utf-8')
            steps.append({
                'step_number': 7,
                'title': 'Decode to Text',
                'description': 'Convert bytes back to string',
                'details': f'{len(plaintext_bytes)} bytes → {len(plaintext)} characters'
            })
            
            # Step 8: Complete
            steps.append({
                'step_number': 8,
                'title': 'Decryption Complete',
                'description': '✓ Data decrypted successfully!',
                'details': f'Result: "{plaintext}"'
            })
            
            return plaintext, steps
            
        except Exception as e:
            steps.append({
                'step_number': len(steps) + 1,
                'title': 'Error',
                'description': 'Decryption failed',
                'details': f'Error: {str(e)}'
            })
            return "", steps
    
    def get_cipher_name(self) -> str:
        """Return the name of the cipher."""
        return self.name
