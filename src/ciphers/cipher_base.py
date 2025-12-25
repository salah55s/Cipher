"""
Base Cipher Interface
Authors: @salah55s, @Fares-Elsaghir, @ZiadMahmoud855, @zeiad1655, @omar97531, @KhaledGamal1
Description: Abstract base class for all cipher implementations.

================================================================================
DESIGN PATTERN: STRATEGY PATTERN
================================================================================
This module defines an abstract base class that all cipher implementations
must inherit from. This allows the GUI and Streamlit app to work with any
cipher implementation interchangeably.

BENEFITS:
  - Consistent interface for all ciphers
  - Easy to add new cipher algorithms
  - GUI/web app doesn't need to know implementation details
  - Step tracking is built into the interface for visualization

INTERFACE CONTRACT:
  - encrypt(plaintext, key) → (ciphertext, steps)
  - decrypt(ciphertext, key) → (plaintext, steps)
  - get_cipher_name() → name string
  - steps list contains dicts with visualization data
================================================================================
"""

from abc import ABC, abstractmethod
from typing import List, Tuple


class CipherBase(ABC):
    """
    Abstract base class for all cipher implementations.
    
    All cipher classes (CaesarCipher, AESCipher, AESLowLevel) inherit from this
    class and must implement the encrypt, decrypt, and get_cipher_name methods.
    
    The encrypt and decrypt methods return a tuple of:
      1. The result string (ciphertext or plaintext)
      2. A list of step dictionaries for visualization
    
    Each step dictionary should contain at minimum:
      - 'step_number': int - Sequential step number
      - 'title': str - Short title for the step
      - 'description': str - What happened in this step
      - 'details': str - Technical details (optional)
    """
    
    @abstractmethod
    def encrypt(self, plaintext: str, key) -> Tuple[str, List[dict]]:
        """
        Encrypt plaintext using the cipher algorithm.
        
        Args:
            plaintext (str): The text to encrypt
            key: The encryption key (type varies by cipher)
                 - CaesarCipher: int (shift value 0-25)
                 - AESCipher/AESLowLevel: str (password)
            
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
            key: The decryption key (must match encryption key)
            
        Returns:
            Tuple[str, List[dict]]: (plaintext, list of step information)
        """
        pass
    
    @abstractmethod
    def get_cipher_name(self) -> str:
        """
        Return the name of the cipher algorithm.
        
        Returns:
            str: Human-readable cipher name (e.g., "Caesar Cipher", "AES-256")
        """
        pass

