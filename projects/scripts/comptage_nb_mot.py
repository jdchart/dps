import os
import json
import csv

# Spécifiez le chemin du dossier contenant les fichiers JSON
json_folder_path = "C:/Users/theoh/Documents/Fac/Thèse/Donnees/DPS_LMI/Fusion/1_Donnees_fusionnes/AvecLength"
# Spécifiez le nom du fichier de sortie CSV
output_csv_path = "nombre_mots_par_fichier.csv"

# Fonction pour compter les mots dans une chaîne de caractères
def count_words(text):
    return len(text.split())

# Liste pour stocker les données (nom du fichier et nombre de mots)
data = []

# Parcourir tous les fichiers dans le dossier JSON
for filename in os.listdir(json_folder_path):
    # Vérifier si le fichier a une extension .json
    if filename.endswith(".json"):
        file_path = os.path.join(json_folder_path, filename)
        
        # Ouvrir et lire le fichier JSON
        with open(file_path, "r", encoding="utf-8") as json_file:
            try:
                json_data = json.load(json_file)
                # Vérifier si la clé 'text' existe dans le JSON
                if "text" in json_data:
                    # Compter les mots dans le texte
                    word_count = count_words(json_data["text"])
                    # Ajouter les informations dans la liste
                    data.append([filename, word_count])
                else:
                    print(f"Attention : le fichier {filename} ne contient pas la clé 'text'.")
            except json.JSONDecodeError:
                print(f"Erreur : le fichier {filename} n'est pas un JSON valide.")

# Écrire les données dans un fichier CSV
with open(output_csv_path, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    # Écrire l'en-tête
    writer.writerow(["nom_fichier", "nombre_mots"])
    # Écrire les lignes de données
    writer.writerows(data)

print(f"Le fichier CSV '{output_csv_path}' a été généré avec succès.")
