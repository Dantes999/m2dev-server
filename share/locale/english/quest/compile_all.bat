@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo ============================================================
echo METIN2 QUEST COMPILER
echo ============================================================
echo.

set COMPILED=0
set FAILED=0
set TOTAL=0

echo Compiling quests...
echo.

for /f "usebackq tokens=*" %%a in ("locale_list") do (
    set "line=%%a"

    REM Skip empty lines
    if not "!line!"=="" (
        REM Get first character
        set "first_char=!line:~0,1!"

        REM Skip lines starting with # (comments)
        if not "!first_char!"=="#" (
            REM Also skip lines that are just spaces
            echo !line! | findstr /r /c:"^[^ ]" >nul 2>&1
            if !errorlevel! equ 0 (
                set /a TOTAL+=1

                REM Compile the quest
                qc.exe "!line!" >nul 2>&1

                if !errorlevel! equ 0 (
                    set /a COMPILED+=1
                    echo [OK] [!TOTAL!] !line!
                ) else (
                    set /a FAILED+=1
                    echo [ERROR] [!TOTAL!] !line!
                )
            )
        )
    )
)

echo.
echo ============================================================
echo COMPILATION SUMMARY
echo ============================================================
echo [OK] Successful: %COMPILED%/%TOTAL%

if %FAILED% gtr 0 (
    echo [ERROR] Failed: %FAILED%/%TOTAL%
    echo ============================================================
    echo COMPILATION FAILED
) else (
    echo ============================================================
    echo SUCCESS: All quests compiled successfully!
)

echo ============================================================
exit /b %FAILED%
