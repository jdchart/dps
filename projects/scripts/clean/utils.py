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