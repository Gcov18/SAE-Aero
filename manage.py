#!/usr/bin/env python3
"""
SAE Aero Project Management Utility

This script provides utilities for managing the SAE Aero project including:
- Running tests
- Cleaning build artifacts
- Generating documentation
- Setting up development environment
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def clean_project():
    """Clean build artifacts and cache files."""
    print("Cleaning project artifacts...")

    # Define patterns to clean
    patterns_to_remove = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        "**/.*cache*",
        "build",
        "dist",
        "*.egg-info",
    ]

    project_root = Path(__file__).parent
    removed_count = 0

    for pattern in patterns_to_remove:
        for path in project_root.glob(pattern):
            try:
                if path.is_file():
                    path.unlink()
                    removed_count += 1
                elif path.is_dir():
                    shutil.rmtree(path)
                    removed_count += 1
            except Exception as e:
                print(f"Warning: Could not remove {path}: {e}")

    print(f"Cleaned {removed_count} items")


def setup_dev_environment():
    """Set up development environment."""
    print("Setting up development environment...")

    # Install requirements
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("Error installing requirements")

    # Install development requirements
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest", "black", "flake8"], check=True)
        print("Development tools installed successfully")
    except subprocess.CalledProcessError:
        print("Error installing development tools")


def run_tests():
    """Run project tests."""
    print("Running tests...")

    # Check if pytest is available
    try:
        subprocess.run([sys.executable, "-m", "pytest", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("pytest not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest"], check=True)

    # Run tests
    test_dir = Path(__file__).parent / "tests"
    if test_dir.exists():
        subprocess.run([sys.executable, "-m", "pytest", str(test_dir)], check=False)
    else:
        print("No tests directory found. Create tests/ directory and add test files.")


def format_code():
    """Format code using black."""
    print("Formatting code...")

    try:
        subprocess.run([sys.executable, "-m", "black", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("black not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "black"], check=True)

    # Format source code
    src_dir = Path(__file__).parent / "src"
    subprocess.run([sys.executable, "-m", "black", str(src_dir)], check=False)

    # Format main files
    main_files = ["main.py", "setup.py", "manage.py"]
    for file in main_files:
        file_path = Path(__file__).parent / file
        if file_path.exists():
            subprocess.run([sys.executable, "-m", "black", str(file_path)], check=False)


def lint_code():
    """Lint code using flake8."""
    print("Linting code...")

    try:
        subprocess.run([sys.executable, "-m", "flake8", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("flake8 not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flake8"], check=True)

    # Lint source code
    src_dir = Path(__file__).parent / "src"
    subprocess.run([sys.executable, "-m", "flake8", str(src_dir)], check=False)


def create_build():
    """Create distribution build."""
    print("Creating distribution build...")

    try:
        subprocess.run([sys.executable, "setup.py", "sdist", "bdist_wheel"], check=True)
        print("Build created successfully in dist/")
    except subprocess.CalledProcessError:
        print("Error creating build")


def show_status():
    """Show project status."""
    print("SAE Aero Project Status")
    print("=" * 30)

    project_root = Path(__file__).parent

    # Count files by type
    py_files = len(list(project_root.glob("**/*.py")))
    log_files = len(list(project_root.glob("logs/*.log")))
    output_files = len(list(project_root.glob("output/**/*.png")))

    print(f"Python files: {py_files}")
    print(f"Log files: {log_files}")
    print(f"Output files: {output_files}")

    # Check if key directories exist
    directories = ["src", "logs", "output", "archive"]
    for directory in directories:
        dir_path = project_root / directory
        status = "✓" if dir_path.exists() else "✗"
        print(f"{directory}/ directory: {status}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="SAE Aero Project Management")
    parser.add_argument(
        "command", choices=["clean", "setup", "test", "format", "lint", "build", "status"], help="Command to execute"
    )

    args = parser.parse_args()

    commands = {
        "clean": clean_project,
        "setup": setup_dev_environment,
        "test": run_tests,
        "format": format_code,
        "lint": lint_code,
        "build": create_build,
        "status": show_status,
    }

    command_func = commands.get(args.command)
    if command_func:
        command_func()
    else:
        print(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
