import re

def test_string_belongs_to_regex(input_string):
    """Test if the input string belongs to the regular expression aba + bb + c(aaa+aa+a)*"""
    
    # Pattern for aba - matches exactly "aba"
    aba_pattern = r'^aba$'
    
    
    # Pattern for bb - matches exactly "bb" 
    bb_pattern = r'^bb$'
    
    # Pattern for c followed by any number of 'a's (0, 1, 2, or 3 in sequence, repeated)
    # ^c - starts with 'c'
    # (a{1,3})* - zero or more occurrences of 'a' repeated 1, 2, or 3 times
    # $ - end of string
    c_pattern = r'^c(a{1,3})*$'
    
    # Test all patterns in order of specificity
    if re.match(aba_pattern, input_string):
        return "aba"  # String matches 'aba' pattern
    elif re.match(bb_pattern, input_string):
        return "bb"   # String matches 'bb' pattern
    elif re.match(c_pattern, input_string):
        # Determine which specific c pattern the string belongs to
        if input_string == "c":
            return "c_only"      # Just 'c' with no 'a's
        elif input_string == "ca":
            return "ca"          # 'c' followed by one 'a'
        elif input_string == "caa":
            return "caa"         # 'c' followed by two 'a's
        elif input_string == "caaa":
            return "caaa"        # 'c' followed by three 'a's
        else:
            # For caaaa, caaaaa, etc. - strings that use the Kleene star repetition
            return "c_kleene_star"
    else:
        return None  # String doesn't match any pattern

def display_aba_nfa():
    """Display NFA for aba using Thompson Construction"""
    print("\nNFA diagram for 'aba': using Thompson Construction")  # Header
    print("=" * 55)  # Separator line
    print()  # Empty line for spacing
    
    # State q0: Initial state with epsilon transition to q1
    print("q0:")
    print("  ε  → {q1}")  # ε-transition to q1
    print()
    
    # State q1: Reads 'a' and goes to q2
    print("q1:")
    print("  a → {q2}")  # 'a' transition to q2
    print()
    
    # State q2: Epsilon transition to q3
    print("q2:")
    print("  ε → {q3}")  # ε-transition to q3
    print()
    
    # State q3: Reads 'b' and goes to q4
    print("q3:")
    print("  b → {q4}")  # 'b' transition to q4
    print()
    
    # State q4: Epsilon transition to q5
    print("q4:")
    print("  ε → {q5}")  # ε-transition to q5
    print()
    
    # State q5: Reads 'a' and goes to q6
    print("q5:")
    print("  a → {q6}")  # 'a' transition to q6
    print()
    
    # State q6: Epsilon transition to final state q7
    print("q6:")
    print("  ε  → {q7} # final state for aba")  # ε-transition to final state
    print("=" * 55)  # Footer separator

def display_aba_nfa_table():
    """Display NFA Transition Table for aba"""
    print("\nNFA Transition Table for 'aba'")  # Table header
    print("=" * 55)  # Separator
    print()  # Spacing
    
    # Column headers for the transition table
    print("State     a          b          c          ε")  # State and input symbols
    print("-" * 50)  # Table border
    
    # q0 transitions: only epsilon transition to q1
    print("q0       -          -          -          {q1}")  # ε → q1
    
    # q1 transitions: only 'a' transition to q2
    print("q1       {q2}       -          -          -")     # a → q2
    
    # q2 transitions: only epsilon transition to q3
    print("q2       -          -          -          {q3}")  # ε → q3
    
    # q3 transitions: only 'b' transition to q4
    print("q3       -          {q4}       -          -")     # b → q4
    
    # q4 transitions: only epsilon transition to q5
    print("q4       -          -          -          {q5}")  # ε → q5
    
    # q5 transitions: only 'a' transition to q6
    print("q5       {q6}       -          -          -")     # a → q6
    
    # q6 transitions: only epsilon transition to q7
    print("q6       -          -          -          {q7}")  # ε → q7
    
    # q7 transitions: no transitions (final state)
    print("q7       -          -          -          -")     # No transitions
    print()  # Spacing
    
    # State information footer
    print("Where: q0 initial state, q7 final state")  # Initial and final states
    print("=" * 55)  # Footer separator

