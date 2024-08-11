import numpy as np

analog_1_file = 'analog_1_512_07252024.volumes.npy'
analog_1_volumes = np.load(analog_1_file)

analog_025_file = 'analog_025_512_07252024.volumes.npy'
analog_025_volumes = np.load(analog_025_file)

digital_1_file = 'digital_1_512_07252024.volumes.npy'
digital_1_volumes = np.load(digital_1_file)

digital_025_file = 'digital_025_512_07252024.volumes.npy'
digital_025_volumes = np.load(digital_025_file)

import matplotlib.pyplot as plt
from math import sqrt, ceil
from matplotlib import cm
crop = 0

analog_1_volume1 = analog_1_volumes[1][..., crop:].max(axis=2)
analog_1_volume2 = analog_1_volumes[2][..., crop:].max(axis=2)
analog_1_volume3 = analog_1_volumes[3][..., crop:].max(axis=2)
analog_1_volume4 = analog_1_volumes[4][..., crop:].max(axis=2)
analog_1_volume5 = analog_1_volumes[5][..., crop:].max(axis=2)

analog_025_volume1 = analog_025_volumes[1][..., crop:].max(axis=2)
analog_025_volume2 = analog_025_volumes[2][..., crop:].max(axis=2)
analog_025_volume3 = analog_025_volumes[3][..., crop:].max(axis=2)
analog_025_volume4 = analog_025_volumes[4][..., crop:].max(axis=2)
analog_025_volume5 = analog_025_volumes[5][..., crop:].max(axis=2)

analog_1_average = analog_1_volume1 / 5 + analog_1_volume2 / 5 + analog_1_volume3 / 5 + analog_1_volume4 / 5 + analog_1_volume5 / 5
analog_025_average = analog_025_volume1 / 5 + analog_025_volume2 / 5 + analog_025_volume3 / 5 + analog_025_volume4 / 5 + analog_025_volume5 / 5

digital_1_volume1 = digital_1_volumes[1][..., crop:].max(axis=2)
digital_1_volume2 = digital_1_volumes[2][..., crop:].max(axis=2)
digital_1_volume3 = digital_1_volumes[3][..., crop:].max(axis=2)
digital_1_volume4 = digital_1_volumes[4][..., crop:].max(axis=2)
digital_1_volume5 = digital_1_volumes[5][..., crop:].max(axis=2)

digital_025_volume1 = digital_025_volumes[1][..., crop:].max(axis=2)
digital_025_volume2 = digital_025_volumes[2][..., crop:].max(axis=2)
digital_025_volume3 = digital_025_volumes[3][..., crop:].max(axis=2)
digital_025_volume4 = digital_025_volumes[4][..., crop:].max(axis=2)
digital_025_volume5 = digital_025_volumes[5][..., crop:].max(axis=2)

digital_1_average = digital_1_volume1 / 5 + digital_1_volume2 / 5 + digital_1_volume3 / 5 + digital_1_volume4 / 5 + digital_1_volume5 / 5
digital_025_average = digital_025_volume1 / 5 + digital_025_volume2 / 5 + digital_025_volume3 / 5 + digital_025_volume4 / 5 + digital_025_volume5 / 5

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def plot_column_with_max_difference(roi_image, x_start, x_end, y_start, y_end, title='Column with Maximum Difference', threshold=50):
    # Extract the region of interest
    roi = roi_image[x_start:x_end, y_start:y_end]

    # Normalize the image to the range 0-1 for better colormap application
    normalized_image = (roi - roi.min()) / (roi.max() - roi.min())

    # Function to count peaks and troughs
    def count_peaks_and_troughs(column):
        peaks, _ = find_peaks(column)
        troughs, _ = find_peaks(-column)
        return peaks, troughs

    # Calculate avg(crest 3 values) - avg(valley 2 values)
    def calculate_difference(column, peaks, troughs):
        if len(peaks) < 3 or len(troughs) < 2:
            return None
        crest_avg = np.mean(np.sort(column[peaks])[-3:])
        valley_avg = np.mean(np.sort(column[troughs])[:2])
        return crest_avg - valley_avg

    # Select columns with exactly 3 crests (peaks) and 2 valleys (troughs) and calculate the differences
    max_diff = -np.inf
    max_diff_column_index = -1
    max_peaks = []
    max_troughs = []

    for i in range(roi.shape[1]):
        column = roi[:, i]
        peaks, troughs = count_peaks_and_troughs(column)
        if len(peaks) == 3 and len(troughs) == 2:
            diff = calculate_difference(column, peaks, troughs)
            if diff is not None and diff > max_diff:
                max_diff = diff
                max_diff_column_index = i
                max_peaks = peaks
                max_troughs = troughs

    # Plot the continuous grayscale image and highlight the selected column
    plt.imshow(normalized_image, cmap='gray', extent=[y_start, y_end, x_end, x_start])
    if max_diff_column_index != -1:
        # Draw vertical lines at the edges of the selected column
        plt.axvline(x=y_start + max_diff_column_index, color='red', linestyle='--', label=f'Selected Column {y_start + max_diff_column_index}')
        plt.axvline(x=y_start + max_diff_column_index + 1, color='red', linestyle='--', label=f'Column Edge {y_start + max_diff_column_index + 1}')
    plt.title(title + ' - Grayscale Image')
    plt.colorbar(label='Intensity')
    plt.legend()
    plt.show()

    # Plot the column with the maximum difference
    if max_diff_column_index != -1:
        plt.figure()
        plt.plot(roi[:, max_diff_column_index], label=f'Column {y_start + max_diff_column_index}')
        plt.scatter(max_peaks, roi[max_peaks, max_diff_column_index], color='red', label='Crests')
        plt.scatter(max_troughs, roi[max_troughs, max_diff_column_index], color='blue', label='Valleys')
        plt.title(title + ' - Column with Maximum Difference')
        plt.xlabel('Row Index')
        plt.ylabel('Value')
        plt.legend()
        plt.show()
        print(f'Selected column index: {y_start + max_diff_column_index}')
        print(f'Crest indices: {max_peaks}')
        print(f'Valley indices: {max_troughs}')
        print(f'Maximum difference (avg(crest 3 values) - avg(valley 2 values)): {max_diff}')
    else:
        print('No column with exactly 3 crests and 2 valleys found.')

# Example usage
roi_image = analog_1_average  # Assuming average_projected_vol is already defined
x_start = 266
x_end = 276
y_start = 165
y_end = 174
plot_column_with_max_difference(roi_image, x_start, x_end, y_start, y_end,title='Analog Amp1 HE4')
