import os
import json
import shutil

class whitelist_scanner:
    def __init__(self, parent_folder_path, subfolder_names=["Good", "Normal", "Bad"], whitelist_path="whitelist.json"):
        self.parent_folder_path = parent_folder_path
        self.subfolder_names = subfolder_names
        self.whitelist_path = whitelist_path
        self.folder_paths = [os.path.join(parent_folder_path, subfolder) for subfolder in subfolder_names]
        self.ban_folder_paths = {folder: os.path.join(folder, "ban") for folder in self.folder_paths}
        self.whitelist = self.load_whitelist()

    def load_whitelist(self):
        full_path = self.whitelist_path
        whitelist = set()
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                data = json.load(f)
                for key in data:
                    for item in data[key]:
                        whitelist.add(item)
        else:
            print("whitelist 不存在！")
        return whitelist

    def get_files_in_folder(self, folder_path):
        file_list = []
        if os.path.exists(folder_path):
            for root, dirs, files in os.walk(folder_path):
                for file_name in files:
                    original_file_name = file_name
                    # 去掉第一個 "_" 之前的部分和 ".yar" 後綴
                    if '_' in file_name:
                        file_name = file_name.split('_', 1)[1]
                    if file_name.endswith('.yar'):
                        file_name = file_name[:-4]
                    file_list.append((original_file_name, file_name))
        else:
            print(f"指定的資料夾 {folder_path} 不存在！")
        return file_list

    def ban_files(self):
        for folder_path in self.folder_paths:
            files = self.get_files_in_folder(folder_path)
            ban_folder_path = self.ban_folder_paths[folder_path]
            if not os.path.exists(ban_folder_path):
                os.makedirs(ban_folder_path)
            for original_file_name, processed_file_name in files:
                if processed_file_name in self.whitelist:
                    source_path = os.path.join(folder_path, original_file_name)
                    dest_path = os.path.join(ban_folder_path, original_file_name)
                    try:
                        shutil.move(source_path, dest_path)
                        print(f"已移動檔案 {original_file_name} 到 {ban_folder_path} 資料夾")
                    except Exception as e:
                        print(f"移動檔案 {original_file_name} 到 {ban_folder_path} 資料夾時發生錯誤：{str(e)}")
