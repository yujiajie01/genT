@echo off
chcp 65001 >nul
echo ====================================
echo Torrent生成器 - 构建 Release 文件
echo ====================================
echo.

echo 正在运行构建脚本...
python build_release.py

echo.
echo 完成！
echo.
pause

