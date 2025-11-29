# Installation Guide

## Quick Start (Without Diagrams)

If you just want to use the core functionality without visual diagrams, you can run the application immediately:

```bash
python main.py
```

The application will work fully for:
- ✅ Regular Expression Validation
- ✅ NFA Generation (with transition tables and ε-closures)
- ✅ DFA Generation (with transition tables)
- ✅ DFA Minimization (with transition tables)
- ✅ String Simulation (with step-by-step trace)

⚠ Visual diagrams will show a warning message but won't break the application.

---

## Full Installation (With Diagrams)

To enable visual automata diagrams, follow these steps:

### Step 1: Install Graphviz (System)

**Windows:**

1. Download the installer from: https://graphviz.org/download/
2. Choose "Windows" → Download the `.exe` installer (e.g., `graphviz-10.0.1-win64.exe`)
3. Run the installer
4. **IMPORTANT:** During installation, check the box that says "Add Graphviz to the system PATH"
   - If you missed this, manually add: `C:\Program Files\Graphviz\bin` to your PATH
5. Restart your terminal/IDE after installation

**To verify Graphviz installation:**
```bash
dot -V
```
Should output something like: `dot - graphviz version 10.0.1 (20240210.0000)`

**If you get "command not found" error:**

Add Graphviz to PATH manually:
1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Go to "Advanced" tab → Click "Environment Variables"
3. Under "System variables", find "Path", click "Edit"
4. Click "New" and add: `C:\Program Files\Graphviz\bin`
5. Click OK on all dialogs
6. **Restart your terminal/IDE**

---

### Step 2: Install Python Packages

```bash
pip install -r requirements.txt
```

This installs:
- `graphviz` - Python wrapper for Graphviz
- `Pillow` - Image display in GUI

---

### Step 3: Run the Application

```bash
python main.py
```

Now all features including visual diagrams should work!

---

## Troubleshooting

### Issue: "failed to execute WindowsPath..., make sure the Graphviz executables are on your systems' PATH"

**Solution:**
1. Verify Graphviz is installed: Run `dot -V` in terminal
2. If not found, add to PATH (see Step 1 above)
3. **Restart your terminal/IDE** after modifying PATH
4. Try running the application again

### Issue: Diagrams still not working after installing Graphviz

**Solution:**
```bash
# Reinstall the Python graphviz package
pip uninstall graphviz
pip install graphviz

# Test if it works
python -c "from graphviz import Digraph; print('Graphviz works!')"
```

### Issue: Application crashes when generating diagrams

**Solution:**
The latest version includes graceful error handling. Update your files and run again:
```bash
python main.py
```

Even if Graphviz is not available, the application will:
- ✅ Continue working with all core features
- ⚠ Show a warning message where diagrams would appear
- 📊 Display all transition tables correctly

---

## Alternative: Use Without Installation

If you cannot install Graphviz on your system, you can:

1. Run the console test (no GUI, no diagrams needed):
   ```bash
   python test_console.py
   ```

2. Use the GUI without diagrams:
   ```bash
   python main.py
   ```
   - All transition tables will be displayed
   - All algorithms will run correctly
   - Simulation will work perfectly
   - Only the visual diagram panels will show a warning

---

## Verifying Installation

Run this test script:

```bash
python test_console.py
```

You should see:
```
================================================================================
ALL TESTS COMPLETED SUCCESSFULLY! ✅
================================================================================
```

This verifies that all core algorithms work correctly.

---

## System Requirements

- Python 3.8 or higher
- Windows/macOS/Linux
- Graphviz (optional, for diagrams)
- 50 MB free disk space

---

## Need Help?

1. Check that Python is installed: `python --version`
2. Check that pip works: `pip --version`
3. For Graphviz issues, verify: `dot -V`
4. Make sure you've restarted your terminal after PATH changes
5. Try running `test_console.py` first to verify core functionality

