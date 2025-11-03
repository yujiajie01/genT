#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单的Torrent种子文件生成器
支持选择文件夹，生成私有种子文件（无tracker）
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
from datetime import datetime


def bencode(data):
    """Bencode编码"""
    if isinstance(data, bytes):
        return str(len(data)).encode() + b':' + data
    elif isinstance(data, str):
        data = data.encode('utf-8')
        return str(len(data)).encode() + b':' + data
    elif isinstance(data, int):
        return b'i' + str(data).encode() + b'e'
    elif isinstance(data, list):
        result = b'l'
        for item in data:
            result += bencode(item)
        result += b'e'
        return result
    elif isinstance(data, dict):
        result = b'd'
        for key in sorted(data.keys()):
            result += bencode(key) + bencode(data[key])
        result += b'e'
        return result
    else:
        raise TypeError(f"不支持的类型: {type(data)}")


def generate_torrent(folder_path, output_path):
    """生成torrent文件"""
    try:
        files_info = []
        total_length = 0
        is_single_file = not os.path.isdir(folder_path)
        
        # 收集文件信息
        if os.path.isdir(folder_path):
            base_path = folder_path
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, base_path)
                    # Windows路径转换
                    if os.name == 'nt':
                        rel_path = rel_path.replace('\\', '/')
                    file_size = os.path.getsize(file_path)
                    files_info.append({
                        'path': rel_path.split('/'),
                        'length': file_size,
                        'file_path': file_path
                    })
                    total_length += file_size
        else:
            # 单个文件
            file_size = os.path.getsize(folder_path)
            files_info.append({
                'path': [os.path.basename(folder_path)],
                'length': file_size,
                'file_path': folder_path
            })
            total_length = file_size
            base_path = os.path.dirname(folder_path) or '.'
        
        # 计算piece hashes
        piece_length = 262144  # 256KB
        pieces = []
        
        current_piece = b''
        for file_info in files_info:
            with open(file_info['file_path'], 'rb') as f:
                remaining = file_info['length']
                while remaining > 0:
                    if len(current_piece) == 0:
                        # 读取一个完整的piece
                        chunk = f.read(piece_length)
                        if len(chunk) == piece_length:
                            pieces.append(hashlib.sha1(chunk).digest())
                            remaining -= len(chunk)
                        else:
                            current_piece = chunk
                            remaining -= len(chunk)
                            break
                    else:
                        # 继续填充当前piece
                        need = piece_length - len(current_piece)
                        chunk = f.read(min(need, remaining))
                        current_piece += chunk
                        remaining -= len(chunk)
                        if len(current_piece) == piece_length:
                            pieces.append(hashlib.sha1(current_piece).digest())
                            current_piece = b''
        
        # 处理最后一个不完整的piece
        if current_piece:
            pieces.append(hashlib.sha1(current_piece).digest())
        
        pieces_hash = b''.join(pieces)
        
        # 构建info字典
        if is_single_file and len(files_info) == 1:
            # 单个文件
            info = {
                b'name': files_info[0]['path'][0].encode('utf-8'),
                b'piece length': piece_length,
                b'pieces': pieces_hash,
                b'length': files_info[0]['length']
            }
        else:
            # 多个文件
            file_list = []
            for file_info in files_info:
                file_list.append({
                    b'path': [p.encode('utf-8') for p in file_info['path']],
                    b'length': file_info['length']
                })
            folder_name = os.path.basename(folder_path) if os.path.isdir(folder_path) else os.path.basename(base_path)
            info = {
                b'name': folder_name.encode('utf-8') if folder_name else b'torrent',
                b'piece length': piece_length,
                b'pieces': pieces_hash,
                b'files': file_list
            }
        
        # 设置为私有（无tracker）
        info[b'private'] = 1
        
        # 构建完整的torrent字典
        torrent = {
            b'info': info,
            b'creation date': int(datetime.now().timestamp()),
            b'created by': b'TorrentGenerator 1.0'
        }
        
        # 编码并写入文件
        torrent_data = bencode(torrent)
        with open(output_path, 'wb') as f:
            f.write(torrent_data)
        
        return True
    except Exception as e:
        raise Exception(f"生成失败: {str(e)}")


def select_folder_and_generate():
    """选择文件夹并生成torrent"""
    # 创建隐藏的根窗口
    root = tk.Tk()
    root.withdraw()
    
    # 选择文件夹
    folder_path = filedialog.askdirectory(title="选择要生成种子的文件夹")
    
    if not folder_path:
        messagebox.showinfo("提示", "未选择文件夹")
        return
    
    # 选择保存位置
    base_name = os.path.basename(folder_path) or "torrent"
    default_filename = f"{base_name}.torrent"
    
    output_path = filedialog.asksaveasfilename(
        title="保存torrent文件",
        defaultextension=".torrent",
        filetypes=[("Torrent文件", "*.torrent"), ("所有文件", "*.*")],
        initialfile=default_filename
    )
    
    if not output_path:
        messagebox.showinfo("提示", "未选择保存位置")
        return
    
    # 显示进度窗口
    progress_window = tk.Toplevel()
    progress_window.title("生成中...")
    progress_window.geometry("300x100")
    progress_window.transient(root)
    progress_window.grab_set()
    
    label = tk.Label(progress_window, text="正在生成torrent文件，请稍候...")
    label.pack(pady=30)
    progress_window.update()
    
    try:
        # 生成torrent
        success = generate_torrent(folder_path, output_path)
        
        progress_window.destroy()
        
        if success:
            messagebox.showinfo("成功", f"Torrent文件已生成:\n{output_path}")
    except Exception as e:
        progress_window.destroy()
        messagebox.showerror("错误", str(e))
    
    root.destroy()


if __name__ == "__main__":
    try:
        select_folder_and_generate()
    except Exception as e:
        messagebox.showerror("错误", f"程序错误: {str(e)}")

