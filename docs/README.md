# Cipher Encryption Tool 🔐

**Authors:** Salah, Fares, Ziad, Zeiad

A comprehensive Python encryption tool featuring both classical Caesar cipher and modern AES-256 encryption with an interactive GUI and visual step-by-step process display.

---

## 🆕 New Features

* ✨ **AES-256 Encryption** - Industry-standard encryption algorithm
* 🖥️ **Interactive GUI** - User-friendly graphical interface using Tkinter
* 📊 **Visual Step Display** - See each step of the encryption/decryption process in real-time
* 🏗️ **Modular Architecture** - Clean, object-oriented design with reusable components
* 📋 **Copy to Clipboard** - Easy copying of encrypted/decrypted results

---

## 📖 Encryption Algorithms

### Caesar Cipher

The Caesar cipher is one of the simplest and oldest encryption techniques. It's a substitution cipher where each letter in the plaintext is shifted by a fixed number of positions in the alphabet.

### AES-256 (Advanced Encryption Standard)

AES-256 is a modern, secure symmetric encryption algorithm used worldwide for protecting sensitive data. It uses:
* **256-bit key** - Extremely strong encryption
* **CBC Mode** - Cipher Block Chaining for enhanced security
* **PKCS7 Padding** - Standard padding scheme
* **SHA-256 Key Derivation** - Convert passwords to encryption keys
* **Random IV** - Initialization vector for each encryption

### How Caesar Cipher Works

**Encryption Process:**

1. Take each letter in the plaintext
2. Shift it forward by a fixed number of positions (the shift/key)
3. Wrap around if you reach the end of the alphabet

**Example:**

* Plaintext: `HELLO`
* Shift: `3`
* Encryption process:
  * H → K (shift 3 positions)
  * E → H
  * L → O
  * L → O
  * O → R
* Ciphertext: `KHOOR`

**Decryption Process:**

* Simply shift backward by the same number of positions
* Ciphertext `KHOOR` with shift `3` → Plaintext `HELLO`

### How AES Works

**Encryption Process:**

1. **Key Derivation** - Generate 256-bit key from password using SHA-256
2. **Encoding** - Convert text to bytes (UTF-8)
3. **Padding** - Apply PKCS7 padding to fit block size (16 bytes)
4. **IV Generation** - Create random initialization vector
5. **AES Encryption** - Encrypt using AES-CBC algorithm
6. **Combination** - Prepend IV to ciphertext
7. **Base64 Encoding** - Encode binary data to text format

**Decryption Process:**

1. **Base64 Decoding** - Decode text to binary
2. **IV Extraction** - Separate IV from ciphertext
3. **AES Decryption** - Decrypt using AES-CBC
4. **Unpadding** - Remove PKCS7 padding
5. **Decoding** - Convert bytes back to text

### Algorithm Complexity

* **Time Complexity:** O(n) - where n is the length of the text
* **Space Complexity:** O(n) - for storing the result

---

## 🚀 Features

* ✅ **Dual Cipher Support** - Caesar cipher and AES-256 encryption
* ✅ **Interactive GUI** - Easy-to-use graphical interface
* ✅ **Visual Process Steps** - See each encryption/decryption step in real-time
* ✅ **Command-Line Interface** - Original CLI still available for Caesar cipher
* ✅ Encrypt and decrypt text messages
* ✅ Preserves non-alphabetic characters (Caesar cipher)
* ✅ Handles both uppercase and lowercase letters
* ✅ Copy results to clipboard
* ✅ Modular, object-oriented design
* ✅ Clear, readable code structure

---

## 📋 Requirements

* Python 3.7 or higher
* `pycryptodome` library for AES encryption
* `tkinter` (usually included with Python)

---

## 💻 Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Or manually install:
```bash
pip install pycryptodome
```

---

## 🎯 Usage

### GUI Application (Recommended)

Launch the graphical interface:

```bash
python cipher_gui.py
```

**GUI Features:**
1. **Select Cipher** - Choose between Caesar or AES-256
2. **Enter Text** - Type or paste your message
3. **Set Key** - Enter shift value (Caesar) or password (AES)
4. **Choose Mode** - Select Encrypt or Decrypt
5. **Process** - Click "Process" to see visual steps and result
6. **Copy Output** - Copy result to clipboard

### Command-Line Interface (Caesar Cipher Only)

### Basic Syntax

