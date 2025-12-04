# image_generator.py
from graphviz import Digraph
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

class AutomataImageGenerator:
    def __init__(self, output_dir="automata_images"):
        """Initialize image generator with output directory"""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_table_image(self, title, headers, data, filename):
        """Generate a table image from data"""
        try:
            # Calculate dimensions
            cell_height = 40
            cell_width = 120
            header_height = 50
            row_height = 40
            
            num_rows = len(data) + 1  # +1 for header
            num_cols = len(headers)
            
            # Calculate image size
            img_width = num_cols * cell_width + 20
            img_height = header_height + num_rows * row_height + 20
            
            # Create image
            img = Image.new('RGB', (img_width, img_height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Try to load font, use default if not available
            try:
                font = ImageFont.truetype("arial.ttf", 14)
                bold_font = ImageFont.truetype("arialbd.ttf", 16)
            except:
                font = ImageFont.load_default()
                bold_font = ImageFont.load_default()
            
            # Draw title
            title_width = draw.textlength(title, font=bold_font)
            title_x = (img_width - title_width) // 2
            draw.text((title_x, 10), title, fill='black', font=bold_font)
            
            # Draw headers
            for col, header in enumerate(headers):
                x = col * cell_width + 10
                y = 40
                # Draw cell background
                draw.rectangle([x, y, x + cell_width - 2, y + header_height - 2], 
                             fill='#4a86e8', outline='black')
                # Draw header text
                header_width = draw.textlength(header, font=bold_font)
                header_x = x + (cell_width - header_width) // 2
                draw.text((header_x, y + 10), header, fill='white', font=bold_font)
            
            # Draw data rows
            for row, row_data in enumerate(data):
                y = header_height + row * row_height + 40
                
                for col, cell in enumerate(row_data):
                    x = col * cell_width + 10
                    
                    # Draw cell background
                    fill_color = '#f0f0f0' if row % 2 == 0 else '#ffffff'
                    draw.rectangle([x, y, x + cell_width - 2, y + row_height - 2], 
                                 fill=fill_color, outline='black')
                    
                    # Draw cell text
                    cell_text = str(cell)
                    cell_width_text = draw.textlength(cell_text, font=font)
                    cell_x = x + (cell_width - cell_width_text) // 2
                    draw.text((cell_x, y + 10), cell_text, fill='black', font=font)
            
            # Save image
            img_path = os.path.join(self.output_dir, filename)
            img.save(img_path)
            print(f"Table image saved: {img_path}")
            return img_path
            
        except Exception as e:
            print(f"Error generating table image: {e}")
            return None
    
    def generate_nfa_table_image(self, pattern):
        """Generate NFA table image for specific pattern"""
        if pattern == "aba":
            title = "NFA Transition Table for 'aba'"
            headers = ["State", "a", "b", "c", "ε"]
            data = [
                ["q0", "-", "-", "-", "{q1}"],
                ["q1", "{q2}", "-", "-", "-"],
                ["q2", "-", "-", "-", "{q3}"],
                ["q3", "-", "{q4}", "-", "-"],
                ["q4", "-", "-", "-", "{q5}"],
                ["q5", "{q6}", "-", "-", "-"],
                ["q6", "-", "-", "-", "{q7}"],
                ["q7", "-", "-", "-", "-"]
            ]
            
        elif pattern == "bb":
            title = "NFA Transition Table for 'bb'"
            headers = ["State", "a", "b", "c", "ε"]
            data = [
                ["q0", "-", "-", "-", "{q1}"],
                ["q1", "-", "{q2}", "-", "-"],
                ["q2", "-", "-", "-", "{q3}"],
                ["q3", "-", "{q4}", "-", "-"],
                ["q4", "-", "-", "-", "{q5}"],
                ["q5", "-", "-", "-", "-"]
            ]
            
        elif pattern == "c_only":
            title = "NFA Transition Table for 'c'"
            headers = ["State", "a", "b", "c", "ε"]
            data = [
                ["q0", "-", "-", "-", "{q1}"],
                ["q1", "-", "-", "{q2}", "-"],
                ["q2", "-", "-", "-", "{q3}"],
                ["q3", "-", "-", "-", "-"]
            ]
            
        elif pattern == "ca":
            title = "NFA Transition Table for 'ca'"
            headers = ["State", "a", "b", "c", "ε"]
            data = [
                ["q0", "-", "-", "-", "{q1}"],
                ["q1", "-", "-", "{q2}", "-"],
                ["q2", "-", "-", "-", "{q3}"],
                ["q3", "{q4}", "-", "-", "-"],
                ["q4", "-", "-", "-", "{q5}"],
                ["q5", "-", "-", "-", "-"]
            ]
            
        elif pattern == "caa":
            title = "NFA Transition Table for 'caa'"
            headers = ["State", "a", "b", "c", "ε"]
            data = [
                ["q0", "-", "-", "-", "{q1}"],
                ["q1", "-", "-", "{q2}", "-"],
                ["q2", "-", "-", "-", "{q3}"],
                ["q3", "{q4}", "-", "-", "-"],
                ["q4", "-", "-", "-", "{q5}"],
                ["q5", "{q6}", "-", "-", "-"],
                ["q6", "-", "-", "-", "{q7}"],
                ["q7", "-", "-", "-", "-"]
            ]
            
        elif pattern == "caaa":
            title = "NFA Transition Table for 'caaa'"
            headers = ["State", "a", "b", "c", "ε"]
            data = [
                ["q0", "-", "-", "-", "{q1}"],
                ["q1", "-", "-", "{q2}", "-"],
                ["q2", "-", "-", "-", "{q3}"],
                ["q3", "{q4}", "-", "-", "-"],
                ["q4", "-", "-", "-", "{q5}"],
                ["q5", "{q6}", "-", "-", "-"],
                ["q6", "-", "-", "-", "{q7}"],
                ["q7", "{q8}", "-", "-", "-"],
                ["q8", "-", "-", "-", "{q9}"],
                ["q9", "-", "-", "-", "-"]
            ]
            
        elif pattern == "c_kleene_star":
            title = "NFA Transition Table for 'c(aaa+aa+a)*'"
            headers = ["State", "a", "b", "c", "ε"]
            data = [
                ["q0", "-", "-", "-", "{q1}"],
                ["q1", "-", "-", "{q2}", "-"],
                ["q2", "-", "-", "-", "{q3}"],
                ["q3", "-", "-", "-", "{q4,q8,q12}"],
                ["q4", "{q5}", "-", "-", "-"],
                ["q5", "-", "-", "-", "{q6}"],
                ["q6", "{q7}", "-", "-", "-"],
                ["q7", "-", "-", "-", "{q16}"],
                ["q8", "{q9}", "-", "-", "-"],
                ["q9", "-", "-", "-", "{q10}"],
                ["q10", "{q11}", "-", "-", "-"],
                ["q11", "-", "-", "-", "{q16}"],
                ["q12", "{q13}", "-", "-", "-"],
                ["q13", "-", "-", "-", "{q14}"],
                ["q14", "-", "-", "-", "{q15}"],
                ["q15", "-", "-", "-", "{q16}"],
                ["q16", "-", "-", "-", "{q3,q17}"],
                ["q17", "-", "-", "-", "{q18}"],
                ["q18", "-", "-", "-", "-"]
            ]
        
        else:
            return None
        
        filename = f"nfa_table_{pattern}.png"
        return self.generate_table_image(title, headers, data, filename)
    
    def generate_dfa_table_image(self, pattern, dfa_data):
        """Generate DFA table image for specific pattern"""
        if pattern == "aba":
            title = "DFA Transition Table for 'aba'"
            headers = ["State", "a", "b", "c"]
            data = [
                ["q0", "q1", "q4", "q4"],
                ["q1", "q4", "q2", "q4"],
                ["q2", "q3", "q4", "q4"],
                ["q3", "q4", "q4", "q4"],
                ["q4", "q4", "q4", "q4"]
            ]
            
        elif pattern == "bb":
            title = "DFA Transition Table for 'bb'"
            headers = ["State", "a", "b", "c"]
            data = [
                ["q0", "q3", "q1", "q3"],
                ["q1", "q3", "q2", "q3"],
                ["q2", "q3", "q3", "q3"],
                ["q3", "q3", "q3", "q3"]
            ]
            
        elif pattern == "c_only":
            title = "DFA Transition Table for 'c'"
            headers = ["State", "a", "b", "c"]
            data = [
                ["q0", "q2", "q2", "q1"],
                ["q1", "q2", "q2", "q2"],
                ["q2", "q2", "q2", "q2"]
            ]
            
        elif pattern == "ca":
            title = "DFA Transition Table for 'ca'"
            headers = ["State", "a", "b", "c"]
            data = [
                ["q0", "q2", "q2", "q1"],
                ["q1", "q3", "q2", "q2"],
                ["q2", "q2", "q2", "q2"],
                ["q3", "q2", "q2", "q2"]
            ]
            
        elif pattern == "caa":
            title = "DFA Transition Table for 'caa'"
            headers = ["State", "a", "b", "c"]
            data = [
                ["q0", "q3", "q3", "q1"],
                ["q1", "q2", "q3", "q3"],
                ["q2", "q4", "q3", "q3"],
                ["q3", "q3", "q3", "q3"],
                ["q4", "q3", "q3", "q3"]
            ]
            
        elif pattern == "caaa":
            title = "DFA Transition Table for 'caaa'"
            headers = ["State", "a", "b", "c"]
            data = [
                ["q0", "q4", "q4", "q1"],
                ["q1", "q2", "q4", "q4"],
                ["q2", "q3", "q4", "q4"],
                ["q3", "q5", "q4", "q4"],
                ["q4", "q4", "q4", "q4"],
                ["q5", "q4", "q4", "q4"]
            ]
            
        elif pattern == "c_kleene_star":
            title = "DFA Transition Table for 'c(aaa+aa+a)*'"
            headers = ["State", "a", "b", "c"]
            data = [
                ["q0", "q2", "q2", "q1"],
                ["q1", "q1", "q2", "q2"],
                ["q2", "q2", "q2", "q2"]
            ]
        
        else:
            return None
        
        filename = f"dfa_table_{pattern}.png"
        return self.generate_table_image(title, headers, data, filename)
    
    def generate_min_dfa_table_image(self, pattern):
        """Generate Minimized DFA table image for specific pattern"""
        if pattern == "aba":
            title = "Minimized DFA Transition Table for 'aba'"
            headers = ["State", "a", "b", "c"]
            data = [
                ["A", "B", "D", "D"],
                ["B", "D", "C", "D"],
                ["C*", "D", "D", "D"],
                ["D", "D", "D", "D"]
            ]
            
        elif pattern == "bb":
            title = "Minimized DFA Transition Table for 'bb'"
            headers = ["State", "a", "b", "c"]
            data = [
                ["A", "C", "B", "C"],
                ["B", "C", "C*", "C"],
                ["C", "C", "C", "C"]
            ]
            
        elif pattern == "c_only":
            title = "Minimized DFA Transition Table for 'c'"
            headers = ["State", "a", "b", "c"]
            data = [
                ["A", "C", "C", "B*"],
                ["B*", "C", "C", "C"],
                ["C", "C", "C", "C"]
            ]
            
        elif pattern == "ca":
            title = "Minimized DFA Transition Table for 'ca'"
            headers = ["State", "a", "b", "c"]
            data = [
                ["A", "C", "C", "B"],
                ["B", "D*", "C", "C"],
                ["C", "C", "C", "C"],
                ["D*", "C", "C", "C"]
            ]
            
        elif pattern == "caa":
            title = "Minimized DFA Transition Table for 'caa'"
            headers = ["State", "a", "b", "c"]
            data = [
                ["A", "D", "D", "B"],
                ["B", "C", "D", "D"],
                ["C", "E*", "D", "D"],
                ["D", "D", "D", "D"],
                ["E*", "D", "D", "D"]
            ]
            
        elif pattern == "caaa":
            title = "Minimized DFA Transition Table for 'caaa'"
            headers = ["State", "a", "b", "c"]
            data = [
                ["A", "D", "D", "B"],
                ["B", "C", "D", "D"],
                ["C", "E", "D", "D"],
                ["D", "D", "D", "D"],
                ["E", "F*", "D", "D"],
                ["F*", "D", "D", "D"]
            ]
            
        elif pattern == "c_kleene_star":
            title = "Minimized DFA Transition Table for 'c(aaa+aa+a)*'"
            headers = ["State", "a", "b", "c"]
            data = [
                ["A", "C", "C", "B*"],
                ["B*", "B*", "C", "C"],
                ["C", "C", "C", "C"]
            ]
        
        else:
            return None
        
        filename = f"min_dfa_table_{pattern}.png"
        return self.generate_table_image(title, headers, data, filename)
    
    def generate_nfa_diagram(self, pattern, nfa_type):
        """Generate NFA diagram for specific pattern"""
        dot = Digraph(comment=f'NFA for {pattern}', format='png')
        dot.attr(rankdir='LR')  # Left to right layout
        
        # Common styling
        dot.attr('node', shape='circle')
        
        if nfa_type == "aba":
            # NFA for aba
            dot.node('start', shape='point')  # Initial point
            dot.node('q0')
            dot.node('q1')
            dot.node('q2')
            dot.node('q3')
            dot.node('q4')
            dot.node('q5')
            dot.node('q6')
            dot.node('q7', shape='doublecircle')  # Final state
            
            # Transitions
            dot.edge('start', 'q0')
            dot.edge('q0', 'q1', label='ε')
            dot.edge('q1', 'q2', label='a')
            dot.edge('q2', 'q3', label='ε')
            dot.edge('q3', 'q4', label='b')
            dot.edge('q4', 'q5', label='ε')
            dot.edge('q5', 'q6', label='a')
            dot.edge('q6', 'q7', label='ε')
            
        elif nfa_type == "bb":
            # NFA for bb
            dot.node('start', shape='point')
            dot.node('q0')
            dot.node('q1')
            dot.node('q2')
            dot.node('q3')
            dot.node('q4')
            dot.node('q5', shape='doublecircle')
            
            dot.edge('start', 'q0')
            dot.edge('q0', 'q1', label='ε')
            dot.edge('q1', 'q2', label='b')
            dot.edge('q2', 'q3', label='ε')
            dot.edge('q3', 'q4', label='b')
            dot.edge('q4', 'q5', label='ε')
            
        elif nfa_type == "c_only":
            # NFA for c
            dot.node('start', shape='point')
            dot.node('q0')
            dot.node('q1')
            dot.node('q2', shape='doublecircle')
            
            dot.edge('start', 'q0')
            dot.edge('q0', 'q1', label='ε')
            dot.edge('q1', 'q2', label='c')
            
        elif nfa_type == "ca":
            # NFA for ca
            dot.node('start', shape='point')
            dot.node('q0')
            dot.node('q1')
            dot.node('q2')
            dot.node('q3')
            dot.node('q4', shape='doublecircle')
            
            dot.edge('start', 'q0')
            dot.edge('q0', 'q1', label='ε')
            dot.edge('q1', 'q2', label='c')
            dot.edge('q2', 'q3', label='ε')
            dot.edge('q3', 'q4', label='a')
            
        elif nfa_type == "caa":
            # NFA for caa
            dot.node('start', shape='point')
            dot.node('q0')
            dot.node('q1')
            dot.node('q2')
            dot.node('q3')
            dot.node('q4')
            dot.node('q5')
            dot.node('q6', shape='doublecircle')
            
            dot.edge('start', 'q0')
            dot.edge('q0', 'q1', label='ε')
            dot.edge('q1', 'q2', label='c')
            dot.edge('q2', 'q3', label='ε')
            dot.edge('q3', 'q4', label='a')
            dot.edge('q4', 'q5', label='ε')
            dot.edge('q5', 'q6', label='a')
            
        elif nfa_type == "caaa":
            # NFA for caaa
            dot.node('start', shape='point')
            dot.node('q0')
            dot.node('q1')
            dot.node('q2')
            dot.node('q3')
            dot.node('q4')
            dot.node('q5')
            dot.node('q6')
            dot.node('q7')
            dot.node('q8', shape='doublecircle')
            
            dot.edge('start', 'q0')
            dot.edge('q0', 'q1', label='ε')
            dot.edge('q1', 'q2', label='c')
            dot.edge('q2', 'q3', label='ε')
            dot.edge('q3', 'q4', label='a')
            dot.edge('q4', 'q5', label='ε')
            dot.edge('q5', 'q6', label='a')
            dot.edge('q6', 'q7', label='ε')
            dot.edge('q7', 'q8', label='a')
            
        elif nfa_type == "c_kleene_star":
            # Simplified NFA for c(aaa+aa+a)*
            dot.node('start', shape='point')
            dot.node('q0')
            dot.node('q1', shape='doublecircle')
            dot.node('q2', shape='doublecircle')
            
            dot.edge('start', 'q0')
            dot.edge('q0', 'q1', label='c')
            dot.edge('q1', 'q2', label='ε')
            dot.edge('q2', 'q2', label='a')
        
        # Save image
        filename = f"{self.output_dir}/nfa_diagram_{pattern}.png"
        dot.render(filename.replace('.png', ''), cleanup=True)
        return filename
    
    def generate_dfa_diagram(self, pattern, dfa_data):
        """Generate DFA diagram for specific pattern"""
        dot = Digraph(comment=f'DFA for {pattern}', format='png')
        dot.attr(rankdir='LR')
        
        # Extract DFA data
        transitions = dfa_data["transitions"]
        initial_state = dfa_data["initial"]
        final_states = dfa_data["final"]
        dead_states = dfa_data["dead_states"]
        
        # Add initial state marker
        dot.node(f'start_{initial_state}', shape='point')
        
        # Add all states
        for state in transitions.keys():
            if state in final_states:
                dot.node(state, shape='doublecircle')
            elif state in dead_states:
                dot.node(state, shape='circle', style='filled', fillcolor='lightgrey')
            else:
                dot.node(state, shape='circle')
        
        # Connect start to initial state
        dot.edge(f'start_{initial_state}', initial_state)
        
        # Add transitions
        transition_labels = {}
        for from_state, trans in transitions.items():
            for symbol, to_state in trans.items():
                key = (from_state, to_state)
                if key in transition_labels:
                    transition_labels[key] += f", {symbol}"
                else:
                    transition_labels[key] = symbol
        
        # Draw edges with combined labels
        for (from_state, to_state), label in transition_labels.items():
            dot.edge(from_state, to_state, label=label)
        
        # Save image
        filename = f"{self.output_dir}/dfa_diagram_{pattern}.png"
        dot.render(filename.replace('.png', ''), cleanup=True)
        return filename
    
    def generate_minimized_dfa_diagram(self, pattern):
        """Generate minimized DFA diagram"""
        dot = Digraph(comment=f'Minimized DFA for {pattern}', format='png')
        dot.attr(rankdir='LR')
        
        if pattern == "aba":
            dot.node('start', shape='point')
            dot.node('A', shape='circle')
            dot.node('B', shape='circle')
            dot.node('C', shape='doublecircle')
            dot.node('D', shape='circle', style='filled', fillcolor='lightgrey')
            
            dot.edge('start', 'A')
            dot.edge('A', 'B', label='a')
            dot.edge('A', 'D', label='b, c')
            dot.edge('B', 'D', label='a, c')
            dot.edge('B', 'C', label='b')
            dot.edge('C', 'D', label='a, b, c')
            dot.edge('D', 'D', label='a, b, c')
            
        elif pattern == "bb":
            dot.node('start', shape='point')
            dot.node('A', shape='circle')
            dot.node('B', shape='circle')
            dot.node('C', shape='doublecircle', style='filled', fillcolor='lightgrey')
            
            dot.edge('start', 'A')
            dot.edge('A', 'C', label='a, c')
            dot.edge('A', 'B', label='b')
            dot.edge('B', 'C', label='a, b, c')
            dot.edge('C', 'C', label='a, b, c')
            
        elif pattern == "c_only":
            dot.node('start', shape='point')
            dot.node('A', shape='circle')
            dot.node('B', shape='doublecircle')
            dot.node('C', shape='circle', style='filled', fillcolor='lightgrey')
            
            dot.edge('start', 'A')
            dot.edge('A', 'C', label='a, b')
            dot.edge('A', 'B', label='c')
            dot.edge('B', 'C', label='a, b, c')
            dot.edge('C', 'C', label='a, b, c')
            
        elif pattern == "ca":
            dot.node('start', shape='point')
            dot.node('A', shape='circle')
            dot.node('B', shape='circle')
            dot.node('C', shape='circle', style='filled', fillcolor='lightgrey')
            dot.node('D', shape='doublecircle')
            
            dot.edge('start', 'A')
            dot.edge('A', 'C', label='a, b')
            dot.edge('A', 'B', label='c')
            dot.edge('B', 'C', label='b, c')
            dot.edge('B', 'D', label='a')
            dot.edge('C', 'C', label='a, b, c')
            dot.edge('D', 'C', label='a, b, c')
            
        elif pattern == "caa":
            dot.node('start', shape='point')
            dot.node('A', shape='circle')
            dot.node('B', shape='circle')
            dot.node('C', shape='circle')
            dot.node('D', shape='circle', style='filled', fillcolor='lightgrey')
            dot.node('E', shape='doublecircle')
            
            dot.edge('start', 'A')
            dot.edge('A', 'D', label='a, b')
            dot.edge('A', 'B', label='c')
            dot.edge('B', 'D', label='b, c')
            dot.edge('B', 'C', label='a')
            dot.edge('C', 'D', label='b, c')
            dot.edge('C', 'E', label='a')
            dot.edge('D', 'D', label='a, b, c')
            dot.edge('E', 'D', label='a, b, c')
            
        elif pattern == "caaa":
            dot.node('start', shape='point')
            dot.node('A', shape='circle')
            dot.node('B', shape='circle')
            dot.node('C', shape='circle')
            dot.node('D', shape='circle', style='filled', fillcolor='lightgrey')
            dot.node('E', shape='circle')
            dot.node('F', shape='doublecircle')
            
            dot.edge('start', 'A')
            dot.edge('A', 'D', label='a, b')
            dot.edge('A', 'B', label='c')
            dot.edge('B', 'D', label='b, c')
            dot.edge('B', 'C', label='a')
            dot.edge('C', 'D', label='b, c')
            dot.edge('C', 'E', label='a')
            dot.edge('D', 'D', label='a, b, c')
            dot.edge('E', 'D', label='b, c')
            dot.edge('E', 'F', label='a')
            dot.edge('F', 'D', label='a, b, c')
            
        elif pattern == "c_kleene_star":
            dot.node('start', shape='point')
            dot.node('A', shape='circle')
            dot.node('B', shape='doublecircle')
            dot.node('C', shape='circle', style='filled', fillcolor='lightgrey')
            
            dot.edge('start', 'A')
            dot.edge('A', 'C', label='a, b')
            dot.edge('A', 'B', label='c')
            dot.edge('B', 'C', label='b, c')
            dot.edge('B', 'B', label='a')
            dot.edge('C', 'C', label='a, b, c')
        
        # Save image
        filename = f"{self.output_dir}/min_dfa_diagram_{pattern}.png"
        dot.render(filename.replace('.png', ''), cleanup=True)
        return filename
    
    def generate_all_images(self, pattern, dfa_data):
        """Generate all types of images for a pattern"""
        images = {}
        
        # Generate table images
        nfa_table = self.generate_nfa_table_image(pattern)
        dfa_table = self.generate_dfa_table_image(pattern, dfa_data)
        min_dfa_table = self.generate_min_dfa_table_image(pattern)
        
        # Generate diagram images
        nfa_diagram = self.generate_nfa_diagram(pattern, pattern)
        dfa_diagram = self.generate_dfa_diagram(pattern, dfa_data)
        min_dfa_diagram = self.generate_minimized_dfa_diagram(pattern)
        
        # Store all image paths
        images = {
            "nfa_table": nfa_table,
            "dfa_table": dfa_table,
            "min_dfa_table": min_dfa_table,
            "nfa_diagram": nfa_diagram,
            "dfa_diagram": dfa_diagram,
            "min_dfa_diagram": min_dfa_diagram
        }
        
        print(f"\nGenerated images for pattern '{pattern}':")
        for img_type, img_path in images.items():
            if img_path:
                print(f"  {img_type}: {os.path.basename(img_path)}")
        
        return images