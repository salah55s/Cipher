"""
Base Cipher Interface
Authors: @salah55s, @Fares-Elsaghir, @ZiadMahmoud855, @zeiad1655, @omar97531
Description: Abstract base class for all cipher implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple


class CipherBase(ABC):
    """Abstract base class for all cipher implementations."""
    
    @abstractmethod
    def encrypt(self, plaintext: str, key) -> Tuple[str, List[dict]]:
        """
        Encrypt plaintext using the cipher algorithm.
        
        Args:
            plaintext (str): The text to encrypt
            key: The encryption key (type varies by cipher)
            
        Returns:
            Tuple[str, List[dict]]: (ciphertext, list of step information)
        """
        pass
    
    @abstractmethod
    def decrypt(self, ciphertext: str, key) -> Tuple[str, List[dict]]:
        """
        Decrypt ciphertext using the cipher algorithm.
        
        Args:
            ciphertext (str): The text to decrypt
            key: The decryption key (type varies by cipher)
            
        Returns:
            Tuple[str, List[dict]]: (plaintext, list of step information)
        """
        pass
    
    @abstractmethod
    def get_cipher_name(self) -> str:
        """Return the name of the cipher algorithm."""
        pass
