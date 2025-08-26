#!/bin/bash

#---------------------------------------------------------------------------#
# This file is part of Xerosploit.                                          #
# Xerosploit is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by      #
# the Free Software Foundation, either version 3 of the License, or         #
# (at your option) any later version.                                       #
#                                                                           #
# Xerosploit is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of            #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
# GNU General Public License for more details.                              #
#                                                                           #
# You should have received a copy of the GNU General Public License         #
# along with Xerosploit.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                           #
#---------------------------------------------------------------------------#
#                                                                           #
#        Copyright © 2016 LionSec (www.lionsec.net)                         #
#                                                                           #
#---------------------------------------------------------------------------#

# Xerosploit pipx installation script

set -e

# Colors for output
RED='\033[1;91m'
GREEN='\033[1;92m'
BLUE='\033[1;94m'
CYAN='\033[1;96m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "┌══════════════════════════════════════════════════════════════┐"
echo "█                                                              █"
echo "█                 Xerosploit pipx Installer                   █"
echo "█                                                              █"
echo "└══════════════════════════════════════════════════════════════┘"
echo -e "${NC}"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}[!] This script should NOT be run as root when using pipx${NC}"
   echo -e "${BLUE}[*] pipx installs packages in user space and doesn't require root${NC}"
   echo -e "${BLUE}[*] However, system dependencies will require sudo access${NC}"
   echo ""
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    elif type lsb_release >/dev/null 2>&1; then
        OS=$(lsb_release -si)
        VER=$(lsb_release -sr)
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        OS=$DISTRIB_ID
        VER=$DISTRIB_RELEASE
    elif [ -f /etc/debian_version ]; then
        OS=Debian
        VER=$(cat /etc/debian_version)
    else
        OS=$(uname -s)
        VER=$(uname -r)
    fi
}

# Install system dependencies
install_system_deps() {
    echo -e "${BLUE}[++] Installing system dependencies...${NC}"
    
    detect_os
    
    case $OS in
        *Ubuntu*|*Debian*|*Kali*|*Parrot*)
            echo -e "${BLUE}[*] Detected Debian-based system: $OS${NC}"
            sudo apt-get update
            sudo apt-get install -y nmap hping3 build-essential python3-pip ruby-dev git libpcap-dev libgmp3-dev
            ;;
        *Fedora*|*Red\ Hat*|*CentOS*|*Rocky*)
            echo -e "${BLUE}[*] Detected Red Hat-based system: $OS${NC}"
            sudo dnf install -y nmap hping3 gcc ruby-devel git libpcap-devel gmp-devel python3-pip
            ;;
        *Arch*)
            echo -e "${BLUE}[*] Detected Arch-based system: $OS${NC}"
            sudo pacman -S --noconfirm nmap hping gcc ruby git libpcap gmp python-pip
            ;;
        *)
            echo -e "${RED}[!] Unsupported OS: $OS${NC}"
            echo -e "${BLUE}[*] Please install the following packages manually:${NC}"
            echo "    nmap hping3 build-essential python3-pip ruby-dev git libpcap-dev libgmp3-dev"
            ;;
    esac
}

# Install bettercap gem
install_bettercap() {
    echo -e "${BLUE}[++] Installing bettercap gem...${NC}"
    
    # Check if we need to remove existing bettercap (for Parrot OS)
    if [[ $OS == *"Parrot"* ]]; then
        echo -e "${BLUE}[*] Removing existing bettercap for Parrot OS${NC}"
        sudo apt-get remove -y bettercap 2>/dev/null || true
    fi
    
    # Install bettercap gem
    if command_exists gem; then
        gem install bettercap
    else
        echo -e "${RED}[!] Ruby gem command not found${NC}"
        exit 1
    fi
}

# Check and install pipx
install_pipx() {
    if ! command_exists pipx; then
        echo -e "${BLUE}[++] Installing pipx...${NC}"
        
        # Try to install pipx using the system package manager first
        case $OS in
            *Ubuntu*|*Debian*|*Kali*|*Parrot*)
                sudo apt-get install -y pipx
                ;;
            *Fedora*|*Red\ Hat*|*CentOS*|*Rocky*)
                sudo dnf install -y pipx
                ;;
            *Arch*)
                sudo pacman -S --noconfirm python-pipx
                ;;
            *)
                # Fallback to pip installation
                python3 -m pip install --user pipx
                ;;
        esac
        
        # Ensure pipx is in PATH
        pipx ensurepath
        
        # Source the shell rc file to update PATH
        if [ -f ~/.bashrc ]; then
            source ~/.bashrc
        elif [ -f ~/.zshrc ]; then
            source ~/.zshrc
        fi
    else
        echo -e "${GREEN}[✓] pipx is already installed${NC}"
    fi
}

# Install xerosploit with pipx
install_xerosploit() {
    echo -e "${BLUE}[++] Installing Xerosploit with pipx...${NC}"
    
    # Install from current directory
    pipx install .
    
    echo -e "${GREEN}[✓] Xerosploit installed successfully!${NC}"
}

# Main installation process
main() {
    echo -e "${BLUE}[++] Starting Xerosploit installation...${NC}"
    
    # Install system dependencies
    install_system_deps
    
    # Install bettercap
    install_bettercap
    
    # Install pipx
    install_pipx
    
    # Install xerosploit
    install_xerosploit
    
    echo ""
    echo -e "${GREEN}[✓] Installation completed successfully!${NC}"
    echo -e "${CYAN}[*] You can now run 'xerosploit' from anywhere in your terminal${NC}"
    echo -e "${CYAN}[*] Note: Make sure ~/.local/bin is in your PATH${NC}"
    echo ""
    echo -e "${BLUE}To uninstall, run: pipx uninstall xerosploit${NC}"
    echo -e "${BLUE}To upgrade, run: pipx upgrade xerosploit${NC}"
}

# Run main function
main
