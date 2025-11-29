"""
String Simulation Module
Simulates string acceptance on DFA with step-by-step trace
"""


class StringSimulator:
    """Simulates string acceptance on a DFA"""

    def __init__(self, dfa):
        self.dfa = dfa

    def simulate(self, input_string):
        """
        Simulate string acceptance on DFA
        Returns: (accepted: bool, trace: list, error: str)
        """
        if not self.dfa or not self.dfa.start:
            return False, [], "DFA not initialized"

        trace = []
        current_state = self.dfa.start

        # Initial state
        trace.append({
            'step': 0,
            'state': f"q{current_state.id}",
            'symbol': 'START',
            'remaining': input_string,
            'description': f"Starting at state q{current_state.id}"
        })

        # Process each character
        for i, symbol in enumerate(input_string):
            # Check if symbol is in alphabet
            if symbol not in self.dfa.alphabet:
                error_msg = f"Symbol '{symbol}' not in alphabet {self.dfa.alphabet}"
                trace.append({
                    'step': i + 1,
                    'state': f"q{current_state.id}",
                    'symbol': symbol,
                    'remaining': input_string[i:],
                    'description': f"ERROR: {error_msg}",
                    'error': True
                })
                return False, trace, error_msg

            # Check if transition exists
            if symbol not in current_state.transitions:
                error_msg = f"No transition from q{current_state.id} on '{symbol}'"
                trace.append({
                    'step': i + 1,
                    'state': f"q{current_state.id}",
                    'symbol': symbol,
                    'remaining': input_string[i:],
                    'description': f"ERROR: {error_msg}",
                    'error': True
                })
                return False, trace, error_msg

            # Make transition
            next_state = current_state.transitions[symbol]

            trace.append({
                'step': i + 1,
                'state': f"q{current_state.id}",
                'symbol': symbol,
                'next_state': f"q{next_state.id}",
                'remaining': input_string[i + 1:],
                'description': f"q{current_state.id} --{symbol}--> q{next_state.id}"
            })

            current_state = next_state

        # Check if final state
        accepted = current_state.is_final

        trace.append({
            'step': len(input_string) + 1,
            'state': f"q{current_state.id}",
            'symbol': 'END',
            'remaining': '',
            'description': f"Ended at state q{current_state.id} ({'FINAL' if current_state.is_final else 'NOT FINAL'})",
            'final': current_state.is_final
        })

        if accepted:
            trace.append({
                'step': len(input_string) + 2,
                'description': '✓ String ACCEPTED',
                'accepted': True
            })
        else:
            trace.append({
                'step': len(input_string) + 2,
                'description': '✗ String REJECTED (not in final state)',
                'accepted': False
            })

        return accepted, trace, None

    def format_trace(self, trace):
        """Format trace as human-readable string"""
        lines = []

        for entry in trace:
            if 'error' in entry and entry['error']:
                lines.append(f"  {entry['description']}")
            elif 'accepted' in entry:
                lines.append(f"\n{entry['description']}")
            elif entry['symbol'] == 'START':
                lines.append(f"Step {entry['step']}: {entry['description']}")
            elif entry['symbol'] == 'END':
                lines.append(f"Step {entry['step']}: {entry['description']}")
            elif 'next_state' in entry:
                lines.append(f"Step {entry['step']}: {entry['description']}")

        return '\n'.join(lines)

    def simulate_multiple(self, test_strings):
        """
        Simulate multiple strings
        Returns: list of (string, accepted, trace) tuples
        """
        results = []

        for test_string in test_strings:
            accepted, trace, error = self.simulate(test_string)
            results.append({
                'string': test_string,
                'accepted': accepted,
                'trace': trace,
                'error': error
            })

        return results