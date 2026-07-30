@echo off
echo ============================================
echo   Haus-Cockpit - Push zu GitHub
echo ============================================
cd /d "%~dp0"
if not exist ".git" (
  git init
  git branch -M main
)
git add .
set /p MSG="Commit-Nachricht (Enter = 'update'): "
if "%MSG%"=="" set MSG=update
git commit -m "%MSG%"
git remote get-url origin >nul 2>&1
if errorlevel 1 (
  echo.
  echo Kein Remote gesetzt. Lege zuerst auf GitHub ein Repo "haus-cockpit" an, dann:
  echo   git remote add origin https://github.com/andre69190-del/haus-cockpit.git
  echo.
  pause
  exit /b
)
git push -u origin main
echo.
echo Fertig. In Coolify jetzt "Deploy" bzw. Redeploy ausloesen.
pause
