import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns

cluster_colors_hex = [
        "#A8C256", #vert jaune
        "#F3D9B1", #beige
        "#C29979", #marron
        "#C33149", #rouge carmin
        "#008744", #vert
        "#FF715B", # rouge doux
        "#2F52E0", #bleu
        "#F9CB40", #orange doux
        "#ff3c26", #orange foncé 
        "#BCED09", #vert citron
        "#0057e7",
        "#d62d20",
        "#ffa700",
        "#ff8640", #orange
        "#ff3c26", #orange foncé 
        "#362559", #violet
        "#ffc578"
]

def display_curve(curve, x_format = "frames", fps = 32, interval = 5, roation = 90):
    def format_time(x, pos):
        total_seconds = x / fps
        minutes = int(total_seconds) // 60
        seconds = int(total_seconds) % 60
        return f"{minutes:02}:{seconds:02}"
    
    if x_format == "frames":
        plt.figure(figsize=(10, 6))
        frame_numbers = np.arange(len(curve))
        plt.plot(frame_numbers, curve, drawstyle='steps-post')
        plt.xlabel('Frame')
        plt.ylabel('DPS')
        plt.title('DPS Curve')
        plt.show()
        plt.close()
    elif x_format == "time":
        plt.figure(figsize=(10, 6))
        frame_numbers = np.arange(len(curve))
        plt.plot(frame_numbers, curve, drawstyle='steps-post')
        plt.xlabel('Time (MM:SS)')
        plt.ylabel('DPS')
        plt.title('DPS Curve')

        max_frames = len(curve)
        interval_frames = int(interval * 60 * fps)
        tick_positions = np.arange(0, max_frames, interval_frames)
        plt.xticks(tick_positions)
        plt.gca().xaxis.set_major_formatter(FuncFormatter(format_time))
        plt.xticks(rotation=roation)

        plt.show()
        plt.close()
    
def save_curve(path, curve, x_format = "frames", fps = 32, interval = 5, roation = 90):
    def format_time(x, pos):
        total_seconds = x / fps
        minutes = int(total_seconds) // 60
        seconds = int(total_seconds) % 60
        return f"{minutes:02}:{seconds:02}"
    
    if x_format == "frames":
        plt.figure(figsize=(10, 6))
        frame_numbers = np.arange(len(curve))
        plt.plot(frame_numbers, curve, drawstyle='steps-post')
        plt.xlabel('Frame')
        plt.ylabel('DPS')
        plt.title('DPS Curve')
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
    elif x_format == "time":
        plt.figure(figsize=(10, 6))
        frame_numbers = np.arange(len(curve))
        plt.plot(frame_numbers, curve, drawstyle='steps-post')
        plt.xlabel('Time (MM:SS)')
        plt.ylabel('DPS')
        plt.title('DPS Curve')
        max_frames = len(curve)

        interval_frames = int(interval * 60 * fps)
        tick_positions = np.arange(0, max_frames, interval_frames)
        plt.xticks(tick_positions)
        plt.gca().xaxis.set_major_formatter(FuncFormatter(format_time))
        plt.xticks(rotation=roation)

        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

def display_heatmap(df):
    heatmap_matrix = df.pivot(index="file", columns="window", values="mean")
    heatmap_matrix.index = [f[:12] for f in heatmap_matrix.index]

    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_matrix, annot=False, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'Mean WPS'})
    plt.title("Évolution du rythme par fenêtres temporelles (WPS moyen)")
    plt.xlabel("Fenêtre temporelle (découpage normalisé)")
    plt.ylabel("Captation")
    plt.tight_layout()
    plt.show()
    plt.close()

def save_heatmap(path, df):
    heatmap_matrix = df.pivot(index="file", columns="window", values="mean")
    heatmap_matrix.index = [f[:12] for f in heatmap_matrix.index]

    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_matrix, annot=False, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'Mean WPS'})
    plt.title("Évolution du rythme par fenêtres temporelles (WPS moyen)")
    plt.xlabel("Fenêtre temporelle (découpage normalisé)")
    plt.ylabel("Captation")
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()

def display_scatter(data, cluster_labels):
    plt.figure(figsize=(10, 6))
    for cluster_id in range(10):
        idx = cluster_labels == cluster_id
        plt.scatter(data[idx, 0], data[idx, 1],
                    color=cluster_colors_hex[cluster_id],
                    label=f"Cluster {cluster_id}", s=200)

    plt.title("Clustering des fenêtres rythmiques (t-SNE)")
    plt.tight_layout()
    plt.show()

