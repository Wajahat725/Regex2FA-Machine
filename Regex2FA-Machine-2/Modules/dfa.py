# dfa.py - Updated without diagram output
class DFASimulator:
    def __init__(self):
        # DFA tables for all regular expression patterns
        # Each pattern has: initial state, final states, dead states, and transition table
        self.dfa_tables = {
            "aba": {  # DFA for pattern "aba"
                "initial": "q0",      # Starting state
                "final": {"q3"},      # Accepting state (string accepted if ends here)
                "dead_states": {"q4"}, # States that lead to rejection
                "transitions": {      # State transition mapping
                    "q0": {"a": "q1", "b": "q4", "c": "q4"},  # From q0: a→q1, b/c→dead
                    "q1": {"a": "q4", "b": "q2", "c": "q4"},  # From q1: b→q2, a/c→dead
                    "q2": {"a": "q3", "b": "q4", "c": "q4"},  # From q2: a→q3 (final), b/c→dead
                    "q3": {"a": "q4", "b": "q4", "c": "q4"},  # From q3 (final): all inputs→dead
                    "q4": {"a": "q4", "b": "q4", "c": "q4"}   # Dead state: all inputs loop to dead
                }
            },
            "bb": {  # DFA for pattern "bb"
                "initial": "q0",
                "final": {"q2"},
                "dead_states": {"q3"},
                "transitions": {
                    "q0": {"a": "q3", "b": "q1", "c": "q3"},  # From q0: b→q1, a/c→dead
                    "q1": {"a": "q3", "b": "q2", "c": "q3"},  # From q1: b→q2 (final), a/c→dead
                    "q2": {"a": "q3", "b": "q3", "c": "q3"},  # From q2 (final): all→dead
                    "q3": {"a": "q3", "b": "q3", "c": "q3"}   # Dead state: all inputs loop
                }
            },
            "c_only": {  # DFA for pattern "c" (just the letter c)
                "initial": "q0",
                "final": {"q1"},
                "dead_states": {"q2"},
                "transitions": {
                    "q0": {"a": "q2", "b": "q2", "c": "q1"},  # From q0: c→q1 (final), a/b→dead
                    "q1": {"a": "q2", "b": "q2", "c": "q2"},  # From q1 (final): all→dead
                    "q2": {"a": "q2", "b": "q2", "c": "q2"}   # Dead state: all inputs loop
                }
            },
            "ca": {  # DFA for pattern "ca"
                "initial": "q0",
                "final": {"q3"},
                "dead_states": {"q2"},
                "transitions": {
                    "q0": {"a": "q2", "b": "q2", "c": "q1"},  # From q0: c→q1, a/b→dead
                    "q1": {"a": "q3", "b": "q2", "c": "q2"},  # From q1: a→q3 (final), b/c→dead
                    "q2": {"a": "q2", "b": "q2", "c": "q2"},  # Dead state: all inputs loop
                    "q3": {"a": "q2", "b": "q2", "c": "q2"}   # From q3 (final): all→dead
                }
            },
            "caa": {  # DFA for pattern "caa"
                "initial": "q0",
                "final": {"q4"},
                "dead_states": {"q3"},
                "transitions": {
                    "q0": {"a": "q3", "b": "q3", "c": "q1"},  # From q0: c→q1, a/b→dead
                    "q1": {"a": "q2", "b": "q3", "c": "q3"},  # From q1: a→q2, b/c→dead
                    "q2": {"a": "q4", "b": "q3", "c": "q3"},  # From q2: a→q4 (final), b/c→dead
                    "q3": {"a": "q3", "b": "q3", "c": "q3"},  # Dead state: all inputs loop
                    "q4": {"a": "q3", "b": "q3", "c": "q3"}   # From q4 (final): all→dead
                }
            },
            "caaa": {  # DFA for pattern "caaa"
                "initial": "q0",
                "final": {"q5"},
                "dead_states": {"q4"},
                "transitions": {
                    "q0": {"a": "q4", "b": "q4", "c": "q1"},  # From q0: c→q1, a/b→dead
                    "q1": {"a": "q2", "b": "q4", "c": "q4"},  # From q1: a→q2, b/c→dead
                    "q2": {"a": "q3", "b": "q4", "c": "q4"},  # From q2: a→q3, b/c→dead
                    "q3": {"a": "q5", "b": "q4", "c": "q4"},  # From q3: a→q5 (final), b/c→dead
                    "q4": {"a": "q4", "b": "q4", "c": "q4"},  # Dead state: all inputs loop
                    "q5": {"a": "q4", "b": "q4", "c": "q4"}   # From q5 (final): all→dead
                }
            },
            "c_kleene_star": {  # DFA for pattern "c(aaa+aa+a)*" (Kleene star)
                "initial": "q0",
                "final": {"q1"},  # q1 is final because it accepts "c" and can loop on 'a'
                "dead_states": {"q2"},
                "transitions": {
                    "q0": {"a": "q2", "b": "q2", "c": "q1"},  # From q0: c→q1 (final), a/b→dead
                    "q1": {"a": "q1", "b": "q2", "c": "q2"},  # From q1: a→q1 (loop for Kleene star), b/c→dead
                    "q2": {"a": "q2", "b": "q2", "c": "q2"}   # Dead state: all inputs loop
                }
            }
        }
    
    def get_dfa_data(self, pattern):
        """Get DFA data for image generation"""
        if pattern in self.dfa_tables:
            return self.dfa_tables[pattern]
        return None
    
    def simulate_dfa(self, pattern, input_string):
        """Simulate DFA step by step for given input string"""
        # Check if the requested pattern exists in our DFA tables
        if pattern not in self.dfa_tables:
            return ["Error: Pattern not found"]  # Return error if pattern not found
        
        # Get the DFA configuration for the specified pattern
        dfa = self.dfa_tables[pattern]
        current_state = dfa["initial"]  # Start from initial state
        steps = []  # List to store simulation steps for display
        
        # Add simulation header information
        steps.append(f"Starting simulation for '{input_string}' on {pattern} DFA")
        steps.append(f"Initial state: {current_state}")
        steps.append(f"Final states: {dfa['final']}")
        steps.append(f"Dead states: {dfa['dead_states']}")
        steps.append("")  # Empty line for spacing
        
        # Process each character in the input string
        for i, char in enumerate(input_string):
            # Check if current state has a transition for this character
            if char not in dfa["transitions"][current_state]:
                steps.append(f"❌ Invalid character '{char}' at position {i+1}")
                steps.append(f"❌ String REJECTED - Invalid input character")
                return steps  # Stop simulation on invalid character
            
            # Get the next state based on current state and input character
            next_state = dfa["transitions"][current_state][char]
            
            # Check if we're entering a dead state
            if next_state in dfa["dead_states"]:
                steps.append(f"Step {i+1}: {current_state} --{char}--> {next_state} ⚠️ (Entered Dead State)")
            else:
                steps.append(f"Step {i+1}: {current_state} --{char}--> {next_state}")
            
            # Move to the next state
            current_state = next_state
            
            # If we're in a dead state, stop processing (no point continuing)
            if current_state in dfa["dead_states"]:
                steps.append("")  # Empty line for spacing
                steps.append(f"❌ Processing stopped - Reached dead state {current_state}")
                steps.append(f"❌ String REJECTED")
                return steps  # Stop simulation when dead state reached
        
        steps.append("")  # Empty line for spacing before final result
        
        # Check if we ended in a final state
        if current_state in dfa["final"]:
            steps.append(f"✅ {current_state} is Final State → String ACCEPTED")
        else:
            steps.append(f"❌ {current_state} is NOT Final State → String REJECTED")
        
        return steps  # Return all simulation steps

