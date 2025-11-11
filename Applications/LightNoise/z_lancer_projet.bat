@echo off
cd /d "%~dp0"

echo ================================
echo Lancement de LightNoise...
echo ================================

:: Chemins possibles de Firefox
set FF64="C:\Program Files\Mozilla Firefox\firefox.exe"
set FF32="C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
set FFUSR="%LOCALAPPDATA%\Mozilla Firefox\firefox.exe"

:: Fichier HTML à ouvrir
set HTML="%~dp0LightNoise.html"

:: Essayer Firefox (64 bits)
if exist %FF64% (
    start "" %FF64% %HTML%
    exit
)

:: Essayer Firefox (32 bits)
if exist %FF32% (
    start "" %FF32% %HTML%
    exit
)

:: Essayer Firefox dans AppData
if exist %FFUSR% (
    start "" %FFUSR% %HTML%
    exit
)

:: Essayer Firefox via PATH
where firefox >nul 2>nul
if %ERRORLEVEL%==0 (
    start firefox %HTML%
    exit
)

:: Si Firefox introuvable → fallback sur Edge
echo Firefox introuvable, lancement avec Edge...
start msedge %HTML%
exit
