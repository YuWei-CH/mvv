import os
import subprocess
import sys
import shutil
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a command and return the result."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=check
        )
        if result.stdout:
            print(f"STDOUT: {result.stdout}")
        if result.stderr:
            print(f"STDERR: {result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        raise

def cleanup_venv(venv_dir):
    """Remove the virtual environment directory."""
    if venv_dir.exists():
        print(f"Cleaning up virtual environment: {venv_dir}")
        try:
            shutil.rmtree(venv_dir)
            print("✓ Virtual environment cleaned up successfully!")
        except Exception as e:
            print(f"⚠ Warning: Failed to clean up virtual environment: {e}")

def test_venv(venv_dir, test_script):
    """Test the virtual environment by running the test script."""
    # Determine the correct Python executable path in the virtual environment
    if os.name == 'nt':  # Windows
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:  # Unix/Linux/Mac
        venv_python = venv_dir / "bin" / "python"
    
    # Run the test script in the virtual environment
    print("Running library import test...")
    try:
        result = run_command(f'"{venv_python}" "{test_script}"')
        print("Library initial importing test successful!")
        return True
    except subprocess.CalledProcessError as e:
        print("Library initial importing test failed!")
        return False

def create_and_test_venv():
    """Create virtual environment and test library installations."""
    
    # Check if uv is available
    try:
        run_command('uv --version')
        print("✓ uv is available")
    except subprocess.CalledProcessError:
        raise RuntimeError("uv is not installed or not available in PATH. Please install uv first.")
    
    # Get current directory and source path
    current_dir = Path.cwd()
    source_dir = current_dir / "source"
    dest_dir = current_dir / "dest"
    venv_dir = source_dir / "venv"
    requirements_file = current_dir / "requirements.txt"
    test_script = current_dir / "test-venv.py"
    
    print(f"Current directory: {current_dir}")
    print(f"Source directory: {source_dir}")
    print(f"Destination directory: {dest_dir}")
    
    # Check if required files exist
    if not requirements_file.exists():
        raise FileNotFoundError(f"Requirements file not found: {requirements_file}")
    
    if not test_script.exists():
        raise FileNotFoundError(f"Test script not found: {test_script}")
    
    # Create source and destination directories if they don't exist
    source_dir.mkdir(exist_ok=True)
    dest_dir.mkdir(exist_ok=True)
    
    # Remove existing venv if it exists
    if venv_dir.exists():
        print(f"Removing existing virtual environment: {venv_dir}")
        shutil.rmtree(venv_dir)
    
    success = False
    moved_success = False
    try:
        # Create virtual environment using uv (to match mvv.sh behavior)
        print("Creating virtual environment using uv...")
        run_command(f'uv venv "{venv_dir}"')
        
        # Install requirements using uv with the virtual environment
        print("Installing requirements using uv...")
        # Activate the virtual environment and install packages
        if os.name == 'nt':  # Windows
            activate_and_install = f'"{venv_dir}/Scripts/activate.bat" && uv pip install -r "{requirements_file}"'
        else:  # Unix/Linux/Mac
            activate_and_install = f'bash -c "source \\"{venv_dir}/bin/activate\\" && uv pip install -r \\"{requirements_file}\\""'
        
        run_command(activate_and_install)
        
        # Test the virtual environment
        success = test_venv(venv_dir, test_script)
        
        if success:
            print("\n" + "="*50)
            print("PHASE 2: Moving virtual environment using mvv.sh")
            print("="*50)
            
            # Move the virtual environment using mvv.sh
            moved_success = move_venv_with_script(venv_dir, dest_dir)
            
            if moved_success:
                # Verify the moved virtual environment
                dest_venv_path = dest_dir / "venv"
                print("\n" + "="*50)
                print("PHASE 3: Verifying moved virtual environment")
                print("="*50)
                
                verify_success = verify_moved_venv(dest_venv_path, test_script)
                
                if verify_success:
                    print("\n✓ All phases completed successfully!")
                    print("1. ✓ Virtual environment created and tested")
                    print("2. ✓ Virtual environment moved using mvv.sh")
                    print("3. ✓ Moved virtual environment verified")
                    success = True
                else:
                    print("\n✗ Verification of moved virtual environment failed!")
                    success = False
            else:
                print("\n✗ Failed to move virtual environment!")
                success = False
    
    finally:
        # Clean up source virtual environment (if it still exists)
        if venv_dir.exists():
            cleanup_venv(venv_dir)
        
        # Clean up moved virtual environment for testing purposes
        dest_venv_path = dest_dir / "venv"
        if dest_venv_path.exists():
            cleanup_venv(dest_venv_path)
    
    return success

def move_venv_with_script(source_venv_path, dest_dir):
    """Move virtual environment using the mvv.sh script."""
    # Get the mvv.sh script path (one level up from current directory)
    current_dir = Path.cwd()
    mvv_script = current_dir.parent / "mvv.sh"
    
    if not mvv_script.exists():
        raise FileNotFoundError(f"mvv.sh script not found: {mvv_script}")
    
    # Ensure the script is executable
    run_command(f'chmod +x "{mvv_script}"')
    
    # Run the mvv.sh script to move the virtual environment
    # The script expects: <source_venv_path> <destination_venv_path>
    # Provide the full destination path including the venv folder name
    dest_venv_path = dest_dir / "venv"
    print(f"Moving virtual environment from {source_venv_path} to {dest_venv_path}")
    try:
        result = run_command(f'"{mvv_script}" "{source_venv_path}" "{dest_venv_path}"')
        print("✓ Virtual environment moved successfully using mvv.sh!")
        return True
    except subprocess.CalledProcessError as e:
        print("✗ Failed to move virtual environment using mvv.sh!")
        return False

def verify_moved_venv(dest_venv_path, test_script):
    """Verify the moved virtual environment works correctly."""
    print(f"Verifying moved virtual environment at: {dest_venv_path}")
    
    # Check if the destination virtual environment exists
    if not dest_venv_path.exists():
        print(f"✗ Virtual environment not found at: {dest_venv_path}")
        return False
    
    # Check if the Python executable exists in the moved venv
    if os.name == 'nt':  # Windows
        venv_python = dest_venv_path / "Scripts" / "python.exe"
    else:  # Unix/Linux/Mac
        venv_python = dest_venv_path / "bin" / "python"
    
    if not venv_python.exists():
        print(f"✗ Python executable not found in moved venv: {venv_python}")
        return False
    
    # Test the moved virtual environment by running the test script
    print("Testing moved virtual environment...")
    try:
        result = run_command(f'"{venv_python}" "{test_script}"')
        print("✓ Moved virtual environment verification successful!")
        return True
    except subprocess.CalledProcessError as e:
        print("✗ Moved virtual environment verification failed!")
        return False

if __name__ == "__main__":
    try:
        success = create_and_test_venv()
        if success:
            print("\nVirtual environment setup and testing completed successfully!")
            sys.exit(0)
        else:
            print("\nVirtual environment testing failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\nError during setup: {e}")
        sys.exit(1)

