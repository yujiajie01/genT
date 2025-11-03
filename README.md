# Torrent种子文件生成器

一个简单快捷的torrent种子文件生成工具。

## 功能特点

- ✅ 选择文件夹生成种子文件
- ✅ 默认私有（无tracker）
- ✅ 简单易用的GUI界面
- ✅ 可打包为exe文件
- ✅ 无需额外依赖，仅使用Python标准库

## 系统要求

- Python 3.6 或更高版本
- Windows/Linux/MacOS（已测试Windows）

## 安装

无需安装额外依赖！程序仅使用Python标准库。

## 使用方法

### 方式1：直接运行Python脚本

双击运行 `torrent_generator.py` 或在命令行中：
```bash
python torrent_generator.py
```

### 方式2：打包为exe（推荐）

**Windows用户**：双击运行 `build.bat` 即可自动打包

或者手动执行：

1. 安装PyInstaller：
```bash
pip install pyinstaller
```

2. 运行打包脚本：
```bash
python build_exe.py
```

或者在命令行中：
```bash
pyinstaller --onefile --windowed --name=TorrentGenerator torrent_generator.py
```

打包完成后，exe文件会在`dist`文件夹中。

## 使用说明

1. 运行程序（Python脚本或exe文件）
2. 在弹出的对话框中选择要生成种子的文件夹或文件
3. 选择保存位置和文件名（默认使用文件夹名称）
4. 等待生成完成

**特点**：
- 生成的torrent文件默认是私有的（`private=1`）
- 不包含任何tracker服务器
- 支持文件夹和单个文件
- 自动计算文件的SHA1哈希值