```bash
python caesar_cipher.py -m "YOUR_MESSAGE" -s SHIFT_VALUE [-e | -d]
```

### Command-Line Arguments

| Argument | Short  | Long          | Required | Description                            |
| -------- | ------ | ------------- | -------- | -------------------------------------- |
| Message  | `-m` | `--message` | Yes      | The text to encrypt or decrypt         |
| Shift    | `-s` | `--shift`   | Yes      | Number of positions to shift (integer) |
| Encrypt  | `-e` | `--encrypt` | Yes*     | Encrypt the message                    |
| Decrypt  | `-d` | `--decrypt` | Yes*     | Decrypt the message                    |

*You must choose either `-e` (encrypt) or `-d` (decrypt), but not both.

---

## 🏗️ Project Structure

```
Caesar/
├── cipher_base.py           # Abstract base class for all ciphers
├── caesar_cipher_class.py   # Caesar cipher implementation (OOP)
├── aes_cipher_class.py      # AES-256 cipher implementation
├── cipher_gui.py            # GUI application (main entry point)
├── caesar_cipher.py         # Original CLI tool
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Architecture Overview

**Modular Design:**
* `CipherBase` - Abstract interface defining cipher contract
* `CaesarCipher` - Implements Caesar cipher with step visualization
* `AESCipher` - Implements AES-256 with step visualization
* `CipherGUI` - Main GUI application coordinating all components

**Key Design Principles:**
* **Inheritance** - All ciphers extend `CipherBase`
* **Encapsulation** - Each class manages its own logic
* **Polymorphism** - GUI works with any cipher through base interface
* **Single Responsibility** - Each module has one clear purpose

---

## 📝 Examples

### GUI Usage Examples

1. **Caesar Encryption:**
   - Input: "Hello World"
   - Cipher: Caesar
   - Key: 3
   - Mode: Encrypt
   - Output: "Khoor Zruog"
   - Steps: See each character transformation

2. **AES Encryption:**
   - Input: "Secret Message"
   - Cipher: AES-256
   - Key: "MyPassword123"
   - Mode: Encrypt
   - Output: Base64 encoded string
   - Steps: See key derivation, padding, encryption, etc.

### Command-Line Examples (Original Caesar Tool)

### Example 1: Encrypt a Message

```bash
python caesar_cipher.py -m "Hello World" -s 3 -e
```

**Output:**

```
==================================================
Original Text:  Hello World
Shift Value:    3
Cipher Text:    Khoor Zruog
==================================================
```

### Example 2: Decrypt a Message

```bash
python caesar_cipher.py -m "Khoor Zruog" -s 3 -d
```

**Output:**

```
==================================================
Cipher Text:    Khoor Zruog
Shift Value:    3
Plain Text:     Hello World
==================================================
```

### Example 3: Using Long Options

```bash
python caesar_cipher.py --message "Attack at dawn!" --shift 5 --encrypt
```

**Output:**

```
==================================================
Original Text:  Attack at dawn!
Shift Value:    5
Cipher Text:    Fyyfrp fy ifbs!
==================================================
```

### Example 4: Large Shift Value

```bash
python caesar_cipher.py -m "Python" -s 13 -e
```

**Output:**

```
==================================================
Original Text:  Python
Shift Value:    13
Cipher Text:    Clguba
==================================================
```

### Example 5: With Mixed Content

```bash
python caesar_cipher.py -m "Meet me at 9 PM!" -s 7 -e
```

**Output:**

```
==================================================
Original Text:  Meet me at 9 PM!
Shift Value:    7
Cipher Text:    Tlla tl ha 9 WT!
==================================================
```

---

## 🔍 Understanding the Code

### Cipher Base Class

```python
class CipherBase(ABC):
    @abstractmethod
    def encrypt(self, plaintext: str, key) -> Tuple[str, List[dict]]:
        """Returns (ciphertext, visualization_steps)"""
        pass
    
    @abstractmethod
    def decrypt(self, ciphertext: str, key) -> Tuple[str, List[dict]]:
        """Returns (plaintext, visualization_steps)"""
        pass
