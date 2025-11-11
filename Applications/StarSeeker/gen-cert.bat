@echo off
setlocal

REM Génère key.pem + cert.pem auto-signés valables 365 jours
REM Exige OpenSSL dans le PATH (installé avec Git for Windows ou Win64 OpenSSL)

if not exist openssl.cnf (
  echo [ERREUR] Fichier openssl.cnf introuvable dans %CD%
  exit /b 1
)

echo.
echo [*] Generation de la clé et du certificat auto-signés...
openssl req -x509 -newkey rsa:2048 -nodes ^
  -keyout key.pem -out cert.pem -days 365 ^
  -config openssl.cnf

if %ERRORLEVEL% neq 0 (
  echo [ERREUR] openssl a echoue.
  exit /b 1
)

echo.
echo [OK] Certificats generes: key.pem, cert.pem
echo   -> Place dans ce dossier. Redemarre: node server.js
endlocal
