import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk

from modules.regex_validator import RegexValidator
from modules.thompson_nfa import ThompsonNFA
from modules.subset_dfa import SubsetConstruction
from modules.minimizer import DFAMinimizer
from modules.simulator import StringSimulator 
from modules.visualizer import AutomataVisualizer


class ColorfulAutomataGUI:
    """Main GUI Application with Colorful Theme"""

    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Automata Theory - Regex to Automata Converter")
        self.root.geometry("1366x768")
        
        # Configure style for colorful theme
        self.setup_styles()

        # Data storage
        self.validator = None
        self.nfa = None
        self.dfa = None
        self.min_dfa = None
        self.simulator = None
        self.visualizer = AutomataVisualizer()

        # Current regex
        self.current_regex = "aba+bb+c(aaa+aa+a)*"
        self.alphabet = {'a', 'b', 'c'}

        # Setup GUI
        self.setup_gui()

    def setup_styles(self):
        """Configure colorful styles for widgets"""
        style = ttk.Style()
        
        # Configure colorful theme
        style.configure('Primary.TButton', 
                       background='#4CAF50', 
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       padding=(10, 5))
        
        style.configure('Success.TButton',
                       background='#2196F3',
                       foreground='white',
                       font=('Arial', 9, 'bold'))
        
        style.configure('Warning.TButton',
                       background='#FF9800',
                       foreground='white',
                       font=('Arial', 9, 'bold'))
        
        style.configure('Danger.TButton',
                       background='#F44336',
                       foreground='white',
                       font=('Arial', 9, 'bold'))
        
        style.configure('Info.TButton',
                       background='#9C27B0',
                       foreground='white',
                       font=('Arial', 9, 'bold'))
        
        style.configure('Secondary.TButton',
                       background='#607D8B',
                       foreground='white',
                       font=('Arial', 9, 'bold'))

    def setup_gui(self):
        """Setup all GUI components"""
        # Create main notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Tab 1: Regex Input & Validation
        self.tab_regex = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_regex, text="🎯 1. Regular Expression")
        self.setup_regex_tab()

        # Tab 2: NFA
        self.tab_nfa = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_nfa, text="🔮 2. NFA (Thompson)")
        self.setup_nfa_tab()

        # Tab 3: DFA
        self.tab_dfa = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_dfa, text="🏗️ 3. DFA (Subset Construction)")
        self.setup_dfa_tab()

        # Tab 4: Minimized DFA
        self.tab_min = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_min, text="📊 4. Minimized DFA")
        self.setup_minimized_tab()

        # Tab 5: String Simulation
        self.tab_sim = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sim, text="🎮 5. String Simulation")
        self.setup_simulation_tab()

        # Status bar
        self.status_bar = tk.Label(self.root, text="🚀 Ready", bd=1, relief=tk.SUNKEN, 
                                 anchor=tk.W, background='#E3F2FD', foreground='#1565C0',
                                 font=('Arial', 9, 'bold'))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_colorful_button(self, parent, text, command, style='Primary.TButton', width=None):
        """Create a colorful button with consistent styling"""
        btn = tk.Button(parent, text=text, command=command, 
                       font=('Arial', 9, 'bold'),
                       relief='raised', bd=2,
                       padx=12, pady=6)
        
        # Set colors based on style
        if style == 'Primary.TButton':
            btn.config(bg='#4CAF50', fg='white', activebackground='#45a049')
        elif style == 'Success.TButton':
            btn.config(bg='#2196F3', fg='white', activebackground='#1976D2')
        elif style == 'Warning.TButton':
            btn.config(bg='#FF9800', fg='white', activebackground='#F57C00')
        elif style == 'Danger.TButton':
            btn.config(bg='#F44336', fg='white', activebackground='#D32F2F')
        elif style == 'Info.TButton':
            btn.config(bg='#9C27B0', fg='white', activebackground='#7B1FA2')
        elif style == 'Secondary.TButton':
            btn.config(bg='#607D8B', fg='white', activebackground='#455A64')
        
        if width:
            btn.config(width=width)
            
        return btn

    def setup_regex_tab(self):
        """Setup Regular Expression tab"""
        frame = ttk.Frame(self.tab_regex, padding=10)
        frame.pack(fill='both', expand=True)

        # Title
        title = tk.Label(frame, text="🔍 Regular Expression Validator", 
                        font=('Arial', 16, 'bold'), foreground='#2E7D32')
        title.pack(pady=10)

        # Info
        info_text = """Assigned Regular Expression: aba + bb + c (aaa + aa + a)*
Alphabet: {a, b, c}

Note: You can use either '+' or '|' for union operations
Spaces are automatically handled

Example accepted strings:
• aba      • bb      • c      • ca
• caa      • caaa    • caaaa  • caaaaa

All other strings will be REJECTED"""
        
        info = tk.Label(frame, text=info_text, justify=tk.LEFT, 
                       background='#E8F5E8', foreground='#1B5E20',
                       font=('Courier', 10), padx=10, pady=10, bd=1, relief='solid')
        info.pack(pady=10, fill='x')

        # Input frame
        input_frame = tk.LabelFrame(frame, text="📝 Enter Regular Expression", 
                                  font=('Arial', 11, 'bold'), bg='#F5F5F5',
                                  padx=10, pady=10)
        input_frame.pack(pady=10, fill='x')

        self.regex_entry = tk.Entry(input_frame, font=('Courier', 12), 
                                   width=50, bd=2, relief='solid')
        self.regex_entry.pack(side=tk.LEFT, padx=5, fill='x', expand=True)
        self.regex_entry.insert(0, self.current_regex)

        validate_btn = self.create_colorful_button(input_frame, "✅ Validate RE", 
                                                 self.validate_regex, 'Success.TButton')
        validate_btn.pack(side=tk.LEFT, padx=5)

        # Output frame
        output_frame = tk.LabelFrame(frame, text="📊 Validation Result", 
                                   font=('Arial', 11, 'bold'), bg='#F5F5F5',
                                   padx=10, pady=10)
        output_frame.pack(pady=10, fill='both', expand=True)

        self.regex_output = scrolledtext.ScrolledText(output_frame, height=15, 
                                                     font=('Courier', 10),
                                                     bg='#FAFAFA', bd=2, relief='solid')
        self.regex_output.pack(fill='both', expand=True)

    def setup_nfa_tab(self):
        """Setup NFA tab"""
        frame = ttk.Frame(self.tab_nfa, padding=10)
        frame.pack(fill='both', expand=True)

        # Title
        title = tk.Label(frame, text="🔮 NFA - Thompson's Construction", 
                        font=('Arial', 16, 'bold'), foreground='#7B1FA2')
        title.pack(pady=10)

        # Button
        btn_frame = tk.Frame(frame, bg='#F5F5F5')
        btn_frame.pack(pady=10)

        generate_btn = self.create_colorful_button(btn_frame, "⚡ Generate NFA", 
                                                 self.generate_nfa, 'Info.TButton')
        generate_btn.pack(side=tk.LEFT, padx=5)

        # Paned window for table and diagram
        paned = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True, pady=10)

        # Left: Transition table
        left_frame = tk.LabelFrame(paned, text="📋 NFA Transition Table & ε-Closures", 
                                 font=('Arial', 11, 'bold'), bg='#F3E5F5',
                                 padx=10, pady=10)
        paned.add(left_frame, weight=1)

        self.nfa_table = scrolledtext.ScrolledText(left_frame, height=20, 
                                                  font=('Courier', 9),
                                                  bg='#FAFAFA', bd=2, relief='solid')
        self.nfa_table.pack(fill='both', expand=True)

        # Right: Diagram
        right_frame = tk.LabelFrame(paned, text="🖼️ NFA Diagram", 
                                  font=('Arial', 11, 'bold'), bg='#F3E5F5',
                                  padx=10, pady=10)
        paned.add(right_frame, weight=1)

        self.nfa_diagram_label = tk.Label(right_frame, bg='white', bd=2, relief='solid')
        self.nfa_diagram_label.pack(fill='both', expand=True)

    def setup_dfa_tab(self):
        """Setup DFA tab"""
        frame = ttk.Frame(self.tab_dfa, padding=10)
        frame.pack(fill='both', expand=True)

        # Title
        title = tk.Label(frame, text="🏗️ DFA - Subset Construction", 
                        font=('Arial', 16, 'bold'), foreground='#1976D2')
        title.pack(pady=10)

        # Button
        btn_frame = tk.Frame(frame, bg='#F5F5F5')
        btn_frame.pack(pady=10)

        generate_btn = self.create_colorful_button(btn_frame, "⚡ Generate DFA", 
                                                 self.generate_dfa, 'Success.TButton')
        generate_btn.pack(side=tk.LEFT, padx=5)

        # Paned window
        paned = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True, pady=10)

        # Left: Table
        left_frame = tk.LabelFrame(paned, text="📋 DFA Transition Table", 
                                 font=('Arial', 11, 'bold'), bg='#E3F2FD',
                                 padx=10, pady=10)
        paned.add(left_frame, weight=1)

        self.dfa_table = scrolledtext.ScrolledText(left_frame, height=20, 
                                                  font=('Courier', 9),
                                                  bg='#FAFAFA', bd=2, relief='solid')
        self.dfa_table.pack(fill='both', expand=True)

        # Right: Diagram
        right_frame = tk.LabelFrame(paned, text="🖼️ DFA Diagram", 
                                  font=('Arial', 11, 'bold'), bg='#E3F2FD',
                                  padx=10, pady=10)
        paned.add(right_frame, weight=1)

        self.dfa_diagram_label = tk.Label(right_frame, bg='white', bd=2, relief='solid')
        self.dfa_diagram_label.pack(fill='both', expand=True)

    def setup_minimized_tab(self):
        """Setup Minimized DFA tab"""
        frame = ttk.Frame(self.tab_min, padding=10)
        frame.pack(fill='both', expand=True)

        # Title
        title = tk.Label(frame, text="📊 Minimized DFA - Table Filling Algorithm", 
                        font=('Arial', 16, 'bold'), foreground='#D84315')
        title.pack(pady=10)

        # Button
        btn_frame = tk.Frame(frame, bg='#F5F5F5')
        btn_frame.pack(pady=10)

        minimize_btn = self.create_colorful_button(btn_frame, "⚡ Minimize DFA", 
                                                 self.minimize_dfa, 'Warning.TButton')
        minimize_btn.pack(side=tk.LEFT, padx=5)

        # Paned window
        paned = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True, pady=10)

        # Left: Table
        left_frame = tk.LabelFrame(paned, text="📋 Minimized DFA Transition Table", 
                                 font=('Arial', 11, 'bold'), bg='#FFF3E0',
                                 padx=10, pady=10)
        paned.add(left_frame, weight=1)

        self.min_table = scrolledtext.ScrolledText(left_frame, height=20, 
                                                  font=('Courier', 9),
                                                  bg='#FAFAFA', bd=2, relief='solid')
        self.min_table.pack(fill='both', expand=True)

        # Right: Diagram
        right_frame = tk.LabelFrame(paned, text="🖼️ Minimized DFA Diagram", 
                                  font=('Arial', 11, 'bold'), bg='#FFF3E0',
                                  padx=10, pady=10)
        paned.add(right_frame, weight=1)

        self.min_diagram_label = tk.Label(right_frame, bg='white', bd=2, relief='solid')
        self.min_diagram_label.pack(fill='both', expand=True)

    def setup_simulation_tab(self):
        """Setup String Simulation tab"""
        frame = ttk.Frame(self.tab_sim, padding=10)
        frame.pack(fill='both', expand=True)

        # Title
        title = tk.Label(frame, text="🎮 String Simulation on Minimized DFA", 
                        font=('Arial', 16, 'bold'), foreground='#00838F')
        title.pack(pady=10)

        # Input frame
        input_frame = tk.LabelFrame(frame, text="🔤 Test String", 
                                  font=('Arial', 11, 'bold'), bg='#E0F7FA',
                                  padx=10, pady=10)
        input_frame.pack(pady=10, fill='x')

        self.sim_entry = tk.Entry(input_frame, font=('Courier', 12), 
                                 width=40, bd=2, relief='solid')
        self.sim_entry.pack(side=tk.LEFT, padx=5, fill='x', expand=True)
        self.sim_entry.insert(0, "aba")

        simulate_btn = self.create_colorful_button(input_frame, "🎯 Simulate", 
                                                 self.simulate_string, 'Primary.TButton')
        simulate_btn.pack(side=tk.LEFT, padx=5)

        # Quick test buttons - Accepted strings
        accepted_frame = tk.LabelFrame(frame, text="✅ Accepted Strings (Click to test)", 
                                     font=('Arial', 11, 'bold'), bg='#E8F5E8',
                                     padx=10, pady=10)
        accepted_frame.pack(pady=10, fill='x')

        accepted_strings = ["aba", "bb", "c", "ca", "caa", "caaa", "caaaa"]
        accepted_btn_frame = tk.Frame(accepted_frame, bg='#E8F5E8')
        accepted_btn_frame.pack()
        
        for i, test_str in enumerate(accepted_strings):
            btn = self.create_colorful_button(accepted_btn_frame, test_str,
                                           lambda s=test_str: self.quick_test(s), 
                                           'Success.TButton', width=6)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Quick test buttons - Rejected strings
        rejected_frame = tk.LabelFrame(frame, text="❌ Rejected Strings (Click to test)", 
                                     font=('Arial', 11, 'bold'), bg='#FFEBEE',
                                     padx=10, pady=10)
        rejected_frame.pack(pady=10, fill='x')

        rejected_strings = ["ab", "a", "b", "abc", "bba", "cab", "caab", ""]
        rejected_btn_frame = tk.Frame(rejected_frame, bg='#FFEBEE')
        rejected_btn_frame.pack()
        
        for i, test_str in enumerate(rejected_strings):
            btn_text = test_str if test_str else "''"
            btn = self.create_colorful_button(rejected_btn_frame, btn_text,
                                           lambda s=test_str: self.quick_test(s), 
                                           'Danger.TButton', width=6)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Comprehensive test button
        test_btn_frame = tk.Frame(frame, bg='#F5F5F5')
        test_btn_frame.pack(pady=10)
        
        comprehensive_btn = self.create_colorful_button(test_btn_frame, 
                                                      "📋 Run Comprehensive Tests", 
                                                      self.run_comprehensive_tests,
                                                      'Info.TButton')
        comprehensive_btn.pack(side=tk.LEFT, padx=5)

        # Output frame
        output_frame = tk.LabelFrame(frame, text="📜 Simulation Trace", 
                                   font=('Arial', 11, 'bold'), bg='#F5F5F5',
                                   padx=10, pady=10)
        output_frame.pack(pady=10, fill='both', expand=True)

        self.sim_output = scrolledtext.ScrolledText(output_frame, height=20, 
                                                   font=('Courier', 10),
                                                   bg='#FAFAFA', bd=2, relief='solid')
        self.sim_output.pack(fill='both', expand=True)

    # Event handlers (keep the same as before, just update class reference)
    def validate_regex(self):
        """Validate regular expression"""
        regex = self.regex_entry.get().strip()
        self.current_regex = regex

        self.regex_output.delete(1.0, tk.END)

        if not regex:
            self.regex_output.insert(tk.END, "❌ ERROR: Regular expression cannot be empty\n")
            self.status_bar.config(text="❌ Validation failed")
            return

        # Validate
        self.validator = RegexValidator(self.alphabet)
        is_valid, message = self.validator.validate(regex)

        if is_valid:
            self.regex_output.insert(tk.END, f"✅ VALID: {message}\n\n", 'success')
            self.regex_output.insert(tk.END, f"Original Regex: {regex}\n")

            # Preprocess
            preprocessed = self.validator.preprocess(regex)
            self.regex_output.insert(tk.END, f"Preprocessed (with explicit concatenation): {preprocessed}\n")

            self.status_bar.config(text="✅ Validation successful - Ready to generate NFA")

            # Configure tag
            self.regex_output.tag_config('success', foreground='#2E7D32', font=('Courier', 10, 'bold'))
        else:
            self.regex_output.insert(tk.END, f"❌ INVALID: {message}\n", 'error')
            self.status_bar.config(text="❌ Validation failed")

            # Configure tag
            self.regex_output.tag_config('error', foreground='#C62828', font=('Courier', 10, 'bold'))

    def generate_nfa(self):
        """Generate NFA from regex"""
        if not self.validator:
            messagebox.showerror("Error", "Please validate the regular expression first!")
            return

        regex = self.regex_entry.get().strip()

        try:
            # Preprocess
            preprocessed = self.validator.preprocess(regex)

            # Build NFA
            thompson = ThompsonNFA(preprocessed)
            self.nfa = thompson.build()

            # Display transition table
            self.nfa_table.delete(1.0, tk.END)
            self.nfa_table.insert(tk.END, "NFA Transition Table:\n")
            self.nfa_table.insert(tk.END, "=" * 60 + "\n\n")

            table = self.nfa.get_transition_table()
            for state, transitions in sorted(table.items()):
                self.nfa_table.insert(tk.END, f"{state}:\n")
                for symbol, next_states in sorted(transitions.items()):
                    next_str = ', '.join(next_states)
                    self.nfa_table.insert(tk.END, f"  {symbol} → {{{next_str}}}\n")
                self.nfa_table.insert(tk.END, "\n")

            # Display epsilon closures
            self.nfa_table.insert(tk.END, "\n" + "=" * 60 + "\n")
            self.nfa_table.insert(tk.END, "ε-Closures:\n")
            self.nfa_table.insert(tk.END, "=" * 60 + "\n\n")

            closures = self.nfa.get_epsilon_closures()
            for state, closure in closures.items():
                closure_str = ', '.join(closure)
                self.nfa_table.insert(tk.END, f"ε-closure({state}) = {{{closure_str}}}\n")

            # Generate diagram
            try:
                diagram_path = self.visualizer.visualize_nfa(self.nfa, 'nfa')
                self.display_image(self.nfa_diagram_label, diagram_path)
            except ImportError as ie:
                self.nfa_diagram_label.config(
                    text=f"⚠ Diagram not available\n\n{str(ie)}\n\nNote: The NFA was generated successfully!\nTransition table is shown on the left.",
                    font=('Arial', 10),
                    foreground='orange',
                    wraplength=400,
                    justify='left'
                )
            except Exception as e:
                self.nfa_diagram_label.config(
                    text=f"⚠ Diagram generation failed:\n{str(e)}\n\nNote: The NFA was generated successfully!\nTransition table is shown on the left.",
                    font=('Arial', 10),
                    foreground='orange',
                    wraplength=400,
                    justify='left'
                )

            self.status_bar.config(text="✅ NFA generated successfully")
            messagebox.showinfo("Success", "NFA generated successfully!\n\n(Diagram may not be available if Graphviz is not installed)")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate NFA: {str(e)}")
            self.status_bar.config(text="❌ NFA generation failed")

    def generate_dfa(self):
        """Generate DFA from NFA"""
        if not self.nfa:
            messagebox.showerror("Error", "Please generate NFA first!")
            return

        try:
            # Build DFA
            subset = SubsetConstruction(self.nfa, self.alphabet)
            self.dfa = subset.build()

            # Display transition table
            self.dfa_table.delete(1.0, tk.END)
            self.dfa_table.insert(tk.END, "DFA Transition Table:\n")
            self.dfa_table.insert(tk.END, "=" * 80 + "\n\n")

            table = self.dfa.get_transition_table()
            for state, data in sorted(table.items()):
                flags = data.get('_flags', [])
                composition = data.get('_composition', '')

                flag_str = f" [{', '.join(flags)}]" if flags else ""
                self.dfa_table.insert(tk.END, f"{state}{flag_str} = {composition}\n")

                for symbol in sorted(self.alphabet):
                    if symbol in data:
                        self.dfa_table.insert(tk.END, f"  {symbol} → {data[symbol]}\n")

                self.dfa_table.insert(tk.END, "\n")

            # Generate diagram
            try:
                diagram_path = self.visualizer.visualize_dfa(self.dfa, 'dfa')
                self.display_image(self.dfa_diagram_label, diagram_path)
            except ImportError as ie:
                self.dfa_diagram_label.config(
                    text=f"⚠ Diagram not available\n\n{str(ie)}\n\nNote: The DFA was generated successfully!\nTransition table is shown on the left.",
                    font=('Arial', 10),
                    foreground='orange',
                    wraplength=400,
                    justify='left'
                )
            except Exception as e:
                self.dfa_diagram_label.config(
                    text=f"⚠ Diagram generation failed:\n{str(e)}\n\nNote: The DFA was generated successfully!\nTransition table is shown on the left.",
                    font=('Arial', 10),
                    foreground='orange',
                    wraplength=400,
                    justify='left'
                )

            self.status_bar.config(text="✅ DFA generated successfully")
            messagebox.showinfo("Success", "DFA generated successfully!\n\n(Diagram may not be available if Graphviz is not installed)")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate DFA: {str(e)}")
            self.status_bar.config(text="❌ DFA generation failed")

    def minimize_dfa(self):
        """Minimize DFA"""
        if not self.dfa:
            messagebox.showerror("Error", "Please generate DFA first!")
            return

        try:
            # Minimize
            minimizer = DFAMinimizer(self.dfa)
            self.min_dfa = minimizer.minimize()

            # Display transition table
            self.min_table.delete(1.0, tk.END)
            self.min_table.insert(tk.END, "Minimized DFA Transition Table:\n")
            self.min_table.insert(tk.END, "=" * 80 + "\n\n")

            table = self.min_dfa.get_transition_table()
            for state, data in sorted(table.items()):
                flags = data.get('_flags', [])
                merged = data.get('_merged_from', '')

                flag_str = f" [{', '.join(flags)}]" if flags else ""
                merge_str = f" (merged from: {merged})" if merged else ""
                self.min_table.insert(tk.END, f"{state}{flag_str}{merge_str}\n")

                for symbol in sorted(self.alphabet):
                    if symbol in data:
                        self.min_table.insert(tk.END, f"  {symbol} → {data[symbol]}\n")

                self.min_table.insert(tk.END, "\n")

            # Show distinguishability table
            self.min_table.insert(tk.END, "\n" + "=" * 80 + "\n")
            self.min_table.insert(tk.END, "Distinguishability Table (✓ = distinguishable, ✗ = equivalent):\n")
            self.min_table.insert(tk.END, "=" * 80 + "\n\n")

            dist_table = minimizer.get_distinguishability_table()
            for pair, mark in dist_table.items():
                self.min_table.insert(tk.END, f"{pair}: {mark}\n")

            # Generate diagram
            try:
                diagram_path = self.visualizer.visualize_minimized_dfa(self.min_dfa, 'minimized_dfa')
                self.display_image(self.min_diagram_label, diagram_path)
            except ImportError as ie:
                self.min_diagram_label.config(
                    text=f"⚠ Diagram not available\n\n{str(ie)}\n\nNote: The minimized DFA was generated successfully!\nTransition table is shown on the left.",
                    font=('Arial', 10),
                    foreground='orange',
                    wraplength=400,
                    justify='left'
                )
            except Exception as e:
                self.min_diagram_label.config(
                    text=f"⚠ Diagram generation failed:\n{str(e)}\n\nNote: The minimized DFA was generated successfully!\nTransition table is shown on the left.",
                    font=('Arial', 10),
                    foreground='orange',
                    wraplength=400,
                    justify='left'
                )

            # Setup simulator
            self.simulator = StringSimulator(self.min_dfa)

            self.status_bar.config(text="✅ DFA minimized successfully")
            messagebox.showinfo("Success", "DFA minimized successfully!\n\n(Diagram may not be available if Graphviz is not installed)")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to minimize DFA: {str(e)}")
            self.status_bar.config(text="❌ DFA minimization failed")

    def simulate_string(self):
        """Simulate string on minimized DFA"""
        if not self.min_dfa or not self.simulator:
            messagebox.showerror("Error", "Please generate and minimize DFA first!")
            return

        test_string = self.sim_entry.get().strip()

        try:
            accepted, trace, error = self.simulator.simulate(test_string)

            self.sim_output.delete(1.0, tk.END)
            self.sim_output.insert(tk.END, f"Input String: '{test_string}'\n")
            self.sim_output.insert(tk.END, "=" * 80 + "\n\n")

            if error:
                self.sim_output.insert(tk.END, f"❌ ERROR: {error}\n\n")

            # Display trace
            for entry in trace:
                if 'error' in entry and entry['error']:
                    self.sim_output.insert(tk.END, f"  {entry['description']}\n", 'error')
                elif 'accepted' in entry:
                    if entry['accepted']:
                        self.sim_output.insert(tk.END, f"\n🎉 {entry['description']}\n", 'success')
                    else:
                        self.sim_output.insert(tk.END, f"\n❌ {entry['description']}\n", 'error')
                else:
                    self.sim_output.insert(tk.END, f"  {entry['description']}\n")

            # Add pattern explanation
            self.sim_output.insert(tk.END, "\n" + "=" * 80 + "\n")
            self.sim_output.insert(tk.END, "📋 Pattern Explanation:\n")
            self.sim_output.insert(tk.END, "- 'aba' (exactly)\n")
            self.sim_output.insert(tk.END, "- 'bb' (exactly)\n") 
            self.sim_output.insert(tk.END, "- 'c' followed by any number of 'a's (0 or more)\n")
            self.sim_output.insert(tk.END, "Any other pattern will be REJECTED\n")

            # Configure tags
            self.sim_output.tag_config('success', foreground='#2E7D32', font=('Courier', 10, 'bold'))
            self.sim_output.tag_config('error', foreground='#C62828', font=('Courier', 10, 'bold'))

            status = "✅ ACCEPTED" if accepted else "❌ REJECTED"
            self.status_bar.config(text=f"Simulation complete - String {status}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to simulate string: {str(e)}")
            self.status_bar.config(text="❌ Simulation failed")

    def quick_test(self, test_string):
        """Quick test with predefined string"""
        self.sim_entry.delete(0, tk.END)
        self.sim_entry.insert(0, test_string)
        self.simulate_string()

    def run_comprehensive_tests(self):
        """Run comprehensive tests to verify automata behavior"""
        if not self.min_dfa or not self.simulator:
            messagebox.showerror("Error", "Please generate and minimize DFA first!")
            return

        try:
            # Define comprehensive test cases
            test_cases = [
                # Accepted strings
                ("aba", True, "Exact match for 'aba'"),
                ("bb", True, "Exact match for 'bb'"),
                ("c", True, "c followed by zero a's"),
                ("ca", True, "c followed by one a"),
                ("caa", True, "c followed by two a's"),
                ("caaa", True, "c followed by three a's"),
                ("caaaa", True, "c followed by four a's"),
                ("caaaaa", True, "c followed by five a's"),
                
                # Rejected strings
                ("", False, "Empty string"),
                ("a", False, "Single 'a'"),
                ("b", False, "Single 'b'"),
                ("ab", False, "Incomplete 'aba'"),
                ("ba", False, "Wrong pattern"),
                ("abc", False, "Extra character after 'aba' pattern"),
                ("abb", False, "Wrong pattern"),
                ("bba", False, "Extra character after 'bb'"),
                ("bbb", False, "Too many b's"),
                ("bc", False, "Wrong pattern"),
                ("ac", False, "Wrong pattern"),
                ("cab", False, "Non-'a' character after c"),
                ("cba", False, "Non-'a' character after c"),
                ("caab", False, "Mixed characters after c"),
                ("caba", False, "Mixed characters after c"),
                ("abac", False, "Extra character"),
                ("bbcc", False, "Extra characters"),
                ("d", False, "Invalid character"),
                ("abcde", False, "Multiple invalid characters"),
            ]
            
            self.sim_output.delete(1.0, tk.END)
            self.sim_output.insert(tk.END, "📋 Comprehensive Test Results\n")
            self.sim_output.insert(tk.END, "=" * 80 + "\n\n")
            
            passed = 0
            failed = 0
            
            for test_string, expected, description in test_cases:
                accepted, trace, error = self.simulator.simulate(test_string)
                status = "PASS" if accepted == expected else "FAIL"
                
                if status == "PASS":
                    passed += 1
                    self.sim_output.insert(tk.END, f"✅ PASS: '{test_string}' - {description}\n", 'success')
                else:
                    failed += 1
                    self.sim_output.insert(tk.END, f"❌ FAIL: '{test_string}' - {description}\n", 'error')
                    self.sim_output.insert(tk.END, f"   Expected: {'ACCEPTED' if expected else 'REJECTED'}\n")
                    self.sim_output.insert(tk.END, f"   Actual: {'ACCEPTED' if accepted else 'REJECTED'}\n")
            
            self.sim_output.insert(tk.END, "\n" + "=" * 80 + "\n")
            self.sim_output.insert(tk.END, f"📊 Summary: {passed} passed, {failed} failed out of {len(test_cases)} tests\n")
            
            if failed == 0:
                self.sim_output.insert(tk.END, "🎉 All tests passed! The automata correctly accepts/rejects strings.\n", 'success')
            else:
                self.sim_output.insert(tk.END, "❌ Some tests failed. The automata may have issues.\n", 'error')
            
            # Configure tags
            self.sim_output.tag_config('success', foreground='#2E7D32', font=('Courier', 10, 'bold'))
            self.sim_output.tag_config('error', foreground='#C62828', font=('Courier', 10, 'bold'))
            
            self.status_bar.config(text=f"📋 Comprehensive tests completed: {passed} passed, {failed} failed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run comprehensive tests: {str(e)}")

    def display_image(self, label, image_path):
        """Display image in label"""
        try:
            image = Image.open(image_path)

            # Resize if too large
            max_width, max_height = 600, 500
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo  # Keep a reference

        except Exception as e:
            label.config(text=f"❌ Error loading image: {str(e)}")


def run_gui():
    """Run the GUI application"""
    root = tk.Tk()
    app = ColorfulAutomataGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()