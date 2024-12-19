import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
data = pd.read_csv("model.csv")  # Original dataset
data1 = pd.read_csv("interpolated_data.csv")  # Interpolated dataset
data2 = pd.read_csv("model(with_peak_at_t=1883.0).csv")
data3 = pd.read_csv("model(with_peak_at_t=1877.0).csv")

# Create a figure for subplots
fig, axs = plt.subplots(3, 2, figsize=(15, 15))  # 3 rows, 2 columns of subplots

### Plot 1: Original Prey and Predator (Left column, Top Row)
ax1 = axs[0, 0]
ax2 = ax1.twinx()
prey_original, = ax1.plot(data["Time"], data["Prey"], label="Prey (Model)", color="red", zorder=1)
prey_interpolated, = ax1.plot(data1["Year"], data1["Hare"], label="Prey (Original)", linestyle="--", color="green", zorder=2)
predator_original, = ax2.plot(data["Time"], data["Predator"], label="Predator (Model)", color="blue", zorder=3)
predator_interpolated, = ax2.plot(data1["Year"], data1["Lynx"], label="Predator (Original)", linestyle="--", color="orange", zorder=4)
ax1.set_xlabel("Time (years)")
ax1.set_ylabel("Prey Population", color="red")
ax2.set_ylabel("Predator Population", color="blue")
ax1.set_title("Original Model: Prey vs Predator")
lines = [prey_original, prey_interpolated, predator_original, predator_interpolated]
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc="best", frameon=True)

### Plot 2: Prey vs Predator (Data2) (Left column, Middle Row)
ax1 = axs[1, 0]
ax2 = ax1.twinx()
prey_original, = ax1.plot(data2["Time"], data2["Prey"], label="Prey (Model)", color="red", zorder=1)
prey_interpolated, = ax1.plot(data1["Year"], data1["Hare"], label="Prey (Original)", linestyle="--", color="green", zorder=2)
predator_original, = ax2.plot(data2["Time"], data2["Predator"], label="Predator (Model)", color="blue", zorder=3)
predator_interpolated, = ax2.plot(data1["Year"], data1["Lynx"], label="Predator (Original)", linestyle="--", color="orange", zorder=4)
ax1.set_xlabel("Time (years)")
ax1.set_ylabel("Prey Population", color="red")
ax2.set_ylabel("Predator Population", color="blue")
ax1.set_title("Model with Peak at t=1883: Prey vs Predator")
lines = [prey_original, prey_interpolated, predator_original, predator_interpolated]
labels = [line.get_label() for line in lines]


### Plot 3: Prey vs Predator (Data3) (Left column, Bottom Row)
ax1 = axs[2, 0]
ax2 = ax1.twinx()
prey_original, = ax1.plot(data3["Time"], data3["Prey"], label="Prey (Model)", color="red", zorder=1)
prey_interpolated, = ax1.plot(data1["Year"], data1["Hare"], label="Prey (Original)", linestyle="--", color="green", zorder=2)
predator_original, = ax2.plot(data3["Time"], data3["Predator"], label="Predator (Model)", color="blue", zorder=3)
predator_interpolated, = ax2.plot(data1["Year"], data1["Lynx"], label="Predator (Original)", linestyle="--", color="orange", zorder=4)
ax1.set_xlabel("Time (years)")
ax1.set_ylabel("Prey Population", color="red")
ax2.set_ylabel("Predator Population", color="blue")
ax1.set_title("Model with Peak at t=1877: Prey vs Predator")
lines = [prey_original, prey_interpolated, predator_original, predator_interpolated]
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc="best", frameon=True)

pop_predator1 = data2[data2["Time"] == 1881]["Predator"]
pop_prey1 = data2[data2["Time"] == 1881]["Prey"]

### Plot 4: Phase Space for Data2 (Right column, Middle Row)
axs[1, 1].plot(data2["Prey"], data2["Predator"], label="Predator/Prey")
axs[1, 1].scatter(pop_prey1, pop_predator1, color="red", label="Beginning of Peak", s=100, zorder=4)
axs[1, 1].set_title("Predator(Prey)( peak t=1883)")
axs[1, 1].set_xlabel("Prey")
axs[1, 1].set_ylabel("Predator")
axs[1, 1].legend(loc="best")

pop_predator2 = data3[data3["Time"] == 1875]["Predator"]
pop_prey2 = data3[data3["Time"] == 1875]["Prey"]
### Plot 5: Phase Space for Data3 (Right column, Bottom Row)
axs[2, 1].plot(data3["Prey"], data3["Predator"], label="Predator/Prey")
axs[2, 1].scatter(pop_prey2,pop_predator2, color="red", label="Beginning of Peak", s=100, zorder=4)
axs[2, 1].set_title("Predator(Prey)( peak t=1877)")
axs[2, 1].set_xlabel("Prey")
axs[2, 1].set_ylabel("Predator")
axs[2, 1].legend(loc="best")

# Hide the top-right subplot (it won't have any plot)
axs[0, 1].axis("off")

# Adjust layout and show the plot
plt.tight_layout()
plt.show()