# ================================================
# DFA DISPLAY FUNCTIONS FOR ALL PATTERNS
# ================================================

def display_aba_dfa():
    """Display DFA for aba using Subset Construction"""
    print("\nDFA Transition Table for 'aba': using Subset Construction")
    print("=" * 60)
    print()
    
    print("State     a          b          c")
    print("-" * 40)
    
    print("q0       q1          q4         q4")
    print("q1       q4          q2         q4")
    print("q2       q3          q4         q4")
    print("q3       q4          q4         q4")
    print("q4       q4          q4         q4")
    print()
    
    print("Where:")
    print("q0 initial State, q3 final State, q4 dead State → String Accepted")
    print("=" * 60)

def display_bb_dfa():
    """Display DFA for bb using Subset Construction"""
    print("\nDFA Transition Table for 'bb': using Subset Construction")
    print("=" * 60)
    print()
    
    print("State     a          b          c")
    print("-" * 40)
    
    print("q0       q3          q1         q3")
    print("q1       q3          q2         q3")
    print("q2       q3          q3         q3")
    print("q3       q3          q3         q3")
    print()
    
    print("Where:")
    print("q0 initial State, q2 final State, q3 dead State → String Accepted")
    print("=" * 60)

def display_c_only_dfa():
    """Display DFA for c only using Subset Construction"""
    print("\nDFA Transition Table for 'c': using Subset Construction")
    print("=" * 60)
    print()
    
    print("State     a          b          c")
    print("-" * 40)
    
    print("q0       q2          q2         q1")
    print("q1       q2          q2         q2")
    print("q2       q2          q2         q2")
    print()
    
    print("Where:")
    print("q0 initial State, q1 final State, q2 dead State → String Accepted")
    print("=" * 60)

