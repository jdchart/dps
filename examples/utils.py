import numpy as np
import matplotlib.pyplot as plt

def display_curve(curve):
    plt.figure(figsize=(10, 6))
    frame_numbers = np.arange(len(curve))
    plt.plot(frame_numbers, curve, drawstyle='steps-post')
    plt.xlabel('Frame')
    plt.ylabel('DPS')
    plt.title('DPS Curve')
    plt.show()