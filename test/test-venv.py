import sys
import importlib

def test_library_imports():
    """Test that all required libraries can be imported successfully."""
    
    # List of libraries to test (library_name, import_name)
    libraries = [
        ('flask', 'flask'),
        ('django', 'django'),
        ('fastapi', 'fastapi'),
        ('requests', 'requests'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('scikit-learn', 'sklearn'),
        ('sqlalchemy', 'sqlalchemy'),
        ('psycopg2-binary', 'psycopg2'),
        ('pytest', 'pytest'),
        ('pytest-cov', 'pytest_cov'),
        ('python-dotenv', 'dotenv'),
        ('pydantic', 'pydantic'),
        ('click', 'click'),
    ]
    
    failed_imports = []
    
    for library_name, import_name in libraries:
        try:
            importlib.import_module(import_name)
            print(f"✓ Successfully imported {library_name}")
        except ImportError as e:
            failed_imports.append((library_name, str(e)))
            print(f"✗ Failed to import {library_name}: {e}")
    
    if failed_imports:
        error_message = "The following libraries failed to import:\n"
        for lib_name, error in failed_imports:
            error_message += f"  - {lib_name}: {error}\n"
        error_message += "\nPlease check the settings"
        raise ImportError(error_message)
    
    print(f"✓ All {len(libraries)} libraries imported successfully!")

if __name__ == "__main__":
    test_library_imports()
