import sys
sys.dont_write_bytecode = True

import os

GAMEDIR = os.getcwd()
CHANNELS_DIR = os.path.join(GAMEDIR, "channels")

def print_separator(title):
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def tail_file(filepath, lines=10):
    """Read last N lines from a file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()
            last_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            return last_lines
    except FileNotFoundError:
        return [f"  [File not found: {filepath}]\n"]
    except Exception as e:
        return [f"  [Error reading file: {e}]\n"]

def show_logs():
    # DB Cache logs
    print_separator("DB CACHE - Last 10 Syserr Entries")
    db_log = os.path.join(CHANNELS_DIR, "db", "syserr.log")
    for line in tail_file(db_log):
        print(f"  {line.rstrip()}")

    # Auth Server logs
    print_separator("AUTH SERVER - Last 10 Syserr Entries")
    auth_log = os.path.join(CHANNELS_DIR, "auth", "syserr.log")
    for line in tail_file(auth_log):
        print(f"  {line.rstrip()}")

    # Game Channel cores
    print_separator("GAME CHANNEL - Core 1 - Last 10 Syserr Entries")
    core1_log = os.path.join(CHANNELS_DIR, "channel1", "core1", "syserr.log")
    for line in tail_file(core1_log):
        print(f"  {line.rstrip()}")

    print_separator("GAME CHANNEL - Core 2 - Last 10 Syserr Entries")
    core2_log = os.path.join(CHANNELS_DIR, "channel1", "core2", "syserr.log")
    for line in tail_file(core2_log):
        print(f"  {line.rstrip()}")

    print_separator("GAME CHANNEL - Core 3 - Last 10 Syserr Entries")
    core3_log = os.path.join(CHANNELS_DIR, "channel1", "core3", "syserr.log")
    for line in tail_file(core3_log):
        print(f"  {line.rstrip()}")

    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    show_logs()
