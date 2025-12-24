#!/usr/bin/env python3
"""
Metin2 Quest Compiler
Compiles all quest files listed in locale_list
Python 3 compatible version
"""

import os
import sys
import shutil
from pathlib import Path

# Configuration
QUEST_DIR = Path("share/locale/english/quest")
LOCALE_LIST = QUEST_DIR / "locale_list"
OBJECT_DIR = QUEST_DIR / "object"
PRE_QC_DIR = QUEST_DIR / "pre_qc"
QC_COMPILER = QUEST_DIR / "qc.exe"

# Colors for terminal output (Windows compatible)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def disable():
        Colors.HEADER = ''
        Colors.OKBLUE = ''
        Colors.OKCYAN = ''
        Colors.OKGREEN = ''
        Colors.WARNING = ''
        Colors.FAIL = ''
        Colors.ENDC = ''
        Colors.BOLD = ''

# Disable colors on Windows if not supported
if os.name == 'nt':
    try:
        import colorama
        colorama.init()
    except ImportError:
        Colors.disable()


def print_header(msg):
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{msg}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")


def print_success(msg):
    print(f"{Colors.OKGREEN}[OK] {msg}{Colors.ENDC}")


def print_error(msg):
    print(f"{Colors.FAIL}[ERROR] {msg}{Colors.ENDC}")


def print_warning(msg):
    print(f"{Colors.WARNING}[WARN] {msg}{Colors.ENDC}")


def print_info(msg):
    print(f"{Colors.OKCYAN}>> {msg}{Colors.ENDC}")


def setup_directories():
    """Create necessary directories"""
    print_info("Setting up directories...")

    # Remove old object directory and recreate
    if OBJECT_DIR.exists():
        shutil.rmtree(OBJECT_DIR)
    OBJECT_DIR.mkdir(parents=True, exist_ok=True)

    # Create pre_qc directory
    PRE_QC_DIR.mkdir(parents=True, exist_ok=True)

    print_success("Directories ready")


def check_requirements():
    """Check if required files exist"""
    print_info("Checking requirements...")

    if not QUEST_DIR.exists():
        print_error(f"Quest directory not found: {QUEST_DIR}")
        return False

    if not LOCALE_LIST.exists():
        print_error(f"locale_list not found: {LOCALE_LIST}")
        return False

    if not QC_COMPILER.exists():
        print_error(f"Quest compiler not found: {QC_COMPILER}")
        print_warning("Looking for alternative qc.exe locations...")

        # Try alternative locations
        alt_locations = [
            Path("share/bin/qc.exe"),
            QUEST_DIR / "qc",
        ]

        for alt_loc in alt_locations:
            if alt_loc.exists():
                print_success(f"Found compiler at: {alt_loc}")
                return True

        return False

    print_success("All requirements met")
    return True


def run_pre_qc(quest_file):
    """Run pre_qc processor on a quest file if it has define statements"""
    try:
        # Import pre_qc module
        sys.path.insert(0, str(QUEST_DIR))
        import pre_qc

        # Change to quest directory for pre_qc
        original_dir = os.getcwd()
        os.chdir(QUEST_DIR)

        result = pre_qc.run(str(quest_file))

        os.chdir(original_dir)
        return result
    except Exception as e:
        if 'original_dir' in locals():
            os.chdir(original_dir)
        # Silently return False - most quests don't have defines
        return False


def compile_quest(quest_file, index, total):
    """Compile a single quest file"""
    quest_path = QUEST_DIR / quest_file

    if not quest_path.exists():
        print_error(f"[{index}/{total}] Quest file not found: {quest_file}")
        return False

    # Run pre_qc if the file has define statements
    use_pre_qc = run_pre_qc(quest_file)

    # Determine which file to compile
    if use_pre_qc:
        compile_file = PRE_QC_DIR / quest_file
    else:
        compile_file = quest_path

    # Compile the quest
    print_info(f"[{index}/{total}] Compiling: {quest_file}")

    # Change to quest directory for compilation
    original_dir = os.getcwd()
    os.chdir(QUEST_DIR)

    try:
        # Run qc compiler
        if use_pre_qc:
            cmd = f'qc.exe "pre_qc/{quest_file}"'
        else:
            cmd = f'qc.exe "{quest_file}"'

        result = os.system(cmd)

        os.chdir(original_dir)

        if result != 0:
            print_error(f"[{index}/{total}] Compilation failed: {quest_file}")
            return False

        print_success(f"[{index}/{total}] Compiled: {quest_file}")
        return True

    except Exception as e:
        os.chdir(original_dir)
        print_error(f"[{index}/{total}] Exception: {quest_file} - {e}")
        return False


def compile_all_quests():
    """Compile all quests from locale_list"""
    print_header("QUEST COMPILATION")

    # Read quest list
    print_info(f"Reading quest list from: {LOCALE_LIST}")

    with open(LOCALE_LIST, 'r', encoding='utf-8') as f:
        quest_files = [line.strip() for line in f if line.strip()]

    total = len(quest_files)
    print_success(f"Found {total} quest files to compile")
    print()

    # Compile each quest
    success_count = 0
    failed_quests = []

    for index, quest_file in enumerate(quest_files, 1):
        if compile_quest(quest_file, index, total):
            success_count += 1
        else:
            failed_quests.append(quest_file)

    # Print summary
    print()
    print_header("COMPILATION SUMMARY")
    print_success(f"Successful: {success_count}/{total}")

    if failed_quests:
        print_error(f"Failed: {len(failed_quests)}/{total}")
        print()
        print_warning("Failed quests:")
        for quest in failed_quests:
            print(f"  - {quest}")
        return False
    else:
        print_success("All quests compiled successfully!")
        return True


def set_permissions():
    """Set permissions on object directory (Unix-like systems)"""
    if os.name != 'nt':  # Not Windows
        try:
            os.system(f'chmod -R 770 {OBJECT_DIR}')
            print_success("Permissions set")
        except Exception as e:
            print_warning(f"Could not set permissions: {e}")


def main():
    """Main compilation process"""
    print()
    print_header("METIN2 QUEST COMPILER")
    print()

    # Check requirements
    if not check_requirements():
        print_error("Requirements check failed!")
        return 1

    print()

    # Setup directories
    setup_directories()
    print()

    # Compile all quests
    success = compile_all_quests()

    # Set permissions
    if success:
        print()
        set_permissions()

    print()

    if success:
        print_header("COMPILATION COMPLETE")
        return 0
    else:
        print_header("COMPILATION FAILED")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print()
        print_warning("Compilation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
