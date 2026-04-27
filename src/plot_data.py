import pandas as pd
import matplotlib.pyplot as plt

# Read the processed data
df = pd.read_csv('data/processed_max_neerslag.csv', index_col='Jaar')

# Plot the time series
plt.figure(figsize=(12, 8))
for column in df.columns:
    plt.plot(df.index, df[column], label=column)

plt.xlabel('Jaar')
plt.ylabel('Maximale neerslag (mm)')
plt.title('Tijdreeksen van Maximale Neerslag')
plt.legend()
plt.grid(True)

# Save the plot
plt.savefig('data/time_series_plot.png')
print("Plot saved to data/time_series_plot.png")

# Show the plot (optional, but since script, save is better)
# plt.show()