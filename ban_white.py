import os
import json
import shutil

def load_whitelist(file_path):
    file_name = 'whitelist.txt'
    full_path = os.path.join(file_path, file_name)
    whitelist = set()
    if os.path.exists(full_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            for key in data:
                for item in data[key]:
                    whitelist.add(item)
    else:
        print("whitelist is not exist！")
    return whitelist




def get_files_in_folder(folder_path):
    file_list = []
    
    if os.path.exists(folder_path):
        
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                
                file_name = file_name[:-4]
                
                file_list.append(file_name)
    else:
        print("指定的資料夾不存在！")
    return file_list


folder_path = "Good"

whitelist_path = "whitelist.json"

ban_folder_path = os.path.join(folder_path, "ban")


whitelist = load_whitelist(whitelist_path)

files = get_files_in_folder(folder_path)


for file_name in files:
    if file_name in whitelist:
        source_path = os.path.join(folder_path, file_name + ".yar")
        dest_path = os.path.join(ban_folder_path, file_name )
        try:
            shutil.move(source_path, dest_path)
            print(f"已移動檔案 {file_name} 到 ban 資料夾")
        except Exception as e:
            print(f"移動檔案 {file_name} 到 ban 資料夾時發生錯誤：{str(e)}")
