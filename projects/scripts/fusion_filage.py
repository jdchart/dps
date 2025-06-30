import os
import json
import re
from glob import glob

def adjust_timers(segment, offset):
    """Ajuste les timers de début et de fin en ajoutant un décalage global."""
    for result in segment.get('result', []):
        result['start'] += offset
        result['end'] += offset
    return segment

def merge_videos_by_date(input_directory, output_directory):
    """Fusionne les fichiers JSON de vidéos fusionnées par date."""
    # Modèle pour extraire la date, le numéro de vidéo et les temps start/end des fichiers merged
    pattern = re.compile(r"(LMI_\d+[A-Za-z0-9]*)_(\d+)_\d+\.\d+_\d+\.\d+_merged\.json$")
    
    # Recherche de tous les fichiers JSON "merged" dans le répertoire
    json_files = glob(os.path.join(input_directory, "*_merged.json"))
    
    # Organisation des fichiers par date et par ordre de vidéo
    date_segments = {}
    for file_path in json_files:
        filename = os.path.basename(file_path)
        match = pattern.search(filename)
        if match:
            date = match.group(1)                    # Date (ex : LMI_20230513)
            video_number = int(match.group(2))        # Numéro de vidéo pour l'ordre de fusion
            start_time = float(filename.split('_')[3])  # Temps de début
            end_time = float(filename.split('_')[4])    # Temps de fin

            if date not in date_segments:
                date_segments[date] = []
            date_segments[date].append((video_number, start_time, file_path, end_time))
    
    # Traitement de chaque date
    for date, segments in date_segments.items():
        # Trier les segments par numéro de vidéo et ensuite par start_time
        segments.sort()  # Cela garantira que les fichiers sont fusionnés dans le bon ordre

        merged_results = []
        texte = ""
        media = []
        start_time_global = segments[0][1]  # Début du premier segment (utilisé pour le nom de sortie)
        current_offset = 0  # Offset global pour ajuster les timers en continu

        for i, (video_number, start_time, file_path, end_time) in enumerate(segments):
            with open(file_path, 'r', encoding='utf-8') as f:
                segment_data = json.load(f)
            
            # Accumuler 'media' de chaque segment sans doublons
            if "media" in segment_data and segment_data["media"] not in media:
                media.append(segment_data["media"])
            
            # Accumuler 'text' de chaque segment
            texte += segment_data.get("text", "") + " "
            
            # Vérifier si 'result' est présent dans le segment
            if 'result' in segment_data:
                # Ajuster les timers de chaque segment en fonction de l'offset actuel
                adjusted_segment = adjust_timers(segment_data, current_offset)
                merged_results.extend(adjusted_segment['result'])
                
                # Mettre à jour l'offset pour le prochain segment
                if adjusted_segment['result']:
                    current_offset = adjusted_segment['result'][-1]['end']

        # Création de la structure finale avec 'text' accumulé, 'media' concaténé, et 'result'
        final_json_data = {
            "text": texte.strip(),  # Enlever les espaces en trop
            "media": media,         # Liste de tous les chemins media
            "result": merged_results
        }
        
        # Calcul du `end_time_global` comme le dernier `end` dans merged_results
        if merged_results:
            end_time_global = merged_results[-1]['end']
        else:
            end_time_global = start_time_global  # Valeur par défaut si aucun 'result' dans les segments
        
        # Création du nom de fichier de sortie avec les temps de début et de fin
        output_filename = f"{date}_0_{end_time_global}_final_merged.json"
        output_path = os.path.join(output_directory, output_filename)
        
        # Sauvegarde du fichier JSON fusionné
        with open(output_path, 'w', encoding='utf-8') as outfile:
            json.dump(final_json_data, outfile, ensure_ascii=False, indent=2)
        print(f"Fichier final fusionné créé : {output_path}")

# Définir le répertoire contenant les fichiers JSON "merged" et le répertoire de sortie
input_directory = "C:/Users/theoh/Documents/Fac/Thèse/Donnees/DPS_LMI/Fusion/output"
output_directory = "C:/Users/theoh/Documents/Fac/Thèse/Donnees/DPS_LMI/Fusion/final_output"
os.makedirs(output_directory, exist_ok=True)

# Fusion des vidéos par date
merge_videos_by_date(input_directory, output_directory)