def display_two_curves(curve1, curve2, label1="Curve 1", label2="Curve 2", x_format="frames", fps=32, interval=5, rotation=90):
    def format_time(x, pos):
        total_seconds = x / fps
        minutes = int(total_seconds) // 60
        seconds = int(total_seconds) % 60
        return f"{minutes:02}:{seconds:02}"
    
    plt.figure(figsize=(10, 6))
    frame_numbers = np.arange(len(curve1))  # Assumes same length for both

    plt.plot(frame_numbers, curve1, label=label1, drawstyle='steps-post')
    plt.plot(frame_numbers, curve2, label=label2, drawstyle='steps-post', alpha=0.7)

    if x_format == "frames":
        plt.xlabel("Frame")
    elif x_format == "time":
        plt.xlabel("Time (MM:SS)")
        interval_frames = int(interval * 60 * fps)
        tick_positions = np.arange(0, len(curve1), interval_frames)
        plt.xticks(tick_positions)
        plt.gca().xaxis.set_major_formatter(FuncFormatter(format_time))
        plt.xticks(rotation=rotation)

    plt.ylabel("Value")
    plt.title("Comparison of Two Curves")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.close()

def indices_to_timeranges(valid_segments, fps):
    time_ranges = []
    start = None

    for i, is_valid in enumerate(valid_segments):
        if is_valid and start is None:
            start = i
        elif not is_valid and start is not None:
            end = i
            time_ranges.append((start / fps, end / fps))  # Convertir les indices en secondes
            start = None

    if start is not None:
        time_ranges.append((start / fps, len(valid_segments) / fps))

    segment_minutes = [(t[0] // 60, t[1] // 60) for t in time_ranges]
    segment_seconds = [(t[0] % 60, t[1] % 60) for t in time_ranges]

    return time_ranges, segment_minutes, segment_seconds

def find_constant_segments_over_threshold(data, threshold, window_size):
    """
    Trouve les segments de `data` où les valeurs dépassent `threshold` 
    sur une période continue d'au moins `window_size`.
    """
    # Identifie les points au-dessus du seuil
    above_threshold = data > threshold
    
    # Crée un masque booléen avec des fenêtres glissantes
    valid_segments = np.convolve(above_threshold, np.ones(window_size, dtype=int), mode='same') >= window_size
    
    return valid_segments

def plot_differentials_with_segments(differentials_of_differentials, fps, threshold, time_window, window_size, out_dest, key = None):
    curves_to_plot = [key] if key else differentials_of_differentials.keys()
    
    for curve_key in curves_to_plot:
        label_for_significant_segments = f"Variations > {threshold} over {time_window} min"

        differ_of_differ = differentials_of_differentials[curve_key]
        valid_segments = find_constant_segments_over_threshold(differ_of_differ, threshold, window_size)
        time_ranges, segment_minutes, segment_seconds = indices_to_timeranges(valid_segments, fps)

        
        # Graphique
        plt.figure(figsize=(15, 5))
        time_axis = np.linspace(0, len(differ_of_differ) / fps, len(differ_of_differ))

        print(time_axis[4999])
        
        plt.plot(time_axis, differ_of_differ, label=f"Differential between the transitions of {curve_key}")
        plt.fill_between(time_axis, 0, differ_of_differ, where=valid_segments, 
                 color='orange', alpha=0.3, label=label_for_significant_segments)

        #plt.axhline(y=threshold, color='red', linestyle='--', label=f"Threshold = {threshold}")
        plt.title(f"Mutation between the transitions from clusters centroids : {curve_key}")
        plt.xlabel("Time (mm:ss)")
        plt.ylabel("Differential of WPS")
        plt.legend()
        plt.tight_layout()
        plt.savefig(out_dest, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()
        
        # Inspection des segments
        print(f"Segments significatifs pour {curve_key} (seuil {threshold} sur {time_window} minutes) :")     
        # Affichage des horaires au format mm:ss

        time_ranges_mmss = []
        for start, end in segment_seconds:
            start_mmss = f"{int(start):02}.{int((start % 1) * 60):02}"
            end_mmss = f"{int(end):02}.{int((end % 1) * 60):02}"
            
            time_ranges_mmss.append((start_mmss, end_mmss))
        
        #time_ranges_mmss = [
        #    (f"{int(start):02}.{int((start % 1) * 60):02}", f"{int(end):02}.{int((end % 1) * 60):02}")
        #    for start, end in segment_seconds
        #]
        
        print("- Horaires au format mm.ss : ", time_ranges)  # Horaires en mm:ss pour la lisibilité