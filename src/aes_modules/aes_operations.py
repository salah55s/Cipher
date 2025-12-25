"""
Low-Level AES Implementation - Core Operations
Authors: @salah55s, @Fares-Elsaghir, @ZiadMahmoud855, @zeiad1655, @omar97531, @KhaledGamal1
Description: ShiftRows, MixColumns, and state manipulation operations.

================================================================================
AES STATE MATRIX
================================================================================
AES operates on a 4x4 matrix of bytes called the "state". Data is organized
in COLUMN-MAJOR order:

    Input bytes: [b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15]
    
    State Matrix:
    +----+-----+-----+------+
    | b0 |  b4 |  b8 | b12  |  ← Row 0
    | b1 |  b5 |  b9 | b13  |  ← Row 1
    | b2 |  b6 | b10 | b14  |  ← Row 2
    | b3 |  b7 | b11 | b15  |  ← Row 3
    +----+-----+-----+------+
      ↑     ↑     ↑     ↑
    Col0  Col1  Col2  Col3

Each AES round applies these transformations (in order for encryption):
  1. SubBytes    - Substitute each byte using S-Box (non-linear)
  2. ShiftRows   - Rotate rows left by different amounts (diffusion)
  3. MixColumns  - Mix data within each column (diffusion) [skipped in final round]
  4. AddRoundKey - XOR with round key (key mixing)
================================================================================
"""

from .aes_galois import (
    gf_multiply_by_2, gf_multiply_by_3,
    gf_multiply_by_9, gf_multiply_by_11,
    gf_multiply_by_13, gf_multiply_by_14
)


# ============================================================================
# SHIFTROWS TRANSFORMATION
# ============================================================================
# ShiftRows provides diffusion by rotating each row of the state matrix.
# This ensures bytes from each column get spread across different columns.
#
# Visual:
#   Before ShiftRows:          After ShiftRows:
#   [a0, a1, a2, a3]           [a0, a1, a2, a3]  ← Row 0: no shift
#   [b0, b1, b2, b3]    →      [b1, b2, b3, b0]  ← Row 1: shift left by 1
#   [c0, c1, c2, c3]           [c2, c3, c0, c1]  ← Row 2: shift left by 2
#   [d0, d1, d2, d3]           [d3, d0, d1, d2]  ← Row 3: shift left by 3

def shift_rows(state):
    """
    Perform ShiftRows transformation.
    Row 0: no shift
    Row 1: shift left by 1
    Row 2: shift left by 2
    Row 3: shift left by 3
    
    Args:
        state: 4x4 matrix of bytes (list of 4 lists, each with 4 bytes)
        
    Returns:
        Transformed state (new list, original unchanged)
    """
    # Create a copy to avoid modifying the original
    new_state = [row[:] for row in state]
    
    # Row 0: no shift (stays the same)
    
    # Row 1: shift left by 1 position
    # [b0, b1, b2, b3] → [b1, b2, b3, b0]
    new_state[1] = state[1][1:] + state[1][:1]
    
    # Row 2: shift left by 2 positions
    # [c0, c1, c2, c3] → [c2, c3, c0, c1]
    new_state[2] = state[2][2:] + state[2][:2]
    
    # Row 3: shift left by 3 positions
    # [d0, d1, d2, d3] → [d3, d0, d1, d2]
    new_state[3] = state[3][3:] + state[3][:3]
    
    return new_state


# ============================================================================
# INVERSE SHIFTROWS (for decryption)
# ============================================================================
# Reverses ShiftRows by rotating rows RIGHT instead of left.

def inv_shift_rows(state):
    """
    Perform inverse ShiftRows transformation (for decryption).
    Row 0: no shift
    Row 1: shift right by 1
    Row 2: shift right by 2
    Row 3: shift right by 3
    
    Args:
        state: 4x4 matrix of bytes
        
    Returns:
        Transformed state (new list)
    """
    new_state = [row[:] for row in state]
    
    # Row 0: no shift (stays the same)
    
    # Row 1: shift right by 1
    # [b1, b2, b3, b0] → [b0, b1, b2, b3]
    new_state[1] = state[1][-1:] + state[1][:-1]
    
    # Row 2: shift right by 2
    # [c2, c3, c0, c1] → [c0, c1, c2, c3]
    new_state[2] = state[2][-2:] + state[2][:-2]
    
    # Row 3: shift right by 3
    # [d3, d0, d1, d2] → [d0, d1, d2, d3]
    new_state[3] = state[3][-3:] + state[3][:-3]
    
    return new_state


# ============================================================================
# MIXCOLUMNS TRANSFORMATION
# ============================================================================
# MixColumns provides diffusion by mixing bytes WITHIN each column.
# Each column is treated as a polynomial and multiplied by a fixed
# polynomial modulo x^4 + 1.
#
# This is equivalent to matrix multiplication in GF(2^8):
#
#   [2 3 1 1]   [s0]   [s0']
#   [1 2 3 1] × [s1] = [s1']    (for each column)
#   [1 1 2 3]   [s2]   [s2']
#   [3 1 1 2]   [s3]   [s3']
#
# Example for column 0:
#   s0' = (2 × s0) ⊕ (3 × s1) ⊕ (1 × s2) ⊕ (1 × s3)
#   s1' = (1 × s0) ⊕ (2 × s1) ⊕ (3 × s2) ⊕ (1 × s3)
#   s2' = (1 × s0) ⊕ (1 × s1) ⊕ (2 × s2) ⊕ (3 × s3)
#   s3' = (3 × s0) ⊕ (1 × s1) ⊕ (1 × s2) ⊕ (2 × s3)
#
# Note: All multiplication is in GF(2^8), addition is XOR.

