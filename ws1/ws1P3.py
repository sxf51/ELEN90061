import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# Read the CSV file, skipping the first row if it is a header
df = pd.read_csv("./ws1/WS1_PKGDIS_2.csv")

# Compute inter-arrival times (IAT) using the 'Time' column
times = df['Time'].values
iat = np.diff(times)

# Compute statistics
iat_min = np.min(iat)
iat_max = np.max(iat)
iat_avg = np.mean(iat)
iat_std = np.std(iat)

# Instantaneous rate (packet per second) for each interval
instantaneous_rate = 1 / iat

# Average rate: total packets / total time
total_time = times[-1] - times[0]
average_rate = len(times) / total_time if total_time > 0 else float('inf')

# Print results
print(f"Inter-arrival time statistics (seconds):")
print(f"  Min: {iat_min}")
print(f"  Max: {iat_max}")
print(f"  Avg: {iat_avg}")
print(f"  Std: {iat_std}")
print()
print(f"Average packet rate: {average_rate} packets/second")
print(f"First 10 instantaneous rates: {instantaneous_rate[:10]}")
print(f"Total packets: {len(times)}")
print(f"Total time: {total_time} seconds")

# Clean the IAT series: keep only values below the 95th percentile
percentile_95 = np.percentile(iat, 95)
iat_clean = iat[iat < percentile_95]

# Compute statistics for the cleaned series
iat_clean_min = np.min(iat_clean)
iat_clean_max = np.max(iat_clean)
iat_clean_avg = np.mean(iat_clean)
iat_clean_std = np.std(iat_clean)

print("\nCleaned inter-arrival time statistics (below 95th percentile):")
print(f"  Min: {iat_clean_min}")
print(f"  Max: {iat_clean_max}")
print(f"  Avg: {iat_clean_avg}")
print(f"  Std: {iat_clean_std}")

import matplotlib.pyplot as plt

# Plot time series of cleaned IATs
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(iat_clean, marker='o', linestyle='-', color='b')
plt.title('Time Series of Cleaned Packet Inter-Arrival Times')
plt.xlabel('Packet Index')
plt.ylabel('Inter-Arrival Time (seconds)')

# Plot histogram of cleaned IATs
plt.subplot(1, 2, 2)
plt.hist(iat_clean, bins=30, color='g', edgecolor='black')
plt.title('Histogram of Cleaned Packet Inter-Arrival Times')
plt.xlabel('Inter-Arrival Time (seconds)')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# Define exponential PDF: f(x; lambda) = lambda * exp(-lambda * x)
def exp_pdf(x, lamb):
    return lamb * np.exp(-lamb * x)

# Histogram data for fitting (density=True for PDF)
hist_vals, bin_edges = np.histogram(iat_clean, bins=30, density=True)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# Fit exponential PDF to histogram
popt, pcov = curve_fit(exp_pdf, bin_centers, hist_vals, p0=[1/np.mean(iat_clean)])
fitted_lambda = popt[0]

print(f"\nFitted exponential rate parameter (lambda): {fitted_lambda}")
print(f"Fitted mean inter-arrival time: {1/fitted_lambda}")

# Plot histogram and fitted exponential PDF
plt.figure(figsize=(7, 4))
plt.hist(iat_clean, bins=30, density=True, alpha=0.6, color='g', edgecolor='black', label='Cleaned IAT Histogram')
x_fit = np.linspace(0, np.max(iat_clean), 200)
plt.plot(x_fit, exp_pdf(x_fit, fitted_lambda), 'r-', label='Fitted Exponential PDF')
plt.title('Exponential Fit to Cleaned Inter-Arrival Times')
plt.xlabel('Inter-Arrival Time (seconds)')
plt.ylabel('Probability Density')
plt.legend()
plt.show()

# Plot the packet IAT distribution and superimpose the fitted exponential distribution
plt.figure(figsize=(8, 5))
plt.hist(iat_clean, bins=30, density=True, alpha=0.6, color='skyblue', edgecolor='black', label='Cleaned IAT Histogram')
plt.plot(x_fit, exp_pdf(x_fit, fitted_lambda), 'r-', linewidth=2, label='Fitted Exponential PDF')
plt.title('Packet Inter-Arrival Time Distribution with Exponential Fit')
plt.xlabel('Inter-Arrival Time (seconds)')
plt.ylabel('Probability Density')
plt.legend()
plt.tight_layout()
plt.show()

