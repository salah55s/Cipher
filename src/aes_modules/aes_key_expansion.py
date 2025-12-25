"""
Low-Level AES Implementation - Key Expansion
Authors: @salah55s, @Fares-Elsaghir, @ZiadMahmoud855, @zeiad1655, @omar97531, @KhaledGamal1
Description: AES key schedule and round key generation.

================================================================================
KEY EXPANSION (RIJNDAEL KEY SCHEDULE)
================================================================================
The original AES key (128/192/256 bits) is expanded into multiple "round keys",
one for each round of encryption plus one initial key.

KEY SIZES AND ROUNDS:
  - AES-128: 16-byte key → 176 bytes (11 round keys × 16 bytes)
  - AES-192: 24-byte key → 208 bytes (13 round keys × 16 bytes)
  - AES-256: 32-byte key → 240 bytes (15 round keys × 16 bytes)

TERMINOLOGY:
  - Nk: Number of 32-bit words in the original key (4, 6, or 8)
  - Nr: Number of rounds (10, 12, or 14)
  - Word: A 32-bit (4-byte) unit

THE ALGORITHM:
  1. The first Nk words are just the original key
  2. For each subsequent word i:
     - If i % Nk == 0: Apply RotWord, SubWord, XOR with Rcon
     - Else if Nk > 6 and i % Nk == 4: Apply SubWord only (AES-256)
     - Then XOR with word[i - Nk]

This ensures each round key is different and non-linearly derived from
the original key.
================================================================================
"""

from .aes_sbox import SBOX


# ============================================================================
# ROUND CONSTANTS (RCON)
# ============================================================================
# Used in key expansion to make each round key unique.
# RCON[i] = 2^(i-1) in GF(2^8), used to XOR with the first byte after RotWord.
# These are the first 30 values (more than enough for AES-256).
RCON = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36,
    0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6,
    0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91
]


# ============================================================================
# KEY EXPANSION HELPER FUNCTIONS
# ============================================================================

def rot_word(word):
    """
    Rotate word left by one byte: [a0, a1, a2, a3] → [a1, a2, a3, a0]
    
    This is used in key expansion to provide diffusion.
    
    Args:
        word: List of 4 bytes
        
    Returns:
        Rotated word (new list)
    """
    # Take bytes 1,2,3 and append byte 0 at the end
    return word[1:] + word[:1]


def sub_word(word):
    """
    Apply S-Box substitution to each byte in a word.
    
    This provides non-linearity in the key schedule, preventing
    related-key attacks.
    
    Args:
        word: List of 4 bytes
        
    Returns:
        Substituted word (new list)
    """
    # Each byte is replaced with its S-Box lookup
    return [SBOX[byte] for byte in word]


def xor_words(word1, word2):
    """
    XOR two 4-byte words together (byte-by-byte).
    
    Args:
        word1: First word (list of 4 bytes)
        word2: Second word (list of 4 bytes)
        
    Returns:
        XOR result (new list of 4 bytes)
    """
    return [word1[i] ^ word2[i] for i in range(4)]


# ============================================================================
# MAIN KEY EXPANSION FUNCTION
# ============================================================================



def key_expansion(key, key_size=16):
    """
    Expand encryption key to round keys.
    
    Args:
        key: Original encryption key (16, 24, or 32 bytes)
        key_size: Size of key in bytes (16 for AES-128, 32 for AES-256)
        
    Returns:
        List of 4-byte words (expanded key)
    """
    # Determine number of rounds based on key size
    if key_size == 16:
        num_rounds = 10
        nk = 4  # Number of 32-bit words in key
    elif key_size == 24:
        num_rounds = 12
        nk = 6
    elif key_size == 32:
        num_rounds = 14
        nk = 8
    else:
        raise ValueError("Invalid key size. Must be 16, 24, or 32 bytes.")
    
    # Number of 32-bit words needed
    num_words = 4 * (num_rounds + 1)
    
    # Convert key to words
    words = []
    for i in range(nk):
        words.append([key[4*i], key[4*i+1], key[4*i+2], key[4*i+3]])
    
    # Expand key
    for i in range(nk, num_words):
        temp = words[i - 1][:]
        
        if i % nk == 0:
            # Apply rot_word, sub_word, and XOR with round constant
            temp = sub_word(rot_word(temp))
            temp[0] ^= RCON[(i // nk) - 1]
        elif nk > 6 and i % nk == 4:
            # For AES-256 only: apply sub_word
            temp = sub_word(temp)
        
        words.append(xor_words(words[i - nk], temp))
    
    return words


def get_round_key(expanded_key, round_num):
    """
    Extract round key from expanded key.
    
    Args:
        expanded_key: List of 4-byte words
        round_num: Round number (0 to num_rounds)
        
    Returns:
        4x4 round key matrix
    """
    # Get 4 words for this round
    start = round_num * 4
    words = expanded_key[start:start + 4]
    
    # Convert to 4x4 matrix
    round_key = [[0 for _ in range(4)] for _ in range(4)]
    
    for col in range(4):
        for row in range(4):
            round_key[row][col] = words[col][row]
    
    return round_key


def derive_key_from_password(password, key_size=32):
    """
    Derive encryption key from password using SHA-256.
    
    Args:
        password: Password string
        key_size: Desired key size in bytes
        
    Returns:
        Derived key as list of bytes
    """
    from hashlib import sha256
    
    # Hash password
    hash_obj = sha256(password.encode('utf-8'))
    key_bytes = hash_obj.digest()
    
    # Truncate or extend to desired size
    if len(key_bytes) > key_size:
        key_bytes = key_bytes[:key_size]
    elif len(key_bytes) < key_size:
        # Extend by hashing again
        while len(key_bytes) < key_size:
            hash_obj = sha256(key_bytes)
            key_bytes += hash_obj.digest()
        key_bytes = key_bytes[:key_size]
    
    return list(key_bytes)
