#!/usr/bin/env python3
from pwn import *
import json
import sys
import os

# Ayarlar
HOST = "bandit.labs.overthewire.org"
PORT = 2220
PASS_FILE = "passwords.json"

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

def connect(level):
    passwords = load_passwords()
    level_key = str(level)
    
    if level_key not in passwords:
        # Eğer şifre dosyada yoksa kullanıcıdan isteyip kaydedelim
        print(f"[*] Level {level} için şifre dosyada yok.")
        pwd = input(f"Level {level} şifresini girin (Kaydetmek için): ").strip()
        if pwd:
            save_password(level, pwd)
            password = pwd
        else:
            print("[-] Şifre girilmedi, çıkılıyor.")
            sys.exit(1)
    else:
        password = passwords[level_key]

    user = f"bandit{level}"
    print(f"[*] Bağlanılıyor: {user}@{HOST}...")

    try:
        # Pwntools SSH bağlantısı
        s = ssh(user=user, host=HOST, port=PORT, password=password)
        # Shell'i interaktif moda al
        s.interactive()
        s.close()
    except Exception as e:
        print(f"[!] Bağlantı hatası: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python3 bandit_tool.py <level_no>")
        sys.exit(1)
    
    connect(sys.argv[1])
