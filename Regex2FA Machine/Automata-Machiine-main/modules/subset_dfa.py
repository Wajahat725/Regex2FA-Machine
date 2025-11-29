"""
Subset Construction Algorithm
Converts NFA to DFA
"""


class DFAState:
    """Represents a DFA state (which is a set of NFA states)"""
    _id_counter = 0

    def __init__(self, nfa_states):
        self.id = DFAState._id_counter
        DFAState._id_counter += 1
        self.nfa_states = frozenset(nfa_states)
        self.transitions = {}
        self.is_final = False
        self.is_start = False

    @classmethod
    def reset_counter(cls):
        cls._id_counter = 0

    def add_transition(self, symbol, state):
        """Add transition on symbol to state"""
        self.transitions[symbol] = state

    def __repr__(self):
        return f"q{self.id}"

    def __hash__(self):
        return hash(self.nfa_states)

    def __eq__(self, other):
        return isinstance(other, DFAState) and self.nfa_states == other.nfa_states


class DFA:
    """Deterministic Finite Automaton"""

    def __init__(self):
        self.start = None
        self.states = set()
        self.final_states = set()
        self.alphabet = set()

    def add_state(self, state):
        """Add a state to DFA"""
        self.states.add(state)
        if state.is_final:
            self.final_states.add(state)

    def get_transition_table(self):
        """Generate DFA transition table"""
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

            # Add NFA states composition
            nfa_states_str = '{' + ', '.join(sorted([f"q{s.id}" for s in state.nfa_states], key=lambda x: int(x[1:]))) + '}'
            table[state_name]['_composition'] = nfa_states_str

            for symbol in sorted_alphabet:
                if symbol in state.transitions:
                    next_state = state.transitions[symbol]
                    table[state_name][symbol] = f"q{next_state.id}"
                else:
                    table[state_name][symbol] = "∅"

        return table


class SubsetConstruction:  # Make sure this class name matches the import
    """Converts NFA to DFA using Subset Construction Algorithm"""

    def __init__(self, nfa, alphabet):
        # Reset counter before building new DFA
        DFAState.reset_counter()
        self.nfa = nfa
        self.alphabet = alphabet - {'ε'}  # Remove epsilon from alphabet
        self.dfa = DFA()
        self.dfa.alphabet = self.alphabet
        self.state_map = {}  # Maps frozenset of NFA states to DFA state

    def build(self):
        """Build DFA from NFA"""
        # Start with epsilon closure of NFA start state
        start_closure = self.nfa.get_epsilon_closure([self.nfa.start])
        start_dfa_state = self._get_or_create_state(start_closure)
        start_dfa_state.is_start = True
        self.dfa.start = start_dfa_state
        self.dfa.add_state(start_dfa_state)

        # Mark as final if contains NFA final state
        if self.nfa.final in start_closure:
            start_dfa_state.is_final = True

        # Process all states using BFS
        queue = [start_dfa_state]
        processed = set()

        while queue:
            current_state = queue.pop(0)

            if current_state in processed:
                continue
            processed.add(current_state)

            # For each symbol in alphabet
            for symbol in sorted(self.alphabet):
                # Find all NFA states reachable on this symbol
                next_nfa_states = set()

                for nfa_state in current_state.nfa_states:
                    if symbol in nfa_state.transitions:
                        next_nfa_states.update(nfa_state.transitions[symbol])

                if next_nfa_states:
                    # Compute epsilon closure of next states
                    next_closure = self.nfa.get_epsilon_closure(next_nfa_states)
                    next_dfa_state = self._get_or_create_state(next_closure)

                    # Mark as final if contains NFA final state
                    if self.nfa.final in next_closure:
                        next_dfa_state.is_final = True

                    # Add transition
                    current_state.add_transition(symbol, next_dfa_state)

                    # Add to DFA and queue if new
                    if next_dfa_state not in processed:
                        self.dfa.add_state(next_dfa_state)
                        queue.append(next_dfa_state)

        return self.dfa

    def _get_or_create_state(self, nfa_states):
        """Get existing DFA state or create new one"""
        frozen_states = frozenset(nfa_states)

        if frozen_states in self.state_map:
            return self.state_map[frozen_states]

        new_state = DFAState(nfa_states)
        self.state_map[frozen_states] = new_state
        return new_state