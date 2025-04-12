import shutil

def export_data(filename="secure_data_backup.json"):
    shutil.copy("storage/users.json", filename)
    return filename

def import_data(file_path):
    shutil.copy(file_path, "storage/users.json")
