#!/bin/bash

# ShadowBits Installation Script with Automatic Virtual Environment
# Usage: curl -sSL https://raw.githubusercontent.com/kaizoku73/ShadowBits/main/install.sh | bash

set -euo pipefail

# Cleanup function for temp directory
cleanup() {
    if [[ -n "${TEMP_DIR:-}" ]] && [[ -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
    fi
}
trap cleanup EXIT

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}ShadowBits Image Steganography Installer${NC}"
echo -e "${BLUE}======================================${NC}"

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠ ${NC} $1"
}

# Check for required dependencies
echo "Checking system requirements..."

# Check Python 3
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed."
    echo "Please install Python 3.7+ and try again."
    exit 1
fi
print_status "Python 3 found: $(python3 --version)"

# Check if python3-venv is available (required on some systems like Ubuntu)
if ! python3 -c "import venv" &>/dev/null; then
    print_error "Python venv module is not available."
    echo "Please install python3-venv package:"
    echo "  Ubuntu/Debian: sudo apt install python3-venv"
    echo "  CentOS/RHEL: sudo yum install python3-venv"
    echo "  Or: python3 -m pip install --user virtualenv"
    exit 1
fi
print_status "Python venv module found"

# Determine installation directory
if [[ $EUID -eq 0 ]]; then
    INSTALL_DIR="/usr/local/bin"
    SHADOWBITS_DIR="/usr/local/share/shadowbits"
    VENV_DIR="/usr/local/share/shadowbits/venv"
    INSTALL_TYPE="system-wide"
    print_status "Installing system-wide"
else
    INSTALL_DIR="$HOME/.local/bin"
    SHADOWBITS_DIR="$HOME/.local/share/shadowbits"
    VENV_DIR="$HOME/.local/share/shadowbits/venv"
    INSTALL_TYPE="user"
    print_status "Installing for current user"
fi

# Create directories
echo "Creating directories..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$SHADOWBITS_DIR"

# Download shadowbits from GitHub
echo "Downloading ShadowBits from GitHub..."
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

if ! curl -fsSL -o shadowbits.tar.gz https://github.com/kaizoku73/shadowbits/archive/refs/heads/main.tar.gz; then
    print_error "Failed to download ShadowBits from GitHub"
    exit 1
fi

tar -xzf shadowbits.tar.gz
cd ShadowBits-main

print_status "Downloaded and extracted ShadowBits"

# Verify the expected directory structure
echo "Verifying repository structure..."
if [[ ! -d "shadowbits" ]]; then
    print_error "Expected 'shadowbits' directory not found in repository"
    echo "Repository structure:"
    ls -la
    exit 1
fi

if [[ ! -f "shadowbits/cli.py" ]]; then
    print_error "cli.py not found in shadowbits/ directory"
    echo "Contents of shadowbits/ directory:"
    ls -la shadowbits/
    exit 1
fi

if [[ ! -f "requirements.txt" ]]; then
    print_error "requirements.txt not found in root directory"
    exit 1
fi

print_status "Repository structure verified"

# Create virtual environment
echo "Creating virtual environment..."
if [[ -d "$VENV_DIR" ]]; then
    print_warning "Virtual environment already exists, removing old one..."
    rm -rf "$VENV_DIR"
fi

python3 -m venv "$VENV_DIR"
print_status "Virtual environment created at $VENV_DIR"

# Activate virtual environment and install dependencies
echo "Installing Python dependencies in virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip in the virtual environment
python -m pip install --upgrade pip

# Install requirements
python -m pip install -r requirements.txt
print_status "Dependencies installed in virtual environment"

# Copy files to installation directory
echo "Installing ShadowBits files..."

# Copy the entire shadowbits package directory
cp -r shadowbits "$SHADOWBITS_DIR/"

# Copy supporting files to the installation directory
cp requirements.txt "$SHADOWBITS_DIR/"
cp README.md "$SHADOWBITS_DIR/" 2>/dev/null || true
cp LICENSE "$SHADOWBITS_DIR/" 2>/dev/null || true

print_status "Files copied to $SHADOWBITS_DIR"

# Verify cli.py is in the correct location
if [[ ! -f "$SHADOWBITS_DIR/shadowbits/cli.py" ]]; then
    print_error "cli.py not found at expected location: $SHADOWBITS_DIR/shadowbits/cli.py"
    echo "Installation directory contents:"
    ls -la "$SHADOWBITS_DIR"
    exit 1
fi

# Test if the shadowbits package can be imported and cli.py works
echo "Testing ShadowBits installation..."
cd "$SHADOWBITS_DIR"

# Test with the virtual environment
if ! "$VENV_DIR/bin/python" -c "import sys; sys.path.append('$SHADOWBITS_DIR'); from shadowbits import cli" &>/dev/null; then
    print_warning "Python import test failed, but continuing..."
else
    print_status "Python import test passed"
fi

# Test cli.py directly
if "$VENV_DIR/bin/python" shadowbits/cli.py --help &>/dev/null; then
    print_status "cli.py execution test passed"
else
    print_warning "cli.py execution test failed, but continuing..."
fi

