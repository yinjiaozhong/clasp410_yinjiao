import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch # used in the legend
import os


# define the variables
initial_temperature = 145
surrounding_temperature = 75
cooling_constant_k = 0.01  # 1/second
time_step_dt = 3           # seconds
target_temperature = 80
cream_temperature_decrease = 5
initial_time = 0

def euler_cooling(initial_temp, surrounding_temp, k, dt, target_temp):

    # Set the starting temperature and time
    temperature = initial_temp
    time = initial_time

    # Store the temperature and time values
    times = [time]
    temperatures = [temperature]

    # Repeat while coffee temperature is above 80 degrees
    while temperature > target_temp:

        # Calculate the cooling rate
        rate_of_change = -k * (temperature - surrounding_temp)

        # Calculate the new temperature using Euler's method
        temperature = temperature + rate_of_change * dt

        # Increase the time by one time step
        time = time + dt

        # Store the new time and temperature
        times.append(time)
        temperatures.append(temperature)


    return times, temperatures

#case 1: add the cream immediately
case1_initial_temp = initial_temperature - cream_temperature_decrease
case1_times, case1_temperatures = euler_cooling(case1_initial_temp,surrounding_temperature,cooling_constant_k,time_step_dt,target_temperature)

#case 2:add the cream later
case2_initial_temp = initial_temperature
case2_target_temperature = target_temperature + cream_temperature_decrease
case2_times, case2_temperatures = euler_cooling(case2_initial_temp,surrounding_temperature,cooling_constant_k,time_step_dt,case2_target_temperature)
case2_temperatures[-1] = case2_temperatures[-1] - cream_temperature_decrease

case1_cooling_time = case1_times[-1]
case2_cooling_time = case2_times[-1]

print("Case 1 cooling time:", case1_cooling_time, "seconds")
print("Case 2 cooling time:", case2_cooling_time, "seconds")

def analytic_cooling(initial_temp, surrounding_temp, k, time):

    # Calculate the exact temperature using the analytic solution
    temperature = surrounding_temp + (initial_temp - surrounding_temp) * np.exp(-k * time)

    return temperature

# Different time steps for comparing Euler's method
dt1 = 3
dt2 = 10
dt3 = 30

# Calculate Euler solutions for different time steps
times_dt1, temp_dt1 = euler_cooling(initial_temperature,surrounding_temperature,cooling_constant_k,dt1,target_temperature)

times_dt2, temp_dt2 = euler_cooling(initial_temperature,surrounding_temperature,cooling_constant_k,dt2,target_temperature)

times_dt3, temp_dt3 = euler_cooling(initial_temperature,surrounding_temperature,cooling_constant_k,dt3,target_temperature)

# Create a time array for the analytic solution
analytic_times = np.linspace(0, max(times_dt1[-1], times_dt2[-1], times_dt3[-1]), 500)

# Calculate the analytic temperature
analytic_temperatures = analytic_cooling(initial_temperature,surrounding_temperature,cooling_constant_k,analytic_times)

# Compare Euler solutions with the analytic solution
plt.figure(figsize=(8, 6))

# Analytic solution
plt.plot(analytic_times,analytic_temperatures,color="black",linestyle="-",linewidth=2,label="Analytic solution")

# Euler solution with dt = 3 seconds
plt.plot(times_dt1,temp_dt1,color="blue",linestyle="--",label="Euler: dt = 3 s")

# Euler solution with dt = 10 seconds
plt.plot(times_dt2,temp_dt2,color="green",linestyle="-.",label="Euler: dt = 10 s")

# Euler solution with dt = 30 seconds
plt.plot(times_dt3,temp_dt3,color="red",linestyle=":",marker="o",label="Euler: dt = 30 s")

# Add labels, title, legend, and grid
plt.xlabel("Time (seconds)")
plt.ylabel("Temperature (degrees)")
plt.title("Euler Method Compared with Analytic Solution")
plt.legend()
plt.grid(True)
# Save the figure in the same folder as this Python file
script_dir = os.path.dirname(os.path.abspath(__file__))
figure_path = os.path.join(script_dir, "coffee_euler_comparison.png")

plt.savefig(figure_path, dpi=300, bbox_inches="tight")
plt.show()