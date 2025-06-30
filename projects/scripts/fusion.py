import os
import json
import re
from glob import glob

def adjust_timers(segment, offset):
    """Ajuste les timers de début et de fin en ajoutant un décalage."""
    for result in segment['result']:
        result['start'] += offset
        result['end'] += offset
    return segment

def merge_json_segments(input_directory, output_directory):
    """Fusionne les segments JSON d'une même vidéo en ajustant les timers."""
    # Modèle pour extraire les parties pertinentes des noms de fichiers
    pattern = re.compile(r"(LMI_\d+)_([\d\.]+)_([\d\.]+)_(\d+)_(\d+)\.json$")
    
    # Recherche de tous les fichiers JSON dans le répertoire
    json_files = glob(os.path.join(input_directory, "*.json"))
    
    # Organisation des fichiers par identifiant unique (date + numéro de vidéo)
    video_segments = {}
    for file_path in json_files:
        filename = os.path.basename(file_path)
        match = pattern.search(filename)
        if match:
            # Utilise date et numéro de vidéo pour créer un identifiant unique
            date = match.group(1)  # ID + date (LMI + YYYYMMDD)
            video_number = match.group(4)  # Numéro de la vidéo
            video_id = f"{date}_{video_number}"  # Identifiant unique pour date + numéro de vidéo
            
            start_time = float(match.group(2))  # Temps de début en secondes, converti en float
            if video_id not in video_segments:
                video_segments[video_id] = []
            video_segments[video_id].append((start_time, file_path))
    
    # Traitement de chaque vidéo
    for video_id, segments in video_segments.items():
        # Tri des segments par temps de début
        segments.sort()
        
        merged_results = []
        for start_time, file_path in segments:
            with open(file_path, 'r', encoding='utf-8') as f:
                segment_data = json.load(f)
            # Ajustement des timers en fonction du point de départ du segment
            adjusted_segment = adjust_timers(segment_data, start_time)
            merged_results.extend(adjusted_segment['result'])
        
        # Sauvegarde du fichier JSON fusionné
        output_path = os.path.join(output_directory, f"{video_id}_merged.json")
        with open(output_path, 'w', encoding='utf-8') as outfile:
            json.dump({"result": merged_results}, outfile, ensure_ascii=False, indent=2)
        print(f"Fichier fusionné créé : {output_path}")

# Définir le répertoire contenant les fichiers JSON et le répertoire de sortie
input_directory = "C:/Users/theoh/Documents/Fac/Thèse/Donnees/DPS_LMI/Fusion/input"
output_directory = "C:/Users/theoh/Documents/Fac/Thèse/Donnees/DPS_LMI/Fusion/output"
os.makedirs(output_directory, exist_ok=True)

# Fusion des segments JSON
merge_json_segments(input_directory, output_directory)
