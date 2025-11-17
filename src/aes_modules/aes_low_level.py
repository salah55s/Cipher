"""
Low-Level AES Implementation - Main Cipher
Authors: Salah, Fares, Ziad, Zeiad
Description: Complete AES-128/256 encryption/decryption with detailed step tracking.
"""

from typing import List, Tuple, Dict
import os
import sys
from pathlib import Path

# Add ciphers to path for cipher_base
sys.path.insert(0, str(Path(__file__).parent.parent))

from ciphers.cipher_base import CipherBase
from .aes_sbox import sub_bytes, inv_sub_bytes
from .aes_operations import (
    shift_rows, inv_shift_rows,
    mix_columns, inv_mix_columns,
    add_round_key, bytes_to_state, state_to_bytes
)
from .aes_key_expansion import (
    key_expansion, get_round_key, derive_key_from_password
)


def pkcs7_pad(data, block_size=16):
    """
    Apply PKCS7 padding to data.
    
    Args:
        data: Data bytes
        block_size: Block size (16 for AES)
        
    Returns:
        Padded data
    """
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding


def pkcs7_unpad(data):
    """
    Remove PKCS7 padding from data.
    
    Args:
        data: Padded data bytes
        
    Returns:
        Unpadded data
    """
    padding_length = data[-1]
    return data[:-padding_length]


