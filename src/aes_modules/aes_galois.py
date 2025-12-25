"""
Low-Level AES Implementation - Galois Field Operations
Authors: @salah55s, @Fares-Elsaghir, @ZiadMahmoud855, @zeiad1655, @omar97531, @KhaledGamal1
Description: Galois Field GF(2^8) arithmetic for AES MixColumns operation.

================================================================================
WHAT IS GF(2^8)?
================================================================================
GF(2^8) is a Galois Field (finite field) with 256 elements (2^8 = 256).
In this field:
  - Addition is XOR (no carry propagation)
  - Multiplication is polynomial multiplication modulo an irreducible polynomial

WHY USE GF(2^8)?
  - Each byte (8 bits) maps to one element of GF(2^8)
  - Operations stay within 8-bit range (results are always 0x00-0xFF)
  - Provides mathematical structure for MixColumns diffusion

THE IRREDUCIBLE POLYNOMIAL:
  x^8 + x^4 + x^3 + x + 1 = 0x11B (binary: 100011011)
  When a multiplication result exceeds 8 bits, we reduce it by XORing with 0x1B
  (the lower 8 bits of 0x11B).

EXAMPLE:
  2 * 0x80 = 0x100 (overflow!)
  Since bit 8 is set, we XOR with 0x1B:
  0x100 & 0xFF = 0x00, then 0x00 ^ 0x1B = 0x1B
================================================================================
"""


# ============================================================================
# XTIME - THE CORE OPERATION
# ============================================================================
# xtime multiplies a byte by 2 in GF(2^8). This is the building block for
# all other multiplications. Think of it as "double and reduce if needed".

def xtime(byte):
    """
    Multiply by 2 in GF(2^8).
    This is used for MixColumns operation.
    
    Args:
        byte: Input byte (0x00 to 0xFF)
        
    Returns:
        Result of multiplication by 2 in GF(2^8)
        
    Algorithm:
        1. Left shift by 1 (multiply by 2 in binary)
        2. If the original high bit was set (overflow), XOR with 0x1B
    """
    # Step 1: Left shift by 1 (multiply by 2), mask to 8 bits
    result = (byte << 1) & 0xFF
    
    # Step 2: If original byte had high bit set (0x80 = 10000000 binary),
    # the result overflowed. XOR with irreducible polynomial 0x1B to reduce.
    if byte & 0x80:
        result ^= 0x1B
    
    return result


# ============================================================================
# GENERAL GF(2^8) MULTIPLICATION
# ============================================================================
# This implements "peasant multiplication" (also called Russian peasant method)
# adapted for GF(2^8). It's like grade-school multiplication but with XOR.

def gf_multiply(a, b):
    """
    Multiply two bytes in GF(2^8) using peasant multiplication.
    
    Args:
        a: First byte (multiplicand)
        b: Second byte (multiplier)
        
    Returns:
        Product in GF(2^8) (always 0x00 to 0xFF)
        
    Algorithm (Russian Peasant Method):
        result = 0
        for each bit in b:
            if bit is 1: result ^= a
            a = xtime(a)  # double a
            b >>= 1       # shift to next bit
    """
    result = 0
    
    for _ in range(8):  # Process all 8 bits of b
        # If lowest bit of b is 1, add a to result (addition = XOR in GF)
        if b & 1:
            result ^= a
        
        # Check if high bit of a is set (will overflow on double)
        high_bit_set = a & 0x80
        
        # Double a (shift left by 1, mask to 8 bits)
        a = (a << 1) & 0xFF
        
        # If high bit was set, reduce by XORing with 0x1B
        if high_bit_set:
            a ^= 0x1B
        
        # Move to next bit of b (divide by 2)
        b >>= 1
    
    return result


# ============================================================================
# OPTIMIZED MULTIPLICATIONS FOR MIXCOLUMNS
# ============================================================================
# MixColumns only needs multiplication by specific constants: 2, 3 for encrypt
# and 9, 11, 13, 14 for decrypt. These can be computed more efficiently using
# combinations of xtime and XOR.
#
# Key insight: Multiplication is distributive in GF(2^8)
#   - 3*b = 2*b + b = xtime(b) ^ b
#   - 9*b = 8*b + b = xtime(xtime(xtime(b))) ^ b
#   etc.

def gf_multiply_by_2(byte):
    """Multiply by 2 in GF(2^8). Same as xtime."""
    return xtime(byte)


def gf_multiply_by_3(byte):
    """
    Multiply by 3 in GF(2^8).
    3 = 2 + 1, so 3*b = 2*b XOR b = xtime(b) ^ b
    """
    return xtime(byte) ^ byte


def gf_multiply_by_9(byte):
    """
    Multiply by 9 in GF(2^8) - used in InvMixColumns.
    9 = 8 + 1 = 2^3 + 1, so 9*b = xtime(xtime(xtime(b))) ^ b
    """
    return xtime(xtime(xtime(byte))) ^ byte


def gf_multiply_by_11(byte):
    """
    Multiply by 11 (0x0B) in GF(2^8) - used in InvMixColumns.
    11 = 8 + 2 + 1, so 11*b = 2*(8*b + b) + b = xtime(xtime(xtime(b)) ^ b) ^ b
    """
    return xtime(xtime(xtime(byte)) ^ byte) ^ byte


def gf_multiply_by_13(byte):
    """
    Multiply by 13 (0x0D) in GF(2^8) - used in InvMixColumns.
    13 = 8 + 4 + 1, so 13*b = 2*(2*(8*b + b)) + b = xtime(xtime(xtime(b) ^ b)) ^ b
    """
    return xtime(xtime(xtime(byte) ^ byte)) ^ byte


def gf_multiply_by_14(byte):
    """
    Multiply by 14 (0x0E) in GF(2^8) - used in InvMixColumns.
    14 = 8 + 4 + 2, so 14*b = 2*(2*(2*b + b) + b) = xtime(xtime(xtime(b) ^ b) ^ b)
    """
    return xtime(xtime(xtime(byte) ^ byte) ^ byte)

