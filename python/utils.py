import os

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                os.remove(file_path)
            for name in dirs:
                dir_path = os.path.join(root, name)
                os.rmdir(dir_path)
        os.rmdir(folder_path)
        print(f"Deleted folder: {folder_path}\n")
    else:
        print(f"Folder does not exist: {folder_path}\n")

def create_empty_folder(folder_path):
    delete_folder(folder_path)
    os.makedirs(folder_path)