class AESLowLevel(CipherBase):
    """Low-level AES implementation with detailed visualization."""
    
    def __init__(self, key_size=128):
        """
        Initialize AES cipher.
        
        Args:
            key_size: Key size in bits (128 or 256)
        """
        self.key_size_bits = key_size
        self.key_size_bytes = key_size // 8
        self.name = f"AES-{key_size} (Low-Level)"
        
        # Number of rounds
        if key_size == 128:
            self.num_rounds = 10
        elif key_size == 256:
            self.num_rounds = 14
        else:
            raise ValueError("Key size must be 128 or 256 bits")
    
    def _encrypt_block(self, block, expanded_key, track_steps=True):
        """
        Encrypt a single 16-byte block.
        
        Args:
            block: 16 bytes to encrypt
            expanded_key: Expanded key schedule
            track_steps: Whether to track detailed steps
            
        Returns:
            Tuple of (encrypted_bytes, steps)
        """
        steps = []
        
        # Convert to state matrix
        state = bytes_to_state(block)
        
        if track_steps:
            steps.append({
                'round': 'initial',
                'operation': 'Convert to State',
                'description': 'Convert 16 bytes to 4x4 state matrix',
                'state_before': None,
                'state_after': [row[:] for row in state],
                'details': 'State is organized in column-major order'
            })
        
        # Initial round key addition
        round_key = get_round_key(expanded_key, 0)
        state = add_round_key(state, round_key)
        
        if track_steps:
            steps.append({
                'round': 0,
                'operation': 'AddRoundKey',
                'description': 'XOR state with round key 0',
                'state_before': bytes_to_state(block),
                'state_after': [row[:] for row in state],
                'round_key': [row[:] for row in round_key],
                'details': 'Each byte: state[i][j] ^= round_key[i][j]'
            })
        
        # Main rounds
        for round_num in range(1, self.num_rounds + 1):
            round_steps = []
            
            # SubBytes
            state_before_sub = [row[:] for row in state]
            state = sub_bytes(state)
            if track_steps:
                round_steps.append({
                    'round': round_num,
                    'operation': 'SubBytes',
                    'description': 'Apply S-Box substitution to each byte',
                    'state_before': state_before_sub,
                    'state_after': [row[:] for row in state],
                    'details': 'Non-linear byte substitution using lookup table'
                })
            
            # ShiftRows
            state_before_shift = [row[:] for row in state]
            state = shift_rows(state)
            if track_steps:
                round_steps.append({
                    'round': round_num,
                    'operation': 'ShiftRows',
                    'description': 'Cyclically shift rows left',
                    'state_before': state_before_shift,
                    'state_after': [row[:] for row in state],
                    'details': 'Row 0: no shift, Row 1: shift 1, Row 2: shift 2, Row 3: shift 3'
                })
            
            # MixColumns (not in final round)
            if round_num < self.num_rounds:
                state_before_mix = [row[:] for row in state]
                state = mix_columns(state)
                if track_steps:
                    round_steps.append({
                        'round': round_num,
                        'operation': 'MixColumns',
                        'description': 'Mix data within columns using GF(2^8) multiplication',
                        'state_before': state_before_mix,
                        'state_after': [row[:] for row in state],
                        'details': 'Linear mixing operation in Galois Field'
                    })
            
            # AddRoundKey
            state_before_key = [row[:] for row in state]
            round_key = get_round_key(expanded_key, round_num)
            state = add_round_key(state, round_key)
            if track_steps:
                round_steps.append({
                    'round': round_num,
                    'operation': 'AddRoundKey',
                    'description': f'XOR state with round key {round_num}',
                    'state_before': state_before_key,
                    'state_after': [row[:] for row in state],
                    'round_key': [row[:] for row in round_key],
                    'details': f'Round {round_num} complete'
                })
            
            steps.extend(round_steps)
        
        # Convert back to bytes
        encrypted_bytes = state_to_bytes(state)
        
        return encrypted_bytes, steps
    
    def _decrypt_block(self, block, expanded_key, track_steps=True):
        """
        Decrypt a single 16-byte block.
        
        Args:
            block: 16 bytes to decrypt
            expanded_key: Expanded key schedule
            track_steps: Whether to track detailed steps
            
        Returns:
            Tuple of (decrypted_bytes, steps)
        """
        steps = []
        
        # Convert to state matrix
        state = bytes_to_state(block)
        
        if track_steps:
            steps.append({
                'round': 'initial',
                'operation': 'Convert to State',
                'description': 'Convert 16 bytes to 4x4 state matrix',
                'state_before': None,
                'state_after': [row[:] for row in state],
                'details': 'State is organized in column-major order'
            })
        
        # Initial round key addition (last round key)
        round_key = get_round_key(expanded_key, self.num_rounds)
        state = add_round_key(state, round_key)
        
        if track_steps:
            steps.append({
                'round': self.num_rounds,
                'operation': 'AddRoundKey',
                'description': f'XOR state with round key {self.num_rounds}',
                'state_before': bytes_to_state(block),
                'state_after': [row[:] for row in state],
                'round_key': [row[:] for row in round_key],
                'details': 'Starting decryption with final round key'
            })
        
        # Main rounds (in reverse)
        for round_num in range(self.num_rounds - 1, -1, -1):
            round_steps = []
            
            # InvShiftRows
            state_before_shift = [row[:] for row in state]
            state = inv_shift_rows(state)
            if track_steps:
                round_steps.append({
                    'round': round_num,
                    'operation': 'InvShiftRows',
                    'description': 'Cyclically shift rows right (inverse)',
                    'state_before': state_before_shift,
                    'state_after': [row[:] for row in state],
                    'details': 'Reverse of ShiftRows operation'
                })
            
            # InvSubBytes
            state_before_sub = [row[:] for row in state]
            state = inv_sub_bytes(state)
            if track_steps:
                round_steps.append({
                    'round': round_num,
                    'operation': 'InvSubBytes',
                    'description': 'Apply inverse S-Box substitution',
                    'state_before': state_before_sub,
                    'state_after': [row[:] for row in state],
                    'details': 'Inverse of SubBytes using inverse S-Box'
                })
            
            # AddRoundKey
            state_before_key = [row[:] for row in state]
            round_key = get_round_key(expanded_key, round_num)
            state = add_round_key(state, round_key)
            if track_steps:
                round_steps.append({
                    'round': round_num,
                    'operation': 'AddRoundKey',
                    'description': f'XOR state with round key {round_num}',
                    'state_before': state_before_key,
                    'state_after': [row[:] for row in state],
                    'round_key': [row[:] for row in round_key],
                    'details': 'XOR is its own inverse'
                })
            
            # InvMixColumns (not in first decryption round)
            if round_num > 0:
                state_before_mix = [row[:] for row in state]
                state = inv_mix_columns(state)
                if track_steps:
                    round_steps.append({
                        'round': round_num,
                        'operation': 'InvMixColumns',
                        'description': 'Inverse mix columns operation',
                        'state_before': state_before_mix,
                        'state_after': [row[:] for row in state],
                        'details': 'Inverse of MixColumns in GF(2^8)'
                    })
            
            steps.extend(round_steps)
        
        # Convert back to bytes
        decrypted_bytes = state_to_bytes(state)
        
        return decrypted_bytes, steps
    
    def encrypt(self, plaintext: str, key: str) -> Tuple[str, List[dict]]:
        """Encrypt plaintext using AES."""
        all_steps = []
        
        # Step 1: Derive key
        derived_key = derive_key_from_password(key, self.key_size_bytes)
        all_steps.append({
            'step_number': 1,
            'title': 'Key Derivation',
            'description': f'Derive {self.key_size_bits}-bit key from password using SHA-256',
            'details': f'Password: "{key}" → {self.key_size_bytes} bytes',
            'data': {'key_hex': ''.join(f'{b:02x}' for b in derived_key[:16]) + '...'}
        })
        
        # Step 2: Expand key
        expanded_key = key_expansion(derived_key, self.key_size_bytes)
        all_steps.append({
            'step_number': 2,
            'title': 'Key Expansion',
            'description': f'Expand key to {len(expanded_key)} round keys',
            'details': f'Generated {len(expanded_key)} 32-bit words for {self.num_rounds + 1} round keys',
            'data': {'num_round_keys': self.num_rounds + 1, 'num_words': len(expanded_key)}
        })
        
        # Step 3: Convert and pad
        plaintext_bytes = plaintext.encode('utf-8')
        padded_bytes = pkcs7_pad(plaintext_bytes)
        all_steps.append({
            'step_number': 3,
            'title': 'Encoding and Padding',
            'description': f'Convert to bytes and apply PKCS7 padding',
            'details': f'Text: {len(plaintext)} chars → {len(plaintext_bytes)} bytes → {len(padded_bytes)} bytes (padded)',
            'data': {'padding_added': len(padded_bytes) - len(plaintext_bytes)}
        })
        
        # Step 4: Encrypt blocks
        ciphertext_bytes = b''
        num_blocks = len(padded_bytes) // 16
        
        for block_num in range(num_blocks):
            block_start = block_num * 16
            block = list(padded_bytes[block_start:block_start + 16])
            
            encrypted_block, block_steps = self._encrypt_block(block, expanded_key, track_steps=True)
            ciphertext_bytes += bytes(encrypted_block)
            
            all_steps.append({
                'step_number': 4 + block_num,
                'title': f'Encrypt Block {block_num + 1}/{num_blocks}',
                'description': f'Process 16-byte block through {self.num_rounds} AES rounds',
                'details': f'Block {block_num + 1} encrypted with {len(block_steps)} operations',
                'data': {
                    'block_number': block_num + 1,
                    'block_steps': block_steps
                }
            })
        
        # Step 5: Encode output
        import base64
        ciphertext_b64 = base64.b64encode(ciphertext_bytes).decode('ascii')
        all_steps.append({
            'step_number': 4 + num_blocks,
            'title': 'Base64 Encoding',
            'description': 'Encode binary output to text format',
            'details': f'{len(ciphertext_bytes)} bytes → {len(ciphertext_b64)} characters',
            'data': {'output': ciphertext_b64}
        })
        
        return ciphertext_b64, all_steps
    
    def decrypt(self, ciphertext: str, key: str) -> Tuple[str, List[dict]]:
        """Decrypt ciphertext using AES."""
        all_steps = []
        
        try:
            # Step 1: Derive key
            derived_key = derive_key_from_password(key, self.key_size_bytes)
            all_steps.append({
                'step_number': 1,
                'title': 'Key Derivation',
                'description': f'Derive {self.key_size_bits}-bit key from password',
                'details': f'Using SHA-256 hash function',
                'data': {'key_hex': ''.join(f'{b:02x}' for b in derived_key[:16]) + '...'}
            })
            
            # Step 2: Expand key
            expanded_key = key_expansion(derived_key, self.key_size_bytes)
            all_steps.append({
                'step_number': 2,
                'title': 'Key Expansion',
                'description': f'Expand key for decryption',
                'details': f'{self.num_rounds + 1} round keys generated',
                'data': {}
            })
            
            # Step 3: Decode from base64
            import base64
            ciphertext_bytes = base64.b64decode(ciphertext)
            all_steps.append({
                'step_number': 3,
                'title': 'Base64 Decoding',
                'description': 'Decode text input to binary',
                'details': f'{len(ciphertext)} characters → {len(ciphertext_bytes)} bytes',
                'data': {}
            })
            
            # Step 4: Decrypt blocks
            plaintext_bytes = b''
            num_blocks = len(ciphertext_bytes) // 16
            
            for block_num in range(num_blocks):
                block_start = block_num * 16
                block = list(ciphertext_bytes[block_start:block_start + 16])
                
                decrypted_block, block_steps = self._decrypt_block(block, expanded_key, track_steps=True)
                plaintext_bytes += bytes(decrypted_block)
                
                all_steps.append({
                    'step_number': 4 + block_num,
                    'title': f'Decrypt Block {block_num + 1}/{num_blocks}',
                    'description': f'Process 16-byte block through inverse AES rounds',
                    'details': f'Block {block_num + 1} decrypted',
                    'data': {
                        'block_number': block_num + 1,
                        'block_steps': block_steps
                    }
                })
            
            # Step 5: Remove padding
            unpadded_bytes = pkcs7_unpad(plaintext_bytes)
            plaintext = unpadded_bytes.decode('utf-8')
            all_steps.append({
                'step_number': 4 + num_blocks,
                'title': 'Remove Padding and Decode',
                'description': 'Remove PKCS7 padding and convert to text',
                'details': f'{len(plaintext_bytes)} bytes → {len(unpadded_bytes)} bytes → "{plaintext}"',
                'data': {'output': plaintext}
            })
            
            return plaintext, all_steps
            
        except Exception as e:
            all_steps.append({
                'step_number': len(all_steps) + 1,
                'title': 'Error',
                'description': 'Decryption failed',
                'details': str(e),
                'data': {}
            })
            return "", all_steps
    
    def get_cipher_name(self) -> str:
        """Return cipher name."""
        return self.name
