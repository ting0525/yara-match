import os
import subprocess
import re
import shutil
from collections import Counter

class YaraCtrl:
    def __init__(self):
        pass

    
    def collect_yara_files(self, base_path):
        # 創建目標資料夾
        target_folder = os.path.join(base_path, 'all_yara')
        os.makedirs(target_folder, exist_ok=True)

        # 遍歷給定路徑下的所有子資料夾
        for root, dirs, files in os.walk(base_path):
            # 排除目標資料夾本身
            if root.startswith(target_folder):
                continue
            
            for file in files:
                if file.endswith('.yar'):
                    source_file = os.path.join(root, file)
                    target_file = os.path.join(target_folder, file)
                    
                    # 複製 .yar 檔案到目標資料夾
                    shutil.copy2(source_file, target_file)
                    print(f"Copied {source_file} to {target_file}")
        
        # 返回目標資料夾的路徑
        return target_folder
    
    
    def merge_yar_files(self, target_tmp_dir):
        """合併 .yar 文件到一個 all.yar 文件，然後轉換成 all.cbin。"""
        # 獲取 target_tmp_dir 的父資料夾路徑
        parent_dir = os.path.dirname(target_tmp_dir)
        
        # 設定 all.yar 和 all.cbin 檔案的路徑
        merged_yar_file = os.path.join(parent_dir, 'all.yar')
        compiled_cbin_file = os.path.join(parent_dir, 'all.cbin')
        
        # 合併 .yar 文件到 all.yar
        with open(merged_yar_file, 'wb') as merged_file:
            for file_name in os.listdir(target_tmp_dir):
                if file_name.endswith('.yar'):
                    file_path = os.path.join(target_tmp_dir, file_name)
                    with open(file_path, 'rb') as file:
                        shutil.copyfileobj(file, merged_file)
        
        # 使用 yarac64.exe 轉換 all.yar 到 all.cbin
        subprocess.run(['yarac64.exe', merged_yar_file, compiled_cbin_file], check=True)
        print(f"Compiled {merged_yar_file} to {compiled_cbin_file}")
        
        return compiled_cbin_file    

    def merge_yar_files(self, target_tmp_dir):
        """合併 .yar 文件到一個 all.yar 文件，然後轉換成 all.cbin。"""
        # 獲取 target_tmp_dir 的父資料夾路徑
        parent_dir = os.path.dirname(target_tmp_dir)
        
        # 設定 all.yar 和 all.cbin 檔案的路徑
        merged_yar_file = os.path.join(parent_dir, 'all.yar')
        compiled_cbin_file = os.path.join(parent_dir, 'all.cbin')
        
        # 合併 .yar 文件到 all.yar
        with open(merged_yar_file, 'wb') as merged_file:
            for file_name in os.listdir(target_tmp_dir):
                if file_name.endswith('.yar'):
                    file_path = os.path.join(target_tmp_dir, file_name)
                    with open(file_path, 'rb') as file:
                        shutil.copyfileobj(file, merged_file)
        
        # 使用 yarac64.exe 轉換 all.yar 到 all.cbin
        subprocess.run(['yarac64.exe', merged_yar_file, compiled_cbin_file], check=True)
        print(f"Compiled {merged_yar_file} to {compiled_cbin_file}")
        
        return compiled_cbin_file

    def scan_with_yar(self, target_path, compiled_cbin_file):
        """使用 Yara 掃描目標路徑。"""
        try:
            result = subprocess.run(
                ["powershell.exe", ".\\yara64.exe", "-C", compiled_cbin_file, target_path, "-r"],
                check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore'
            )
            
            # 獲取 compiled_cbin_file 的父資料夾路徑
            log_dir = os.path.dirname(compiled_cbin_file)
            log_file = os.path.join(log_dir, 'log.txt')
              
            # 將輸出寫入log.txt，但在此之前檢查重複內容
            output_lines = result.stdout.split('\n')
            seen = set()
            with open(log_file, 'a', encoding='utf-8') as f:
                for line in output_lines:
                    if line not in seen:
                        seen.add(line)
                        f.write(line + '\n')
            print(f"Log written to {log_file}")
            return log_file
        except subprocess.CalledProcessError as e:
            print(f"Error scanning with Yara: {e}")
            return None
    
    def process_yara_files(self, parent_dir):
        """處理臨時文件，並根據掃描結果將 .yar 文件分類。"""
        all_yara_path = os.path.join(parent_dir, 'all_yara')
        log_file_path = os.path.join(parent_dir, 'log.txt')
        
        # 讀取 log.txt 文件並計算每個 .yar 文件的出現次數
        with open(log_file_path, 'r', encoding='utf-8') as f:
            yar_names = [line.split(' ')[0] for line in f]
        target_yar_counts = Counter(yar_names)
        
        # 定義分類
        categories = {'Good': [], 'Normal': [], 'Bad': []}
        
        # 遍歷目錄中的 .yar 文件並分類
        for yar_file in filter(lambda f: f.endswith('.yar'), os.listdir(all_yara_path)):
            count = target_yar_counts.get(os.path.splitext(yar_file)[0], 0)
            new_name = f"{count}_{yar_file}"
            category = 'Good' if count >= 3 else 'Normal' if count == 2 else 'Bad'
            categories[category].append(new_name)
            os.rename(os.path.join(all_yara_path, yar_file), os.path.join(all_yara_path, new_name))
        
        # 創建分類目錄並移動文件
        for category, files in categories.items():
            category_path = os.path.join(all_yara_path, category)
            os.makedirs(category_path, exist_ok=True)
            for file in files:
                shutil.move(os.path.join(all_yara_path, file), category_path)
        
        
        return all_yara_path
