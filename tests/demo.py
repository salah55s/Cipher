"""
Demo Script - Cipher Tool Examples
Authors: @salah55s, @Fares-Elsaghir, @ZiadMahmoud855, @zeiad1655, @omar97531
Description: Demonstrates the capabilities of both Caesar and AES ciphers.
"""

from caesar_cipher_class import CaesarCipher
from aes_cipher_class import AESCipher
import time


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_steps(steps, show_all=False):
    """Print visualization steps."""
    if show_all:
        for step in steps:
            print(f"\n  Step {step['step_number']}: {step['title']}")
            print(f"    → {step['description']}")
            print(f"    ℹ {step['details']}")
    else:
        print(f"\n  ℹ Total steps: {len(steps)}")
        print(f"    First: {steps[0]['title']}")
        print(f"    Last: {steps[-1]['title']}")


def demo_caesar():
    """Demonstrate Caesar cipher."""
    print_header("CAESAR CIPHER DEMONSTRATION")
    
    cipher = CaesarCipher()
    
    # Example 1: Simple encryption
    print("\n📝 Example 1: Simple Encryption")
    plaintext = "Hello World"
    shift = 3
    
    print(f"  Input: {plaintext}")
    print(f"  Shift: {shift}")
    
    ciphertext, steps = cipher.encrypt(plaintext, shift)
    print(f"  Output: {ciphertext}")
    print_steps(steps)
    
    # Example 2: Decryption
    print("\n📝 Example 2: Decryption")
    print(f"  Input: {ciphertext}")
    print(f"  Shift: {shift}")
    
    decrypted, steps = cipher.decrypt(ciphertext, shift)
    print(f"  Output: {decrypted}")
    print(f"  ✓ Match: {plaintext == decrypted}")
    
    # Example 3: Large shift
    print("\n📝 Example 3: Large Shift Value")
    shift = 13  # ROT13
    plaintext = "Secret Message"
    
    print(f"  Input: {plaintext}")
    print(f"  Shift: {shift} (ROT13)")
    
    ciphertext, _ = cipher.encrypt(plaintext, shift)
    print(f"  Output: {ciphertext}")
    
    # ROT13 is its own inverse
    double_encrypted, _ = cipher.encrypt(ciphertext, shift)
    print(f"  Encrypt again: {double_encrypted}")
    print(f"  ✓ ROT13 property: Encrypting twice gives original!")


def demo_aes():
    """Demonstrate AES cipher."""
    print_header("AES-256 CIPHER DEMONSTRATION")
    
    cipher = AESCipher(key_size=256)
    
    # Example 1: Basic encryption
    print("\n📝 Example 1: Basic Encryption")
    plaintext = "This is a secret message"
    password = "MyPassword123"
    
    print(f"  Input: {plaintext}")
    print(f"  Password: {password}")
    
    ciphertext, steps = cipher.encrypt(plaintext, password)
    print(f"  Output: {ciphertext}")
    print_steps(steps)
    
    # Example 2: Decryption
    print("\n📝 Example 2: Decryption")
    print(f"  Input: {ciphertext[:50]}...")
    print(f"  Password: {password}")
    
    decrypted, steps = cipher.decrypt(ciphertext, password)
    print(f"  Output: {decrypted}")
    print(f"  ✓ Match: {plaintext == decrypted}")
    
    # Example 3: Different outputs for same input
    print("\n📝 Example 3: Randomized Encryption (IV)")
    plaintext = "Same text"
    
    encrypted1, _ = cipher.encrypt(plaintext, password)
    encrypted2, _ = cipher.encrypt(plaintext, password)
    
    print(f"  Input: {plaintext}")
    print(f"  First encryption: {encrypted1[:40]}...")
    print(f"  Second encryption: {encrypted2[:40]}...")
    print(f"  ℹ Outputs are different (unique IV for each encryption)")
    print(f"  ℹ But both decrypt to the same plaintext!")
    
    decrypted1, _ = cipher.decrypt(encrypted1, password)
    decrypted2, _ = cipher.decrypt(encrypted2, password)
    print(f"  Decrypt 1: {decrypted1}")
    print(f"  Decrypt 2: {decrypted2}")
    print(f"  ✓ Both match original: {plaintext == decrypted1 == decrypted2}")


def demo_comparison():
    """Compare Caesar and AES."""
    print_header("CAESAR vs AES-256 COMPARISON")
    
    plaintext = "Attack at dawn!"
    
    # Caesar
    print("\n🔵 Caesar Cipher (Shift 5):")
    caesar = CaesarCipher()
    caesar_encrypted, _ = caesar.encrypt(plaintext, 5)
    print(f"  Original: {plaintext}")
    print(f"  Encrypted: {caesar_encrypted}")
    print(f"  Length change: {len(plaintext)} → {len(caesar_encrypted)}")
    print(f"  Security: ⚠️  Educational only (25 possible keys)")
    
    # AES
    print("\n🟢 AES-256:")
    aes = AESCipher(key_size=256)
    aes_encrypted, _ = aes.encrypt(plaintext, "password123")
    print(f"  Original: {plaintext}")
    print(f"  Encrypted: {aes_encrypted}")
    print(f"  Length change: {len(plaintext)} → {len(aes_encrypted)}")
    print(f"  Security: ✓ Military-grade (2^256 possible keys)")


def demo_visual_steps():
    """Demonstrate detailed step visualization."""
    print_header("DETAILED STEP VISUALIZATION")
    
    print("\n🔍 Caesar Cipher - Character by Character:")
    caesar = CaesarCipher()
    plaintext = "ABC"
    shift = 3
    
    print(f"  Encrypting '{plaintext}' with shift {shift}...")
    _, steps = caesar.encrypt(plaintext, shift)
    print_steps(steps, show_all=True)
    
    print("\n🔍 AES-256 - Complete Process:")
    aes = AESCipher(key_size=256)
    plaintext = "Hi"
    password = "test"
    
    print(f"  Encrypting '{plaintext}' with password '{password}'...")
    _, steps = aes.encrypt(plaintext, password)
    print_steps(steps, show_all=True)


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 60)
    print("  🔐 CIPHER TOOL DEMONSTRATION")
    print("  Authors: @salah55s, @Fares-Elsaghir, @ZiadMahmoud855, @zeiad1655, @omar97531")
    print("=" * 60)
    
    time.sleep(1)
    
    # Run demos
    demo_caesar()
    time.sleep(1)
    
    demo_aes()
    time.sleep(1)
    
    demo_comparison()
    time.sleep(1)
    
    demo_visual_steps()
    
    # Final message
    print_header("DEMONSTRATION COMPLETE")
    print("\n✓ All examples executed successfully!")
    print("\n💡 Next steps:")
    print("  • Run 'python cipher_gui.py' to launch the GUI")
    print("  • Try encrypting your own messages")
    print("  • Experiment with different keys and passwords")
    print("  • Watch the visual steps in the GUI")
    print("\n📚 For more info: Read README.md and QUICKSTART.md")
    print()


if __name__ == "__main__":
    main()
