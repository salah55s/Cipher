"""
Low-Level AES Implementation - Galois Field Operations
Authors: Salah, Fares, Ziad, Zeiad
Description: Galois Field GF(2^8) arithmetic for AES MixColumns operation.
"""


def xtime(byte):
    """
    Multiply by 2 in GF(2^8).
    This is used for MixColumns operation.
    
    Args:
        byte: Input byte
        
    Returns:
        Result of multiplication by 2 in GF(2^8)
    """
    # Left shift by 1
    result = (byte << 1) & 0xFF
    
    # If the high bit was set, XOR with 0x1B (irreducible polynomial)
    if byte & 0x80:
        result ^= 0x1B
    
    return result


def gf_multiply(a, b):
    """
    Multiply two bytes in GF(2^8).
    
    Args:
        a: First byte
        b: Second byte
        
    Returns:
        Product in GF(2^8)
    """
    result = 0
    
    for _ in range(8):
        # If lowest bit of b is set, XOR a into result
        if b & 1:
            result ^= a
        
        # Check if high bit of a is set
        high_bit_set = a & 0x80
        
        # Multiply a by 2 (shift left)
        a = (a << 1) & 0xFF
        
        # If high bit was set, XOR with 0x1B
        if high_bit_set:
            a ^= 0x1B
        
        # Divide b by 2 (shift right)
        b >>= 1
    
    return result


def gf_multiply_by_2(byte):
    """Shortcut: multiply by 2 in GF(2^8)."""
    return xtime(byte)


def gf_multiply_by_3(byte):
    """Shortcut: multiply by 3 in GF(2^8)."""
    return xtime(byte) ^ byte


def gf_multiply_by_9(byte):
    """Shortcut: multiply by 9 in GF(2^8)."""
    return xtime(xtime(xtime(byte))) ^ byte


def gf_multiply_by_11(byte):
    """Shortcut: multiply by 11 (0x0B) in GF(2^8)."""
    return xtime(xtime(xtime(byte)) ^ byte) ^ byte


def gf_multiply_by_13(byte):
    """Shortcut: multiply by 13 (0x0D) in GF(2^8)."""
    return xtime(xtime(xtime(byte) ^ byte)) ^ byte


def gf_multiply_by_14(byte):
    """Shortcut: multiply by 14 (0x0E) in GF(2^8)."""
    return xtime(xtime(xtime(byte) ^ byte) ^ byte)
