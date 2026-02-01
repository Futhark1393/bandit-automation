#!/usr/bin/env python3
from pwn import *
import json
import sys
import os

# Ayarlar
HOST = "bandit.labs.overthewire.org"
PORT = 2220
PASS_FILE = "passwords.json"

# Log kirliliğini azalt (Sadece hataları gör)
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
    print(f"[+] Level {level} şifresi kaydedildi.")

def connect(level, command=None):
    passwords = load_passwords()
    level_key = str(level)
    
    if level_key not in passwords:
        print(f"[*] Level {level} için şifre dosyada yok.")
        pwd = input(f"Level {level} şifresini girin: ").strip()
        if pwd:
            save_password(level, pwd)
            password = pwd
        else:
            sys.exit(1)
    else:
        password = passwords[level_key]

    user = f"bandit{level}"
    print(f"[*] Bağlanılıyor: {user}@{HOST}...")

    try:
        # SSH Bağlantısını kur
        s = ssh(user=user, host=HOST, port=PORT, password=password)
        
        if command:
            # Tek seferlik komut modu
            print(f"[*] Komut çalıştırılıyor: {command}")
            # run() metodunda tty gerekmez, direkt çıktıyı alırız
            output = s.run(command).recvall().decode('utf-8')
            print("-" * 30)
            print(output.strip())
            print("-" * 30)
        else:
            # İnteraktif mod (shell metodu kullanılarak)
            print("[*] İnteraktif Bash başlatılıyor (Shell Modu)...")
            # process yerine shell() kullanıyoruz, bu daha kararlıdır
            sh = s.shell('/bin/bash')
            sh.interactive()
            sh.close()
            
        s.close()
    except Exception as e:
        print(f"[!] Hata: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python3 bandit_tool.py <level_no> [komut]")
        print("Örnek 1: python3 bandit_tool.py 0")
        print("Örnek 2: python3 bandit_tool.py 0 'cat readme'")
        sys.exit(1)
    
    level = sys.argv[1]
    cmd = sys.argv[2] if len(sys.argv) > 2 else None
    
    connect(level, cmd)