def mix_columns(state):
    """
    Perform MixColumns transformation.
    Multiply each column by a fixed matrix in GF(2^8).
    
    Matrix:
    [2 3 1 1]
    [1 2 3 1]
    [1 1 2 3]
    [3 1 1 2]
    
    Args:
        state: 4x4 matrix of bytes
        
    Returns:
        Transformed state (new list)
    """
    new_state = [[0 for _ in range(4)] for _ in range(4)]
    
    # Process each of the 4 columns
    for col in range(4):
        # Extract the 4 bytes of this column
        s0 = state[0][col]  # Row 0
        s1 = state[1][col]  # Row 1
        s2 = state[2][col]  # Row 2
        s3 = state[3][col]  # Row 3
        
        # Apply matrix multiplication in GF(2^8)
        # Each row of the result is a linear combination of the input bytes
        new_state[0][col] = gf_multiply_by_2(s0) ^ gf_multiply_by_3(s1) ^ s2 ^ s3
        new_state[1][col] = s0 ^ gf_multiply_by_2(s1) ^ gf_multiply_by_3(s2) ^ s3
        new_state[2][col] = s0 ^ s1 ^ gf_multiply_by_2(s2) ^ gf_multiply_by_3(s3)
        new_state[3][col] = gf_multiply_by_3(s0) ^ s1 ^ s2 ^ gf_multiply_by_2(s3)
    
    return new_state


# ============================================================================
# INVERSE MIXCOLUMNS (for decryption)
# ============================================================================
# Uses the inverse matrix. The constants 9, 11, 13, 14 are more complex
# than the encryption constants 1, 2, 3.

def inv_mix_columns(state):
    """
    Perform inverse MixColumns transformation (for decryption).
    
    Inverse Matrix:
    [14 11 13  9]    (0x0E 0x0B 0x0D 0x09)
    [ 9 14 11 13]    (0x09 0x0E 0x0B 0x0D)
    [13  9 14 11]    (0x0D 0x09 0x0E 0x0B)
    [11 13  9 14]    (0x0B 0x0D 0x09 0x0E)
    
    Args:
        state: 4x4 matrix of bytes
        
    Returns:
        Transformed state (new list)
    """
    new_state = [[0 for _ in range(4)] for _ in range(4)]
    
    for col in range(4):
        # Extract the 4 bytes of this column
        s0 = state[0][col]
        s1 = state[1][col]
        s2 = state[2][col]
        s3 = state[3][col]
        
        # Apply inverse matrix multiplication in GF(2^8)
        # Uses constants 9, 11, 13, 14 (compared to 1, 2, 3 for forward)
        new_state[0][col] = gf_multiply_by_14(s0) ^ gf_multiply_by_11(s1) ^ gf_multiply_by_13(s2) ^ gf_multiply_by_9(s3)
        new_state[1][col] = gf_multiply_by_9(s0) ^ gf_multiply_by_14(s1) ^ gf_multiply_by_11(s2) ^ gf_multiply_by_13(s3)
        new_state[2][col] = gf_multiply_by_13(s0) ^ gf_multiply_by_9(s1) ^ gf_multiply_by_14(s2) ^ gf_multiply_by_11(s3)
        new_state[3][col] = gf_multiply_by_11(s0) ^ gf_multiply_by_13(s1) ^ gf_multiply_by_9(s2) ^ gf_multiply_by_14(s3)
    
    return new_state


# ============================================================================
# ADDROUNDKEY TRANSFORMATION
# ============================================================================
# The simplest operation: just XOR the state with the round key.
# XOR is its own inverse, so the same operation is used for both
# encryption and decryption.

def add_round_key(state, round_key):
    """
    XOR state with round key.
    
    This is used in both encryption and decryption (XOR is self-inverse).
    Each byte of the state is XORed with the corresponding byte of the key.
    
    Args:
        state: 4x4 matrix of bytes (current cipher state)
        round_key: 4x4 matrix of bytes (derived from the master key)
        
    Returns:
        Transformed state (new list)
    """
    # XOR each byte: state[row][col] ^= round_key[row][col]
    return [[state[i][j] ^ round_key[i][j] for j in range(4)] for i in range(4)]


# ============================================================================
# STATE CONVERSION UTILITIES
# ============================================================================
# These functions convert between a linear byte array (16 bytes) and the
# 4x4 state matrix. Note the COLUMN-MAJOR order!

def bytes_to_state(data):
    """
    Convert 16 bytes to 4x4 state matrix (column-major order).
    
    Input bytes are arranged into columns, not rows:
      bytes: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
      state[row][col] = bytes[row + 4*col]
      
      Result:      Col0 Col1 Col2 Col3
      Row 0:       [ 0,   4,   8,  12 ]
      Row 1:       [ 1,   5,   9,  13 ]
      Row 2:       [ 2,   6,  10,  14 ]
      Row 3:       [ 3,   7,  11,  15 ]
    
    Args:
        data: List of 16 bytes (as integers 0-255)
        
    Returns:
        4x4 state matrix (list of 4 lists)
    """
    state = [[0 for _ in range(4)] for _ in range(4)]
    
    # Fill state in column-major order
    for i in range(4):      # row
        for j in range(4):  # column
            state[i][j] = data[i + 4 * j]
    
    return state


def state_to_bytes(state):
    """
    Convert 4x4 state matrix to 16 bytes (column-major order).
    
    Args:
        state: 4x4 state matrix
        
    Returns:
        List of 16 bytes
    """
    data = []
    
    for j in range(4):
        for i in range(4):
            data.append(state[i][j])
    
    return data
