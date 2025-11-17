#!/usr/bin/env python3
"""Quick test to verify the new project structure"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Test imports
print("Testing imports...")
try:
    from ciphers.caesar_cipher_class import CaesarCipher
    print("✓ Caesar cipher imported")
except ImportError as e:
    print(f"✗ Caesar cipher import failed: {e}")
    sys.exit(1)

try:
    from aes_modules.aes_low_level import AESLowLevel
    print("✓ AES low-level imported")
except ImportError as e:
    print(f"✗ AES import failed: {e}")
    sys.exit(1)

# Quick functionality test
print("\nTesting Caesar cipher...")
caesar = CaesarCipher()
encrypted, steps = caesar.encrypt("Hello", 3)
print(f"  Input: 'Hello'")
print(f"  Output: '{encrypted}'")
print(f"  Steps: {len(steps)}")

print("\nTesting AES-128...")
aes = AESLowLevel(key_size=128)
encrypted, steps = aes.encrypt("Test", "password")
print(f"  Input: 'Test'")
print(f"  Output: {encrypted[:30]}...")
print(f"  Steps: {len(steps)}")

print("\n✅ All tests passed! Project structure is working correctly.")
print("\n📝 New structure:")
print("   src/ciphers/     - Cipher implementations")
print("   src/aes_modules/ - Low-level AES components")
print("   src/gui/         - GUI applications")
print("   tests/           - Tests and demos")
print("   docs/            - Documentation")
