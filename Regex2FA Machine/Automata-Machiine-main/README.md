# Automata Theory Project

## Regular Expression: `aba + bb + c (aaa + aa + a)*`

This project implements a complete automata theory toolkit that converts the regular expression `aba + bb + c (aaa + aa + a)*` into equivalent automata representations.

### Features

1. **Regular Expression Validation** - Validates the regex syntax
2. **NFA Generation** - Uses Thompson's construction algorithm
3. **DFA Generation** - Uses subset construction algorithm
4. **DFA Minimization** - Uses table-filling algorithm
5. **String Simulation** - Tests strings on the minimized DFA
6. **Visual Diagrams** - Generates automata diagrams using Graphviz

### Alphabet
- **{a, b, c}**

### Example Accepted Strings
- `aba` - From the first alternative
- `bb` - From the second alternative  
- `c` - From the third alternative (with empty string from Kleene star)
- `ca` - From the third alternative with one 'a'
- `caa` - From the third alternative with two 'a's
- `caaa` - From the third alternative with three 'a's
- `caaaa` - From the third alternative with four 'a's

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt