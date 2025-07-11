# mvv - Move Virtual Environment

A fast and efficient CLI tool to move Python virtual environments from one location to another while preserving all installed packages and dependencies.

## Features

- **Fast package migration**: Uses `uv` for multithreaded package installation
- **Preserves environment**: Maintains all installed packages with exact versions
- **Cross-platform**: Works on Linux, macOS, and Windows
- **Simple usage**: Just provide source and destination paths
- **Automatic cleanup**: Handles temporary files automatically

## Prerequisites

- [uv](https://docs.astral.sh/uv/) - Fast Python package installer
- Python 3.7+
- Bash (for Unix-like systems)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd mvv
   ```

2. Make the script executable:
   ```bash
   chmod +x mvv.sh
   ```

3. Optionally, add to your PATH for global access:
   ```bash
   sudo cp mvv.sh /usr/local/bin/mvv
   ```

## Usage

```bash
./mvv.sh <source_venv_path> <destination_venv_path>
```

### Examples

1. **Move virtual environment to specific path:**
   ```bash
   ./mvv.sh /path/to/old/venv /path/to/new/venv
   ```

2. **Move virtual environment to directory (keeps same name):**
   ```bash
   ./mvv.sh /path/to/old/venv /path/to/new/directory/
   ```

## How it Works

The tool performs the following steps:

1. **Export packages**: Freezes all installed packages from the source environment
2. **Create new environment**: Creates a fresh virtual environment at the destination
3. **Install packages**: Installs all packages using `uv` for fast, multithreaded installation
4. **Cleanup**: Removes temporary files

## Testing

The project includes a comprehensive test suite to validate the move process:

```bash
cd test
python3 test.py
```

The test script will:
- Create a virtual environment with test packages
- Move it using the `mvv.sh` script
- Verify all packages work correctly in the new location
- Clean up test environments

## Benefits

- **Speed**: Uses `uv` for significantly faster package installation compared to pip
- **Reliability**: Preserves exact package versions and dependencies
- **Flexibility**: Works with any Python virtual environment
- **Safety**: Creates new environment rather than moving files directly

## Limitations

- Requires `uv` to be installed
- Source virtual environment must be created with standard tools (`venv`, `virtualenv`, or `uv venv`)
- Some compiled extensions may need to be rebuilt in the new environment

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## TODO

- [ ] Add support for conda environments
- [ ] Implement progress bar for large package installations
- [ ] Add option to preserve virtual environment activation scripts
- [ ] Support for requirements.txt input instead of existing venv
- [ ] Add verbose/quiet mode options
- [ ] Cross-platform batch/PowerShell script for Windows
