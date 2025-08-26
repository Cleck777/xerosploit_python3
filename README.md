
[![Version](https://img.shields.io/badge/Xerosploit-Version_2.0-brightgreen.svg?maxAge=259200)]()
[![PyPI](https://img.shields.io/badge/Python-3.6+-blue.svg)]()
[![Build](https://img.shields.io/badge/Supported_OS-linux-orange.svg)]()
[![AUR](https://img.shields.io/aur/license/yaourt.svg)]()
[![pipx](https://img.shields.io/badge/install%20with-pipx-green.svg)]()

Xerosploit
=
Xerosploit is a penetration testing toolkit whose goal is to perform man in the middle attacks for testing purposes. It brings various modules that allow to realise efficient attacks, and also allows to carry out denial of service attacks and port scanning.
Powered by <a href="https://www.bettercap.org"> bettercap</a> and <a href="https://www.bettercap.org"> nmap</a>.

![](http://i.imgur.com/bbr48Ep.png)

Dependencies
=

- nmap 
- hping3 
- build-essential 
- ruby-dev 
- libpcap-dev 
- libgmp3-dev
- tabulate 
- terminaltables




Installation
=

## Method 1: pipx Installation (Recommended)

pipx installs Xerosploit in an isolated environment and makes it available globally.

### Prerequisites
- Python 3.6+
- pipx (will be installed automatically if not present)

### Quick Install
```bash
git clone https://github.com/LionSec/xerosploit
cd xerosploit
chmod +x install_pipx.sh
./install_pipx.sh
```

### Manual pipx Installation
```bash
# Install system dependencies (requires sudo)
sudo apt-get update
sudo apt-get install -y nmap hping3 build-essential python3-pip ruby-dev git libpcap-dev libgmp3-dev

# Install bettercap gem
gem install bettercap

# Install pipx if not available
sudo apt-get install -y pipx
# OR: python3 -m pip install --user pipx

# Install xerosploit
pipx install .

# Run xerosploit
xerosploit
```

### pipx Management
```bash
# Upgrade xerosploit
pipx upgrade xerosploit

# Uninstall xerosploit
pipx uninstall xerosploit

# List installed packages
pipx list
```

## Method 2: Traditional Installation
Dependencies will be automatically installed.

```bash
git clone https://github.com/LionSec/xerosploit
cd xerosploit && sudo python install.py
sudo xerosploit
```

## Installation Notes
- pipx method does not require root privileges for the Python package installation
- Traditional method requires root privileges
- Both methods require sudo for system dependencies
- Make sure `~/.local/bin` is in your PATH when using pipx


Tested on
=

<table>
    <tr>
        <th>Operative system</th>
        <th> Version </th>
    </tr>
    <tr>
        <td>Ubuntu</td>
        <td> 16.04  / 15.10 </td>
    </tr>
    <tr>
        <td>Kali linux</td>
        <td> Rolling / Sana</td>
    </tr>
    <tr>
        <td>Parrot OS</td>
        <td>3.1 </td>
    </tr>
</table>



features 
=
- Port scanning
- Network mapping
- Dos attack
- Html code injection
- Javascript code injection
- Download intercaption and replacement
- Sniffing
- Dns spoofing
- Background audio reproduction
- Images replacement
- Drifnet
- Webpage defacement and more ...

Demonstration
=
https://www.youtube.com/watch?v=35QUrtZEV9U

I have some questions!
=

Please visit https://github.com/LionSec/xerosploit/issues

Donations
=
- Paypal : https://www.paypal.me/lionsec
- Bitcoin : 12dM5kZjYMizNuXaqu7QZBLNDkXjfKYpRD


Contact
=
- Website : https://neodrix.com
- Youtube : https://youtube.com/inf98es
- Facebook : https://facebook.com/in98
- Twitter: @LionSec1
- Email : informatic98es@gmail.com
