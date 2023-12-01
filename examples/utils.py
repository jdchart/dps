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