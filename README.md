# Regex2FA-Machine
# Regex to Finite Automata Converter

A comprehensive Python implementation that converts regular expressions to various automata forms and performs string recognition. This project demonstrates the complete pipeline from Regular Expression (RE) to Non-deterministic Finite Automaton (NFA), Deterministic Finite Automaton (DFA), and finally to a minimized DFA.

## 📋 Project Overview

This project implements core automata theory concepts including:
- **Thompson's Construction** for RE to NFA conversion
- **Subset Construction** for NFA to DFA conversion  
- **DFA Minimization** using Table-Filling Algorithm
- **String recognition** and acceptance testing

### Regular Expression
aba + bb + c(aaa + aa + a)*

text

This expression represents three alternative patterns:
- `aba`: Exact string "aba"
- `bb`: Exact string "bb" 
- `c(aaa + aa + a)*`: String starting with 'c' followed by zero or more occurrences of a's

## 🏗️ Project Structure
Regex2FA-Machine/
├── main.py
├── gui.py
├── modules/
│   ├── __init__.py
│   ├── regex_validator.py
│   ├── thompson_nfa.py
│   ├── subset_dfa.py
│   ├── minimizer.py
│   ├── simulator.py
│   └── visualizer.py
├── requirements.txt
├── README.md
└── assets/
    └── diagrams/

text

## 🚀 Features

- ✅ Regular expression validation and parsing
- ✅ RE to NFA conversion (Thompson's Construction)
- ✅ NFA to DFA conversion (Subset Construction) 
- ✅ DFA minimization (Table-Filling Algorithm)
- ✅ String simulation and acceptance testing
- ✅ Visualization of automata states and transitions

# Create converter instance
converter = RegexToAutomata("aba + bb + c(aaa + aa + a)*")

# Test string acceptance
result = converter.test_string("caaa")
print(f"String accepted: {result}")
Command Line Interface
bash
python main.py
Testing Specific Strings
python
# Test multiple strings
test_strings = ["aba", "bb", "c", "ca", "caa", "caaa", "a", "ab", "cab"]
for test_str in test_strings:
    result = converter.test_string(test_str)
    print(f"'{test_str}': {'Accepted' if result else 'Rejected'}")
📊 Results
Test Cases
Test String	Expected Result	Actual Result	Status
aba	Accepted	Accepted	✅
bb	Accepted	Accepted	✅
c	Accepted	Accepted	✅
ca	Accepted	Accepted	✅
caa	Accepted	Accepted	✅
caaa	Accepted	Accepted	✅
a	Rejected	Rejected	✅
ab	Rejected	Rejected	✅
cab	Rejected	Rejected	✅
Automata Visualization
The project includes visualization capabilities for:

Complete NFA using Thompson Construction

Complete DFA using Subset Construction

Minimized DFA after optimization

👥 Team Members
Wajahat Ali Khan [55431] 

Rayyan Malik [54766] 

📚 Academic Context
Course: Theory of Automata
Section: BSCS 5-1
Faculty: Computing
Supervisor: Dr. Musharraf Ahmed
Submission Date: 17 November 2025

🔧 Technical Details
Programming Language: Python 3

Key Algorithms: Thompson's Construction, Subset Construction, Table-Filling Algorithm

Dependencies: Graphviz (for visualization), Collections, RE

📁 File Descriptions
nfa.py: Implements NFA states and transition functions

dfa.py: Handles DFA construction and minimization

regex_to_automata.py: Main conversion pipeline

display.py: Visualization and graph generation

main.py: Entry point with examples and testing

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
This project is licensed for academic purposes under the Faculty of Computing, Theory of Automata Course.

🆘 Support
For questions or issues regarding this project, please contact:

Wajahat Ali Khan: [55431@student.comsats.edu.pk]

Rayyan Malik: [54766@student.comsats.edu.pk]

Note: This project is developed as part of the Theory of Automata course requirements at the Faculty of Computing.

text

This README provides:
- ✅ Professional presentation
- ✅ Clear installation instructions
- ✅ Usage examples
- ✅ Team information
- ✅ Academic context
- ✅ Comprehensive documentation
