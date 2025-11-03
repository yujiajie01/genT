#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
构建脚本：生成 exe 和 zip 文件用于 GitHub Release
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def build_exe():
    """构建 exe 文件"""
    print("=" * 50)
    print("Building exe file...")
    print("=" * 50)
    
    # 检查是否已经存在 exe
    dist_dir = Path("dist")
    exe_file = dist_dir / "TorrentGenerator.exe"
    if exe_file.exists():
        print("[OK] exe file already exists, skipping build")
        return True
    
    try:
        import PyInstaller.__main__
        
        PyInstaller.__main__.run([
            'torrent_generator.py',
            '--onefile',
            '--windowed',
            '--name=TorrentGenerator',
            '--icon=NONE',
            '--clean',
        ])
        
        print("[OK] exe file built successfully")
        return True
    except ImportError:
        print("Error: PyInstaller not installed")
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        # 重新运行
        import PyInstaller.__main__
        PyInstaller.__main__.run([
            'torrent_generator.py',
            '--onefile',
            '--windowed',
            '--name=TorrentGenerator',
            '--icon=NONE',
            '--clean',
        ])
        print("[OK] exe file built successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to build exe: {e}")
        return False

def create_release_dir():
    """创建 release 目录"""
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    return release_dir

def create_zip(release_dir):
    """创建 zip 文件"""
    print("\n" + "=" * 50)
    print("Creating zip file...")
    print("=" * 50)
    
    import zipfile
    from datetime import datetime
    
    # 获取版本号（从日期或 git tag）
    version = datetime.now().strftime("%Y%m%d")
    
    # 检查 dist 目录
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("[ERROR] dist directory not found, please build exe first")
        return False
    
    exe_file = dist_dir / "TorrentGenerator.exe"
    if not exe_file.exists():
        print("[ERROR] TorrentGenerator.exe not found, please build exe first")
        return False
    
    # 创建 zip 文件
    zip_filename = release_dir / f"TorrentGenerator-v{version}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 添加 exe 文件
        zipf.write(exe_file, "TorrentGenerator.exe")
        # 添加 README
        if Path("README.md").exists():
            zipf.write("README.md", "README.md")
    
    print(f"[OK] Zip file created: {zip_filename}")
    return True

def copy_exe_to_release(release_dir):
    """复制 exe 到 release 目录"""
    dist_dir = Path("dist")
    exe_file = dist_dir / "TorrentGenerator.exe"
    
    if exe_file.exists():
        shutil.copy2(exe_file, release_dir / "TorrentGenerator.exe")
        print(f"[OK] exe file copied to release directory")
        return True
    else:
        print("[ERROR] exe file not found")
        return False

def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("Torrent Generator - Build Release Files")
    print("=" * 50 + "\n")
    
    # 创建 release 目录
    release_dir = create_release_dir()
    
    # 构建 exe
    if not build_exe():
        print("\nBuild failed!")
        return
    
    # 复制 exe 到 release
    copy_exe_to_release(release_dir)
    
    # 创建 zip
    if not create_zip(release_dir):
        print("\nFailed to create zip!")
        return
    
    print("\n" + "=" * 50)
    print("Build completed!")
    print("=" * 50)
    print(f"\nRelease files ready in: {release_dir.absolute()}")
    print("\nFile list:")
    for file in release_dir.iterdir():
        size = file.stat().st_size / (1024 * 1024)  # MB
        print(f"  - {file.name} ({size:.2f} MB)")
    print("\nYou can now create a GitHub Release and upload these files!")

if __name__ == "__main__":
    main()