def display_bb_nfa():
    """Display NFA for bb using Thompson Construction"""
    print("\nNFA diagram for 'bb': using Thompson Construction")  # Header
    print("=" * 55)  # Separator
    print()  # Spacing
    
    # State q0: Initial state with epsilon transition to q1
    print("q0:")
    print("  ε → {q1}")  # ε-transition to q1
    print()
    
    # State q1: Reads 'b' and goes to q2
    print("q1:")
    print("  b → {q2}")  # 'b' transition to q2
    print()
    
    # State q2: Epsilon transition to q3
    print("q2:")
    print("  ε → {q3}")  # ε-transition to q3
    print()
    
    # State q3: Reads 'b' and goes to q4
    print("q3:")
    print("  b → {q4}")  # 'b' transition to q4
    print()
    
    # State q4: Epsilon transition to final state q5
    print("q4:")
    print("  ε → {q5} # final state for bb")  # ε-transition to final state
    print("=" * 55)  # Footer separator

def display_bb_nfa_table():
    """Display NFA Transition Table for bb"""
    print("\nNFA Transition Table for 'bb'")  # Table header
    print("=" * 55)  # Separator
    print()  # Spacing
    
    # Column headers
    print("State     a          b          c          ε")  # State and input symbols
    print("-" * 50)  # Table border
    
    # q0 transitions: only epsilon transition to q1
    print("q0       -          -          -          {q1}")  # ε → q1
    
    # q1 transitions: only 'b' transition to q2
    print("q1       -          {q2}       -          -")     # b → q2
    
    # q2 transitions: only epsilon transition to q3
    print("q2       -          -          -          {q3}")  # ε → q3
    
    # q3 transitions: only 'b' transition to q4
    print("q3       -          {q4}       -          -")     # b → q4
    
    # q4 transitions: only epsilon transition to q5
    print("q4       -          -          -          {q5}")  # ε → q5
    
    # q5 transitions: no transitions (final state)
    print("q5       -          -          -          -")     # No transitions
    print()  # Spacing
    
    # State information
    print("Where: q0 initial state, q5 final state")  # Initial and final states
    print("=" * 55)  # Footer separator

def display_c_only_nfa():
    """Display NFA for c only using Thompson Construction"""
    print("\nNFA diagram for 'c': using Thompson Construction")  # Header
    print("=" * 55)  # Separator
    print()  # Spacing
    
    # State q0: Initial state with epsilon transition to q1
    print("q0:")
    print("  ε  → {q1}")  # ε-transition to q1
    print()
    
    # State q1: Reads 'c' and goes to q2
    print("q1:")
    print("  c → {q2}")  # 'c' transition to q2
    print()
    
    # State q2: Epsilon transition to final state q3
    print("q2:")
    print("  ε → {q3} # final state for c")  # ε-transition to final state
    print("=" * 55)  # Footer separator

def display_c_only_nfa_table():
    """Display NFA Transition Table for c only"""
    print("\nNFA Transition Table for 'c'")  # Table header
    print("=" * 60)  # Separator
    print()  # Spacing
    
    # Column headers
    print("State     a          b          c          ε")  # State and input symbols
    print("-" * 50)  # Table border
    
    # q0 transitions: only epsilon transition to q1
    print("q0       -          -          -          {q1}")  # ε → q1
    
    # q1 transitions: only 'c' transition to q2
    print("q1       -          -          {q2}       -")     # c → q2
    
    # q2 transitions: only epsilon transition to q3
    print("q2       -          -          -          {q3}")  # ε → q3
    
    # q3 transitions: no transitions (final state)
    print("q3       -          -          -          -")     # No transitions
    print()  # Spacing
    
    # State information
    print("Where: q0 initial state, q3 final state")  # Initial and final states
    print("=" * 55)  # Footer separator

