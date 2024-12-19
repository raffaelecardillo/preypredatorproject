import numpy as np
import pandas as pd
from scipy.optimize import least_squares

filename = "interpolated_data.csv" 
data = pd.read_csv(filename)

t = data["Year"].values
prey_population = data["Hare"].values
predator_population = data["Lynx"].values

# Slopes approximation
def compute_slope(y, t, limit = 4.5):
    dy_dt = np.gradient(y, t)
    # Extreme values elimination 

    # We chose the factor 4.5 as a limit of slope's reliability because it matched 
    # pretty well the points where we wanted to exclude the slopes

    median_slope = np.median(np.abs(dy_dt))
    valid = np.abs(dy_dt) < limit * median_slope
    return dy_dt, valid

prey_slope, prey_valid = compute_slope(prey_population, t)
predator_slope, predator_valid = compute_slope(predator_population, t)

# Valid variables filter
valid = prey_valid & predator_valid # keeps the slopes only if valid in both prey and predators curve
t_filtered = t[valid]
prey_population_filtered = prey_population[valid]
predator_population_filtered = predator_population[valid]
prey_slope_filtered = prey_slope[valid]
predator_slope_filtered = predator_slope[valid]

# Equations system for Lotka-Volterra
def lotka_volterra_equations(params, prey, predator, prey_slope, predator_slope):
    r, a, b, m = params
    v1 = r * prey - a * prey * predator - prey_slope # v1 and v2 are the residual values
    v2 = b * prey * predator - m * predator - predator_slope
    return np.concatenate([v1, v2])

# Given data
prey_data = prey_population_filtered
predator_data = predator_population_filtered

prey_slope_data = prey_slope_filtered
predator_slope_data = predator_slope_filtered

# Initial estimation of parameters from litterature
params0 = [0.5, 0.02, 0.3, 0.01]  # r, a, b, m

# Solving equations with least squares method
result = least_squares(
    lotka_volterra_equations,
    params0,
    args=(prey_data, predator_data, prey_slope_data, predator_slope_data),
    method="lm"
)

# Adjusted parameters with the right units (year^-1)
params_fit = result.x * 4

print(params_fit)

# Saving results in text file that'll be read by the C code
with open("parameters.txt", "w") as f:
    for param in params_fit:
        f.write(f"{param}\n")
print("Parameters saved to 'parameters.txt'.")

# printing results
print("adjusted parameters (r, a, b, m) :")
print(params_fit)


