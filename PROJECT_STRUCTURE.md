# Cipher Encryption Tool - Project Structure

## 📁 Directory Organization

```
Caesar/
├── src/                          # Source code
│   ├── __init__.py
│   ├── ciphers/                  # Cipher implementations
│   │   ├── __init__.py
│   │   ├── cipher_base.py        # Abstract base class
│   │   ├── caesar_cipher_class.py # Caesar cipher
│   │   └── aes_cipher_class.py   # AES high-level (pycryptodome)
│   ├── aes_modules/              # Low-level AES components
│   │   ├── __init__.py
│   │   ├── aes_sbox.py           # S-Box lookup tables
│   │   ├── aes_galois.py         # GF(2^8) arithmetic
│   │   ├── aes_operations.py     # Core AES operations
│   │   ├── aes_key_expansion.py  # Key schedule
│   │   └── aes_low_level.py      # Complete AES implementation
│   └── gui/                      # GUI applications
│       ├── __init__.py
│       └── cipher_gui.py         # Tkinter GUI
├── tests/                        # Test files and demos
│   ├── __init__.py
│   ├── test_ciphers.py           # Unit tests
│   └── demo.py                   # Demo script
├── docs/                         # Documentation
│   ├── README.md                 # Main documentation
│   └── QUICKSTART.md             # Quick start guide
├── streamlit_app.py              # Streamlit web UI (main entry)
├── run_gui.py                    # Tkinter GUI launcher
├── caesar_cipher.py              # Original CLI tool
├── caesar_cipher.c               # C implementation
├── caesar_cipher                 # Compiled C binary
└── requirements.txt              # Python dependencies
```

---

## 🎯 Module Overview

### `src/ciphers/`
**Cipher Implementations**

- `cipher_base.py` - Abstract base class defining the cipher interface
- `caesar_cipher_class.py` - Object-oriented Caesar cipher with step tracking
- `aes_cipher_class.py` - High-level AES using pycryptodome library

### `src/aes_modules/`
**Low-Level AES Components** (Built from scratch for education)

- `aes_sbox.py` - S-Box and inverse S-Box lookup tables
- `aes_galois.py` - Galois Field GF(2^8) multiplication operations
- `aes_operations.py` - ShiftRows, MixColumns, AddRoundKey operations
- `aes_key_expansion.py` - Key schedule generation (Rijndael key expansion)
- `aes_low_level.py` - Complete AES-128/256 cipher with visualization

### `src/gui/`
**Graphical User Interfaces**

- `cipher_gui.py` - Tkinter-based desktop application

### `tests/`
**Testing and Demos**

- `test_ciphers.py` - Automated tests for all ciphers
- `demo.py` - Interactive demonstration script

### `docs/`
**Documentation**

- `README.md` - Complete project documentation
- `QUICKSTART.md` - Quick start guide

---

## 🚀 Running the Application

### 1. Web UI (Streamlit) - Recommended
```bash
streamlit run streamlit_app.py
```
**Features:**
- Modern web interface
- Rich visualizations with Plotly
- Step-by-step expandable sections
- Matrix heatmaps
- Round-by-round analysis

### 2. Desktop GUI (Tkinter)
```bash
python run_gui.py
```
or
```bash
python src/gui/cipher_gui.py
```

### 3. Command Line (Caesar only)
```bash
python caesar_cipher.py -m "Hello" -s 3 -e
```

### 4. Demo Script
```bash
python tests/demo.py
```

### 5. Run Tests
```bash
python tests/test_ciphers.py
```

---

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or manually
pip install pycryptodome streamlit plotly pandas
```

---

## 🏗️ Architecture

### Modular Design

```
CipherBase (Abstract)
    ↓
├── CaesarCipher
├── AESCipher (high-level)
└── AESLowLevel (from scratch)
    ↓
    ├── aes_sbox (S-Box)
    ├── aes_galois (GF math)
    ├── aes_operations (transforms)
    └── aes_key_expansion (key schedule)
```

### Benefits
- ✅ **Separation of Concerns** - Each module has one responsibility
- ✅ **Reusability** - Components can be used independently
- ✅ **Testability** - Easy to test individual modules
- ✅ **Maintainability** - Clear structure for updates
- ✅ **Educational** - Learn from modular components

---

## 🔧 Development

### Adding a New Cipher

1. Create new file in `src/ciphers/`
2. Inherit from `CipherBase`
3. Implement `encrypt()` and `decrypt()` methods
4. Return result and visualization steps
5. Add to GUI/Streamlit choices

Example:
```python
from src.ciphers.cipher_base import CipherBase

class MyCipher(CipherBase):
    def encrypt(self, plaintext, key):
        # Implementation
        steps = [...]
        return ciphertext, steps
    
    def decrypt(self, ciphertext, key):
        # Implementation
        steps = [...]
        return plaintext, steps
    
    def get_cipher_name(self):
        return "My Cipher"
```

### Project Standards

- **Python 3.7+** required
- **PEP 8** style guide
- **Type hints** where appropriate
- **Docstrings** for all functions
- **Modular design** - single responsibility
- **Step tracking** - for visualization

---

## 📚 Key Features by Module

### Streamlit App (`streamlit_app.py`)
- ✨ Modern web interface
- 📊 Interactive Plotly charts
- 🔍 Expandable step sections
- 🎨 Matrix heatmaps
- 📱 Responsive design

### Low-Level AES (`src/aes_modules/`)
- 🔐 Built from scratch
- 📖 Educational implementation
- 🔬 Every operation visible
- 🎓 Learn cryptography internals
- 🧪 Modular components

### Tkinter GUI (`src/gui/cipher_gui.py`)
- 🖥️ Desktop application
- 📋 Clipboard integration
- 📊 Scrollable step display
- 🎯 Simple interface

---

## 🎓 Learning Path

1. **Start** with `tests/demo.py` to see examples
2. **Read** `docs/README.md` for concepts
3. **Use** `streamlit_app.py` for visualization
4. **Study** `src/aes_modules/` for low-level details
5. **Experiment** with different inputs
6. **Extend** by adding new ciphers

---

## 👥 Authors

- [@salah55s](https://github.com/salah55s) - Salah Eldin
- [@Fares-Elsaghir](https://github.com/Fares-Elsaghir) - Fares
- [@ZiadMahmoud855](https://github.com/ZiadMahmoud855) - Ziad Mahmoud Ahmed
- [@zeiad1655](https://github.com/zeiad1655) - Zeiad
- [@omar97531](https://github.com/omar97531) - Omar
- [@KhaledGamal1](https://github.com/KhaledGamal1) - Khaled Gamal

---

## 📄 License

Educational project - Feel free to use and modify!

---

**Happy Encrypting! 🔐**
