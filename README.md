# 🔐 Caesar Cipher Encryption Tool

A comprehensive cryptography education tool implementing **Caesar Cipher** and **AES (128/256-bit)** encryption with interactive visualizations.

## 📥 Quick Start

```bash
# Install dependencies  
pip install -r requirements.txt

# Run the web UI (recommended)
streamlit run streamlit_app.py

# Or run the desktop GUI
python run_gui.py
```

---

## 🏗️ Architecture Overview

```mermaid
graph TB
    subgraph "User Interfaces"
        A[streamlit_app.py<br/>Web UI with Plotly] 
        B[cipher_gui.py<br/>Tkinter Desktop]
        C[caesar_cipher.py<br/>CLI Tool]
    end
    
    subgraph "Cipher Classes"
        D[CipherBase<br/>Abstract Interface]
        E[CaesarCipher]
        F[AESCipher<br/>uses pycryptodome]
        G[AESLowLevel<br/>built from scratch]
    end
    
    subgraph "AES Modules"
        H[aes_sbox.py<br/>S-Box lookups]
        I[aes_galois.py<br/>GF(2^8) math]
        J[aes_operations.py<br/>ShiftRows, MixColumns]
        K[aes_key_expansion.py<br/>Key Schedule]
    end
    
    A --> E & G
    B --> E & F
    C --> E
    D -.-> E & F & G
    G --> H & I & J & K
```

---

## 📊 Data Flow

### Caesar Cipher Encryption

```
Input: "Hello World", shift=3
   ↓
1. For each character:
   ↓
2. If alphabetic:
   - Get position (H=7)
   - Add shift: (7 + 3) mod 26 = 10
   - Convert back: K
   ↓
3. Result: "Khoor Zruog"
```

### AES Encryption Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AES ENCRYPTION FLOW                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ PASSWORD ──► SHA-256 ──► derive_key_from_password() ──► 16/32-byte KEY     │
│                                                                             │
│ KEY ──► key_expansion() ──► [Round Key 0] [Round Key 1] ... [Round Key N]  │
│                                                                             │
│ PLAINTEXT ──► UTF-8 encode ──► pkcs7_pad() ──► 16-byte BLOCKS              │
│                                                                             │
│ For each BLOCK:                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ bytes_to_state() ──► 4x4 STATE MATRIX                               │   │
│   │                                                                     │   │
│   │ Round 0: AddRoundKey (XOR with Round Key 0)                         │   │
│   │                                                                     │   │
│   │ Rounds 1 to N-1:                                                    │   │
│   │   SubBytes    ──► S-Box substitution (non-linear)                   │   │
│   │   ShiftRows   ──► Rotate rows left (diffusion)                      │   │
│   │   MixColumns  ──► Matrix multiply in GF(2^8) (diffusion)            │   │
│   │   AddRoundKey ──► XOR with round key                                │   │
│   │                                                                     │   │
│   │ Final Round (no MixColumns):                                        │   │
│   │   SubBytes → ShiftRows → AddRoundKey                                │   │
│   │                                                                     │   │
│   │ state_to_bytes() ──► 16-byte CIPHERTEXT BLOCK                       │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│ CIPHERTEXT BLOCKS ──► base64.encode() ──► OUTPUT STRING                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Module Reference

### AES Modules (`src/aes_modules/`)

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `aes_sbox.py` | Non-linear substitution | `sub_bytes(state)`, `inv_sub_bytes(state)` |
| `aes_galois.py` | GF(2^8) arithmetic | `gf_multiply(a,b)`, `xtime(byte)` |
| `aes_operations.py` | State transformations | `shift_rows()`, `mix_columns()`, `add_round_key()` |
| `aes_key_expansion.py` | Key schedule | `key_expansion(key, key_size)`, `get_round_key()` |
| `aes_low_level.py` | Main cipher | `encrypt(plaintext, key)`, `decrypt(ciphertext, key)` |

### Cipher Classes (`src/ciphers/`)

| Class | Description | Key Type |
|-------|-------------|----------|
| `CipherBase` | Abstract interface | - |
| `CaesarCipher` | Classical substitution | `int` (0-25) |
| `AESCipher` | High-level AES (pycryptodome) | `str` (password) |
| `AESLowLevel` | Educational AES (from scratch) | `str` (password) |

---

## 📝 Function Call Chain

### Encryption Example

```python
# User calls:
cipher = AESLowLevel(key_size=256)
result, steps = cipher.encrypt("Secret Message", "password123")

# Internal call chain:
encrypt()
├── derive_key_from_password()    # password → 32-byte key using SHA-256
├── key_expansion()               # 32-byte key → 15 round keys
├── pkcs7_pad()                   # pad message to 16-byte blocks
└── for each block:
    └── _encrypt_block()
        ├── bytes_to_state()      # 16 bytes → 4x4 matrix
        ├── add_round_key()       # XOR with round key 0
        └── for round 1 to 14:
            ├── sub_bytes()       # S-Box substitution
            ├── shift_rows()      # rotate rows
            ├── mix_columns()     # (skipped in final round)
            └── add_round_key()   # XOR with round key
```

---

## 📂 Project Structure

```
Caesar/
├── streamlit_app.py      # Web UI entry point
├── run_gui.py            # Desktop GUI launcher
├── requirements.txt      # Python dependencies
│
├── src/
│   ├── aes_modules/      # Low-level AES components
│   │   ├── aes_sbox.py         # S-Box lookup tables
│   │   ├── aes_galois.py       # Galois field arithmetic
│   │   ├── aes_operations.py   # Core transformations
│   │   ├── aes_key_expansion.py# Key schedule
│   │   └── aes_low_level.py    # Complete AES cipher
│   │
│   ├── ciphers/          # Cipher implementations
│   │   ├── cipher_base.py      # Abstract base class
│   │   ├── caesar_cipher.py    # CLI tool
│   │   ├── caesar_cipher_class.py # Caesar with visualization
│   │   └── aes_cipher_class.py # AES using pycryptodome
│   │
│   └── gui/              # Desktop application
│       └── cipher_gui.py       # Tkinter GUI
│
└── tests/
    └── test_ciphers.py   # Unit tests
```

---

## 🎓 Educational Notes

### Why Two AES Implementations?

1. **AESCipher** (`aes_cipher_class.py`) - Uses `pycryptodome` library
   - Production-ready, secure, fast
   - Black-box: you can't see the internal steps

2. **AESLowLevel** (`aes_low_level.py`) - Built from scratch
   - Educational: every operation is visible
   - Step-by-step visualization possible
   - Understand exactly how AES works

### Key Concepts

| Concept | Purpose in AES |
|---------|----------------|
| **S-Box** | Non-linearity (prevents linear attacks) |
| **ShiftRows** | Diffusion across columns |
| **MixColumns** | Diffusion within columns |
| **AddRoundKey** | Key mixing |
| **Key Expansion** | Derive many round keys from one master key |
| **GF(2^8)** | Finite field math that keeps all values 0-255 |

---

## 👥 Authors

- [@salah55s](https://github.com/salah55s)
- [@Fares-Elsaghir](https://github.com/Fares-Elsaghir)
- [@ZiadMahmoud855](https://github.com/ZiadMahmoud855)
- [@zeiad1655](https://github.com/zeiad1655)
- [@omar97531](https://github.com/omar97531)
- [@KhaledGamal1](https://github.com/KhaledGamal1)

---

**Happy Encrypting! 🔐**
