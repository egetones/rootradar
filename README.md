<div align="center">

# RootRadar

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Type](https://img.shields.io/badge/Type-Blue_Team_Scanner-blue)

<p>
  <strong>A Linux Persistence Scanner designed to detect unauthorized startup mechanisms.</strong>
</p>

[Report Bug](https://github.com/egetones/rootradar/issues) · [Request Feature](https://github.com/egetones/rootradar/issues)

</div>

---

## Description

**RootRadar** is a Python-based utility developed for **Defensive Security** (Blue Team operations). Its primary function is to scan common and critical Linux system directories and configuration files for unauthorized persistence mechanisms.

It specifically looks for code injection in user startup files (`.bashrc`), scheduled tasks (`cron`), and active system services (`systemd`) which could be used by malware or rootkits (like **Phantom**) to maintain access after a reboot.

### Key Features

  **Persistence Detection:** Scans the most critical points of persistence on Linux.
  **Configuration Audit:** Analyzes user shell initialization files for suspicious commands.
  **Systemd Monitoring:** Checks for recently modified or suspicious system services.
  **Colorized Output:** Provides clear, actionable alerts in the terminal.

---

## Usage

### 1. Compile/Run
Since this is a simple Python script with no external dependencies, simply clone and run:
```bash
git clone https://github.com/egetones/rootradar.git
cd rootradar
python3 rootradar.py
```
### 2. Permissions
Note that reading files in /etc/systemd/ requires root privileges. Run with sudo for a complete system scan:
```bash
sudo python3 rootradar.py
