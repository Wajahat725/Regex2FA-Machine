# gui.py - Simplified version without All Images button
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk
import os
import sys
import io

# Import your modules
from Modules.nfa import test_string_belongs_to_regex
from Modules.dfa import DFASimulator
from Modules.image_generator import AutomataImageGenerator

class RegexAutomataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Regex to Automata Converter")
        self.root.geometry("1400x800")
        
        self.simulator = DFASimulator()
        self.image_generator = AutomataImageGenerator()
        
        # Store image references
        self.image_references = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="Regular Expression to Automata Converter", 
                              font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Regex display
        regex_frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=2)
        regex_frame.pack(pady=10, padx=20, fill=tk.X)
        
        regex_label = tk.Label(regex_frame, text="Regular Expression: aba + bb + c(aaa+aa+a)*", 
                              font=("Arial", 14))
        regex_label.pack(pady=10)
        
        # Input section
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="Enter String to Test:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(input_frame, textvariable=self.input_var, font=("Arial", 12), width=30)
        self.input_entry.grid(row=0, column=1, padx=5)
        
        test_button = tk.Button(input_frame, text="Test String", command=self.test_string, 
                               font=("Arial", 12), bg="lightblue")
        test_button.grid(row=0, column=2, padx=5)
        
        clear_button = tk.Button(input_frame, text="Clear", command=self.clear_all, 
                                font=("Arial", 12))
        clear_button.grid(row=0, column=3, padx=5)
        
        # Result display
        result_frame = tk.Frame(self.root)
        result_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(result_frame, text="Result:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.result_text = scrolledtext.ScrolledText(result_frame, height=4, width=140, 
                                                    font=("Courier", 10))
        self.result_text.pack(pady=5)
        
        # Tabbed display
        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_tabs(notebook)
    
    def create_tabs(self, notebook):
        # NFA Tables Tab
        self.setup_nfa_tab(notebook)
        
        # DFA Tables Tab
        self.setup_dfa_tab(notebook)
        
        # Minimized DFA Tables Tab
        self.setup_min_dfa_tab(notebook)
        
        # Simulation Tab
        self.setup_simulation_tab(notebook)
    
    def setup_nfa_tab(self, notebook):
        """Setup NFA tab with text table"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="NFA Table")
        
        # Text area for NFA table
        self.nfa_text = scrolledtext.ScrolledText(tab, width=140, height=35,
                                                 font=("Courier", 10))
        self.nfa_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Image label for NFA table image
        self.nfa_image_label = tk.Label(tab, text="NFA Table Image will appear here",
                                       font=("Arial", 12))
        self.nfa_image_label.pack(pady=10)
    
    def setup_dfa_tab(self, notebook):
        """Setup DFA tab with text table"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="DFA Table")
        
        # Text area for DFA table
        self.dfa_text = scrolledtext.ScrolledText(tab, width=140, height=35,
                                                 font=("Courier", 10))
        self.dfa_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Image label for DFA table image
        self.dfa_image_label = tk.Label(tab, text="DFA Table Image will appear here",
                                       font=("Arial", 12))
        self.dfa_image_label.pack(pady=10)
    
    def setup_min_dfa_tab(self, notebook):
        """Setup Minimized DFA tab with text table"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Minimized DFA Table")
        
        # Text area for Minimized DFA table
        self.min_dfa_text = scrolledtext.ScrolledText(tab, width=140, height=35,
                                                     font=("Courier", 10))
        self.min_dfa_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Image label for Minimized DFA table image
        self.min_dfa_image_label = tk.Label(tab, text="Minimized DFA Table Image will appear here",
                                           font=("Arial", 12))
        self.min_dfa_image_label.pack(pady=10)
    
    def setup_simulation_tab(self, notebook):
        """Setup simulation tab"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Simulation")
        
        self.sim_text = scrolledtext.ScrolledText(tab, width=140, height=40,
                                                 font=("Courier", 10))
        self.sim_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def load_and_display_image(self, image_path, label_widget, max_size=(600, 400)):
        """Load and display an image in a label widget"""
        try:
            if os.path.exists(image_path):
                # Open and resize image
                img = Image.open(image_path)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(img)
                
                # Store reference to prevent garbage collection
                self.image_references[image_path] = photo
                
                # Update label
                label_widget.config(image=photo)
                label_widget.image = photo
                label_widget.config(text="")  # Clear text
            else:
                label_widget.config(text=f"Image not found:\n{image_path}", image='')
        except Exception as e:
            label_widget.config(text=f"Error loading image:\n{str(e)}", image='')
    
    def test_string(self):
        input_string = self.input_var.get().strip()
        
        if not input_string:
            messagebox.showwarning("Input Required", "Please enter a string to test.")
            return
        
        # Clear previous results
        self.clear_all_displays()
        
        # Test the string
        result = test_string_belongs_to_regex(input_string)
        
        # Display result
        self.result_text.delete(1.0, tk.END)
        if result:
            self.result_text.insert(tk.END, f"✓ String '{input_string}' - ACCEPTED\n")
            self.result_text.insert(tk.END, f"Belongs to pattern: {result}\n")
            
            # Get DFA data for image generation
            dfa_data = self.simulator.get_dfa_data(result)
            
            if dfa_data:
                # Generate all images
                all_images = self.image_generator.generate_all_images(result, dfa_data)
                
                # Display text tables
                self.display_nfa_table_text(result)
                self.display_dfa_table_text(result)
                self.display_min_dfa_table_text(result)
                
                # Display table images
                if all_images.get("nfa_table"):
                    self.load_and_display_image(all_images["nfa_table"], self.nfa_image_label)
                
                if all_images.get("dfa_table"):
                    self.load_and_display_image(all_images["dfa_table"], self.dfa_image_label)
                
                if all_images.get("min_dfa_table"):
                    self.load_and_display_image(all_images["min_dfa_table"], self.min_dfa_image_label)
                
                # Run simulation
                self.run_simulation(result, input_string)
            else:
                self.result_text.insert(tk.END, "Error: Could not generate DFA data\n")
        else:
            self.result_text.insert(tk.END, f"✗ String '{input_string}' - REJECTED\n")
            self.result_text.insert(tk.END, "Does not belong to the regular expression\n")
    
    def display_nfa_table_text(self, pattern):
        """Display NFA table in text form"""
        try:
            if pattern == "aba":
                from Modules.nfa import display_aba_nfa_table
                output = self.capture_output(display_aba_nfa_table)
            elif pattern == "bb":
                from Modules.nfa import display_bb_nfa_table
                output = self.capture_output(display_bb_nfa_table)
            elif pattern == "c_only":
                from Modules.nfa import display_c_only_nfa_table
                output = self.capture_output(display_c_only_nfa_table)
            elif pattern == "ca":
                from Modules.nfa import display_ca_nfa_table
                output = self.capture_output(display_ca_nfa_table)
            elif pattern == "caa":
                from Modules.nfa import display_caa_nfa_table
                output = self.capture_output(display_caa_nfa_table)
            elif pattern == "caaa":
                from Modules.nfa import display_caaa_nfa_table
                output = self.capture_output(display_caaa_nfa_table)
            elif pattern == "c_kleene_star":
                from Modules.nfa import display_c_kleene_star_nfa_table
                output = self.capture_output(display_c_kleene_star_nfa_table)
            else:
                output = f"No NFA table available for pattern: {pattern}\n"
            
            self.nfa_text.delete(1.0, tk.END)
            self.nfa_text.insert(tk.END, output)
            
        except Exception as e:
            self.nfa_text.delete(1.0, tk.END)
            self.nfa_text.insert(tk.END, f"Error displaying NFA table: {str(e)}\n")
    
    def display_dfa_table_text(self, pattern):
        """Display DFA table in text form"""
        try:
            if pattern == "aba":
                from Modules.dfa import display_aba_dfa
                output = self.capture_output(display_aba_dfa)
            elif pattern == "bb":
                from Modules.dfa import display_bb_dfa
                output = self.capture_output(display_bb_dfa)
            elif pattern == "c_only":
                from Modules.dfa import display_c_only_dfa
                output = self.capture_output(display_c_only_dfa)
            elif pattern == "ca":
                from Modules.dfa import display_ca_dfa
                output = self.capture_output(display_ca_dfa)
            elif pattern == "caa":
                from Modules.dfa import display_caa_dfa
                output = self.capture_output(display_caa_dfa)
            elif pattern == "caaa":
                from Modules.dfa import display_caaa_dfa
                output = self.capture_output(display_caaa_dfa)
            elif pattern == "c_kleene_star":
                from Modules.dfa import display_c_kleene_star_dfa
                output = self.capture_output(display_c_kleene_star_dfa)
            else:
                output = f"No DFA table available for pattern: {pattern}\n"
            
            self.dfa_text.delete(1.0, tk.END)
            self.dfa_text.insert(tk.END, output)
            
        except Exception as e:
            self.dfa_text.delete(1.0, tk.END)
            self.dfa_text.insert(tk.END, f"Error displaying DFA table: {str(e)}\n")
    
    def display_min_dfa_table_text(self, pattern):
        """Display Minimized DFA table in text form"""
        try:
            # Try importing from minimized_dfa (your file name)
            if pattern == "aba":
                from Modules.minimized_dfa import display_aba_minimized_dfa
                output = self.capture_output(display_aba_minimized_dfa)
            elif pattern == "bb":
                from Modules.minimized_dfa import display_bb_minimized_dfa
                output = self.capture_output(display_bb_minimized_dfa)
            elif pattern == "c_only":
                from Modules.minimized_dfa import display_c_only_minimized_dfa
                output = self.capture_output(display_c_only_minimized_dfa)
            elif pattern == "ca":
                from Modules.minimized_dfa import display_ca_minimized_dfa
                output = self.capture_output(display_ca_minimized_dfa)
            elif pattern == "caa":
                from Modules.minimized_dfa import display_caa_minimized_dfa
                output = self.capture_output(display_caa_minimized_dfa)
            elif pattern == "caaa":
                from Modules.minimized_dfa import display_caaa_minimized_dfa
                output = self.capture_output(display_caaa_minimized_dfa)
            elif pattern == "c_kleene_star":
                from Modules.minimized_dfa import display_c_kleene_star_minimized_dfa
                output = self.capture_output(display_c_kleene_star_minimized_dfa)
            else:
                output = f"No Minimized DFA table available for pattern: {pattern}\n"
            
            self.min_dfa_text.delete(1.0, tk.END)
            self.min_dfa_text.insert(tk.END, output)
            
        except ImportError as e:
            self.min_dfa_text.delete(1.0, tk.END)
            self.min_dfa_text.insert(tk.END, f"Import error: {str(e)}\nMake sure minimized_dfa.py exists\n")
        except Exception as e:
            self.min_dfa_text.delete(1.0, tk.END)
            self.min_dfa_text.insert(tk.END, f"Error displaying Minimized DFA table: {str(e)}\n")
    
    def capture_output(self, func):
        """Capture print output from a function"""
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            func()
            output = sys.stdout.getvalue()
        except Exception as e:
            output = f"Error executing function: {str(e)}"
        finally:
            sys.stdout = old_stdout
        
        return output
    
    def run_simulation(self, pattern, input_string):
        """Run DFA simulation and display steps"""
        self.sim_text.delete(1.0, tk.END)
        
        steps = self.simulator.simulate_dfa(pattern, input_string)
        
        for step in steps:
            self.sim_text.insert(tk.END, step + "\n")
    
    def clear_all_displays(self):
        """Clear all text and image displays"""
        # Clear text displays
        self.nfa_text.delete(1.0, tk.END)
        self.dfa_text.delete(1.0, tk.END)
        self.min_dfa_text.delete(1.0, tk.END)
        self.sim_text.delete(1.0, tk.END)
        
        # Clear image labels
        self.nfa_image_label.config(text="NFA Table Image will appear here", image='')
        self.dfa_image_label.config(text="DFA Table Image will appear here", image='')
        self.min_dfa_image_label.config(text="Minimized DFA Table Image will appear here", image='')
        
        # Clear image references
        self.image_references.clear()
    
    def clear_all(self):
        """Clear all input and displays"""
        self.input_var.set("")
        self.result_text.delete(1.0, tk.END)
        self.clear_all_displays()

def run_gui():
    root = tk.Tk()
    app = RegexAutomataGUI(root)
    root.mainloop()

if __name__ == "__main__":
    # Install required packages if not already installed
    # pip install graphviz pillow
    run_gui()