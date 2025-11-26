import random
import os
import zipfile
import time


def backup(directory, zip_path):
    
    directory_path = os.path.abspath(directory)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory_path)
                zipf.write(file_path, arcname)


def generate_zip_filename(zip_name):

    timestamp = time.strftime("%Y%m%d%H%M%S")
    rand = ''.join(random.choices("abcdef0123456789", k=6))
    return f"{timestamp}_{rand}_{zip_name}.zip"



def main():

    zip_name = generate_zip_filename("server_backup")
    zip_dir = "/home/user/script/test_in"
    output_dir = "/home/user/script/test_out"

    backup(zip_dir, f"{output_dir}/{zip_name}")




if __name__ == "__main__":
    main()
