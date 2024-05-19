import tkinter as tk
from tkinter import filedialog
from yara_control import YaraCtrl
from whitelist_maker import WhitelistControl
from Whitelist_Scanner import whitelist_scanner
from duplicate_chunk import YaraDuplicate

class FolderSelector:
    def __init__(self, master):
        self.master = master
        self.master.title("Select Folders")
        self.master.geometry("400x300")
        
        self.label1 = tk.Label(master, text="No folder selected yet")
        self.label1.pack(pady=5)
        
        self.button1 = tk.Button(master, text="Select Yara rule Folder", command=self.select_folder1)
        self.button1.pack(pady=5)

        self.label2 = tk.Label(master, text="No folder selected yet")
        self.label2.pack(pady=5)
        
        self.button2 = tk.Button(master, text="Select Sample Folder ", command=self.select_folder2)
        self.button2.pack(pady=5)
        
        self.label3 = tk.Label(master, text="No folder selected yet")
        self.label3.pack(pady=5)
        
        self.button3 = tk.Button(master, text="Select Whitelist Folder", command=self.select_folder3)
        self.button3.pack(pady=5)

        self.confirm_button = tk.Button(master, text="Confirm", command=self.confirm_folders)
        self.confirm_button.pack(pady=10)

        self.folder1 = ''
        self.folder2 = ''
        self.folder3 = ''

    def select_folder1(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.label1.config(text="Selected folder Yara rule path: " + folder_path)
            print("User-selected folder Yara rule path:", folder_path) 
            self.folder1 = folder_path

    def select_folder2(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.label2.config(text="Selected folder Sample path: " + folder_path)
            print("User-selected folder Sample path:", folder_path) 
            self.folder2 = folder_path

    def select_folder3(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.label3.config(text="Selected folder Whitelist path: " + folder_path)
            print("User-selected folder Whitelist path:", folder_path)
            self.folder3 = folder_path

    def confirm_folders(self):
        if self.folder1 and self.folder2 and self.folder3:
            print("Confirmed Yara rule folder :", self.folder1)
            print("Confirmed Sample folder :", self.folder2)
            print("Confirmed Whitelist folder :", self.folder3)
            # Add any further actions here based on confirmed folders
            # For now, let's just close the window
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    folder_selector = FolderSelector(root)
    root.mainloop()
    
    yara_ctrl = YaraCtrl()
    all_yara_path = yara_ctrl.collect_yara_files(folder_selector.folder1)
    compiled_cbin_file = yara_ctrl.merge_yar_files(all_yara_path)
    log_file = yara_ctrl.scan_with_yar(folder_selector.folder2, compiled_cbin_file)
    all_yara_path = yara_ctrl.process_yara_files(folder_selector.folder1)
 
    whitelist_ctrl = WhitelistControl()
    whitelist_ctrl.run_scan(folder_selector.folder3, folder_selector.folder1) #白名單路徑
    whitelist_ctrl.to_Json()

    W_scanner = whitelist_scanner(all_yara_path)
    W_scanner.ban_files()

    check_duplicate = YaraDuplicate(all_yara_path)
    check_duplicate.process_all()
    
    whitelist_ctrl.delete_whitelist_files()





    











