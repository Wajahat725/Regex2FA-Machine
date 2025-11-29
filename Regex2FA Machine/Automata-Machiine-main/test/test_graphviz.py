"""Test Graphviz Installation"""

import os
import sys

print("=" * 80)
print("Graphviz Installation Test")
print("=" * 80)

# Check PATH
print("\n1. Checking System PATH:")
paths = os.environ.get("PATH", "").split(os.pathsep)
graphviz_paths = [p for p in paths if "graphviz" in p.lower()]

if graphviz_paths:
    print("✅ Graphviz found in PATH:")
    for p in graphviz_paths:
        print(f"   {p}")
else:
    print("❌ Graphviz NOT found in PATH")

# Try to import graphviz module
print("\n2. Checking Python graphviz module:")
try:
    import graphviz
    print(f"✅ graphviz module installed: {graphviz.__version__}")
except ImportError:
    print("❌ graphviz module not installed")
    print("   Run: pip install graphviz")

# Try to execute dot command
print("\n3. Checking dot.exe executable:")
import subprocess
try:
    result = subprocess.run(["dot", "-V"], capture_output=True, text=True)
    print(f"✅ dot.exe accessible:")
    print(f"   {result.stderr.strip()}")
except FileNotFoundError:
    print("❌ dot.exe not found")
    print("   Graphviz executables not accessible")
except Exception as e:
    print(f"❌ Error: {e}")

# Try to create a simple graph
print("\n4. Testing diagram generation:")
try:
    from graphviz import Digraph
    dot = Digraph()
    dot.node('A', 'Test')
    dot.render('test_output', format='png', cleanup=True)

    if os.path.exists('test_output.png'):
        print("✅ Diagram generation successful!")
        os.remove('test_output.png')
    else:
        print("⚠️ Diagram file not created")
except Exception as e:
    print(f"❌ Diagram generation failed: {e}")

print("\n" + "=" * 80)
print("Test Complete!")
print("=" * 80)
