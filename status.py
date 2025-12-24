import sys
sys.dont_write_bytecode = True

import os
import json
import psutil

GAMEDIR = os.getcwd()
PIDS_FILE = os.path.join(GAMEDIR, "pids.json")

def print_green(text):
	print("\033[1;32m" + text + "\033[0m")

def print_red(text):
	print("\033[1;31m" + text + "\033[0m")

def print_yellow(text):
	print("\033[1;33m" + text + "\033[0m")

def check_process_status(pid):
	"""Check if a process is running by PID"""
	try:
		process = psutil.Process(pid)
		return process.is_running()
	except (psutil.NoSuchProcess, psutil.AccessDenied):
		return False

def main():
	if not os.path.exists(PIDS_FILE):
		print_red("> No PID file found. Server might not be running.")
		print_yellow("> Run 'python start.py' to start the server.")
		return

	with open(PIDS_FILE, "r") as f:
		pids = json.load(f)

	print_green("=" * 60)
	print_green(" SERVER STATUS")
	print_green("=" * 60)

	# Check DB
	if "db" in pids:
		db_info = pids["db"]
		status = check_process_status(db_info["pid"])
		status_text = print_green("✓ RUNNING") if status else print_red("✗ STOPPED")
		print(f"\n[DB Cache]")
		print(f"  Name: {db_info['name']}")
		print(f"  PID:  {db_info['pid']}")
		print(f"  Status: ", end="")
		if status:
			print_green("✓ RUNNING")
		else:
			print_red("✗ STOPPED")

	# Check Auth
	if "auth" in pids:
		auth_info = pids["auth"]
		status = check_process_status(auth_info["pid"])
		print(f"\n[Auth Server]")
		print(f"  Name: {auth_info['name']}")
		print(f"  PID:  {auth_info['pid']}")
		print(f"  Status: ", end="")
		if status:
			print_green("✓ RUNNING")
		else:
			print_red("✗ STOPPED")

	# Check Channels
	if "channel" in pids:
		print(f"\n[Game Channels]")
		running_count = 0
		stopped_count = 0

		for core_info in pids["channel"]:
			status = check_process_status(core_info["pid"])
			status_icon = "✓" if status else "✗"
			status_color = print_green if status else print_red

			print(f"  {status_icon} {core_info['name']:25} PID: {core_info['pid']:6} ", end="")
			if status:
				print_green("RUNNING")
				running_count += 1
			else:
				print_red("STOPPED")
				stopped_count += 1

		print(f"\n  Total Cores: {running_count + stopped_count}")
		print(f"  Running: ", end="")
		print_green(str(running_count))
		print(f"  Stopped: ", end="")
		if stopped_count > 0:
			print_red(str(stopped_count))
		else:
			print_green(str(stopped_count))

	print_green("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
	main()
