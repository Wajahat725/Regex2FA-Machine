# Quick Start Guide - Automata Theory Project

## ⚡ Run Immediately (No Installation Required)

Your project is ready to run! The core functionality works without any additional installations.

### Option 1: Run Console Tests (Recommended First)

```bash
python test_console.py
```

This will:
- ✅ Validate the regex `d(de*d|ef*e|fd*f)df`
- ✅ Generate NFA with Thompson's Construction
- ✅ Generate DFA with Subset Construction
- ✅ Minimize DFA with Table-Filling Algorithm
- ✅ Test strings: `ddddf`, `deedf`, `dffdf`
- 📊 Show all transition tables and traces

**Expected output:** `ALL TESTS COMPLETED SUCCESSFULLY! ✅`

---

### Option 2: Run GUI Application

```bash
python main.py
```

The GUI will open with 5 tabs:

#### Tab 1: Regular Expression
- Pre-filled with: `d(de*d|ef*e|fd*f)df`
- Click **"Validate RE"** to check syntax

#### Tab 2: NFA (Thompson)
- Click **"Generate NFA"**
- View transition table and ε-closures

#### Tab 3: DFA (Subset Construction)
- Click **"Generate DFA"**
- View transition table with state compositions

#### Tab 4: Minimized DFA
- Click **"Minimize DFA"**
- View minimized table and distinguishability analysis

#### Tab 5: String Simulation
- Enter a test string (or use quick test buttons)
- Click **"Simulate"** to see step-by-step trace
- Try: `ddddf`, `deedf`, `dffdf` (should be ACCEPTED)

---

## ⚠ About Diagrams

**If you see a warning about Graphviz:**

Don't worry! The application works perfectly without it. You'll see:
- ✅ All transition tables
- ✅ All algorithms work correctly
- ✅ String simulation with full traces
- ⚠ Diagram panels will show a warning message

**To enable diagrams (optional):**
1. See `INSTALLATION.md` for detailed instructions
2. Install Graphviz from: https://graphviz.org/download/
3. Add to PATH: `C:\Program Files\Graphviz\bin`
4. Run: `pip install graphviz pillow`
5. Restart your terminal/IDE

---

## 📝 Test the Assigned Regex

### Regular Expression: `d(de*d|ef*e|fd*f)df`

**This matches:**
- `d` followed by one of:
  - `de*d` (d, zero or more e's, then d)
  - `ef*e` (e, zero or more f's, then e)
  - `fd*f` (f, zero or more d's, then f)
- Ending with `df`

### ✅ Accepted Strings

| String | Pattern Match |
|--------|---------------|
| `ddddf` | d + (d + e* + d) + df = d(dεd)df |
| `deedf` | d + (e + f* + e) + df = d(eεe)df |
| `dffdf` | d + (f + d* + f) + df = d(fεf)df |
| `dddddf` | d + (d + e* + d) + df = d(deddd)df |
| `deeedf` | d + (e + f* + e) + df = d(efeee)df |

### ❌ Rejected Strings

| String | Reason |
|--------|--------|
| `def` | Doesn't match pattern (incomplete) |
| `ddd` | Missing final 'df' |
| `ddedf` | Wrong middle pattern |
| `dddf` | Missing one more 'd' before 'df' |

---

## 🎯 What Each Module Does

### 1. `regex_validator.py`
- Checks syntax errors
- Validates alphabet (only d, e, f allowed)
- Adds explicit concatenation operators

### 2. `thompson_nfa.py`
- Implements Thompson's Construction
- Creates NFA with ε-transitions
- Shows ε-closures for each state

### 3. `subset_dfa.py`
- Converts NFA to DFA
- Uses Subset Construction Algorithm
- Shows which NFA states form each DFA state

### 4. `minimizer.py`
- Minimizes DFA using Table-Filling Algorithm
- Merges equivalent states
- Shows distinguishability table

### 5. `simulator.py`
- Simulates string acceptance
- Shows step-by-step transitions
- Returns ACCEPTED or REJECTED with trace

### 6. `visualizer.py`
- Generates diagrams (requires Graphviz)
- Creates PNG images for NFA, DFA, Minimized DFA

### 7. `gui.py`
- Complete graphical interface
- 5 tabs for different stages
- Interactive string testing

---

## 📊 Understanding the Output

### NFA Transition Table Example
```
q0:
  d → ['q1']
  
q1:
  ε → ['q2', 'q10', 'q18']
```
- ε means epsilon (empty) transition
- Multiple next states = non-determinism

### DFA Transition Table Example
```
q1 [START] = {q0, q1, q2}
  d → q2
  e → q3
  f → q4
```
- Each state is a set of NFA states
- One transition per symbol = deterministic

### Simulation Trace Example
```
String: ddddf

Step 1: q0 --d--> q1
Step 2: q1 --d--> q2
Step 3: q2 --d--> q2
Step 4: q2 --d--> q3
Step 5: q3 --f--> q4 (FINAL)

✓ String ACCEPTED
```

---

## 🐛 Common Issues

### Issue: "Module not found"
**Solution:** Make sure you're in the project directory
```bash
cd C:\Users\abuba\PycharmProjects\AutomataMachine
python main.py
```

### Issue: Graphviz error when clicking Generate buttons
**Solution:** This is expected! The application continues to work. See the transition tables on the left side. To fix, see `INSTALLATION.md`.

### Issue: GUI doesn't open
**Solution:** 
1. Check Python is installed: `python --version`
2. Try the console test first: `python test_console.py`
3. Install Pillow: `pip install pillow`

---

## ✅ Success Checklist

After running `test_console.py`, you should see:

- ✅ Regex validated successfully
- ✅ NFA generated with ~30+ states
- ✅ DFA generated with ~10-15 states
- ✅ Minimized DFA with fewer states
- ✅ Strings `ddddf`, `deedf`, `dffdf` ACCEPTED
- ✅ Strings `def`, `ddd` REJECTED

---

## 📚 Next Steps

1. ✅ Run `python test_console.py` to verify everything works
2. 🖥️ Run `python main.py` to use the GUI
3. 🧪 Test with your own strings
4. 📊 (Optional) Install Graphviz for visual diagrams
5. 📖 Read `README.md` for theoretical background

---

## 💡 Tips

- Use the **Quick Test** buttons in the Simulation tab
- View **transition tables** to understand state transitions
- Check **ε-closures** to see epsilon transitions
- Compare **DFA vs Minimized DFA** to see state reduction
- The **preprocessed regex** shows explicit concatenation operators

---

**Ready to start?**

```bash
python test_console.py
```

Then:

```bash
python main.py
```

**Enjoy exploring Automata Theory! 🚀**