def display_ca_nfa():
    """Display NFA for ca using Thompson Construction"""
    print("\nNFA diagram for 'ca': using Thompson Construction")  # Header
    print("=" * 55)  # Separator
    print()  # Spacing
    
    # State q0: Initial state with epsilon transition to q1
    print("q0:")
    print("  ε  → {q1}")  # ε-transition to q1
    print()
    
    # State q1: Reads 'c' and goes to q2
    print("q1:")
    print("  c → {q2}")  # 'c' transition to q2
    print()
    
    # State q2: Epsilon transition to q3
    print("q2:")
    print("  ε → {q3}")  # ε-transition to q3
    print()
    
    # State q3: Reads 'a' and goes to q4
    print("q3:")
    print("  a → {q4}")  # 'a' transition to q4
    print()
    
    # State q4: Epsilon transition to final state q5
    print("q4:")
    print("  ε → {q5} # final state for ca")  # ε-transition to final state
    print("=" * 55)  # Footer separator

def display_ca_nfa_table():
    """Display NFA Transition Table for ca"""
    print("\nNFA Transition Table for 'ca'")  # Table header
    print("=" * 55)  # Separator
    print()  # Spacing
    
    # Column headers
    print("State     a          b          c          ε")  # State and input symbols
    print("-" * 50)  # Table border
    
    # q0 transitions: only epsilon transition to q1
    print("q0       -          -          -          {q1}")  # ε → q1
    
    # q1 transitions: only 'c' transition to q2
    print("q1       -          -          {q2}       -")     # c → q2
    
    # q2 transitions: only epsilon transition to q3
    print("q2       -          -          -          {q3}")  # ε → q3
    
    # q3 transitions: only 'a' transition to q4
    print("q3       {q4}       -          -          -")     # a → q4
    
    # q4 transitions: only epsilon transition to q5
    print("q4       -          -          -          {q5}")  # ε → q5
    
    # q5 transitions: no transitions (final state)
    print("q5       -          -          -          -")     # No transitions
    print()  # Spacing
    
    # State information
    print("Where: q0 initial state, q5 final state")  # Initial and final states
    print("=" * 55)  # Footer separator

def display_caa_nfa():
    """Display NFA for caa using Thompson Construction"""
    print("\nNFA diagram for 'caa': using Thompson Construction")  # Header
    print("=" * 55)  # Separator
    print()  # Spacing
    
    # State q0: Initial state with epsilon transition to q1
    print("q0:")
    print("  ε  → {q1}")  # ε-transition to q1
    print()
    
    # State q1: Reads 'c' and goes to q2
    print("q1:")
    print("  c → {q2}")  # 'c' transition to q2
    print()
    
    # State q2: Epsilon transition to q3
    print("q2:")
    print("  ε → {q3}")  # ε-transition to q3
    print()
    
    # State q3: Reads 'a' and goes to q4
    print("q3:")
    print("  a → {q4}")  # 'a' transition to q4
    print()
    
    # State q4: Epsilon transition to q5
    print("q4:")
    print("  ε → {q5}")  # ε-transition to q5
    print()
    
    # State q5: Reads 'a' and goes to q6
    print("q5:")
    print("  a → {q6}")  # 'a' transition to q6
    print()
    
    # State q6: Epsilon transition to final state q7
    print("q6:")
    print("  ε → {q7} # final state for caa")  # ε-transition to final state
    print("=" * 55)  # Footer separator

def display_caa_nfa_table():
    """Display NFA Transition Table for caa"""
    print("\nNFA Transition Table for 'caa'")  # Table header
    print("=" * 55)  # Separator
    print()  # Spacing
    
    # Column headers
    print("State     a          b          c          ε")  # State and input symbols
    print("-" * 50)  # Table border
    
    # q0 transitions: only epsilon transition to q1
    print("q0       -          -          -          {q1}")  # ε → q1
    
    # q1 transitions: only 'c' transition to q2
    print("q1       -          -          {q2}       -")     # c → q2
    
    # q2 transitions: only epsilon transition to q3
    print("q2       -          -          -          {q3}")  # ε → q3
    
    # q3 transitions: only 'a' transition to q4
    print("q3       {q4}       -          -          -")     # a → q4
    
    # q4 transitions: only epsilon transition to q5
    print("q4       -          -          -          {q5}")  # ε → q5
    
    # q5 transitions: only 'a' transition to q6
    print("q5       {q6}       -          -          -")     # a → q6
    
    # q6 transitions: only epsilon transition to q7
    print("q6       -          -          -          {q7}")  # ε → q7
    
    # q7 transitions: no transitions (final state)
    print("q7       -          -          -          -")     # No transitions
    print()  # Spacing
    
    # State information
    print("Where: q0 initial state, q7 final state")  # Initial and final states
    print("=" * 55)  # Footer separator

