@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo ============================================================
echo COMPILING QUESTS WITH PRE_QC PREPROCESSING
echo ============================================================
echo.

set COMPILED=0
set FAILED=0
set TOTAL=0

REM List of quests that need pre_qc
set "quests[0]=systems/dragon_soul.quest"
set "quests[1]=systems/dragon_soul_refine.quest"
set "quests[2]=systems/dragon_soul_shop.quest"
set "quests[3]=systems/dragon_soul_daily_gift_mgr.quest"
set "quests[4]=systems/dragon_soul_daily_gift.quest"
set "quests[5]=dungeons/flame_dungeon.quest"
set "quests[6]=dungeons/spider_dungeon_3floor_boss.quest"
set "quests[7]=events/event_flame_dungeon_open.quest"
set "quests[8]=events/new_christmas.quest"
set "quests[9]=events/new_christmas_2012.quest"
set "quests[10]=events/new_christmas_2012_nog.quest"
set "quests[11]=events/new_christmas_2012_sock.quest"
set "quests[12]=main_quests/main_quest_lv60.quest"
set "quests[13]=main_quests/main_quest_lv66.quest"
set "quests[14]=main_quests/main_quest_lv72.quest"
set "quests[15]=main_quests/main_quest_lv78.quest"
set "quests[16]=main_quests/main_quest_lv84.quest"
set "quests[17]=main_quests/main_quest_lv90.quest"
set "quests[18]=main_quests/main_quest_lv91.quest"
set "quests[19]=main_quests/main_quest_lv92.quest"
set "quests[20]=main_quests/main_quest_lv93.quest"
set "quests[21]=main_quests/main_quest_lv94.quest"
set "quests[22]=main_quests/main_quest_lv95.quest"
set "quests[23]=main_quests/main_quest_lv96.quest"
set "quests[24]=main_quests/main_quest_lv97.quest"
set "quests[25]=main_quests/main_quest_lv98.quest"
set "quests[26]=main_quests/main_quest_flame_lv99.quest"
set "quests[27]=main_quests/main_quest_flame_lv100.quest"
set "quests[28]=main_quests/main_quest_flame_lv101.quest"
set "quests[29]=main_quests/main_quest_flame_lv102.quest"
set "quests[30]=main_quests/main_quest_flame_lv103.quest"
set "quests[31]=main_quests/main_quest_flame_lv104.quest"
set "quests[32]=main_quests/main_quest_flame_lv105.quest"
set "quests[33]=misc/test_att_resist.quest"

set idx=0

:loop
if not defined quests[%idx%] goto :done

set "quest=!quests[%idx%]!"
set /a idx+=1
set /a TOTAL+=1

echo [!TOTAL!] Processing: !quest!

REM Run pre_qc to preprocess the quest
python pre_qc.py "!quest!" >nul 2>&1

if !errorlevel! neq 0 (
    echo     [WARN] Pre-processing failed, trying direct compile...
    qc.exe "!quest!" >nul 2>&1

    if !errorlevel! equ 0 (
        set /a COMPILED+=1
        echo     [OK] !quest! (direct)
    ) else (
        set /a FAILED+=1
        echo     [ERROR] !quest!
    )
) else (
    REM Compile the preprocessed version
    qc.exe "pre_qc/!quest!" >nul 2>&1

    if !errorlevel! equ 0 (
        set /a COMPILED+=1
        echo     [OK] !quest! (pre_qc)
    ) else (
        set /a FAILED+=1
        echo     [ERROR] !quest!
    )
)

goto :loop

:done

echo.
echo ============================================================
echo COMPILATION SUMMARY
echo ============================================================
echo Total quests: %TOTAL%
echo Compiled successfully: %COMPILED%
echo Failed: %FAILED%
echo ============================================================

if %FAILED% gtr 0 (
    echo.
    echo WARNING: Some quests still failed to compile!
    exit /b 1
) else (
    echo.
    echo SUCCESS: All quests compiled successfully!
    exit /b 0
)