```

### Caesar Cipher Implementation

#### `caesar_cipher_encrypt(text, shift)`

Encrypts the plaintext by shifting each letter forward by the shift value.

**Logic:**

```python
shifted = (ord(char) - ascii_offset + shift) % 26
```

* Uses ASCII values to perform the shift
* Modulo 26 ensures wrapping (A-Z or a-z)
* Preserves case (uppercase/lowercase)
* Returns both result and visualization steps

#### `caesar_cipher_decrypt(text, shift)`

Decrypts the ciphertext by calling encrypt with a negative shift value.

### AES Cipher Implementation

**Key Features:**
* Uses `pycryptodome` library for AES operations
* SHA-256 for password-to-key derivation
* CBC mode with random IV for each encryption
* PKCS7 padding for block alignment
* Base64 encoding for text-safe output

**Security Considerations:**
* Each encryption uses a unique IV
* Password is hashed to create consistent key
* Industry-standard AES-256 encryption
* Proper padding and encoding

---

## 🛡️ Security Notes

### Caesar Cipher

⚠️ **Warning:** The Caesar cipher is **NOT secure** for real-world applications!

* Only 25 possible keys (shifts)
* Extremely vulnerable to brute force attacks
* Can be broken using frequency analysis
* Use only for educational purposes or simple obfuscation

### AES-256

✅ **Secure for real-world use** when properly implemented!

* Industry-standard encryption
* Used by governments and businesses worldwide
* Strong password required for security
* Resistant to brute force attacks

**Best Practices:**
* Use strong, unique passwords (12+ characters)
* Store passwords securely (never in code)
* Don't reuse passwords across applications
* Keep encryption keys secret

---

## 🧪 Testing

### Test Caesar Cipher

```bash
# Using GUI
1. Launch: python cipher_gui.py
2. Select Caesar cipher
3. Enter "Testing" with shift 10
4. Click Encrypt → Should get "Docdyd"
5. Decrypt "Docdyd" with shift 10 → Should get "Testing"

# Using CLI
python caesar_cipher.py -m "Testing" -s 10 -e
python caesar_cipher.py -m "Docdyd" -s 10 -d
```

### Test AES-256

```bash
# Using GUI
1. Launch: python cipher_gui.py
2. Select AES-256
3. Enter "Secret" with password "test123"
4. Click Encrypt → Get base64 string
5. Copy output and decrypt with same password → Should get "Secret"
```

---

## ❓ FAQ

**Q: What's the difference between Caesar and AES?**

A: Caesar is a classical, educational cipher (not secure). AES is modern, military-grade encryption used for real security needs.

**Q: Can I use AES for sensitive data?**

A: Yes! AES-256 is considered secure when used with strong passwords. However, this is an educational implementation - for production use, consider established libraries and security audits.

**Q: Why does AES output look random?**

A: AES output is base64-encoded binary data. This makes it safe to copy/paste but appears as random characters.

**Q: What happens if I use a negative shift in Caesar?**

A: Negative shifts work! A shift of -3 is the same as a shift of 23.

**Q: What if my Caesar shift is greater than 26?**

A: The modulo operation handles this automatically. Shift 27 = Shift 1.

**Q: Can I see the encryption process?**

A: Yes! The GUI shows detailed step-by-step visualization of the entire encryption/decryption process.

**Q: How do I decrypt an AES message?**

A: Use the exact same password you used for encryption. Copy the encrypted output, paste it as input, select Decrypt mode, and process.

---

## 🎓 Learning Resources

* [Caesar Cipher on Wikipedia](https://en.wikipedia.org/wiki/Caesar_cipher)
* [AES Encryption Explained](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
* [Cryptography Basics](https://en.wikipedia.org/wiki/Cryptography)
* [Python Cryptography Tutorial](https://cryptography.io/en/latest/)

---

## 👥 Team

* Salah
* Fares
* Ziad
* Zeiad

---

## 📄 License

This is an educational project. Feel free to use and modify as needed.

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas for enhancements:

* Add more cipher algorithms (RSA, DES, etc.)
* Implement file encryption/decryption
* Add brute force decryption tool
* Frequency analysis visualization
* Support for other languages
* Dark mode for GUI
* Export encryption logs
* Password strength indicator

---

## 📜 Changelog

**Version 2.0** (Current)
* ✨ Added AES-256 encryption
* ✨ New GUI with Tkinter
* ✨ Visual step-by-step display
* ✨ Modular class architecture
* ✨ Copy to clipboard feature

**Version 1.0**
* Initial Caesar cipher CLI implementation

---

**Happy Encrypting! 🔐**
