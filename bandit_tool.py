#!/usr/bin/env python3
from pwn import *
import json
import sys
import os

# Configuration
HOST = "bandit.labs.overthewire.org"
PORT = 2220
PASS_FILE = "passwords.json"

# Reduce log verbosity (Only show errors)
context.log_level = 'error'

def load_passwords():
    if not os.path.exists(PASS_FILE):
        return {}
    try:
        with open(PASS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_password(level, password):
    passwords = load_passwords()
    passwords[str(level)] = password
    with open(PASS_FILE, "w") as f:
        json.dump(passwords, f, indent=4)
    print(f"[+] Password for Level {level} saved.")

def connect(level, command=None):
    passwords = load_passwords()
    level_key = str(level)
    
    if level_key not in passwords:
        print(f"[*] Password for Level {level} not found in file.")
        pwd = input(f"Enter password for Level {level}: ").strip()
        if pwd:
            save_password(level, pwd)
            password = pwd
        else:
            sys.exit(1)
    else:
        password = passwords[level_key]

    user = f"bandit{level}"
    print(f"[*] Connecting to: {user}@{HOST}...")

    try:
        # Establish SSH Connection
        s = ssh(user=user, host=HOST, port=PORT, password=password)
        
        if command:
            # Single command mode
            print(f"[*] Executing command: {command}")
            # No need for tty in run(), just get the output
            output = s.run(command).recvall().decode('utf-8')
            print("-" * 30)
            print(output.strip())
            print("-" * 30)
        else:
            # Interactive mode (using shell method)
            print("[*] Starting Interactive Bash (Shell Mode)...")
            # Using shell() instead of process() for better stability
            sh = s.shell('/bin/bash')
            sh.interactive()
            sh.close()
            
        s.close()
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 bandit_tool.py <level_no> [command]")
        print("Example 1: python3 bandit_tool.py 0")
        print("Example 2: python3 bandit_tool.py 0 'cat readme'")
        sys.exit(1)
    
    level = sys.argv[1]
    cmd = sys.argv[2] if len(sys.argv) > 2 else None
    
    connect(level, cmd)
