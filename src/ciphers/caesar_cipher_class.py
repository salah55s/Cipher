"""
Caesar Cipher Class Implementation
Authors: Salah, Fares, Ziad, Zeiad
Description: Object-oriented implementation of Caesar cipher with step visualization.
"""

from typing import List, Tuple
from .cipher_base import CipherBase


class CaesarCipher(CipherBase):
    """Caesar cipher implementation with visual step tracking."""
    
    def __init__(self):
        """Initialize the Caesar cipher."""
        self.name = "Caesar Cipher"
    
    def encrypt(self, plaintext: str, key: int) -> Tuple[str, List[dict]]:
        """
        Encrypt plaintext using Caesar cipher.
        
        Args:
            plaintext (str): The text to encrypt
            key (int): The shift value
            
        Returns:
            Tuple[str, List[dict]]: (ciphertext, visualization steps)
        """
        steps = []
        result = ""
        shift = key % 26  # Normalize shift to 0-25
        
        # Initial step
        steps.append({
            'step_number': 0,
            'title': 'Initialize',
            'description': f'Starting Caesar cipher encryption with shift value: {shift}',
            'details': f'Input: "{plaintext}"'
        })
        
        # Process each character
        for i, char in enumerate(plaintext):
            if char.isalpha():
                # Determine if uppercase or lowercase
                ascii_offset = ord('A') if char.isupper() else ord('a')
                original_pos = ord(char) - ascii_offset
                
                # Shift the character
                shifted_pos = (original_pos + shift) % 26
                encrypted_char = chr(shifted_pos + ascii_offset)
                result += encrypted_char
                
                # Record step
                steps.append({
                    'step_number': i + 1,
                    'title': f'Encrypt character {i + 1}',
                    'description': f'"{char}" → "{encrypted_char}"',
                    'details': f'Position: {original_pos} + {shift} = {shifted_pos} (mod 26)'
                })
            else:
                # Keep non-alphabetic characters unchanged
                result += char
                steps.append({
                    'step_number': i + 1,
                    'title': f'Keep character {i + 1}',
                    'description': f'"{char}" → "{char}"',
                    'details': 'Non-alphabetic character (unchanged)'
                })
        
        # Final step
        steps.append({
            'step_number': len(plaintext) + 1,
            'title': 'Complete',
            'description': 'Encryption complete!',
            'details': f'Ciphertext: "{result}"'
        })
        
        return result, steps
    
    def decrypt(self, ciphertext: str, key: int) -> Tuple[str, List[dict]]:
        """
        Decrypt ciphertext using Caesar cipher.
        
        Args:
            ciphertext (str): The text to decrypt
            key (int): The shift value
            
        Returns:
            Tuple[str, List[dict]]: (plaintext, visualization steps)
        """
        steps = []
        result = ""
        shift = key % 26  # Normalize shift to 0-25
        
        # Initial step
        steps.append({
            'step_number': 0,
            'title': 'Initialize',
            'description': f'Starting Caesar cipher decryption with shift value: {shift}',
            'details': f'Input: "{ciphertext}"'
        })
        
        # Process each character
        for i, char in enumerate(ciphertext):
            if char.isalpha():
                # Determine if uppercase or lowercase
                ascii_offset = ord('A') if char.isupper() else ord('a')
                original_pos = ord(char) - ascii_offset
                
                # Shift backward
                shifted_pos = (original_pos - shift) % 26
                decrypted_char = chr(shifted_pos + ascii_offset)
                result += decrypted_char
                
                # Record step
                steps.append({
                    'step_number': i + 1,
                    'title': f'Decrypt character {i + 1}',
                    'description': f'"{char}" → "{decrypted_char}"',
                    'details': f'Position: {original_pos} - {shift} = {shifted_pos} (mod 26)'
                })
            else:
                # Keep non-alphabetic characters unchanged
                result += char
                steps.append({
                    'step_number': i + 1,
                    'title': f'Keep character {i + 1}',
                    'description': f'"{char}" → "{char}"',
                    'details': 'Non-alphabetic character (unchanged)'
                })
        
        # Final step
        steps.append({
            'step_number': len(ciphertext) + 1,
            'title': 'Complete',
            'description': 'Decryption complete!',
            'details': f'Plaintext: "{result}"'
        })
        
        return result, steps
    
    def get_cipher_name(self) -> str:
        """Return the name of the cipher."""
        return self.name
