import subprocess
import json
import chardet
import os


class WhitelistControl:
    def __init__(self, yara_exe_path='yara64.exe', output_file='whitelist.txt'):
        self.yara_exe_path = yara_exe_path
        self.output_file = output_file

    def run_scan(self, target_path, cbin_path):
        # 構建PowerShell命令，使用指定的cbin_path
        command = f'{self.yara_exe_path} -C {cbin_path}/all.cbin {target_path} -r'

        # 使用subprocess.run執行命令，並將輸出重定向到指定文件
        with open(self.output_file, 'a') as output:
            process = subprocess.Popen(['powershell', '-Command', command], stdout=output, stderr=subprocess.STDOUT)
            process.wait()


    def to_Json(self):
        json_file_path = "whitelist.json"
        whitelist_data = {}  

        file_path = f"whitelist.txt"  

        with open(file_path, 'rb') as file:
            encoding = chardet.detect(file.read())['encoding']

        rule_names = []

        with open(file_path, 'r', encoding=encoding) as file:
            for line in file:
                rule_name = line.split(' ')[0]
                rule_names.append(rule_name)

        whitelist_data["whitelist"] = rule_names

        with open(json_file_path, 'w') as json_file:
            json.dump(whitelist_data, json_file, indent=4)

    def delete_whitelist_files(self):
        """
        刪除與此Python程式同一資料夾內的whitelist.json和whitelist.txt檔案。
        """
        # 取得當前程式所在的資料夾路徑
        current_directory = os.path.dirname(os.path.abspath(__file__))
        
        files_to_delete = ["whitelist.json", "whitelist.txt"]
        
        for filename in files_to_delete:
            file_path = os.path.join(current_directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"{filename} 已成功刪除。")
                else:
                    print(f"{filename} 不存在於資料夾 {current_directory} 中。")
            except Exception as e:
                print(f"刪除 {filename} 時發生錯誤：{e}")









