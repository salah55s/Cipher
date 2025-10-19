"""
Caesar Cipher Implementation
Authors: Salah, Fares, Ziad, Zeiad
Description: A command-line tool for encrypting and decrypting text using the Caesar cipher algorithm.
"""

import argparse
import sys


def caesar_cipher_encrypt(text, shift):
    """
    Encrypts the given text using Caesar cipher with the specified shift.
    
    Args:
        text (str): The plaintext to encrypt
        shift (int): The number of positions to shift each letter
        
    Returns:
        str: The encrypted ciphertext
    """
    result = ""
    
    for char in text:
        if char.isalpha():
            # Determine if the character is uppercase or lowercase
            ascii_offset = ord('A') if char.isupper() else ord('a')
            
            # Shift the character and wrap around using modulo 26
            shifted = (ord(char) - ascii_offset + shift) % 26
            result += chr(shifted + ascii_offset)
        else:
            # Keep non-alphabetic characters unchanged
            result += char
    
    return result


def caesar_cipher_decrypt(text, shift):
    """
    Decrypts the given ciphertext using Caesar cipher with the specified shift.
    
    Args:
        text (str): The ciphertext to decrypt
        shift (int): The number of positions the letters were shifted
        
    Returns:
        str: The decrypted plaintext
    """
    # Decryption is just encryption with negative shift
    return caesar_cipher_encrypt(text, -shift)


def main():
    """
    Main function to handle command-line arguments and execute the Caesar cipher.
    """
    parser = argparse.ArgumentParser(
        description='Caesar Cipher - Encrypt or decrypt text using the Caesar cipher algorithm.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Encrypt a message:
    python caesar_cipher.py -m "Hello World" -s 3 -e
    
  Decrypt a message:
    python caesar_cipher.py -m "Khoor Zruog" -s 3 -d
    
  Using long options:
    python caesar_cipher.py --message "Secret Message" --shift 5 --encrypt
        """
    )
    
    parser.add_argument(
        '-m', '--message',
        type=str,
        required=True,
        help='The text message to encrypt or decrypt'
    )
    
    parser.add_argument(
        '-s', '--shift',
        type=int,
        required=True,
        help='The shift value (number of positions to shift each letter)'
    )
    
    # Create mutually exclusive group for encrypt/decrypt
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '-e', '--encrypt',
        action='store_true',
        help='Encrypt the message'
    )
    mode_group.add_argument(
        '-d', '--decrypt',
        action='store_true',
        help='Decrypt the message'
    )
    
    args = parser.parse_args()
    
    # Process the message based on the mode
    if args.encrypt:
        result = caesar_cipher_encrypt(args.message, args.shift)
        print(f"\n{'='*50}")
        print(f"Original Text:  {args.message}")
        print(f"Shift Value:    {args.shift}")
        print(f"Cipher Text:    {result}")
        print(f"{'='*50}\n")
    else:  # decrypt
        result = caesar_cipher_decrypt(args.message, args.shift)
        print(f"\n{'='*50}")
        print(f"Cipher Text:    {args.message}")
        print(f"Shift Value:    {args.shift}")
        print(f"Plain Text:     {result}")
        print(f"{'='*50}\n")


if __name__ == "__main__":
    main()