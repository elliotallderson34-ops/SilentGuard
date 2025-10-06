import re
import subprocess
import time
import geopy.geocoders
import argparse
import csv
import json
from datetime import datetime

# Netsh command (list form is safer than shell=True)
NETSH_CMD = ["netsh", "wlan", "show", "networks", "mode=bssid"]

HEADERS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; DuckDuckGo-Favicons-Bot/1.0; +https://duckduckgo.com)",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/120.0.0.0 Safari/537.36",
    "Opera/9.80 (Android; Opera Mini/82.0.2254/191.303; U; en) Presto/2.12.423 Version/12.16",
    "Wget/1.21.4"
]

# regex patterns (case-insensitive)
_re_ssid = re.compile(r"^\s*SSID\s+\d+\s*:\s*(.*)$", re.IGNORECASE)
_re_bssid = re.compile(r"^\s*BSSID\s+\d+\s*:\s*([0-9A-Fa-f:-]+)", re.IGNORECASE)
_re_signal = re.compile(r"^\s*Signal\s*:\s*(\d+)%", re.IGNORECASE)
_re_channel = re.compile(r"^\s*Channel\s*:\s*(\d+)", re.IGNORECASE)
_re_radio = re.compile(r"^\s*Radio type\s*:\s*(.*)$", re.IGNORECASE)
_re_auth = re.compile(r"^\s*Authentication\s*:\s*(.*)$", re.IGNORECASE)
_re_encrypt = re.compile(r"^\s*Encryption\s*:\s*(.*)$", re.IGNORECASE)


def run_netsh_command(retries: int = 3, delay: float = 1.0) -> str | None:
    """
    Run netsh command and return stdout as str, or None on failure.
    """
    attempt = 0
    while attempt < retries:
        try:
            proc = subprocess.run(NETSH_CMD, capture_output=True, text=True, timeout=10)
            if proc.returncode == 0:
                return proc.stdout
            else:
                # non-zero exit, retry
                attempt += 1
                time.sleep(delay)
        except FileNotFoundError:
            print("[!] netsh command not found (are you on Windows?).")
            return None
        except subprocess.TimeoutExpired:
            attempt += 1
            time.sleep(delay)
    print(f"[!] Failed to run netsh after {retries} attempts.")
    return None


def get_network_location(ssid):
    """
    Get the location of a network using its SSID.
    """
    try:
        geolocator = geopy.geocoders.Nominatim(user_agent=HEADERS[0])
        location = geolocator.geocode(ssid)
        if location:
            return location.latitude, location.longitude
        else:
            return None
    except Exception as e:
        print(f"[!] Error getting location for {ssid}: {e}")
        return None


def parse_netsh_output(output: str) -> list:
    """
    Parse netsh 'show networks mode=bssid' output into a list of networks.
    Each network is a dict: {SSID, BSSID, SIGNAL, CHANNEL, RADIO, AUTH, ENCRYPTION, LOCATION}
    There may be multiple entries with the same SSID (different BSSIDs).
    """
    networks = []
    current_ssid = None
    current_entry = None

    for raw_line in output.splitlines():
        line = raw_line.rstrip()

        ssid_match = _re_ssid.match(line)
        bssid_match = _re_bssid.match(line)
        signal_match = _re_signal.match(line)
        channel_match = _re_channel.match(line)
        radio_match = _re_radio.match(line)
        auth_match = _re_auth.match(line)
        encrypt_match = _re_encrypt.match(line)

        if ssid_match:
            # New SSID block; save any in-progress entry
            current_ssid = ssid_match.group(1).strip()
            # don't append yet — BSSID usually follows
            current_entry = None
        elif bssid_match:
            # Start a new entry for this BSSID, attach the last seen SSID
            # If a previous current_entry exists, save it first
            if current_entry:
                networks.append(current_entry)
            current_entry = {"SSID": current_ssid, "BSSID": bssid_match.group(1).strip()}
        elif signal_match and current_entry is not None:
            try:
                current_entry["SIGNAL"] = int(signal_match.group(1))
            except ValueError:
                current_entry["SIGNAL"] = signal_match.group(1)
        elif channel_match and current_entry is not None:
            current_entry["CHANNEL"] = channel_match.group(1).strip()
        elif radio_match:
            # radio may be at SSID block level or BSSID level; attach to current_entry if present
            if current_entry is not None:
                current_entry["RADIO"] = radio_match.group(1).strip()
        elif auth_match:
            if current_entry is not None:
                current_entry["AUTH"] = auth_match.group(1).strip()
        elif encrypt_match:
            if current_entry is not None:
                current_entry["ENCRYPTION"] = encrypt_match.group(1).strip()

    # append last entry if exists
    if current_entry:
        networks.append(current_entry)

    # Get the location of each network
    for network in networks:
        location = get_network_location(network["SSID"])
        if location:
            network["LOCATION"] = location

    return networks


def save_json(rows: list, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"timestamp": datetime.utcnow().isoformat(), "results": rows}, f, indent=2)
    print(f"[+] Saved JSON to {len(path)} rows to {path}")


def main():
    p = argparse.ArgumentParser(description="Windows netsh Wi-Fi scanner")
    p.add_argument("--json", help="Save results to JSON")
    args = p.parse_args()

    out = run_netsh_command()
    if out is None:
        return

    rows = parse_netsh_output(out)
    if not rows:
        print("[+] No networks parsed (empty output).")
    else:
        for r in rows:
            print(r)


    if args.json:
        save_json(rows, args.json)


if __name__ == "__main__":
    main()
