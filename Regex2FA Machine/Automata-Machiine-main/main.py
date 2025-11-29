"""
Automata Theory Project
Main Entry Point

Regular Expression: aba + bb + c (aaa + aa + a)*
Alphabet: {a, b, c}

Author: Automata Theory Course Project
Date: November 2025
"""

import sys
import os

# Add modules directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.gui import run_gui


def main():
    """Main entry point"""
    print("=" * 80)
    print("Automata Theory - Regular Expression to Automata Converter")
    print("=" * 80)
    print()
    print("Assigned Regular Expression: aba + bb + c (aaa + aa + a)*")
    print("Alphabet: {a, b, c}")
    print()
    print("Features:")
    print("  1. Regular Expression Validation")
    print("  2. NFA Generation (Thompson's Construction)")
    print("  3. DFA Generation (Subset Construction)")
    print("  4. DFA Minimization (Table-Filling Algorithm)")
    print("  5. String Simulation with Step-by-Step Trace")
    print("  6. Visual Automata Diagrams")
    print()
    print("=" * 80)
    print()
    print("Starting GUI...")
    print()

    # Run GUI
    run_gui()


if __name__ == "__main__":
    main()