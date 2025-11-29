"""
Automata Diagram Generator
Generates visual diagrams for NFA, DFA, and Minimized DFA using Graphviz
"""

import os

try:
    from graphviz import Digraph
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False


class AutomataVisualizer:
    """Generates visual diagrams for automata"""

    def __init__(self, output_dir='assets/diagrams'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.graphviz_available = GRAPHVIZ_AVAILABLE

    def _check_graphviz(self):
        """Check if Graphviz is available"""
        if not self.graphviz_available:
            raise ImportError(
                "Graphviz is not installed. Please install:\n"
                "1. Download from: https://graphviz.org/download/\n"
                "2. Add to PATH: C:\\Program Files\\Graphviz\\bin\n"
                "3. Install Python package: pip install graphviz"
            )

    def visualize_nfa(self, nfa, filename='nfa'):
        """Generate NFA diagram"""
        self._check_graphviz()

        dot = Digraph(comment='NFA')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='circle')

        # Add invisible start node
        dot.node('', shape='none')

        # Add all states
        sorted_states = sorted(nfa.states, key=lambda s: s.id)

        for state in sorted_states:
            state_name = f'q{state.id}'

            if state.is_final:
                dot.node(state_name, state_name, shape='doublecircle', style='filled', fillcolor='lightblue')
            elif state == nfa.start:
                dot.node(state_name, state_name, style='filled', fillcolor='lightgreen')
            else:
                dot.node(state_name, state_name)

        # Add start arrow
        dot.edge('', f'q{nfa.start.id}')

        # Add transitions
        for state in sorted_states:
            state_name = f'q{state.id}'

            for symbol, next_states in state.transitions.items():
                for next_state in next_states:
                    next_name = f'q{next_state.id}'

                    # Use ε for epsilon transitions
                    label = 'ε' if symbol == 'ε' else symbol

                    # Check for duplicate edges
                    existing_edges = [e for e in dot.body if f'{state_name} -> {next_name}' in e]

                    if existing_edges:
                        # Find existing label and append
                        for i, line in enumerate(dot.body):
                            if f'{state_name} -> {next_name}' in line and '[label=' in line:
                                # Extract existing label
                                start = line.find('label="') + 7
                                end = line.find('"', start)
                                existing_label = line[:start] + line[start:end] + ',' + label + line[end:]
                                dot.body[i] = existing_label
                                break
                        else:
                            dot.edge(state_name, next_name, label=label)
                    else:
                        dot.edge(state_name, next_name, label=label)

        # Render
        output_path = os.path.join(self.output_dir, filename)
        dot.render(output_path, format='png', cleanup=True)

        return output_path + '.png'

    def visualize_dfa(self, dfa, filename='dfa'):
        """Generate DFA diagram"""
        self._check_graphviz()

        dot = Digraph(comment='DFA')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='circle')

        # Add invisible start node
        dot.node('', shape='none')

        # Add all states
        sorted_states = sorted(dfa.states, key=lambda s: s.id)

        for state in sorted_states:
            state_name = f'q{state.id}'

            if state.is_final:
                dot.node(state_name, state_name, shape='doublecircle', style='filled', fillcolor='lightblue')
            elif state.is_start:
                dot.node(state_name, state_name, style='filled', fillcolor='lightgreen')
            else:
                dot.node(state_name, state_name)

        # Add start arrow
        if dfa.start:
            dot.edge('', f'q{dfa.start.id}')

        # Add transitions
        for state in sorted_states:
            state_name = f'q{state.id}'

            for symbol, next_state in state.transitions.items():
                next_name = f'q{next_state.id}'
                dot.edge(state_name, next_name, label=symbol)

        # Render
        output_path = os.path.join(self.output_dir, filename)
        dot.render(output_path, format='png', cleanup=True)

        return output_path + '.png'

    def visualize_minimized_dfa(self, min_dfa, filename='minimized_dfa'):
        """Generate Minimized DFA diagram"""
        self._check_graphviz()

        dot = Digraph(comment='Minimized DFA')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='circle')

        # Add invisible start node
        dot.node('', shape='none')

        # Add all states with merged information
        sorted_states = sorted(min_dfa.states, key=lambda s: s.id)

        for state in sorted_states:
            state_name = f'q{state.id}'

            # Add label with original states
            if state_name in min_dfa.state_groups:
                original = ','.join(min_dfa.state_groups[state_name])
                label = f'{state_name}\\n({original})'
            else:
                label = state_name

            if state.is_final:
                dot.node(state_name, label, shape='doublecircle', style='filled', fillcolor='lightblue')
            elif state.is_start:
                dot.node(state_name, label, style='filled', fillcolor='lightgreen')
            else:
                dot.node(state_name, label)

        # Add start arrow
        if min_dfa.start:
            dot.edge('', f'q{min_dfa.start.id}')

        # Add transitions
        for state in sorted_states:
            state_name = f'q{state.id}'

            for symbol, next_state in state.transitions.items():
                next_name = f'q{next_state.id}'
                dot.edge(state_name, next_name, label=symbol)

        # Render
        output_path = os.path.join(self.output_dir, filename)
        dot.render(output_path, format='png', cleanup=True)

        return output_path + '.png'

    def visualize_all(self, nfa, dfa, min_dfa):
        """Generate all three diagrams"""
        paths = {
            'nfa': self.visualize_nfa(nfa, 'nfa'),
            'dfa': self.visualize_dfa(dfa, 'dfa'),
            'minimized_dfa': self.visualize_minimized_dfa(min_dfa, 'minimized_dfa')
        }

        return paths