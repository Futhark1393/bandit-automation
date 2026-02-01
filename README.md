# Bandit Automation Tool 🚩

An automation tool based on Python and `pwntools` designed to accelerate **OverTheWire Bandit** wargame solutions.

## 🚀 Features

* **Auto Login:** Stores passwords in a local JSON file and handles SSH connections automatically.
* **Quick Command Mode:** Execute remote commands without opening a shell (e.g., `cat readme`) to get flags instantly.
* **Stable Shell:** Provides a fully interactive terminal experience (PTY supported) using the `pwntools` shell method.

## 🛠️ Installation

Install the required dependencies:

```bash
pip install pwntools
```

📖 Usage

1. Interactive Mode (SSH Shell) Connects to the specified level and drops you into a shell:

```bash
python3 bandit_tool.py <level_no>
# Example:
python3 bandit_tool.py 0
```

2. Command Execution Mode Connects, runs a single command, prints the output, and exits:

```bash
python3 bandit_tool.py <level_no> "<command>"
# Example:
python3 bandit_tool.py 0 "cat readme"
```

📂 Configuration

Passwords are stored in passwords.json. The script will prompt you for the password if it's not already saved.

```JSON
{
    "0": "bandit0",
    "1": "..."
}
```

## 📚 Solutions & Write-ups

For detailed walkthroughs and solutions for each level, check out my dedicated repository:
👉 **[Bandit Wargame Solutions](https://github.com/Futhark1393/Bandit-Wargame-Solutions)**


## 🐛 Known Issues & Help Wanted

We are currently aware of a few minor UX glitches related to the `pwntools` SSH shell handling:

1.  **Visual Artifacts:** You may see raw ANSI escape codes (e.g., `\x1b[?2004h`) appearing in the terminal. This is due to how PTY/TTY is allocated to prevent "blind typing".
2.  **Double Exit:** When closing an interactive session, you might need to type `exit` twice (once to close the remote bash, once to close the local pwntools process).

**Contributions are welcome!** If you know how to fix these PTY rendering issues without losing input visibility, please submit a Pull Request. 🛠️
