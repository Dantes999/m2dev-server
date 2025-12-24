#!/usr/bin/env python3
"""Quest compiler with pre_qc support"""
import os
import subprocess
import sys

QUEST_DIR = os.getcwd()
LOCALE_LIST = os.path.join(QUEST_DIR, "locale_list")

# Quests that need pre_qc preprocessing
PRE_QC_QUESTS = [
    'dragon_soul.quest',
    'dragon_soul_refine.quest',
    'dragon_soul_shop.quest',
    'dragon_soul_daily_gift.quest',
    'dragon_soul_daily_gift_mgr.quest',
    'flame_dungeon.quest',
    'event_flame_dungeon_open.quest',
    'main_quest_lv60.quest',
    'main_quest_lv66.quest',
    'main_quest_lv72.quest',
    'main_quest_lv78.quest',
    'main_quest_lv84.quest',
    'main_quest_lv90.quest',
    'main_quest_lv91.quest',
    'main_quest_lv92.quest',
    'main_quest_lv93.quest',
    'main_quest_lv94.quest',
    'main_quest_lv95.quest',
    'main_quest_lv96.quest',
    'main_quest_lv97.quest',
    'main_quest_lv98.quest',
    'main_quest_flame_lv99.quest',
    'main_quest_flame_lv100.quest',
    'main_quest_flame_lv101.quest',
    'main_quest_flame_lv102.quest',
    'main_quest_flame_lv103.quest',
    'main_quest_flame_lv104.quest',
    'main_quest_flame_lv105.quest',
]

def needs_pre_qc(quest_path):
    """Check if quest needs pre_qc preprocessing"""
    quest_name = os.path.basename(quest_path)
    return quest_name in PRE_QC_QUESTS

def run_pre_qc(quest_file):
    """Run pre_qc on a quest file"""
    try:
        sys.path.insert(0, QUEST_DIR)
        import pre_qc

        original_dir = os.getcwd()
        os.chdir(QUEST_DIR)

        result = pre_qc.run(quest_file)

        os.chdir(original_dir)
        return result
    except Exception as e:
        return False

def compile_quest(quest_path):
    """Compile a single quest"""
    full_path = os.path.join(QUEST_DIR, quest_path)

    if not os.path.exists(full_path):
        return False, f"File not found: {quest_path}"

    # Check if needs pre_qc
    if needs_pre_qc(quest_path):
        if run_pre_qc(quest_path):
            # Use pre_qc version
            compile_path = f"pre_qc/{quest_path}"
        else:
            compile_path = quest_path
    else:
        compile_path = quest_path

    # Compile
    try:
        result = subprocess.run(
            ['qc.exe', compile_path],
            cwd=QUEST_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return True, None
        else:
            error = result.stdout + result.stderr
            # Extract first line of error
            error_line = error.split('\n')[0] if error else "Unknown error"
            return False, error_line
    except subprocess.TimeoutExpired:
        return False, "Compilation timeout"
    except Exception as e:
        return False, str(e)

def main():
    print("="*60)
    print("METIN2 QUEST COMPILER")
    print("="*60)
    print()

    # Read quest list
    quests = []
    with open(LOCALE_LIST, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Strip whitespace and Windows line endings
            line = line.strip().replace('\r', '').replace('\n', '')

            # Skip empty lines and comments
            if line and not line.startswith('#'):
                quests.append(line)

    total = len(quests)
    compiled = 0
    failed = 0
    failed_list = []

    print(f"Found {total} quests to compile")
    print()

    for i, quest in enumerate(quests, 1):
        success, error = compile_quest(quest)

        if success:
            compiled += 1
            print(f"[OK] [{i}/{total}] Compiled: {quest}")
        else:
            failed += 1
            failed_list.append((quest, error))
            print(f"[ERROR] [{i}/{total}] Failed: {quest}")
            if error:
                print(f"    {error}")

    print()
    print("="*60)
    print("COMPILATION SUMMARY")
    print("="*60)
    print(f"Total: {total}")
    print(f"Compiled: {compiled}")
    print(f"Failed: {failed}")

    if failed_list:
        print()
        print("Failed quests:")
        for quest, error in failed_list[:10]:  # Show first 10
            print(f"  - {quest}")
            if error:
                print(f"    {error[:80]}")

    print("="*60)

    return failed == 0

if __name__ == "__main__":
    os.chdir(QUEST_DIR)
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[WARN] Compilation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
