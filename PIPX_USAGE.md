# Xerosploit pipx Usage Examples

## Installation with pipx

### Quick installation
```bash
git clone https://github.com/LionSec/xerosploit
cd xerosploit
./install_pipx.sh
```

### Manual installation
```bash
# Install system dependencies
sudo apt-get install -y nmap hping3 build-essential python3-pip ruby-dev git libpcap-dev libgmp3-dev

# Install bettercap
gem install bettercap

# Install with pipx
pipx install .
```

## Usage

### Basic usage
```bash
# Run xerosploit
xerosploit

# Test installation
python3 test_installation.py
```

### pipx management
```bash
# Check installed packages
pipx list

# Upgrade xerosploit
pipx upgrade xerosploit

# Reinstall (useful for development)
pipx uninstall xerosploit
pipx install .

# Install in development mode (for developers)
pipx install -e .
```

## Troubleshooting

### PATH issues
If `xerosploit` command is not found after installation:
```bash
# Add pipx bin directory to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Permission issues
If you get permission errors:
```bash
# Don't use sudo with pipx
# Only use sudo for system dependencies
sudo apt-get install -y nmap hping3 build-essential python3-pip ruby-dev git libpcap-dev libgmp3-dev
gem install bettercap
pipx install .  # No sudo here
```

### Missing dependencies
If some dependencies are missing:
```bash
# Install missing system packages
sudo apt-get update
sudo apt-get install -y nmap hping3 build-essential python3-pip ruby-dev git libpcap-dev libgmp3-dev

# Reinstall bettercap if needed
gem install bettercap

# Test the installation
python3 test_installation.py
```

## Development

### Setting up development environment
```bash
# Install in editable mode
pipx install -e .

# Install development dependencies
pipx inject xerosploit pytest black flake8
```

### Running tests
```bash
# Test the installation
python3 test_installation.py

# Run with verbose output
python3 test_installation.py -v
```
