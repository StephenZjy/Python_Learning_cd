import os

def load_files(file_dir, file_type='.bin'):
    # 遍历源目录中的所有文件
    bin_files = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if file.endswith(file_type):
                    bin_files.append(os.path.join(root, file))
    return sorted(bin_files)