import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

# Read the processed data
df = pd.read_csv('data/processed_max_neerslag.csv', index_col='Jaar')

# Select one time series, e.g., 'Waarneming 1 uur'
ts = df['Waarneming 1 uur'].dropna()

# Fit auto ARIMA
model = auto_arima(ts, seasonal=False, trace=True, error_action='ignore', suppress_warnings=True)
print(model.summary())

# Fit the model
model_fit = ARIMA(ts, order=model.order).fit()

# Forecast next 10 years
forecast = model_fit.forecast(steps=10)
print("Forecast for next 10 years:")
print(forecast)

# Plot the original and forecast
plt.figure(figsize=(10, 6))
plt.plot(ts.index, ts, label='Observed')
forecast_years = range(int(ts.index[-1]) + 1, int(ts.index[-1]) + 11)
plt.plot(forecast_years, forecast, label='Forecast', color='red')
plt.xlabel('Jaar')
plt.ylabel('Waarneming 1 uur')
plt.title('ARIMA Forecast')
plt.legend()
plt.savefig('data/arima_forecast.png')
print("Forecast plot saved to data/arima_forecast.png")