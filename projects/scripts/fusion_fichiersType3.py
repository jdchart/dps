import os
import json
import re
from glob import glob

def adjust_timers(segment, offset):
    """Ajuste les timers de début et de fin en ajoutant un décalage."""
    if 'result' in segment:  # Vérifie la présence de 'result'
        for result in segment['result']:
            result['start'] += offset
            result['end'] += offset
    return segment

def merge_json_segments(input_directory, output_directory):
    """Fusionne les segments JSON d'une même vidéo en ajustant les timers, en accumulant 'text' et en conservant 'media'."""
    # Modèle pour extraire les parties pertinentes des noms de fichiers
    # Modification : La date accepte les lettres et les chiffres (ex. "LMI_2005V2")
    pattern = re.compile(r"(LMI_[A-Za-z0-9]+)_(\d+(\.\d+)?)_(\d+(\.\d+)?)_(\d+)_(\d+)\.json$")
    
    # Recherche de tous les fichiers JSON dans le répertoire
    json_files = glob(os.path.join(input_directory, "*.json"))
    
    # Organisation des fichiers par identifiant unique (date + numéro de vidéo)
    video_segments = {}
    for file_path in json_files:
        filename = os.path.basename(file_path)
        match = pattern.search(filename)
        if match:
            date = match.group(1)                  # Identifiant de date (e.g., LMI_2005V2)
            start_time = float(match.group(2))     # Temps de début du segment (e.g., 600)
            end_time = float(match.group(4))       # Temps de fin du segment (e.g., 900)
            video_number = int(match.group(6))     # Numéro de vidéo (e.g., 1)
            segment = int(match.group(7))          # Numéro du segment
            
            # Identifiant unique en utilisant date et numéro de vidéo
            video_id = f"{date}_{video_number}"

            if video_id not in video_segments:
                video_segments[video_id] = []
            video_segments[video_id].append((start_time, file_path, end_time))
    
    # Traitement de chaque vidéo
    for video_id, segments in video_segments.items():
        # Trier les segments par temps de début
        segments.sort()
        
        merged_results = []
        texte = ""
        media = None
        start_time_global = segments[0][0]  # Début du premier segment
        end_time_global = segments[-1][2]   # Fin du dernier segment

        for i, (start_time, file_path, end_time) in enumerate(segments):
            with open(file_path, 'r', encoding='utf-8') as f:
                segment_data = json.load(f)
            
            # Conserver 'media' une seule fois depuis le premier fichier
            if i == 0:
                media = segment_data.get("media")
            
            # Accumuler 'text' de chaque segment
            texte += segment_data.get("text", "") + " "
            
            # Vérifier si 'result' est présent dans le segment
            if 'result' in segment_data:
                # Ajustement des timers en fonction du point de départ du segment
                adjusted_segment = adjust_timers(segment_data, start_time)
                merged_results.extend(adjusted_segment['result'])

        # Création de la structure finale avec 'text' accumulé, 'media' et 'result'
        final_json_data = {
            "text": texte.strip(),  # Enlever les espaces en trop
            "media": media,
            "result": merged_results
        }
        
        # Création du nom de fichier de sortie avec les temps de début et de fin
        output_filename = f"{video_id}_{start_time_global}_{str(end_time_global)}_merged.json"
        output_path = os.path.join(output_directory, output_filename)
        
        # Sauvegarde du fichier JSON fusionné
        with open(output_path, 'w', encoding='utf-8') as outfile:
            json.dump(final_json_data, outfile, ensure_ascii=False, indent=2)
        print(f"Fichier fusionné créé : {output_path}")

# Définir le répertoire contenant les fichiers JSON et le répertoire de sortie
input_directory = "C:/Users/theoh/Documents/Fac/Thèse/Donnees/DPS_LMI/Fusion/input"
output_directory = "C:/Users/theoh/Documents/Fac/Thèse/Donnees/DPS_LMI/Fusion/output"
os.makedirs(output_directory, exist_ok=True)

# Fusion des segments JSON
merge_json_segments(input_directory, output_directory)
