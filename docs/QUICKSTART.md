# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the GUI
```bash
python cipher_gui.py
```
or
```bash
python run_gui.py
```

### 3. Start Encrypting!
- Select your cipher algorithm (Caesar or AES-256)
- Enter your text
- Set your key/password
- Choose encrypt or decrypt
- Click "Process" to see the magic happen!

---

## 📚 Feature Overview

### Caesar Cipher
- **Best for:** Learning cryptography basics
- **Key Type:** Numeric shift (0-25)
- **Security:** Educational only (not secure)
- **Output:** Same alphabet characters

**Example:**
- Input: `Hello World`
- Key: `3`
- Output: `Khoor Zruog`

### AES-256 Encryption
- **Best for:** Real encryption needs
- **Key Type:** Password/passphrase
- **Security:** Military-grade (when used properly)
- **Output:** Base64 encoded string

**Example:**
- Input: `Secret Message`
- Key: `MySecurePassword123`
- Output: `d7Lge8JmfC+YVnQaNl/wgycP...`

---

## 🎯 Usage Tips

### For Caesar Cipher:
1. Use shift values between 0-25 (larger values work too)
2. Remember: decryption uses the same shift value
3. Only letters are encrypted; numbers and symbols stay the same
4. Watch the visual steps to learn how it works!

### For AES-256:
1. Use strong passwords (12+ characters recommended)
2. Mix uppercase, lowercase, numbers, and symbols
3. Save your password securely - you'll need it to decrypt!
4. The same input with the same password always gives different output (random IV)
5. To decrypt: paste the encrypted output as input and use the same password

---

## 🔍 Visual Steps Feature

The GUI shows you **every step** of the encryption/decryption process:

### Caesar Cipher Steps:
- Initialization
- Character-by-character transformation
- Position calculations
- Final result

### AES-256 Steps:
- Key derivation (SHA-256)
- Text encoding (UTF-8)
- Padding application (PKCS7)
- IV generation
- AES encryption (CBC mode)
- Base64 encoding
- Final result

This educational feature helps you understand exactly what's happening under the hood!

---

## 🛠️ Troubleshooting

**Problem:** GUI doesn't launch
- **Solution:** Make sure tkinter is installed (usually comes with Python)
- On Linux: `sudo apt-get install python3-tk`

**Problem:** "Module not found: Crypto"
- **Solution:** Install pycryptodome: `pip install pycryptodome`

**Problem:** AES decryption fails
- **Solution:** Make sure you're using the EXACT same password used for encryption

**Problem:** Caesar cipher output looks wrong
- **Solution:** Check that shift value is a valid number

---

## 🎓 Code Structure

```
cipher_base.py           → Abstract interface (inheritance)
    ↓
caesar_cipher_class.py   → Caesar implementation
aes_cipher_class.py      → AES implementation
    ↓
cipher_gui.py           → GUI that uses both ciphers
```

**Benefits of this architecture:**
- ✅ Easy to add new ciphers
- ✅ Each cipher is independent
- ✅ GUI works with any cipher
- ✅ Clean, readable code
- ✅ Testable components

---

## 📝 Quick Reference

### Command-Line (Caesar only):
```bash
# Encrypt
python caesar_cipher.py -m "Hello" -s 3 -e

# Decrypt
python caesar_cipher.py -m "Khoor" -s 3 -d
```

### Python API:
```python
from caesar_cipher_class import CaesarCipher
from aes_cipher_class import AESCipher

# Caesar
caesar = CaesarCipher()
encrypted, steps = caesar.encrypt("Hello", 3)
decrypted, steps = caesar.decrypt(encrypted, 3)

# AES
aes = AESCipher(key_size=256)
encrypted, steps = aes.encrypt("Secret", "password")
decrypted, steps = aes.decrypt(encrypted, "password")
```

---

## 🎮 Try These Examples

1. **Basic Caesar:**
   - Text: `ATTACK AT DAWN`
   - Shift: `13`
   - Result: `NGGNPX NG QNJA`

2. **Caesar with Numbers:**
   - Text: `Meet at 9 PM`
   - Shift: `5`
   - Result: `Rjjy fy 9 UT`

3. **AES Short Message:**
   - Text: `Hi`
   - Password: `test123`
   - Result: (try it yourself!)

4. **AES Long Message:**
   - Text: `This is a much longer message to demonstrate AES encryption with multiple blocks.`
   - Password: `SuperSecret456!`
   - Result: (try it yourself!)

---

## 💡 Educational Value

This tool demonstrates:
- **Classical cryptography** (Caesar cipher)
- **Modern cryptography** (AES-256)
- **Object-oriented programming** (classes, inheritance)
- **GUI development** (Tkinter)
- **Algorithm visualization** (step-by-step display)
- **Software architecture** (modular design)

Perfect for:
- 🎓 Computer science students
- 👨‍💻 Learning cryptography
- 🔒 Understanding encryption
- 🏗️ Studying software design patterns

---

**Need Help?** Check the main README.md for detailed documentation!
