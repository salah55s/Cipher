"""
Low-Level AES Implementation - Core Operations
Authors: Salah, Fares, Ziad, Zeiad
Description: ShiftRows, MixColumns, and state manipulation operations.
"""

from .aes_galois import (
    gf_multiply_by_2, gf_multiply_by_3,
    gf_multiply_by_9, gf_multiply_by_11,
    gf_multiply_by_13, gf_multiply_by_14
)


def shift_rows(state):
    """
    Perform ShiftRows transformation.
    Row 0: no shift
    Row 1: shift left by 1
    Row 2: shift left by 2
    Row 3: shift left by 3
    
    Args:
        state: 4x4 matrix of bytes
        
    Returns:
        Transformed state
    """
    new_state = [row[:] for row in state]
    
    # Row 1: shift left by 1
    new_state[1] = state[1][1:] + state[1][:1]
    
    # Row 2: shift left by 2
    new_state[2] = state[2][2:] + state[2][:2]
    
    # Row 3: shift left by 3
    new_state[3] = state[3][3:] + state[3][:3]
    
    return new_state


def inv_shift_rows(state):
    """
    Perform inverse ShiftRows transformation.
    Row 0: no shift
    Row 1: shift right by 1
    Row 2: shift right by 2
    Row 3: shift right by 3
    
    Args:
        state: 4x4 matrix of bytes
        
    Returns:
        Transformed state
    """
    new_state = [row[:] for row in state]
    
    # Row 1: shift right by 1
    new_state[1] = state[1][-1:] + state[1][:-1]
    
    # Row 2: shift right by 2
    new_state[2] = state[2][-2:] + state[2][:-2]
    
    # Row 3: shift right by 3
    new_state[3] = state[3][-3:] + state[3][:-3]
    
    return new_state


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
        Transformed state
    """
    new_state = [[0 for _ in range(4)] for _ in range(4)]
    
    for col in range(4):
        # Extract column
        s0 = state[0][col]
        s1 = state[1][col]
        s2 = state[2][col]
        s3 = state[3][col]
        
        # Apply matrix multiplication in GF(2^8)
        new_state[0][col] = gf_multiply_by_2(s0) ^ gf_multiply_by_3(s1) ^ s2 ^ s3
        new_state[1][col] = s0 ^ gf_multiply_by_2(s1) ^ gf_multiply_by_3(s2) ^ s3
        new_state[2][col] = s0 ^ s1 ^ gf_multiply_by_2(s2) ^ gf_multiply_by_3(s3)
        new_state[3][col] = gf_multiply_by_3(s0) ^ s1 ^ s2 ^ gf_multiply_by_2(s3)
    
    return new_state


def inv_mix_columns(state):
    """
    Perform inverse MixColumns transformation.
    
    Matrix:
    [14 11 13  9]
    [ 9 14 11 13]
    [13  9 14 11]
    [11 13  9 14]
    
    Args:
        state: 4x4 matrix of bytes
        
    Returns:
        Transformed state
    """
    new_state = [[0 for _ in range(4)] for _ in range(4)]
    
    for col in range(4):
        # Extract column
        s0 = state[0][col]
        s1 = state[1][col]
        s2 = state[2][col]
        s3 = state[3][col]
        
        # Apply inverse matrix multiplication in GF(2^8)
        new_state[0][col] = gf_multiply_by_14(s0) ^ gf_multiply_by_11(s1) ^ gf_multiply_by_13(s2) ^ gf_multiply_by_9(s3)
        new_state[1][col] = gf_multiply_by_9(s0) ^ gf_multiply_by_14(s1) ^ gf_multiply_by_11(s2) ^ gf_multiply_by_13(s3)
        new_state[2][col] = gf_multiply_by_13(s0) ^ gf_multiply_by_9(s1) ^ gf_multiply_by_14(s2) ^ gf_multiply_by_11(s3)
        new_state[3][col] = gf_multiply_by_11(s0) ^ gf_multiply_by_13(s1) ^ gf_multiply_by_9(s2) ^ gf_multiply_by_14(s3)
    
    return new_state


def add_round_key(state, round_key):
    """
    XOR state with round key.
    
    Args:
        state: 4x4 matrix of bytes
        round_key: 4x4 matrix of bytes (round key)
        
    Returns:
        Transformed state
    """
    return [[state[i][j] ^ round_key[i][j] for j in range(4)] for i in range(4)]


def bytes_to_state(data):
    """
    Convert 16 bytes to 4x4 state matrix (column-major order).
    
    Args:
        data: List of 16 bytes
        
    Returns:
        4x4 state matrix
    """
    state = [[0 for _ in range(4)] for _ in range(4)]
    
    for i in range(4):
        for j in range(4):
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
