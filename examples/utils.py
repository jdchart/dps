import os
import subprocess

def collect_files(path, accepted = []):
    final_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            ext = os.path.splitext(file)[1][1:].lower()
            if ext in accepted or len(accepted) == 0:
                final_list.append(os.path.join(root, file))
    return final_list

def get_dest_and_file_list(file_folder):
    out_dir = os.path.join(os.getcwd(), "output")
    if os.path.isdir(out_dir) == False:
        os.makedirs(out_dir)
 
    file_list = collect_files(file_folder, ["wav"])

    return out_dir, file_list