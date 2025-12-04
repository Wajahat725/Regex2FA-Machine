def display_aba_minimized_dfa():
    """Display Minimized DFA Transition Table for the pattern 'aba'"""
    print("\nMinimized DFA Transition Table for 'aba'")
    print("=" * 60)
    print()
    # Transition table header
    print("State     a          b          c")
    print("-" * 40)
    # Transition table rows showing state transitions for each input symbol
    print("A         B          D          D")
    print("B         D          C          D")
    print("C*        D          D          D")  # C is final state (indicated by *)
    print("D         D          D          D")  # D is dead/absorbing state
    print()
    # State explanations
    print("Where:")
    print("A = {q0} (Initial State)")
    print("B = {q1}")
    print("C = {q2, q3} (Final State)")  # States q2 and q3 merged during minimization
    print("D = {q4} (Dead State)")  # Single dead state for all non-accepting paths
    print("=" * 60)

def display_bb_minimized_dfa():
    """Display Minimized DFA Transition Table for the pattern 'bb'"""
    print("\nMinimized DFA Transition Table for 'bb'")
    print("=" * 60)
    print()
    print("State     a          b          c")
    print("-" * 40)
    print("A         C          B          C")
    print("B         C          C*         C")  # B transitions to final state C on 'b'
    print("C         C          C          C")  # C is combined dead/final state
    print()
    print("Where:")
    print("A = {q0} (Initial State)")
    print("B = {q1}")
    print("C = {q2, q3} (Final + Dead States merged)")  # Optimization: merged similar states
    print("=" * 60)

def display_c_only_minimized_dfa():
    """Display Minimized DFA Transition Table for the pattern 'c' (single character)"""
    print("\nMinimized DFA Transition Table for 'c'")
    print("=" * 60)
    print()
    print("State     a          b          c")
    print("-" * 40)
    print("A         C          C          B*")  # On 'c', transition from A to final state B
    print("B*        C          C          C")   # B is final state, all inputs go to dead state
    print("C         C          C          C")   # C is absorbing dead state
    print()
    print("Where:")
    print("A = {q0} (Initial State)")
    print("B = {q1} (Final State)")
    print("C = {q2} (Dead State)")
    print("=" * 60)

def display_ca_minimized_dfa():
    """Display Minimized DFA Transition Table for the pattern 'ca'"""
    print("\nMinimized DFA Transition Table for 'ca'")
    print("=" * 60)
    print()
    print("State     a          b          c")
    print("-" * 40)
    print("A         C          C          B")   # On 'c', transition from A to B
    print("B         D*         C          C")   # On 'a', transition from B to final state D
    print("C         C          C          C")   # C is dead state
    print("D*        C          C          C")   # D is final state
    print()
    print("Where:")
    print("A = {q0} (Initial State)")
    print("B = {q1}")
    print("C = {q2} (Dead State)")
    print("D = {q3} (Final State)")
    print("=" * 60)

def display_caa_minimized_dfa():
    """Display Minimized DFA Transition Table for the pattern 'caa'"""
    print("\nMinimized DFA Transition Table for 'caa'")
    print("=" * 60)
    print()
    print("State     a          b          c")
    print("-" * 40)
    print("A         D          D          B")   # Sequence starts with 'c'
    print("B         C          D          D")   # Second character must be 'a'
    print("C         E*         D          D")   # Third character must be 'a' to reach final state
    print("D         D          D          D")   # Dead state for invalid transitions
    print("E*        D          D          D")   # Final state after recognizing "caa"
    print()
    print("Where:")
    print("A = {q0} (Initial State)")
    print("B = {q1}")
    print("C = {q2}")
    print("D = {q3} (Dead State)")
    print("E = {q4} (Final State)")
    print("=" * 60)

def display_caaa_minimized_dfa():
    """Display Minimized DFA Transition Table for the pattern 'caaa'"""
    print("\nMinimized DFA Transition Table for 'caaa'")
    print("=" * 60)
    print()
    print("State     a          b          c")
    print("-" * 40)
    print("A         D          D          B")   # Must start with 'c'
    print("B         C          D          D")   # First 'a' after 'c'
    print("C         E          D          D")   # Second 'a'
    print("D         D          D          D")   # Dead state
    print("E         F*         D          D")   # Third 'a' leads to final state
    print("F*        D          D          D")   # Final state after "caaa"
    print()
    print("Where:")
    print("A = {q0} (Initial State)")
    print("B = {q1}")
    print("C = {q2}")
    print("D = {q4} (Dead State)")
    print("E = {q3}")
    print("F = {q5} (Final State)")
    print("=" * 60)

def display_c_kleene_star_minimized_dfa():
    """Display Minimized DFA Transition Table for the pattern 'c(aaa+aa+a)*' (Kleene star pattern)"""
    print("\nMinimized DFA Transition Table for 'c(aaa+aa+a)*'")
    print("=" * 60)
    print()
    print("State     a          b          c")
    print("-" * 40)
    print("A         C          C          B*")  # Initial state, 'c' leads to final state B
    print("B*        B*         C          C")   # B is final and loops on 'a' (Kleene star)
    print("C         C          C          C")   # Dead state for invalid inputs
    print()
    print("Where:")
    print("A = {q0} (Initial State)")
    # Multiple states merged into one final state due to Kleene star pattern
    print("B = {q1, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18} (Final State)")
    print("C = {q2} (Dead State)")
    print("=" * 60)