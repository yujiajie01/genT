@echo off
chcp 65001 >nul
echo ====================================
echo Torrent生成器 - 打包exe
echo ====================================
echo.

echo 正在安装PyInstaller...
pip install pyinstaller

echo.
echo 正在打包为exe文件...
pyinstaller --onefile --windowed --name=TorrentGenerator --clean torrent_generator.py

echo.
echo 打包完成！exe文件在 dist 文件夹中
echo.
pause

