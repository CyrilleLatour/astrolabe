@echo off
REM Toujours se placer dans le dossier où se trouve ce script
cd /d "%~dp0"

echo ================================
echo Lancement de WorldWatch avec serveur HTTP...
echo ================================

:: Se placer dans le dossier www (toujours relatif au batch)
cd "MontreApp\www"

:: Chemins possibles de Firefox
set FF64="C:\Program Files\Mozilla Firefox\firefox.exe"
set FF32="C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
set FFUSR="%LOCALAPPDATA%\Mozilla Firefox\firefox.exe"

:: URL du serveur local
set URL="http://localhost:8000/montre.html"

echo Demarrage du serveur HTTP Python...
echo Le serveur sera accessible sur : %URL%
echo Pour arreter le serveur, fermez cette fenetre ou appuyez sur Ctrl+C
echo.

:: Attendre 2 secondes puis ouvrir le navigateur
timeout /t 2 /nobreak >nul

:: Essayer Firefox (64 bits)
if exist %FF64% (
    start "" %FF64% %URL%
    goto :server
)

:: Essayer Firefox (32 bits)
if exist %FF32% (
    start "" %FF32% %URL%
    goto :server
)

:: Essayer Firefox dans AppData
if exist %FFUSR% (
    start "" %FFUSR% %URL%
    goto :server
)

:: Essayer Firefox via PATH
where firefox >nul 2>nul
if %ERRORLEVEL%==0 (
    start firefox %URL%
    goto :server
)

:: Si Firefox introuvable → fallback sur Edge
echo Firefox introuvable, lancement avec Edge...
start msedge %URL%

:server
:: Lancer le serveur HTTP Python
python -m http.server
