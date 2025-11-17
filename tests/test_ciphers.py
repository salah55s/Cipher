"""
Test script for cipher implementations
"""

from caesar_cipher_class import CaesarCipher
from aes_cipher_class import AESCipher

def test_caesar():
    """Test Caesar cipher."""
    print("=" * 50)
    print("Testing Caesar Cipher")
    print("=" * 50)
    
    cipher = CaesarCipher()
    plaintext = "Hello World"
    key = 3
    
    # Encrypt
    ciphertext, encrypt_steps = cipher.encrypt(plaintext, key)
    print(f"\nOriginal: {plaintext}")
    print(f"Encrypted: {ciphertext}")
    print(f"Steps: {len(encrypt_steps)} steps")
    
    # Decrypt
    decrypted, decrypt_steps = cipher.decrypt(ciphertext, key)
    print(f"Decrypted: {decrypted}")
    print(f"Match: {plaintext == decrypted}")
    

def test_aes():
    """Test AES cipher."""
    print("\n" + "=" * 50)
    print("Testing AES-256 Cipher")
    print("=" * 50)
    
    cipher = AESCipher(key_size=256)
    plaintext = "Secret Message"
    password = "MyPassword123"
    
    # Encrypt
    ciphertext, encrypt_steps = cipher.encrypt(plaintext, password)
    print(f"\nOriginal: {plaintext}")
    print(f"Encrypted: {ciphertext[:50]}...")
    print(f"Steps: {len(encrypt_steps)} steps")
    
    # Decrypt
    decrypted, decrypt_steps = cipher.decrypt(ciphertext, password)
    print(f"Decrypted: {decrypted}")
    print(f"Match: {plaintext == decrypted}")


if __name__ == "__main__":
    test_caesar()
    test_aes()
    print("\n" + "=" * 50)
    print("✓ All tests completed!")
    print("=" * 50)
