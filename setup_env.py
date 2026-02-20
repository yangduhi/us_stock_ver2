import subprocess
import sys
from importlib.util import find_spec


def run_command(command):
    print(f"Running: {command}")
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e)
        sys.exit(1)


def main():
    print("Starting Ultimate MCP Environment Setup...")

    # 1. Upgrade pip
    print("\n[1/4] Upgrading pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip")

    # 2. Install requirements
    print("\n[2/4] Installing requirements...")
    run_command(f"{sys.executable} -m pip install -r requirements.txt")

    # 3. Install Playwright browsers
    print("\n[3/4] Installing Playwright browsers...")
    run_command(f"{sys.executable} -m playwright install")

    # 4. Verify installation
    print("\n[4/4] Verifying installation...")
    try:
        required_modules = [
            "pandas",
            "playwright",
            "sqlalchemy",
            "networkx",
            "github",
            "google.genai",
        ]
        missing = [module for module in required_modules if find_spec(module) is None]
        if missing:
            raise ImportError(f"Missing modules: {', '.join(missing)}")
        print("All major dependencies imported successfully.")
    except ImportError as e:
        print(f"Verification failed: {e}")
        sys.exit(1)

    print("\nUltimate MCP Environment Setup Complete!")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Version: {sys.version}")


if __name__ == "__main__":
    main()