def display_ca_dfa():
    """Display DFA for ca using Subset Construction"""
    print("\nDFA Transition Table for 'ca': using Subset Construction")
    print("=" * 60)
    print()
    
    print("State     a          b          c")
    print("-" * 40)
    
    print("q0       q2          q2         q1")
    print("q1       q3          q2         q2")
    print("q2       q2          q2         q2")
    print("q3       q2          q2         q2")
    print()
    
    print("Where:")
    print("q0 initial State, q3 final State, q2 dead State → String Accepted")
    print("=" * 60)

def display_caa_dfa():
    """Display DFA for caa using Subset Construction"""
    print("\nDFA Transition Table for 'caa': using Subset Construction")
    print("=" * 60)
    print()
    
    print("State     a          b          c")
    print("-" * 40)
    
    print("q0       q3          q3         q1")
    print("q1       q2          q3         q3")
    print("q2       q4          q3         q3")
    print("q3       q3          q3         q3")
    print("q4       q3          q3         q3")
    print()
    
    print("Where:")
    print("q0 initial State, q4 final State, q3 dead State → String Accepted")
    print("=" * 60)

def display_caaa_dfa():
    """Display DFA for caaa using Subset Construction"""
    print("\nDFA Transition Table for 'caaa': using Subset Construction")
    print("=" * 60)
    print()
    
    print("State     a          b          c")
    print("-" * 40)
    
    print("q0       q4          q4         q1")
    print("q1       q2          q4         q4")
    print("q2       q3          q4         q4")
    print("q3       q5          q4         q4")
    print("q4       q4          q4         q4")
    print("q5       q4          q4         q4")
    print()
    
    print("Where:")
    print("q0 initial State, q5 final State, q4 dead State → String Accepted")
    print("=" * 60)

def display_c_kleene_star_dfa():
    """Display DFA for c(aaa+aa+a)* using Subset Construction"""
    print("\nDFA Transition Table for 'c(aaa+aa+a)*': using Subset Construction")
    print("=" * 60)
    print()
    
    print("State     a          b          c")
    print("-" * 40)
    
    print("q0       q2          q2         q1")
    print("q1       q1          q2         q2")
    print("q2       q2          q2         q2")
    print()
    
    print("Where:")
    print("q0 initial State, q1 final State, q2 dead State → String Accepted")
    print("=" * 60)