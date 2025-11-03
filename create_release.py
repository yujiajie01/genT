#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建 GitHub Release 的辅助脚本
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def check_gh_cli():
    """检查是否安装了 GitHub CLI"""
    try:
        subprocess.run(['gh', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def create_release_with_gh():
    """使用 GitHub CLI 创建 release"""
    release_dir = Path("release")
    if not release_dir.exists():
        print("[ERROR] release directory not found")
        print("Please run build_release.py first")
        return False
    
    # 获取版本号
    version = datetime.now().strftime("%Y%m%d")
    tag_name = f"v{version}"
    
    # 查找文件
    zip_files = list(release_dir.glob("*.zip"))
    exe_files = list(release_dir.glob("*.exe"))
    
    if not zip_files and not exe_files:
        print("[ERROR] No release files found in release directory")
        return False
    
    print(f"Creating release {tag_name}...")
    
    # 创建 tag
    try:
        subprocess.run(['git', 'tag', tag_name], check=True)
        print(f"[OK] Created tag: {tag_name}")
    except subprocess.CalledProcessError:
        print(f"[WARN] Tag {tag_name} may already exist")
    
    # 推送 tag
    try:
        subprocess.run(['git', 'push', 'origin', tag_name], check=True)
        print(f"[OK] Pushed tag to remote")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to push tag: {e}")
        return False
    
    # 创建 release
    release_title = f"Torrent Generator v{version}"
    release_notes = f"""
## Torrent Generator v{version}

### 下载
- **TorrentGenerator.exe** - Windows 可执行文件
- **TorrentGenerator-v{version}.zip** - 压缩包（包含 exe 和 README）

### 使用方法
1. 下载 TorrentGenerator.exe 或解压 zip 文件
2. 双击运行 TorrentGenerator.exe
3. 选择要生成种子的文件夹
4. 选择保存位置

### 功能特点
- ✅ 选择文件夹生成种子文件
- ✅ 默认私有（无tracker）
- ✅ 简单易用的GUI界面
- ✅ 无需额外依赖
"""
    
    # 准备文件参数
    file_args = []
    for file in zip_files + exe_files:
        file_args.extend(['-a', str(file)])
    
    cmd = [
        'gh', 'release', 'create', tag_name,
        '--title', release_title,
        '--notes', release_notes.strip()
    ] + file_args
    
    try:
        subprocess.run(cmd, check=True)
        print(f"[OK] Release created successfully!")
        print(f"Visit: https://github.com/yujiajie01/genT/releases/tag/{tag_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to create release: {e}")
        print("\nYou can manually create release at:")
        print(f"https://github.com/yujiajie01/genT/releases/new")
        return False

def create_release_manual():
    """手动创建 release 的说明"""
    release_dir = Path("release")
    version = datetime.now().strftime("%Y%m%d")
    tag_name = f"v{version}"
    
    print("\n" + "=" * 50)
    print("Manual Release Creation Instructions")
    print("=" * 50)
    print("\n1. Create tag and push:")
    print(f"   git tag {tag_name}")
    print(f"   git push origin {tag_name}")
    print("\n2. Create release on GitHub:")
    print(f"   Visit: https://github.com/yujiajie01/genT/releases/new")
    print(f"   Tag: {tag_name}")
    print(f"   Title: Torrent Generator v{version}")
    print("\n3. Upload files from release directory:")
    files = list(release_dir.iterdir())
    for file in files:
        print(f"   - {file.name}")
    print("\n" + "=" * 50)

def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("GitHub Release Creator")
    print("=" * 50 + "\n")
    
    if check_gh_cli():
        print("[OK] GitHub CLI found")
        if create_release_with_gh():
            return
    else:
        print("[INFO] GitHub CLI not found")
        print("You can install it from: https://cli.github.com/")
    
    create_release_manual()

if __name__ == "__main__":
    main()

