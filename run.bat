@echo off
chcp 65001 >nul
echo ====================================
echo Torrent生成器 - 快速启动
echo ====================================
echo.

python torrent_generator.py

if errorlevel 1 (
    echo.
    echo 错误：无法运行Python脚本
    echo 请确保已安装Python 3.6或更高版本
    echo.
    pause
)

