/*
 * Caesar Cipher Implementation in C
 * Authors: Salah, Fares, Ziad, Zeiad
 * Description: A command-line tool for encrypting and decrypting text using Caesar cipher
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TEXT_LENGTH 1000

/**
 * Encrypts a character using Caesar cipher
 * @param ch: The character to encrypt
 * @param shift: The shift value
 * @return: The encrypted character
 */
char encrypt_char(char ch, int shift) {
    if (isalpha(ch)) {
        char base = isupper(ch) ? 'A' : 'a';
        return (char)((ch - base + shift) % 26 + base);
    }
    return ch;
}

/**
 * Decrypts a character using Caesar cipher
 * @param ch: The character to decrypt
 * @param shift: The shift value
 * @return: The decrypted character
 */
char decrypt_char(char ch, int shift) {
    if (isalpha(ch)) {
        char base = isupper(ch) ? 'A' : 'a';
        // Handle negative modulo correctly
        return (char)((ch - base - shift + 26) % 26 + base);
    }
    return ch;
}

/**
 * Encrypts the entire text using Caesar cipher
 * @param text: The plaintext to encrypt
 * @param shift: The shift value
 * @param result: Buffer to store the encrypted text
 */
void caesar_encrypt(const char *text, int shift, char *result) {
    int i;
    // Normalize shift to 0-25 range
    shift = shift % 26;
    if (shift < 0) shift += 26;
    
    for (i = 0; text[i] != '\0'; i++) {
        result[i] = encrypt_char(text[i], shift);
    }
    result[i] = '\0';
}

/**
 * Decrypts the entire text using Caesar cipher
 * @param text: The ciphertext to decrypt
 * @param shift: The shift value
 * @param result: Buffer to store the decrypted text
 */
void caesar_decrypt(const char *text, int shift, char *result) {
    int i;
    // Normalize shift to 0-25 range
    shift = shift % 26;
    if (shift < 0) shift += 26;
    
    for (i = 0; text[i] != '\0'; i++) {
        result[i] = decrypt_char(text[i], shift);
    }
    result[i] = '\0';
}

/**
 * Displays usage information
 */
void print_usage(const char *program_name) {
    printf("\nCaesar Cipher - Encrypt or decrypt text\n");
    printf("Authors: Salah, Fares, Ziad, Zeiad\n\n");
    printf("Usage: %s <mode> <shift> <message>\n\n", program_name);
    printf("Arguments:\n");
    printf("  <mode>     : 'e' or 'encrypt' for encryption\n");
    printf("               'd' or 'decrypt' for decryption\n");
    printf("  <shift>    : Integer value for the shift (e.g., 3, 5, 13)\n");
    printf("  <message>  : The text to encrypt or decrypt (use quotes for spaces)\n\n");
    printf("Examples:\n");
    printf("  Encrypt: %s e 3 \"Hello World\"\n", program_name);
    printf("  Decrypt: %s d 3 \"Khoor Zruog\"\n", program_name);
    printf("  Using long form: %s encrypt 5 \"Secret Message\"\n\n", program_name);
}

/**
 * Main function
 */
int main(int argc, char *argv[]) {
    char result[MAX_TEXT_LENGTH];
    int shift;
    int is_encrypt;
    
    // Check if arguments are provided
    if (argc != 4) {
        print_usage(argv[0]);
        return 1;
    }
    
    // Determine mode (encrypt or decrypt)
    if (strcmp(argv[1], "e") == 0 || strcmp(argv[1], "encrypt") == 0) {
        is_encrypt = 1;
    } else if (strcmp(argv[1], "d") == 0 || strcmp(argv[1], "decrypt") == 0) {
        is_encrypt = 0;
    } else {
        printf("Error: Invalid mode '%s'\n", argv[1]);
        print_usage(argv[0]);
        return 1;
    }
    
    // Parse shift value
    shift = atoi(argv[2]);
    
    // Check message length
    if (strlen(argv[3]) >= MAX_TEXT_LENGTH) {
        printf("Error: Message too long (max %d characters)\n", MAX_TEXT_LENGTH - 1);
        return 1;
    }
    
    // Process the message
    printf("\n");
    printf("==================================================\n");
    
    if (is_encrypt) {
        caesar_encrypt(argv[3], shift, result);
        printf("Original Text:  %s\n", argv[3]);
        printf("Shift Value:    %d\n", shift);
        printf("Cipher Text:    %s\n", result);
    } else {
        caesar_decrypt(argv[3], shift, result);
        printf("Cipher Text:    %s\n", argv[3]);
        printf("Shift Value:    %d\n", shift);
        printf("Plain Text:     %s\n", result);
    }
    
    printf("==================================================\n\n");
    
    return 0;
}