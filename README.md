SilentGuard 🔐

Compact, privacy-first network & system tooling (Python + Tkinter)
Built by Allen — elliotallderson34-ops — self-taught Python developer focused on practical security tooling with a friendly UX for non-coders.

What is SilentGuard

SilentGuard is a small collection of focused Python tools for network reconnaissance, vulnerability confirmation, Wi-Fi scripting, and system defense. Tools are deliberately lightweight, readable, and come with a simple Tkinter launcher so non-technical users can run them without using a terminal.

Design goals

Practical: solve real recon Bug-Bounty pentesting & defense tasks quickly.

Tool equall to linux tool like nmap burpsuit bruteforce exploitaion tools 

Local & private: no automatic exfiltration or secret network exfiltration.

Usable by non-coders: Tkinter launcher for one-click runs.

Ethical: include warnings and require user consent for any destructive/copy operations.

Included tools (short)

Each script in /tools includes a short header explaining usage.

Recon & Vulnerability Scanner (recon_vuln_scanner.py)
Lightweight reconnaissance + vulnerability confirmation flows — scans targets, checks for common misconfigurations and known weak settings (safe-by-default; designed for authorized testing).

Wi-Fi Toolkit (wifi_scanner.py)
Parses netsh wlan show networks mode=bssid (Windows) or equivalent, extracts SSID/BSSID/signal/channel/frequency and saves CSV for analysis.

USB Guard (usb_guard_windows_gui.py)
Defensive monitor that detects removable devices, shows a GUI prompt, optionally scans with Windows Defender and quarantines only with explicit user consent.

System Logger (system_logger.py)
Periodic local logging of basic system/network stats for audit/monitoring.

GUI Launcher (gui_launcher.py)
Simple Tkinter launcher that lists tools in /tools/ and runs them; recommended for non-technical operators.

OFFENSIVE_TOOLS(for attacking systems with permission for RED TEAM ONLY)
TOOLS LIKE BRUTEFORCE DDOS_ATTACKS_KEYLOGGER EXPLOITS TO ERASE DATA LOCTION TRACKER USING (IP)

⚠️ Important — Ethics & Responsibility (Read carefully)

These tools can be used for both defensive and offensive testing.
You are responsible for any actions you perform using these tools.

Only run reconnaissance, vulnerability checks, or device monitoring on systems you own or have explicit written permission to test.

Do NOT use these tools to access, copy, or modify data on systems that you do not have authorization for.

The author (Allen / elliotallderson34-ops) is not responsible for misuse. By using this code you accept responsibility for your actions.

This repository is released under GPL-3.0 — see LICENSE for terms.

Quickstart (Windows recommended for some tools)
# clone
git clone https://github.com/elliotallderson34-ops/SilentGuard.git
cd SilentGuard

# (optional) create virtual environment
python -m venv venv
venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

Run via GUI launcher (recommended for non-coders)
python gui_launcher.py


Click Run next to the desired tool (e.g., wifi_scanner.py, usb_guard_windows_gui.py).

Outputs saved under scans/, logs under logs/ (check files after run).

Run a tool directly (example)
python tools/wifi_scanner.py
# output -> scans/latest.csv and scans/scan_YYYYMMDD_HHMMSS.csv

Example output (wifi_scanner)
ts,ssid,bssid,signal_pct,radio,channel,frequency
2025-10-05T18:12:34Z,HomeNet,4C:0B:BE:A3:1F:12,86,802.11n,11,2412

Files & structure
SilentGuard/
├── tools/                    # individual scripts (wifi_scanner.py, recon_vuln_scanner.py, usb_guard_windows_gui.py, ...)
├── scans/                    # generated outputs (ignored in VCS)
├── logs/                     # logged events
├── samples/                  # demo CSVs / screenshots
├── assets/                   # demo GIF / images
├── gui_launcher.py           # one-click launcher for non-technical users
├── requirements.txt
├── README.md
└── LICENSE (GPL-3.0)

Dependencies

Add or edit in requirements.txt. Typical libs used:
requests
random
socket
selenium
subprocess
os
tkinter
hashlib
difflib
b64encode
time
urlib.parse
phonenumber
psutil
Pillow
plyer
geopy
requests


tkinter is builtin with standard Python distributions.

Safety & deployment notes

Tools that interact with system devices (USB, Defender) may require administrator privileges on Windows. Warn users and request consent before elevating.

All copy/quarantine actions in the shipped scripts are explicitly user-confirmed — no silent copying.

If you plan to package tools as .exe, test on a sandbox VM first.

How I work (for clients / collaborators)

Small focused scripts — delivered with README & 3 days of basic support.

I do ethical/defensive/offensive work only with permission . I refuse tasks involving unauthorized data exfiltration, stealthy malware, or illegal surveillance if not under circumstances.

If you want a custom tool or script for specific task or integration, open an issue or contact me via GitHub/Fiverr.

Contributing

Fork the repo.

Add your tool under tools/ with a header that documents usage and OS requirements.

Add a single-line entry to the README Tools section.

Make a PR — I’ll review and merge.

Contact

GitHub: @elliotallderson34-ops

Fiverr: (paste your Fiverr gig link here)
Discord / Email: (theaiexplorers7@gmail.com)

License

This repository is released under the GNU General Public License v3.0 (GPL-3.0) — see LICENSE for full terms.  
