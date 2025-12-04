# main.py
import subprocess
import sys

def check_requirements():
    """Check if required packages are installed"""
    required_packages = ['graphviz', 'PIL']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_packages(packages):
    """Install missing packages"""
    print("Installing missing packages...")
    for package in packages:
        if package == 'PIL':
            package_name = 'Pillow'
        else:
            package_name = package
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✓ Successfully installed {package_name}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package_name}")
            return False
    return True

def main():
    print("=" * 60)
    print("Regex to Automata Converter with Image Generation")
    print("=" * 60)
    print()
    
    # Check for Graphviz installation (system level)
    try:
        subprocess.run(['dot', '-V'], capture_output=True, check=True)
        print("✓ Graphviz is installed on system")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Graphviz not found. Please install Graphviz:")
        print("   Windows: Download from https://graphviz.org/download/")
        print("   macOS: brew install graphviz")
        print("   Linux: sudo apt-get install graphviz")
        print()
        print("After installing Graphviz, restart the application.")
        input("Press Enter to continue anyway...")
    
    # Check Python packages
    missing = check_requirements()
    
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        choice = input("Do you want to install them? (y/n): ")
        if choice.lower() == 'y':
            if not install_packages(missing):
                print("Failed to install required packages.")
                return
        else:
            print("Cannot run without required packages.")
            return
    
    print()
    print("Starting GUI application...")
    print()
    
    # Import and run GUI
    try:
        from gui import run_gui
        run_gui()
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()