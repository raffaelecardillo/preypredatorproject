import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

data = pd.read_csv('inputs/data.csv')

# Extract values from data file 
years = data['Year']
hares = data['Hare']*1000
lynxes = data['Lynx']*(9/160)*1000

# Cubic interpolation function for populations
interp_hares = interp1d(years, hares, kind='cubic')
interp_lynxes = interp1d(years, lynxes, kind='cubic')

# Create new years array with 0.25 intervals 
new_years = np.arange(years.min(), years.max(), 0.25)

# Populations at these new years
new_hares = interp_hares(new_years)
new_lynxes = interp_lynxes(new_years)

# Create a new DataFrame with interpolated data
interpolated_data = pd.DataFrame({
    'Year': new_years,
    'Hare': new_hares,
    'Lynx': new_lynxes
})

# Save the interpolated data in a new CSV file
interpolated_data.to_csv('interpolated_data.csv', index=False)

print("interpolated data have been saved to 'interpolated_populations.csv'.")

