import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
import warnings
warnings.filterwarnings('ignore')

# Read the processed data
df = pd.read_csv('data/processed_max_neerslag.csv', index_col='Jaar')

# Select the 10 dagen time series
ts = df['Waarneming 10 dagen'].dropna()

print("Time Series: Waarneming 10 dagen")
print(f"Length: {len(ts)}")
print(f"Mean: {ts.mean():.2f}")
print(f"Std: {ts.std():.2f}")

# Check stationarity with ADF test
adf_result = adfuller(ts)
print(f"ADF Statistic: {adf_result[0]:.4f}")
print(f"p-value: {adf_result[1]:.4f}")
print("Stationary" if adf_result[1] < 0.05 else "Non-stationary")

# Ljung-Box test for autocorrelation
lb_test = acorr_ljungbox(ts, lags=10)
print("Ljung-Box test for autocorrelation:")
print(lb_test)

# Fit auto ARIMA
print("\nFitting ARIMA...")
model = auto_arima(ts, seasonal=False, trace=True, error_action='ignore', suppress_warnings=True)
print(model.summary())

# Fit the model
model_fit = ARIMA(ts, order=model.order).fit()

# Residuals analysis
residuals = model_fit.resid
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(residuals)
plt.title('Residuals')
plt.subplot(2, 1, 2)
plt.acorr(residuals, maxlags=20)
plt.title('Autocorrelation of Residuals')
plt.tight_layout()
plt.savefig('data/arima_residuals_10dagen.png')
print("Residuals plot saved to data/arima_residuals_10dagen.png")

# Forecast next 10 years
forecast = model_fit.forecast(steps=10)
print("\nForecast for next 10 years:")
forecast_years = range(int(ts.index[-1]) + 1, int(ts.index[-1]) + 11)
for year, val in zip(forecast_years, forecast):
    print(f"{year}: {val:.2f}")

# Plot the original, trend, and forecast
trend = df['Trendlijn 10 dagen'].dropna()
plt.figure(figsize=(12, 8))
plt.plot(ts.index, ts, label='Waarneming 10 dagen', color='blue')
plt.plot(trend.index, trend, label='Trendlijn (regressie)', color='green', linestyle='--')
plt.plot(forecast_years, forecast, label='ARIMA Forecast', color='red')
plt.xlabel('Jaar')
plt.ylabel('Maximale neerslag 10 dagen (mm)')
plt.title('Analyse van 10 dagen reeks met ARIMA')
plt.legend()
plt.grid(True)
plt.savefig('data/analysis_10dagen.png')
print("Analysis plot saved to data/analysis_10dagen.png")