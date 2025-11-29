"""
Test Script for Automata Theory Project
Tests all modules without GUI
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.regex_validator import RegexValidator
from modules.thompson_nfa import ThompsonNFA
from modules.subset_dfa import SubsetConstruction
from modules.minimizer import DFAMinimizer
from modules.simulator import StringSimulator


def test_regex_validation():
    """Test regex validator"""
    print("=" * 80)
    print("TEST 1: Regular Expression Validation")
    print("=" * 80)

    regex = "d(de*d|ef*e|fd*f)df"
    alphabet = {'d', 'e', 'f'}

    validator = RegexValidator(alphabet)

    print(f"\nRegex: {regex}")
    print(f"Alphabet: {alphabet}")

    is_valid, message = validator.validate(regex)

    print(f"\nValidation Result: {'✓ VALID' if is_valid else '✗ INVALID'}")
    print(f"Message: {message}")

    if is_valid:
        preprocessed = validator.preprocess(regex)
        print(f"Preprocessed: {preprocessed}")

    print("\n✅ Validation test completed\n")

    return validator, preprocessed if is_valid else None


def test_nfa_generation(preprocessed):
    """Test NFA generation"""
    print("=" * 80)
    print("TEST 2: NFA Generation (Thompson's Construction)")
    print("=" * 80)

    thompson = ThompsonNFA(preprocessed)
    nfa = thompson.build()

    print(f"\nNFA generated with {len(nfa.states)} states")
    print(f"Start state: q{nfa.start.id}")
    print(f"Final state: q{nfa.final.id}")

    print("\nTransition Table:")
    table = nfa.get_transition_table()
    for state, transitions in sorted(table.items())[:10]:  # Show first 10
        print(f"{state}:")
        for symbol, next_states in sorted(transitions.items()):
            print(f"  {symbol} → {next_states}")

    print("\nε-Closures (first 5):")
    closures = nfa.get_epsilon_closures()
    for i, (state, closure) in enumerate(closures.items()):
        if i >= 5:
            break
        print(f"ε-closure({state}) = {closure}")

    print("\n✅ NFA generation test completed\n")

    return nfa


def test_dfa_generation(nfa):
    """Test DFA generation"""
    print("=" * 80)
    print("TEST 3: DFA Generation (Subset Construction)")
    print("=" * 80)

    alphabet = {'d', 'e', 'f'}
    subset = SubsetConstruction(nfa, alphabet)
    dfa = subset.build()

    print(f"\nDFA generated with {len(dfa.states)} states")
    print(f"Start state: q{dfa.start.id}")
    print(f"Final states: {[f'q{s.id}' for s in dfa.final_states]}")

    print("\nTransition Table:")
    table = dfa.get_transition_table()
    for state, data in sorted(table.items()):
        flags = data.get('_flags', [])
        composition = data.get('_composition', '')

        flag_str = f" [{', '.join(flags)}]" if flags else ""
        print(f"\n{state}{flag_str} = {composition}")

        for symbol in sorted(alphabet):
            if symbol in data:
                print(f"  {symbol} → {data[symbol]}")

    print("\n✅ DFA generation test completed\n")

    return dfa


def test_dfa_minimization(dfa):
    """Test DFA minimization"""
    print("=" * 80)
    print("TEST 4: DFA Minimization (Table-Filling Algorithm)")
    print("=" * 80)

    minimizer = DFAMinimizer(dfa)
    min_dfa = minimizer.minimize()

    print(f"\nMinimized DFA with {len(min_dfa.states)} states")
    print(f"Original DFA had {len(dfa.states)} states")
    print(f"Reduction: {len(dfa.states) - len(min_dfa.states)} states merged")

    print("\nMinimized Transition Table:")
    table = min_dfa.get_transition_table()
    alphabet = {'d', 'e', 'f'}

    for state, data in sorted(table.items()):
        flags = data.get('_flags', [])
        merged = data.get('_merged_from', '')

        flag_str = f" [{', '.join(flags)}]" if flags else ""
        merge_str = f" (merged from: {merged})" if merged else ""
        print(f"\n{state}{flag_str}{merge_str}")

        for symbol in sorted(alphabet):
            if symbol in data:
                print(f"  {symbol} → {data[symbol]}")

    print("\nDistinguishability Table (sample):")
    dist_table = minimizer.get_distinguishability_table()
    for i, (pair, mark) in enumerate(dist_table.items()):
        if i >= 10:  # Show first 10
            print("  ...")
            break
        print(f"  {pair}: {mark}")

    print("\n✅ DFA minimization test completed\n")

    return min_dfa


def test_string_simulation(min_dfa):
    """Test string simulation"""
    print("=" * 80)
    print("TEST 5: String Simulation")
    print("=" * 80)

    simulator = StringSimulator(min_dfa)

    test_strings = [
        ("ddddf", True),
        ("deedf", True),
        ("dffdf", True),
        ("def", False),
        ("ddd", False),
        ("ddedf", False)
    ]

    print("\nTesting strings:\n")

    for test_string, expected in test_strings:
        accepted, trace, error = simulator.simulate(test_string)

        status = "✓ ACCEPTED" if accepted else "✗ REJECTED"
        match = "✓" if (accepted == expected) else "✗ UNEXPECTED"

        print(f"String: '{test_string}' → {status} {match}")

        if error:
            print(f"  Error: {error}")

        # Show trace for first accepted string
        if accepted and test_string == "ddddf":
            print("\n  Detailed trace:")
            for entry in trace:
                if 'description' in entry:
                    print(f"    {entry['description']}")

    print("\n✅ String simulation test completed\n")


def main():
    """Run all tests"""
    print("\n")
    print("=" * 80)
    print("         AUTOMATA THEORY PROJECT - TEST SUITE         ")
    print("=" * 80)
    print()

    try:
        # Test 1: Validation
        validator, preprocessed = test_regex_validation()

        if not preprocessed:
            print("❌ Validation failed. Stopping tests.")
            return

        # Test 2: NFA
        nfa = test_nfa_generation(preprocessed)

        # Test 3: DFA
        dfa = test_dfa_generation(nfa)

        # Test 4: Minimization
        min_dfa = test_dfa_minimization(dfa)

        # Test 5: Simulation
        test_string_simulation(min_dfa)

        print("=" * 80)
        print("ALL TESTS COMPLETED SUCCESSFULLY! ✅")
        print("=" * 80)
        print()
        print("Next steps:")
        print("  1. Install Graphviz: https://graphviz.org/download/")
        print("  2. Install Python packages: pip install -r requirements.txt")
        print("  3. Run GUI: python main.py")
        print()

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

