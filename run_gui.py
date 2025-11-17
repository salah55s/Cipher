#!/usr/bin/env python3
"""
Cipher Tool Launcher
Quick launcher for the cipher GUI application.
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Launch the cipher GUI."""
    try:
        # Add src to path
        sys.path.insert(0, str(Path(__file__).parent / 'src'))
        
        from src.gui.cipher_gui import main as gui_main
        print("🔐 Launching Cipher Encryption Tool...")
        gui_main()
    except ImportError as e:
        print(f"❌ Error: Missing dependency - {e}")
        print("\n📦 Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✅ Installation complete! Please run the launcher again.")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
