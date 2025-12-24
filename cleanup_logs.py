#!/usr/bin/env python3
"""
Log Cleanup Script for Metin2 Server
Cleans up syslog.log and syserr.log files for all channels and cores
"""

import os
import sys
from pathlib import Path

def cleanup_logs(base_path):
    """Clean up all log files in the server directory"""
    base_path = Path(base_path)

    if not base_path.exists():
        print(f"Error: Path {base_path} does not exist!")
        return False

    # Patterns to search for
    log_patterns = [
        "channels/*/syslog.log",
        "channels/*/syserr.log",
        "channels/*/*/syslog.log",
        "channels/*/*/syserr.log",
        "channels/*/*/*/syslog.log",
        "channels/*/*/*/syserr.log",
    ]

    cleaned_count = 0

    print("=" * 60)
    print("Metin2 Server Log Cleanup")
    print("=" * 60)

    for pattern in log_patterns:
        for log_file in base_path.glob(pattern):
            if log_file.is_file():
                try:
                    # Get file size before
                    size_before = log_file.stat().st_size

                    # Clear the file
                    with open(log_file, 'w') as f:
                        f.write('')

                    print(f"✓ Cleaned: {log_file.relative_to(base_path)} ({size_before:,} bytes)")
                    cleaned_count += 1

                except Exception as e:
                    print(f"✗ Failed to clean {log_file.relative_to(base_path)}: {e}")

    print("=" * 60)
    print(f"Cleaned {cleaned_count} log file(s)")
    print("=" * 60)

    return True

if __name__ == "__main__":
    # Get the script's directory
    script_dir = Path(__file__).parent

    # Allow custom path as argument
    if len(sys.argv) > 1:
        base_path = Path(sys.argv[1])
    else:
        base_path = script_dir

    print(f"Base path: {base_path.absolute()}\n")
    cleanup_logs(base_path)