def display_caaa_nfa():
    """Display NFA for caaa using Thompson Construction"""
    print("\nNFA diagram for 'caaa': using Thompson Construction")  # Header
    print("=" * 55)  # Separator
    print()  # Spacing
    
    # State q0: Initial state with epsilon transition to q1
    print("q0:")
    print("  ε  → {q1}")  # ε-transition to q1
    print()
    
    # State q1: Reads 'c' and goes to q2
    print("q1:")
    print("  c → {q2}")  # 'c' transition to q2
    print()
    
    # State q2: Epsilon transition to q3
    print("q2:")
    print("  ε → {q3}")  # ε-transition to q3
    print()
    
    # State q3: Reads 'a' and goes to q4
    print("q3:")
    print("  a → {q4}")  # 'a' transition to q4
    print()
    
    # State q4: Epsilon transition to q5
    print("q4:")
    print("  ε → {q5}")  # ε-transition to q5
    print()
    
    # State q5: Reads 'a' and goes to q6
    print("q5:")
    print("  a → {q6}")  # 'a' transition to q6
    print()
    
    # State q6: Epsilon transition to q7
    print("q6:")
    print("  ε → {q7}")  # ε-transition to q7
    print()
    
    # State q7: Reads 'a' and goes to q8
    print("q7:")
    print("  a → {q8}")  # 'a' transition to q8
    print()
    
    # State q8: Epsilon transition to final state q9
    print("q8:")
    print("  ε → {q9} # final state for caaa")  # ε-transition to final state
    print("=" * 55)  # Footer separator

def display_caaa_nfa_table():
    """Display NFA Transition Table for caaa"""
    print("\nNFA Transition Table for 'caaa'")  # Table header
    print("=" * 55)  # Separator
    print()  # Spacing
    
    # Column headers
    print("State     a          b          c          ε")  # State and input symbols
    print("-" * 50)  # Table border
    
    # q0 transitions: only epsilon transition to q1
    print("q0       -          -          -          {q1}")  # ε → q1
    
    # q1 transitions: only 'c' transition to q2
    print("q1       -          -          {q2}       -")     # c → q2
    
    # q2 transitions: only epsilon transition to q3
    print("q2       -          -          -          {q3}")  # ε → q3
    
    # q3 transitions: only 'a' transition to q4
    print("q3       {q4}       -          -          -")     # a → q4
    
    # q4 transitions: only epsilon transition to q5
    print("q4       -          -          -          {q5}")  # ε → q5
    
    # q5 transitions: only 'a' transition to q6
    print("q5       {q6}       -          -          -")     # a → q6
    
    # q6 transitions: only epsilon transition to q7
    print("q6       -          -          -          {q7}")  # ε → q7
    
    # q7 transitions: only 'a' transition to q8
    print("q7       {q8}       -          -          -")     # a → q8
    
    # q8 transitions: only epsilon transition to q9
    print("q8       -          -          -          {q9}")  # ε → q9
    
    # q9 transitions: no transitions (final state)
    print("q9       -          -          -          -")     # No transitions
    print()  # Spacing
    
    # State information
    print("Where: q0 initial state, q9 final state")  # Initial and final states
    print("=" * 55)  # Footer separator

