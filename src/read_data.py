import pandas as pd

# Path to the Excel file
file_path = '../Maximale neerslag.xlsx'

# Load the Excel file
excel_file = pd.ExcelFile(file_path, engine='openpyxl')

# Read the Data sheet
df = pd.read_excel(file_path, sheet_name='Data', engine='openpyxl')

print("Data sheet shape:", df.shape)
print("All rows:")
print(df)

# Extract years from row 2 (index 2)
years = df.iloc[2, 1:].values  # Skip first column

# Extract data for multiple measurements
measurements = {
    'Waarneming 1 uur': df.iloc[9, 1:].values,
    'Waarneming 1 dag': df.iloc[10, 1:].values,
    'Waarneming 10 dagen': df.iloc[11, 1:].values,
    'Trendlijn 1 uur': df.iloc[12, 1:].values,
    'Trendlijn 1 dag': df.iloc[13, 1:].values,
    'Trendlijn 10 dagen': df.iloc[14, 1:].values,
}

# Create DataFrame with years as index
df_processed = pd.DataFrame(measurements, index=years)
df_processed.index.name = 'Jaar'

print("\nProcessed data with multiple columns:")
print(df_processed.head(10))

# Save the processed data
df_processed.to_csv('data/processed_max_neerslag.csv')
print("Data saved to data/processed_max_neerslag.csv")