# Importing necessary libraries
import numpy as np  
import pandas as pd  
from scipy.optimize import least_squares 

# Reading the interpolated data
filename = "interpolated_data.csv" 
data = pd.read_csv(filename)

# Extracting columns for time (Year), prey (Hare), and predator (Lynx) populations
t = data["Year"].values
prey_population = data["Hare"].values
predator_population = data["Lynx"].values

# Function to compute the slope (rate of change) of population data
def compute_slope(y, t, limit=4.5):
    dy_dt = np.gradient(y, t)  # Calculate the slope (rate of change) of the population
    # Remove extreme slope values based on a threshold limit
    # The threshold limit (4.5 times the median slope) is chosen for reliability
    median_slope = np.median(np.abs(dy_dt))
    valid = np.abs(dy_dt) < limit * median_slope
    return dy_dt, valid  # Return slopes and their validity status

# Compute the slopes for prey and predator populations and filter invalid values
prey_slope, prey_valid = compute_slope(prey_population, t)
predator_slope, predator_valid = compute_slope(predator_population, t)

# Keep only the data points where both prey and predator slopes are valid
valid = prey_valid & predator_valid
t_filtered = t[valid]
prey_population_filtered = prey_population[valid]
predator_population_filtered = predator_population[valid]
prey_slope_filtered = prey_slope[valid]
predator_slope_filtered = predator_slope[valid]

# Define the system of equations for the Lotka-Volterra model
def lotka_volterra_equations(params, prey, predator, prey_slope, predator_slope):
    r, a, b, m = params  # Parameters: prey growth rate (r), predation rate (a), predator reproduction rate (b), predator mortality rate (m)
    # Residual values for prey and predator equations
    v1 = r * prey - a * prey * predator - prey_slope
    v2 = b * prey * predator - m * predator - predator_slope
    return np.concatenate([v1, v2])  # Combine both residuals into a single array

# Filtered data for use in optimization
prey_data = prey_population_filtered
predator_data = predator_population_filtered
prey_slope_data = prey_slope_filtered
predator_slope_data = predator_slope_filtered

# Initial parameter guesses based on literature
params0 = [0.5, 0.02, 0.3, 0.01]  # r, a, b, m

# Use least squares optimization to fit the Lotka-Volterra equations to the data
result = least_squares(
    lotka_volterra_equations,  # Function defining the equations
    params0,  # Initial parameter estimates
    args=(prey_data, predator_data, prey_slope_data, predator_slope_data),  # Data for fitting
    method = "lm"  # Levenberg-Marquardt method for non-linear least squares
)

# Adjust the parameters to have the correct units (convert from 3 months^-1 to year^-1)
params_fit = result.x * 4

# Print the optimized parameters to the console
print(params_fit)

# Save the optimized parameters 
with open("parameters.txt", "w") as f:
    for param in params_fit:
        f.write(f"{param}\n")  # Write each parameter on a new line
print("Parameters saved to 'parameters.txt'.")

print("Adjusted parameters (r, a, b, m):")
print(params_fit)
