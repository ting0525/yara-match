import os
import shutil

class directory:
    def __init__(self, path):
        self.path = path

    def count_subdirectories(self):
        # 初始化計數器
        subdirectories_count = 0
        
        # 檢查路徑是否存在
        if not os.path.exists(self.path):
            print("path not exists")
            return
        
        # 遍歷該路徑下的所有檔案和資料夾
        for entry in os.listdir(self.path):
            entry_path = os.path.join(self.path, entry)
            # 檢查是否為資料夾
            if os.path.isdir(entry_path):
                subdirectories_count += 1
        print(subdirectories_count)
        return subdirectories_count


    












