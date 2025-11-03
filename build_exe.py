#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用PyInstaller打包exe的脚本
"""

import PyInstaller.__main__

PyInstaller.__main__.run([
    'torrent_generator.py',
    '--onefile',
    '--windowed',
    '--name=TorrentGenerator',
    '--icon=NONE',
    '--clean',
])

