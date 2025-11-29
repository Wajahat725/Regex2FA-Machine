"""
DFA Minimization using Table-Filling Algorithm (Myhill-Nerode)
"""


class MinimizedDFA:
    """Minimized DFA with merged states"""

    def __init__(self):
        self.start = None
        self.states = set()
        self.final_states = set()
        self.alphabet = set()
        self.state_groups = {}  # Maps minimized state to original states

    def get_transition_table(self):
        """Generate minimized DFA transition table"""
        table = {}
        sorted_states = sorted(self.states, key=lambda s: s.id)
        sorted_alphabet = sorted(self.alphabet)

        for state in sorted_states:
            state_name = f"q{state.id}"
            table[state_name] = {}

            # Mark special states
            flags = []
            if state.is_start:
                flags.append("START")
            if state.is_final:
                flags.append("FINAL")

            if flags:
                table[state_name]['_flags'] = flags

            # Show original states that were merged
            if state_name in self.state_groups:
                original = ', '.join(sorted(self.state_groups[state_name]))
                table[state_name]['_merged_from'] = original

            for symbol in sorted_alphabet:
                if symbol in state.transitions:
                    next_state = state.transitions[symbol]
                    table[state_name][symbol] = f"q{next_state.id}"
                else:
                    table[state_name][symbol] = "∅"

        return table


class MinimizedDFAState:
    """State in minimized DFA"""
    _id_counter = 0

    def __init__(self, original_states=None):
        self.id = MinimizedDFAState._id_counter
        MinimizedDFAState._id_counter += 1
        self.original_states = original_states or []
        self.transitions = {}
        self.is_final = False
        self.is_start = False

    @classmethod
    def reset_counter(cls):
        cls._id_counter = 0

    def add_transition(self, symbol, state):
        """Add transition"""
        self.transitions[symbol] = state

    def __repr__(self):
        return f"q{self.id}"


class DFAMinimizer:
    """Minimizes DFA using Table-Filling Algorithm"""

    def __init__(self, dfa):
        MinimizedDFAState.reset_counter()
        self.dfa = dfa
        self.min_dfa = MinimizedDFA()
        self.min_dfa.alphabet = dfa.alphabet
        self.distinguishable = {}
        self.equivalence_classes = []

    def minimize(self):
        """Minimize the DFA"""
        # Step 1: Build distinguishability table
        self._build_distinguishability_table()

        # Step 2: Find equivalence classes
        self._find_equivalence_classes()

        # Step 3: Build minimized DFA
        self._build_minimized_dfa()

        return self.min_dfa

    def _build_distinguishability_table(self):
        """Build table marking distinguishable state pairs"""
        states = list(self.dfa.states)

        # Initialize: mark pairs where one is final and one is not
        for i in range(len(states)):
            for j in range(i + 1, len(states)):
                state1, state2 = states[i], states[j]
                pair = self._make_pair(state1, state2)

                if (state1.is_final and not state2.is_final) or \
                   (not state1.is_final and state2.is_final):
                    self.distinguishable[pair] = True
                else:
                    self.distinguishable[pair] = False

        # Iteratively mark distinguishable pairs
        changed = True
        while changed:
            changed = False

            for i in range(len(states)):
                for j in range(i + 1, len(states)):
                    state1, state2 = states[i], states[j]
                    pair = self._make_pair(state1, state2)

                    if self.distinguishable[pair]:
                        continue

                    # Check if any transition leads to distinguishable states
                    for symbol in self.dfa.alphabet:
                        next1 = state1.transitions.get(symbol)
                        next2 = state2.transitions.get(symbol)

                        # If one has transition and other doesn't
                        if (next1 is None) != (next2 is None):
                            self.distinguishable[pair] = True
                            changed = True
                            break

                        # If both have transitions
                        if next1 and next2 and next1 != next2:
                            next_pair = self._make_pair(next1, next2)
                            if self.distinguishable.get(next_pair, False):
                                self.distinguishable[pair] = True
                                changed = True
                                break

    def _make_pair(self, state1, state2):
        """Create ordered pair tuple"""
        return tuple(sorted([state1.id, state2.id]))

    def _find_equivalence_classes(self):
        """Find equivalence classes from distinguishability table"""
        states = list(self.dfa.states)
        assigned = set()

        for state in states:
            if state in assigned:
                continue

            # Find all states equivalent to this one
            equiv_class = [state]
            assigned.add(state)

            for other_state in states:
                if other_state in assigned:
                    continue

                if state == other_state:
                    continue

                pair = self._make_pair(state, other_state)
                if not self.distinguishable.get(pair, False):
                    equiv_class.append(other_state)
                    assigned.add(other_state)

            self.equivalence_classes.append(equiv_class)

    def _build_minimized_dfa(self):
        """Build minimized DFA from equivalence classes"""
        # Create new states for each equivalence class
        class_to_state = {}

        for equiv_class in self.equivalence_classes:
            new_state = MinimizedDFAState(equiv_class)

            # Check if any state in class is final
            if any(s.is_final for s in equiv_class):
                new_state.is_final = True
                self.min_dfa.final_states.add(new_state)

            # Check if start state is in class
            if self.dfa.start in equiv_class:
                new_state.is_start = True
                self.min_dfa.start = new_state

            self.min_dfa.states.add(new_state)

            # Map all states in class to this new state
            for state in equiv_class:
                class_to_state[state] = new_state

        # Build transitions
        for equiv_class in self.equivalence_classes:
            representative = equiv_class[0]
            new_state = class_to_state[representative]

            for symbol in self.dfa.alphabet:
                if symbol in representative.transitions:
                    target = representative.transitions[symbol]
                    target_new_state = class_to_state[target]
                    new_state.add_transition(symbol, target_new_state)

        # Store state groups for display
        for state in self.min_dfa.states:
            state_name = f"q{state.id}"
            original_names = [f"q{s.id}" for s in state.original_states]
            self.min_dfa.state_groups[state_name] = original_names

    def get_distinguishability_table(self):
        """Get the distinguishability table for display"""
        states = sorted(list(self.dfa.states), key=lambda s: s.id)
        table = {}

        for i in range(len(states)):
            for j in range(i + 1, len(states)):
                state1, state2 = states[i], states[j]
                pair = self._make_pair(state1, state2)
                pair_name = f"(q{state1.id}, q{state2.id})"
                table[pair_name] = "✓" if self.distinguishable.get(pair, False) else "✗"

        return table