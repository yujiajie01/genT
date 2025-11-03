@echo off
chcp 65001 >nul
echo ====================================
echo 创建 GitHub Release
echo ====================================
echo.

python create_release.py

echo.
pause

