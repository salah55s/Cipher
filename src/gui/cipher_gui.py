"""
Cipher GUI Application
Authors: @salah55s, @Fares-Elsaghir, @ZiadMahmoud855, @zeiad1655, @omar97531, @KhaledGamal1
Description: Interactive GUI for Caesar and AES cipher with visual step display.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Optional
import sys
from pathlib import Path

# Add ciphers to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ciphers.caesar_cipher_class import CaesarCipher
from ciphers.aes_cipher_class import AESCipher
from ciphers.cipher_base import CipherBase


class CipherGUI:
    """Main GUI application for cipher encryption/decryption."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Cipher Encryption Tool")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Initialize ciphers
        self.caesar = CaesarCipher()
        self.aes = AESCipher(key_size=256)
        self.current_cipher: Optional[CipherBase] = None
        
        # Configure style
        self.setup_styles()
        
        # Create UI components
        self.create_header()
        self.create_cipher_selection()
        self.create_input_section()
        self.create_key_section()
        self.create_mode_selection()
        self.create_action_buttons()
        self.create_steps_display()
        self.create_output_section()
        
        # Set default cipher
        self.cipher_var.set("caesar")
        self.on_cipher_change()
    
    def setup_styles(self):
        """Configure ttk styles for the application."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Header.TLabel', 
                       font=('Arial', 18, 'bold'),
                       foreground='#2c3e50',
                       padding=10)
        
        style.configure('Section.TLabel',
                       font=('Arial', 11, 'bold'),
                       foreground='#34495e',
                       padding=5)
        
        style.configure('Action.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=10)
        
        style.configure('Step.TFrame',
                       background='#ecf0f1',
                       relief='solid',
                       borderwidth=1)
    
    def create_header(self):
        """Create the application header."""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=10, pady=10)
        
        title = ttk.Label(header_frame,
                         text="🔐 Cipher Encryption Tool",
                         style='Header.TLabel')
        title.pack()
        
        subtitle = ttk.Label(header_frame,
                            text="Caesar & AES Encryption with Visual Steps",
                            font=('Arial', 10),
                            foreground='#7f8c8d')
        subtitle.pack()
    
    def create_cipher_selection(self):
        """Create cipher type selection radio buttons."""
        frame = ttk.LabelFrame(self.root, text="Select Cipher Algorithm", padding=10)
        frame.pack(fill='x', padx=10, pady=5)
        
        self.cipher_var = tk.StringVar(value="caesar")
        
        caesar_radio = ttk.Radiobutton(frame,
                                       text="Caesar Cipher (Classical)",
                                       variable=self.cipher_var,
                                       value="caesar",
                                       command=self.on_cipher_change)
        caesar_radio.pack(side='left', padx=20)
        
        aes_radio = ttk.Radiobutton(frame,
                                    text="AES-256 (Advanced Encryption Standard)",
                                    variable=self.cipher_var,
                                    value="aes",
                                    command=self.on_cipher_change)
        aes_radio.pack(side='left', padx=20)
    
    def create_input_section(self):
        """Create input text area."""
        frame = ttk.LabelFrame(self.root, text="Input Text", padding=10)
        frame.pack(fill='both', padx=10, pady=5, expand=False)
        
        self.input_text = scrolledtext.ScrolledText(frame,
                                                     height=4,
                                                     font=('Courier', 10),
                                                     wrap='word')
        self.input_text.pack(fill='both', expand=True)
        self.input_text.insert('1.0', 'Enter your text here...')
        self.input_text.bind('<FocusIn>', self.clear_placeholder)
    
    def create_key_section(self):
        """Create key/password input section."""
        frame = ttk.LabelFrame(self.root, text="Encryption Key", padding=10)
        frame.pack(fill='x', padx=10, pady=5)
        
        # Key label and entry
        key_frame = ttk.Frame(frame)
        key_frame.pack(fill='x')
        
        self.key_label = ttk.Label(key_frame, text="Shift Value:", width=15)
        self.key_label.pack(side='left', padx=5)
        
        self.key_entry = ttk.Entry(key_frame, font=('Arial', 10))
        self.key_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.key_entry.insert(0, '3')
        
        # Key hint
        self.key_hint = ttk.Label(frame,
                                  text="Enter a number (0-25) for shift value",
                                  font=('Arial', 9),
                                  foreground='#7f8c8d')
        self.key_hint.pack(pady=2)
    
    def create_mode_selection(self):
        """Create encrypt/decrypt mode selection."""
        frame = ttk.LabelFrame(self.root, text="Operation Mode", padding=10)
        frame.pack(fill='x', padx=10, pady=5)
        
        self.mode_var = tk.StringVar(value="encrypt")
        
        encrypt_radio = ttk.Radiobutton(frame,
                                       text="🔒 Encrypt",
                                       variable=self.mode_var,
                                       value="encrypt")
        encrypt_radio.pack(side='left', padx=30)
        
        decrypt_radio = ttk.Radiobutton(frame,
                                       text="🔓 Decrypt",
                                       variable=self.mode_var,
                                       value="decrypt")
        decrypt_radio.pack(side='left', padx=30)
    
    def create_action_buttons(self):
        """Create action buttons."""
        frame = ttk.Frame(self.root)
        frame.pack(fill='x', padx=10, pady=10)
        
        process_btn = ttk.Button(frame,
                                text="🚀 Process",
                                style='Action.TButton',
                                command=self.process_cipher)
        process_btn.pack(side='left', padx=5)
        
        clear_btn = ttk.Button(frame,
                              text="🗑️ Clear All",
                              command=self.clear_all)
        clear_btn.pack(side='left', padx=5)
    
    def create_steps_display(self):
        """Create visual steps display area."""
        frame = ttk.LabelFrame(self.root, text="🔍 Process Steps (Dynamic Visualization)", padding=10)
        frame.pack(fill='both', padx=10, pady=5, expand=True)
        
        # Create canvas with scrollbar
        canvas_frame = ttk.Frame(frame)
        canvas_frame.pack(fill='both', expand=True)
        
        self.steps_canvas = tk.Canvas(canvas_frame, bg='white', height=200)
        scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=self.steps_canvas.yview)
        
        self.steps_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        self.steps_canvas.pack(side='left', fill='both', expand=True)
        
        # Frame inside canvas for steps
        self.steps_frame = ttk.Frame(self.steps_canvas)
        self.canvas_window = self.steps_canvas.create_window((0, 0), window=self.steps_frame, anchor='nw')
        
        self.steps_frame.bind('<Configure>', self.on_steps_configure)
        self.steps_canvas.bind('<Configure>', self.on_canvas_configure)
    
    def create_output_section(self):
        """Create output text area."""
        frame = ttk.LabelFrame(self.root, text="Output Result", padding=10)
        frame.pack(fill='both', padx=10, pady=5, expand=False)
        
        self.output_text = scrolledtext.ScrolledText(frame,
                                                      height=4,
                                                      font=('Courier', 10),
                                                      wrap='word',
                                                      state='disabled')
        self.output_text.pack(fill='both', expand=True)
        
        # Copy button
        copy_btn = ttk.Button(frame, text="📋 Copy to Clipboard", command=self.copy_output)
        copy_btn.pack(pady=5)
    
    def on_cipher_change(self):
        """Handle cipher type change."""
        cipher_type = self.cipher_var.get()
        
        if cipher_type == "caesar":
            self.current_cipher = self.caesar
            self.key_label.config(text="Shift Value:")
            self.key_entry.delete(0, 'end')
            self.key_entry.insert(0, '3')
            self.key_hint.config(text="Enter a number (0-25) for shift value")
        else:  # aes
            self.current_cipher = self.aes
            self.key_label.config(text="Password:")
            self.key_entry.delete(0, 'end')
            self.key_entry.insert(0, 'SecurePassword123')
            self.key_hint.config(text="Enter a strong password for encryption/decryption")
    
    def clear_placeholder(self, event):
        """Clear placeholder text on focus."""
        if self.input_text.get('1.0', 'end-1c') == 'Enter your text here...':
            self.input_text.delete('1.0', 'end')
    
    def clear_all(self):
        """Clear all input and output fields."""
        self.input_text.delete('1.0', 'end')
        self.input_text.insert('1.0', 'Enter your text here...')
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', 'end')
        self.output_text.config(state='disabled')
        self.clear_steps()
    
    def clear_steps(self):
        """Clear all step visualizations."""
        for widget in self.steps_frame.winfo_children():
            widget.destroy()
    
    def display_steps(self, steps: list):
        """Display visualization steps dynamically."""
        self.clear_steps()
        
        for step in steps:
            step_frame = ttk.Frame(self.steps_frame, style='Step.TFrame')
            step_frame.pack(fill='x', padx=5, pady=3)
            
            # Step header
            header = ttk.Label(step_frame,
                             text=f"Step {step['step_number']}: {step['title']}",
                             font=('Arial', 10, 'bold'),
                             foreground='#2980b9')
            header.pack(anchor='w', padx=10, pady=(5, 0))
            
            # Description
            desc = ttk.Label(step_frame,
                           text=step['description'],
                           font=('Arial', 9),
                           foreground='#34495e')
            desc.pack(anchor='w', padx=20, pady=2)
            
            # Details
            details = ttk.Label(step_frame,
                              text=step['details'],
                              font=('Courier', 8),
                              foreground='#7f8c8d')
            details.pack(anchor='w', padx=20, pady=(0, 5))
        
        # Update scroll region
        self.steps_frame.update_idletasks()
        self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox('all'))
    
    def on_steps_configure(self, event):
        """Update scroll region when steps frame changes."""
        self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox('all'))
    
    def on_canvas_configure(self, event):
        """Update canvas window width when canvas is resized."""
        self.steps_canvas.itemconfig(self.canvas_window, width=event.width)
    
    def process_cipher(self):
        """Process encryption or decryption."""
        # Get input
        input_text = self.input_text.get('1.0', 'end-1c').strip()
        if not input_text or input_text == 'Enter your text here...':
            messagebox.showwarning("Input Required", "Please enter text to process!")
            return
        
        # Get key
        key_str = self.key_entry.get().strip()
        if not key_str:
            messagebox.showwarning("Key Required", "Please enter an encryption key!")
            return
        
        # Validate and convert key for Caesar cipher
        if self.cipher_var.get() == "caesar":
            try:
                key = int(key_str)
            except ValueError:
                messagebox.showerror("Invalid Key", "Caesar cipher requires a numeric shift value!")
                return
        else:
            key = key_str
        
        # Process based on mode
        mode = self.mode_var.get()
        
        try:
            if mode == "encrypt":
                result, steps = self.current_cipher.encrypt(input_text, key)
            else:
                result, steps = self.current_cipher.decrypt(input_text, key)
            
            # Display steps
            self.display_steps(steps)
            
            # Display output
            self.output_text.config(state='normal')
            self.output_text.delete('1.0', 'end')
            self.output_text.insert('1.0', result)
            self.output_text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def copy_output(self):
        """Copy output to clipboard."""
        output = self.output_text.get('1.0', 'end-1c')
        if output:
            self.root.clipboard_clear()
            self.root.clipboard_append(output)
            messagebox.showinfo("Copied", "Output copied to clipboard!")
        else:
            messagebox.showwarning("No Output", "Nothing to copy!")


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = CipherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
