import json
import os
import csv

def read_json(path : str) -> dict:
    """Donner le chemin vers un fichier json et retourner un dict."""
    if os.path.isfile(path):
        if os.path.splitext(path)[1].lower() == ".json":
            with open(path, 'r') as f:
                return json.load(f)
        else:
            print("Erreur ! Il ne s'agit pas d'un fichier json !")
    else:
        print("Erreur ! Le fichier n'existe pas !")

def check_dir_exists(filepath):
    """Check if folder exists, if not, create it."""
    if os.path.isdir(os.path.dirname(filepath)) == False:
        os.makedirs(os.path.dirname(filepath))

def write_csv(path : str, content : list[list]) -> None:
    """
    Donner un chemin de destination et du contenu et enregistrer au format csv.
    
    Si le dossier n'existe pas, cette fonction créera le dossier de manière récursive.
    """
    if os.path.splitext(path)[1] == ".csv":
        check_dir_exists(path)

        with open(path, mode='w') as f:
            writer = csv.writer(f)
            for row in content:
                writer.writerow(row)
    else:
        print("Erreur ! Il faut donner un fichier avec une extension \"csv\" !")