# Create executable wrapper script that uses the virtual environment
echo "Creating chromoshift command..."
cat > "$INSTALL_DIR/shadowbits" << 'EOF'
#!/bin/bash
# ShadowBits wrapper script with virtual environment

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Determine the installation directory based on script location
if [[ "$SCRIPT_DIR" == "/usr/local/bin" ]]; then
    SHADOWBITS_DIR="/usr/local/share/shadowbits"
    VENV_DIR="/usr/local/share/shadowbits/venv"
elif [[ "$SCRIPT_DIR" == "$HOME/.local/bin" ]]; then
    SHADOWBITS_DIR="$HOME/.local/share/shadowbits"
    VENV_DIR="$HOME/.local/share/shadowbits/venv"
else
    # Fallback - try to find it relative to script location
    SHADOWBITS_DIR="$(dirname "$SCRIPT_DIR")/share/shadowbits"
    VENV_DIR="$SHADOWBITS_DIR/venv"
fi

# Check if shadowbits directory exists
if [[ ! -d "$SHADOWBITS_DIR" ]]; then
    echo "Error: ShadowBits installation directory not found: $SHADOWBITS_DIR" >&2
    exit 1
fi

# Check if virtual environment exists
if [[ ! -d "$VENV_DIR" ]]; then
    echo "Error: ShadowBits virtual environment not found: $VENV_DIR" >&2
    echo "Try reinstalling ShadowBits with the install script." >&2
    exit 1
fi

# Check if cli.py exists
if [[ ! -f "$SHADOWBITS_DIR/shadowbits/cli.py" ]]; then
    echo "Error: cli.py not found at: $SHADOWBITS_DIR/shadowbits/cli.py" >&2
    exit 1
fi

# Check if Python interpreter exists in venv
if [[ ! -f "$VENV_DIR/bin/python" ]]; then
    echo "Error: Python interpreter not found in virtual environment: $VENV_DIR/bin/python" >&2
    exit 1
fi

# Set PYTHONPATH to include the installation directory
export PYTHONPATH="$SHADOWBITS_DIR:${PYTHONPATH:-}"

# Execute cli.py using the virtual environment's Python interpreter
# This ensures all dependencies are available and isolated
exec "$VENV_DIR/bin/python" "$SHADOWBITS_DIR/shadowbits/cli.py" "$@"
EOF

chmod +x "$INSTALL_DIR/shadowbits"
print_status "ShadowBits command created"

# Verify installation
echo "Verifying installation..."

# Check if shadowbits command is in PATH
if command -v shadowbits &> /dev/null; then
    print_status "ShadowBits command is available in PATH!"
    
    # Test the actual command
    echo "Testing shadowbits command..."
    if timeout 10 shadowbits --help &>/dev/null; then
        print_status "ShadowBits command works correctly!"
    else
        print_warning "ShadowBits command found but help test failed"
        echo "You may need to check the installation"
    fi
else
    print_error "Installation failed - shadowbits command not found in PATH"
    
    if [[ $INSTALL_TYPE == "user" ]]; then
        print_warning "~/.local/bin might not be in your PATH"
        echo ""
        echo "To add ~/.local/bin to your PATH, run one of these commands:"
        echo "For bash users:"
        echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc && source ~/.bashrc"
        echo ""
        echo "For zsh users:"
        echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc && source ~/.zshrc"
        echo ""
        echo "Or use the full path: ~/.local/bin/shadowbits"
    fi
    exit 1
fi

# Cleanup
cleanup

echo ""
echo -e "${GREEN}ShadowBits installed successfully!${NC}"
echo ""
echo -e "${BLUE}Installation Details:${NC}"
echo "  Command location: $INSTALL_DIR/shadowbits"
echo "  Package location: $SHADOWBITS_DIR/shadowbits/"
echo "  Virtual environment: $VENV_DIR"
echo "  Installation type: $INSTALL_TYPE"
echo ""

# Show virtual environment info
echo -e "${BLUE}Virtual Environment Info:${NC}"
echo "  All Python dependencies are isolated in their own virtual environment"
echo "  No conflicts with your system Python packages"
echo "  Virtual environment is automatically activated when you run 'shadowbits'"
echo ""

# Usage examples
echo -e "${BLUE}Usage Examples:${NC}"
echo "  # Embed a secret file in image"
echo "  shadowbits img embed --in \"secret file\" --cover image.png --key password"
echo ""
echo "  # Embed a secret file in audio"
echo "  shadowbits aud embed --in \"secret file\" --cover audio.wav --key mypassword"
echo ""
echo "  # Extract hidden file from image"
echo "  shadowbits img extract --stego encoded.png --key password"
echo ""
echo "  # Extract hidden file from audio"
echo "  shadowbits aud extract --stego encoded.wav --key mypassword"
echo ""
echo -e "${BLUE}Get Help:${NC}"
echo "  shadowbits --help"
echo "  shadowbits embed --help"
echo "  shadowbits extract --help"

if [[ $INSTALL_TYPE == "user" ]] && [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    print_warning "Remember to add ~/.local/bin to your PATH to use 'shadowbits' from anywhere!"
fi

echo ""
echo -e "${GREEN}Note: shadowbits runs in its own virtual environment, so there's no need to activate any venv manually!${NC}"