from pathlib import Path
import shutil
import re

class YaraDuplicate:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.pattern = re.compile(r"\$chunk_[1-9]+[0-9]* = {([\t\n 0-9A-F?]*)}")
        self.exist_chunk = {}
        
    def process_directory(self, input_dir, duplicate_dir, unique_dir):
        input_dir = Path(input_dir)
        duplicate_dir = Path(duplicate_dir)
        unique_dir = Path(unique_dir)

        duplicate_dir.mkdir(parents=True, exist_ok=True)
        unique_dir.mkdir(parents=True, exist_ok=True)

        yars = input_dir.glob('*.yar')

        for yar in yars:
            with yar.open() as f:
                content = f.read()

            match = self.pattern.search(content)

            if match:
                match_str = match.group(1).replace(' ', '').replace('\n', '').replace('\t', '')

                if match_str in self.exist_chunk:
                    self.exist_chunk[match_str] += 1
                    self.move_file(yar, duplicate_dir)
                else:
                    self.exist_chunk[match_str] = 1
                    self.move_file(yar, unique_dir)

    def move_file(self, file_path, target_dir):
        target_path = target_dir / file_path.name
        shutil.move(file_path, target_path)

    def process_all(self):
        subfolders = ['Good', 'Normal', 'Bad']
        for folder in subfolders:
            input_dir = self.base_dir / folder
            duplicate_dir = self.base_dir / f'duplicate_{folder}'
            unique_dir = self.base_dir / f'unique_{folder}'
            self.process_directory(input_dir, duplicate_dir, unique_dir)

# # 使用方式
# organizer = YaraDuplicate('/path/to/parent/folder')
# organizer.process_all()
