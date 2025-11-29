class State:
    """Represents an NFA state"""
    _id_counter = 0

    def __init__(self):
        self.id = State._id_counter
        State._id_counter += 1
        self.transitions = {}  # {symbol: [states]}
        self.is_final = False

    @classmethod
    def reset_counter(cls):
        cls._id_counter = 0

    def add_transition(self, symbol, state):
        """Add a transition on symbol to state"""
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        if state not in self.transitions[symbol]:
            self.transitions[symbol].append(state)

    def __repr__(self):
        return f"q{self.id}"


class NFA:
    """Non-deterministic Finite Automaton"""

    def __init__(self, start, final):
        self.start = start
        self.final = final
        self.states = set()
        self._collect_states()

    def _collect_states(self):
        """Collect all reachable states"""
        visited = set()
        stack = [self.start]

        while stack:
            state = stack.pop()
            if state in visited:
                continue
            visited.add(state)
            self.states.add(state)

            for symbol, next_states in state.transitions.items():
                for next_state in next_states:
                    if next_state not in visited:
                        stack.append(next_state)

        self.states.add(self.final)

    def get_epsilon_closure(self, states):
        """Compute ε-closure of a set of states"""
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            if 'ε' in state.transitions:
                for next_state in state.transitions['ε']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)

        return closure

    def get_transition_table(self):
        """Generate NFA transition table"""
        table = {}
        sorted_states = sorted(self.states, key=lambda s: s.id)

        for state in sorted_states:
            state_name = f"q{state.id}"
            table[state_name] = {}

            for symbol in sorted(state.transitions.keys()):
                next_states = state.transitions[symbol]
                table[state_name][symbol] = [f"q{s.id}" for s in sorted(next_states, key=lambda s: s.id)]

        return table

    def get_epsilon_closures(self):
        """Get epsilon closures for all states"""
        closures = {}
        sorted_states = sorted(self.states, key=lambda s: s.id)

        for state in sorted_states:
            closure = self.get_epsilon_closure([state])
            closures[f"q{state.id}"] = sorted([f"q{s.id}" for s in closure], key=lambda x: int(x[1:]))

        return closures


class ThompsonNFA:
    """Thompson's Construction Algorithm Implementation"""

    def __init__(self, regex):
        # Reset counter before building new NFA
        State.reset_counter()
        self.regex = regex
        self.nfa = None

    def build(self):
        """Build NFA from preprocessed regex with explicit concatenation"""
        self.nfa = self._regex_to_nfa(self.regex)
        self.nfa.final.is_final = True
        return self.nfa

    def _regex_to_nfa(self, regex):
        """Convert regex to NFA using Thompson's construction"""
        postfix = self._infix_to_postfix(regex)
        return self._postfix_to_nfa(postfix)

    def _infix_to_postfix(self, regex):
        """Convert infix regex to postfix notation"""
        precedence = {'|': 1, '.': 2, '*': 3}
        output = []
        stack = []

        for char in regex:
            if char not in ['|', '.', '*', '(', ')']:
                # Operand (alphabet symbol)
                output.append(char)
            elif char == '(':
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack:
                    stack.pop()  # Remove '('
            elif char in precedence:
                while stack and stack[-1] != '(' and stack[-1] in precedence and precedence[stack[-1]] >= precedence[char]:
                    output.append(stack.pop())
                stack.append(char)

        while stack:
            output.append(stack.pop())

        return ''.join(output)

    def _postfix_to_nfa(self, postfix):
        """Convert postfix regex to NFA"""
        stack = []

        for char in postfix:
            if char == '|':
                # Union
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(self._union(nfa1, nfa2))
            elif char == '.':
                # Concatenation
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(self._concatenation(nfa1, nfa2))
            elif char == '*':
                # Kleene Star
                nfa = stack.pop()
                stack.append(self._kleene_star(nfa))
            else:
                # Single character
                stack.append(self._single_char(char))

        return stack[0]

    def _single_char(self, char):
        """Create NFA for a single character"""
        start = State()
        final = State()
        start.add_transition(char, final)
        return NFA(start, final)

    def _concatenation(self, nfa1, nfa2):
        """Concatenate two NFAs"""
        # Connect final state of nfa1 to start state of nfa2 with ε-transition
        nfa1.final.add_transition('ε', nfa2.start)
        nfa1.final.is_final = False
        return NFA(nfa1.start, nfa2.final)

    def _union(self, nfa1, nfa2):
        """Union of two NFAs"""
        start = State()
        final = State()

        # ε-transitions from new start to both NFAs
        start.add_transition('ε', nfa1.start)
        start.add_transition('ε', nfa2.start)

        # ε-transitions from both NFAs to new final
        nfa1.final.add_transition('ε', final)
        nfa2.final.add_transition('ε', final)

        nfa1.final.is_final = False
        nfa2.final.is_final = False

        return NFA(start, final)

    def _kleene_star(self, nfa):
        """Kleene star of an NFA"""
        start = State()
        final = State()

        # ε-transition from new start to old start
        start.add_transition('ε', nfa.start)

        # ε-transition from old final to old start (loop)
        nfa.final.add_transition('ε', nfa.start)

        # ε-transition from old final to new final
        nfa.final.add_transition('ε', final)

        # ε-transition from new start to new final (for empty string)
        start.add_transition('ε', final)

        nfa.final.is_final = False

        return NFA(start, final)