def display_c_kleene_star_nfa():
    """Display NFA for c(aaa+aa+a)* - the full Kleene star implementation"""
    print("\nNFA diagram for 'c(aaa+aa+a)*': using Thompson Construction")  # Header
    print("=" * 55)  # Separator
    print()  # Spacing
    
    # State q0: Initial state with epsilon transition to q1
    print("q0:")
    print("  ε  → {q1}")  # ε-transition to q1
    print()
    
    # State q1: Reads 'c' and goes to q2
    print("q1:")
    print("  c → {q2}")  # 'c' transition to q2
    print()
    
    # State q2: Epsilon transition to q3 (first final state for 'c')
    print("q2:")
    print("  ε → {q3} # final state for c")  # ε-transition to q3 (accepts just 'c')
    print()
    
    # State q3: Epsilon transition to three alternatives (aaa, aa, or a)
    print("q3:")
    print("  ε → {q4,q8,q12} # ε-transition to three alternatives")  # Branch to three paths
    print()
    
    # First alternative: 'aaa' path
    print("q4:")
    print("  a → {q5} # first a of 'aaa'")  # First 'a' of 'aaa'
    print()
    print("q5:")
    print("  ε → {q6}")  # ε-transition between 'a's
    print()
    print("q6:")
    print("  a → {q7} # second a of 'aaa'")  # Second 'a' of 'aaa'
    print()
    print("q7:")
    print("  ε → {q16}")  # ε-transition to merge point
    print()
    
    # Second alternative: 'aa' path
    print("q8:")
    print("  a → {q9} # first a of 'aa'")  # First 'a' of 'aa'
    print()
    print("q9:")
    print("  ε → {q10}")  # ε-transition between 'a's
    print()
    print("q10:")
    print("  a → {q11} # second a of 'aa'")  # Second 'a' of 'aa'
    print()
    print("q11:")
    print("  ε → {q16}")  # ε-transition to merge point
    print()
    
    # Third alternative: single 'a' path
    print("q12:")
    print("  a → {q13} # single 'a'")  # Single 'a' transition
    print()
    print("q13:")
    print("  ε → {q14}")  # ε-transition chain
    print()
    print("q14:")
    print("  ε → {q15}")  # ε-transition chain
    print()
    print("q15:")
    print("  ε → {q16}")  # ε-transition to merge point
    print()
    
    # Merge point: loop back for repetition or go to final state
    print("q16:")
    print("  ε → {q3,q17} # loop back to q3 for repetition or go to final state")  # Kleene star loop
    print()
    
    # Final state for the complete pattern
    print("q17:")
    print("  ε → {q18} # final state for c(aaa+aa+a)*")  # Final state
    print("=" * 55)  # Footer separator

def display_c_kleene_star_nfa_table():
    """Display NFA Transition Table for c(aaa+aa+a)*"""
    print("\nNFA Transition Table for 'c(aaa+aa+a)*'")  # Table header
    print("=" * 55)  # Separator
    print()  # Spacing
    
    # Column headers
    print("State     a          b          c          ε")  # State and input symbols
    print("-" * 50)  # Table border
    
    # q0 transitions: only epsilon transition to q1
    print("q0       -          -          -          {q1}")  # ε → q1
    
    # q1 transitions: only 'c' transition to q2
    print("q1       -          -          {q2}       -")     # c → q2
    
    # q2 transitions: only epsilon transition to q3
    print("q2       -          -          -          {q3}")  # ε → q3
    
    # q3 transitions: only epsilon transitions to three alternative paths
    print("q3       -          -          -          {q4,q8,q12}")  # ε → three branches
    
    # 'aaa' path transitions
    print("q4       {q5}       -          -          -")     # a → q5 (first a of aaa)
    print("q5       -          -          -          {q6}")  # ε → q6
    print("q6       {q7}       -          -          -")     # a → q7 (second a of aaa)
    print("q7       -          -          -          {q16}") # ε → q16
    
    # 'aa' path transitions
    print("q8       {q9}       -          -          -")     # a → q9 (first a of aa)
    print("q9       -          -          -          {q10}") # ε → q10
    print("q10      {q11}      -          -          -")     # a → q11 (second a of aa)
    print("q11      -          -          -          {q16}") # ε → q16
    
    # Single 'a' path transitions
    print("q12      {q13}      -          -          -")     # a → q13 (single a)
    print("q13      -          -          -          {q14}") # ε → q14
    print("q14      -          -          -          {q15}") # ε → q15
    print("q15      -          -          -          {q16}") # ε → q16
    
    # Merge point transitions: loop back or go to final state
    print("q16      -          -          -          {q3,q17}")  # ε → loop back or final
    
    # Final state transition
    print("q17      -          -          -          {q18}") # ε → q18 (final)
    
    # Final state: no transitions
    print("q18      -          -          -          -")     # No transitions
    print()  # Spacing
    
    # State information (note: both q3 and q18 are final states)
    print("Where: q0 initial state, q3,q18 final states")  # Multiple final states
    print("=" * 55)  # Footer separator