# Caesar Cipher Implementation

**Authors:** Salah, Fares, Ziad, Zeiad

A Python implementation of the classical Caesar cipher encryption and decryption algorithm.

---

## 📖 What is Caesar Cipher?

The Caesar cipher is one of the simplest and oldest encryption techniques. It's a substitution cipher where each letter in the plaintext is shifted by a fixed number of positions in the alphabet.

### How It Works

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

### Algorithm Complexity

* **Time Complexity:** O(n) - where n is the length of the text
* **Space Complexity:** O(n) - for storing the result

---

## 🚀 Features

* ✅ Encrypt text messages using Caesar cipher
* ✅ Decrypt cipher text back to plaintext
* ✅ Preserves non-alphabetic characters (spaces, punctuation, numbers)
* ✅ Handles both uppercase and lowercase letters
* ✅ Command-line interface with argument parsing
* ✅ Clear output formatting

---

## 📋 Requirements

* Python 3.6 or higher
* No external dependencies required (uses only standard library)

---

## 💻 Installation

1. Download the `caesar_cipher.py` file
2. No installation needed - it's a standalone script!

---

## 🎯 Usage

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

## 📝 Examples

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

### Core Functions

#### `caesar_cipher_encrypt(text, shift)`

Encrypts the plaintext by shifting each letter forward by the shift value.

**Logic:**

```python
shifted = (ord(char) - ascii_offset + shift) % 26
```

* Uses ASCII values to perform the shift
* Modulo 26 ensures wrapping (A-Z or a-z)
* Preserves case (uppercase/lowercase)

#### `caesar_cipher_decrypt(text, shift)`

Decrypts the ciphertext by calling encrypt with a negative shift value.

**Logic:**

```python
return caesar_cipher_encrypt(text, -shift)
```

* Decryption is the inverse operation of encryption
* Simply shifts backward instead of forward

---

## 🛡️ Security Note

⚠️ **Warning:** The Caesar cipher is **NOT secure** for real-world applications!

* Only 25 possible keys (shifts)
* Extremely vulnerable to brute force attacks
* Can be broken using frequency analysis
* Use only for educational purposes or simple obfuscation

For actual security needs, use modern encryption algorithms like AES.

---

## 🧪 Testing

### Test the Encryption and Decryption

```bash
# Encrypt
python caesar_cipher.py -m "Testing" -s 10 -e
# Output: Docdyd

# Decrypt the result
python caesar_cipher.py -m "Docdyd" -s 10 -d
# Output: Testing
```

Both should return the original message!

---

## ❓ FAQ

**Q: What happens if I use a negative shift value?**

A: Negative shifts work! A shift of -3 is the same as a shift of 23.

**Q: What if my shift is greater than 26?**

A: The modulo operation handles this automatically. Shift 27 = Shift 1.

**Q: Are numbers and special characters encrypted?**

A: No, only letters (A-Z, a-z) are shifted. Everything else remains unchanged.

**Q: Can I use this for Arabic text?**

A: This implementation is designed for English (Latin alphabet). For Arabic, you'd need a modified version.

---

## 📚 Additional Resources

* [Caesar Cipher on Wikipedia](https://en.wikipedia.org/wiki/Caesar_cipher)
* [Cryptography Basics](https://en.wikipedia.org/wiki/Cryptography)

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

Feel free to enhance this implementation with:

* Support for other languages
* GUI interface
* Brute force decryption (try all shifts)
* Frequency analysis tools

---

**Happy Encrypting! 🔐**
