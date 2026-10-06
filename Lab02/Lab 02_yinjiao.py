import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.integrate import ode

# Folder for saving figures
script_dir = os.path.dirname(os.path.abspath(__file__))
figure_dir = os.path.join(script_dir, "figures")
os.makedirs(figure_dir, exist_ok=True)

# Parameters given in the lab02
a = 1
b = 2
c = 1
d = 3

N_initial = np.array([0.3, 0.6])

t_start = 0
t_end = 100
dt = 1.0

# set the competition function to calculate population change for two competing species
def competition(t, N, a=1, b=2, c=1, d=3):
    # Initialize time rate of change 
    dNdt = np.zeros(2)
    # RHS of Lotka voltera model
    dNdt[0] = a*N[0]*(1-N[0]) - b*N[0]*N[1]
    dNdt[1] = c*N[1]*(1-N[1]) - d*N[0]*N[1]

    return dNdt

# Set the predator-prey function to calculate population change for prey and predator species
def predator_prey(t, N, a=1, b=2, c=1, d=3):
    # Initialize time rate of change 
    dNdt = np.zeros(2)
    # N1 is prey and N2 is predator
    dNdt[0] = a*N[0] - b*N[0]*N[1]
    dNdt[1] = -c*N[1] + d*N[0]*N[1]

    return dNdt

# Euler solver to solve a two-population ODE system using Euler's method

def euler_solver(model, N_initial, t_start, t_end, dt, a, b, c, d):
    # Create the time steps
    times = np.arange(t_start, t_end + dt, dt)
    # Store N1 and N2 at every time step
    populations = np.zeros((len(times), 2))
    populations[0] = N_initial
    # Step forward through time
    for i in range(len(times) - 1):
        # Calculate the population change at the current time
        dNdt = model(times[i], populations[i], a, b, c, d)
        # Update both populations using Euler's method
        populations[i + 1] = populations[i] + dNdt * dt

    return times, populations

# RK45 solver to solve a two-population ODE system using RK45

def rk45_solver(model, N_initial, t_start, t_end, dt, a, b, c, d):
    # Set up the RK45 integrator
    solver = ode(model).set_integrator("dopri5")
    solver.set_initial_value(N_initial, t_start)
    solver.set_f_params(a, b, c, d)
    # Store the initial time and populations
    times = [t_start]
    populations = [N_initial.copy()]

    # Integrate forward in time
    while solver.successful() and solver.t < t_end:
        solver.integrate(min(solver.t + dt, t_end))
        times.append(solver.t)
        populations.append(solver.y.copy())

    return np.array(times), np.array(populations)

# Task 1: Competition model

# Run the competition model with Euler's method
t_euler, N_euler = euler_solver(competition,N_initial,t_start,t_end,dt,a, b, c, d)

print("Competition model - Euler method")
print("Final N1:", N_euler[-1, 0])
print("Final N2:", N_euler[-1, 1])

# Run the same competition model with RK45
t_rk45, N_rk45 = rk45_solver(competition,N_initial,t_start,t_end,dt,a, b, c, d)

print("\nCompetition model - RK45")
print("Final N1:", N_rk45[-1, 0])
print("Final N2:", N_rk45[-1, 1])

# Compare Euler and RK45 for the competition model
fig, ax = plt.subplots(figsize=(8, 5))

# Euler results
ax.plot(t_euler, N_euler[:, 0], "--", label="N1 - Euler")
ax.plot(t_euler, N_euler[:, 1], "--", label="N2 - Euler")

# RK45 results
ax.plot(t_rk45, N_rk45[:, 0], "-", label="N1 - RK45")
ax.plot(t_rk45, N_rk45[:, 1], "-", label="N2 - RK45")

ax.set_xlabel("Time (years)")
ax.set_ylabel("Normalized population")
ax.set_title("Competition Model: Euler vs RK45 (dt = 1 year)")
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(figure_dir, "task1_competition_euler_vs_rk45.png"),dpi=300)
plt.show()

# Test how the Euler time step changes the solution
dt_values = [1.0, 0.5, 0.1, 0.05]

fig, ax = plt.subplots(figsize=(8, 5))

for dt_test in dt_values:

    t_test, N_test = euler_solver(
        competition,
        N_initial,
        t_start,
        t_end,
        dt_test,
        a, b, c, d
    )

    ax.plot(
        t_test,
        N_test[:, 0],
        label=f"Euler N1, dt={dt_test}"
    )

# Add the RK45 result as a reference
ax.plot(t_rk45,N_rk45[:, 0],"k--",linewidth=2,label="RK45 N1")

ax.set_xlabel("Time (years)")
ax.set_ylabel("Normalized population")
ax.set_title("Competition Model: Effect of Euler Time Step")
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(figure_dir, "task1_competition_timestep_test.png"),dpi=300)
plt.show()

print("\nEuler time-step test")

for dt_test in dt_values:

    t_test, N_test = euler_solver(competition,
        N_initial,
        t_start,
        t_end,
        dt_test,
        a, b, c, d
    )

    print(f"dt = {dt_test}: "
        f"N1 = {N_test[-1, 0]:.6f}, "
        f"N2 = {N_test[-1, 1]:.6f}"
    )

# Task 1: Predator-prey model

dt_predator = 0.05

# Run the predator-prey model with Euler's method
t_pred_euler, N_pred_euler = euler_solver(
    predator_prey,
    N_initial,
    t_start,
    t_end,
    dt_predator,
    a, b, c, d
)

# Run the same model with RK45
t_pred_rk45, N_pred_rk45 = rk45_solver(
    predator_prey,
    N_initial,
    t_start,
    t_end,
    dt_predator,
    a, b, c, d
)

print("\nPredator-prey model - Euler method")
print("Final prey:", N_pred_euler[-1, 0])
print("Final predator:", N_pred_euler[-1, 1])

print("\nPredator-prey model - RK45")
print("Final prey:", N_pred_rk45[-1, 0])
print("Final predator:", N_pred_rk45[-1, 1])

# Compare Euler and RK45 for the predator-prey model

fig, ax = plt.subplots(figsize=(8, 5))

# Euler results
ax.plot(
    t_pred_euler,
    N_pred_euler[:, 0],
    "--",
    label="Prey - Euler"
)

ax.plot(
    t_pred_euler,
    N_pred_euler[:, 1],
    "--",
    label="Predator - Euler"
)

# RK45 results
ax.plot(
    t_pred_rk45,
    N_pred_rk45[:, 0],
    "-",
    label="Prey - RK45"
)

ax.plot(
    t_pred_rk45,
    N_pred_rk45[:, 1],
    "-",
    label="Predator - RK45"
)

ax.set_xlabel("Time (years)")
ax.set_ylabel("Normalized population")
ax.set_title("Predator-Prey Model: Euler vs RK45 (dt = 0.05 year)")
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(figure_dir,"task1_predator_prey_euler_vs_rk45.png"),dpi=300)
plt.show()

# Test the Euler time step for the predator-prey model

dt_pred_values = [0.1, 0.05, 0.02, 0.01]

print("\nPredator-prey Euler time-step test")

for dt_test in dt_pred_values:

    t_test, N_test = euler_solver(
        predator_prey,
        N_initial,
        t_start,
        t_end,
        dt_test,
        a, b, c, d
    )

    print(
        f"dt = {dt_test}: "
        f"prey = {N_test[-1, 0]:.6f}, "
        f"predator = {N_test[-1, 1]:.6f}"
    )

# Plot the effect of Euler time step on the predator-prey model

fig, ax = plt.subplots(figsize=(8, 5))

for dt_test in [0.05, 0.02, 0.01]:

    t_test, N_test = euler_solver(
        predator_prey,
        N_initial,
        t_start,
        t_end,
        dt_test,
        a, b, c, d
    )

    # Plot prey population for each Euler time step
    ax.plot(
        t_test,
        N_test[:, 0],
        label=f"Euler prey, dt={dt_test}"
    )

# RK45 is used as the reference solution
ax.plot(
    t_pred_rk45,
    N_pred_rk45[:, 0],
    "k--",
    linewidth=2,
    label="RK45 prey"
)

ax.set_xlabel("Time (years)")
ax.set_ylabel("Normalized prey population")
ax.set_title("Predator-Prey Model: Effect of Euler Time Step")
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(figure_dir,"task1_predator_prey_timestep_test.png"),dpi=300)
plt.show()

# Validate the competition model using its analytical equilibrium

a_val = 1.0
b_val = 0.5
c_val = 1.0
d_val = 0.5

# Calculate the expected coexistence equilibrium
N1_eq = c_val * (a_val - b_val) / (c_val*a_val - b_val*d_val)
N2_eq = a_val * (c_val - d_val) / (c_val*a_val - b_val*d_val)

# Start away from equilibrium and integrate toward the steady state
N_validation = np.array([0.3, 0.4])

t_val, N_val = rk45_solver(
    competition,
    N_validation,
    0,
    100,
    0.1,
    a_val, b_val, c_val, d_val
)

print("\nCompetition model validation")
print(f"Expected equilibrium: N1 = {N1_eq:.6f}, N2 = {N2_eq:.6f}")
print(f"RK45 final result:   N1 = {N_val[-1, 0]:.6f}, N2 = {N_val[-1, 1]:.6f}")


# Task 2: Competition model parameter study

# Use RK45 for the parameter experiments
competition_cases = [
    ("Species 1 wins", 1.0, 0.5, 1.0, 2.0),
    ("Species 2 wins", 1.0, 2.0, 1.0, 0.5),
    ("Coexistence",    1.0, 0.5, 1.0, 0.5)]

N_task2 = np.array([0.3, 0.6])

fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)

for ax, (case, a_case, b_case, c_case, d_case) in zip(axes, competition_cases):

    # Run each competition case with the same initial populations
    t_case, N_case = rk45_solver(
        competition,
        N_task2,
        0,
        100,
        0.1,
        a_case, b_case, c_case, d_case)

    ax.plot(t_case, N_case[:, 0], label="Species 1")
    ax.plot(t_case, N_case[:, 1], label="Species 2")

    ax.set_title(case)
    ax.set_xlabel("Time (years)")
    ax.grid(alpha=0.3)

    # Print the final populations for comparison
    print(f"\n{case}")
    print(f"a={a_case}, b={b_case}, c={c_case}, d={d_case}")
    print(f"Final N1 = {N_case[-1, 0]:.4f}")
    print(f"Final N2 = {N_case[-1, 1]:.4f}")

axes[0].set_ylabel("Normalized population")
axes[0].legend()

fig.suptitle("Competition Model: Effect of Coefficient Values")

plt.tight_layout()
plt.savefig(os.path.join(figure_dir,"task2_competition_coefficient_cases.png"),dpi=300)
plt.show()

# Test the effect of initial conditions

a_ic = 1.0
b_ic = 2.0
c_ic = 1.0
d_ic = 2.0

initial_cases = [
    ("More Species 1", np.array([0.6, 0.3])),
    ("Equal Initial Population", np.array([0.5, 0.5])),
    ("More Species 2", np.array([0.3, 0.6]))
]

fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)

for ax, (case, N_start) in zip(axes, initial_cases):

    # Keep the coefficients fixed and only change initial populations
    t_case, N_case = rk45_solver(
        competition,
        N_start,
        0,
        100,
        0.1,
        a_ic, b_ic, c_ic, d_ic
    )

    ax.plot(t_case, N_case[:, 0], label="Species 1")
    ax.plot(t_case, N_case[:, 1], label="Species 2")

    ax.set_title(case)
    ax.set_xlabel("Time (years)")
    ax.grid(alpha=0.3)

    print(f"\n{case}")
    print(f"Initial N1 = {N_start[0]}, N2 = {N_start[1]}")
    print(f"Final N1 = {N_case[-1, 0]:.4f}")
    print(f"Final N2 = {N_case[-1, 1]:.4f}")

axes[0].set_ylabel("Normalized population")
axes[0].legend()

fig.suptitle("Competition Model: Effect of Initial Conditions")

plt.tight_layout()
plt.savefig(os.path.join(figure_dir,"task2_competition_initial_conditions.png"),dpi=300)
plt.show()


# Task 3: Predator-prey model

# Use the original predator-prey parameters
a_pred = 1.0
b_pred = 2.0
c_pred = 1.0
d_pred = 3.0

N_pred_initial = np.array([0.3, 0.6])

# Run the predator-prey model with RK45
t_pred, N_pred = rk45_solver(
    predator_prey,
    N_pred_initial,
    0,
    100,
    0.05,
    a_pred, b_pred, c_pred, d_pred
)

# Plot the trajectory in phase space
fig, ax = plt.subplots(figsize=(6, 6))

ax.plot(
    N_pred[:, 0],
    N_pred[:, 1]
)

# Mark the initial population
ax.scatter(
    N_pred_initial[0],
    N_pred_initial[1],
    label="Initial condition"
)

ax.set_xlabel("Prey population (N1)")
ax.set_ylabel("Predator population (N2)")
ax.set_title("Predator-Prey Phase Diagram")
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(figure_dir,"task3_predator_prey_phase_diagram.png"),dpi=300)
plt.show()

# Test different initial conditions for the predator-prey model

pred_initial_cases = [
    ("IC 1", np.array([0.3, 0.6])),
    ("IC 2", np.array([0.2, 0.4])),
    ("IC 3", np.array([0.5, 0.7]))
]

fig, ax = plt.subplots(figsize=(7, 6))

for case, N_start in pred_initial_cases:

    # Keep model parameters fixed and change only the initial populations
    t_case, N_case = rk45_solver(
        predator_prey,
        N_start,
        0,
        100,
        0.05,
        a_pred, b_pred, c_pred, d_pred
    )

    ax.plot(
        N_case[:, 0],
        N_case[:, 1],
        label=f"{case}: ({N_start[0]}, {N_start[1]})"
    )

# Mark the equilibrium point
N1_eq_pred = c_pred / d_pred
N2_eq_pred = a_pred / b_pred

ax.scatter(
    N1_eq_pred,
    N2_eq_pred,
    marker="x",
    s=80,
    label="Equilibrium"
)

ax.set_xlabel("Prey population (N1)")
ax.set_ylabel("Predator population (N2)")
ax.set_title("Predator-Prey Model: Effect of Initial Conditions")
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(figure_dir,"task3_predator_prey_initial_conditions.png"),dpi=300)
plt.show()

# Population versus time for different initial conditions

predator_initial_cases = [
    ("IC 1: (0.3, 0.6)", np.array([0.3, 0.6])),
    ("IC 2: (0.2, 0.4)", np.array([0.2, 0.4])),
    ("IC 3: (0.5, 0.7)", np.array([0.5, 0.7]))
]

fig, axes = plt.subplots(1, 3,figsize=(12, 4),sharex=True,sharey=True)

for ax, (title, initial_case) in zip(axes, predator_initial_cases):

    # Solve the predator-prey model for this initial condition
    t_case, N_case = rk45_solver(
        predator_prey,
        initial_case,
        t_start,
        t_end,
        dt_predator,
        a, b, c, d
    )

    ax.plot(t_case, N_case[:, 0], label="Prey")
    ax.plot(t_case, N_case[:, 1], label="Predator")

    ax.set_title(title)
    ax.set_xlabel("Time (years)")
    ax.grid(alpha=0.3)

axes[0].set_ylabel("Normalized population")

# Put the legend on the last panel
axes[2].legend(loc="upper right")

fig.suptitle("Predator-Prey Model: Population vs Time for Different Initial Conditions")
plt.tight_layout()
plt.savefig(os.path.join(figure_dir,"task3_predator_prey_initial_conditions_timeseries.png"),dpi=300)
plt.show()

# Test the effect of coefficient values on predator-prey behavior

pred_parameter_cases = [
    ("Baseline", 1.0, 2.0, 1.0, 3.0),
    ("Higher prey growth", 1.5, 2.0, 1.0, 3.0),
    ("Higher predator death", 1.0, 2.0, 1.5, 3.0)
]

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, (case, a_case, b_case, c_case, d_case) in zip(
    axes, pred_parameter_cases
):

    # Keep the initial condition fixed and change the coefficients
    t_case, N_case = rk45_solver(
        predator_prey,
        N_pred_initial,
        0,
        100,
        0.05,
        a_case, b_case, c_case, d_case
    )

    ax.plot(
        N_case[:, 0],
        N_case[:, 1]
    )

    # Mark the equilibrium for this parameter set
    N1_eq = c_case / d_case
    N2_eq = a_case / b_case

    ax.scatter(
        N1_eq,
        N2_eq,
        marker="x",
        s=70,
        label="Equilibrium"
    )

    ax.set_title(case)
    ax.set_xlabel("Prey population (N1)")
    ax.grid(alpha=0.3)

    print(f"\n{case}")
    print(f"a={a_case}, b={b_case}, c={c_case}, d={d_case}")
    print(f"Equilibrium N1 = {N1_eq:.4f}")
    print(f"Equilibrium N2 = {N2_eq:.4f}")

axes[0].set_ylabel("Predator population (N2)")
axes[0].legend(loc="upper right")

fig.suptitle("Predator-Prey Model: Effect of Coefficient Values")

plt.tight_layout()
plt.savefig(os.path.join(figure_dir,"task3_predator_prey_coefficient_cases.png"),dpi=300)
plt.show()

# Population versus time for different coefficient values

predator_coefficient_cases = [
    ("Baseline", 1.0, 2.0, 1.0, 3.0),
    ("Higher prey growth", 1.5, 2.0, 1.0, 3.0),
    ("Higher predator death", 1.0, 2.0, 1.5, 3.0)
]

fig, axes = plt.subplots(
    1, 3,
    figsize=(12, 4),
    sharex=True
)

for ax, (title, a_test, b_test, c_test, d_test) in zip(
    axes,
    predator_coefficient_cases
):

    # Solve the model using this set of coefficients
    t_case, N_case = rk45_solver(
        predator_prey,
        N_initial,
        t_start,
        t_end,
        dt_predator,
        a_test,
        b_test,
        c_test,
        d_test
    )

    ax.plot(t_case, N_case[:, 0], label="Prey")
    ax.plot(t_case, N_case[:, 1], label="Predator")

    ax.set_title(title)
    ax.set_xlabel("Time (years)")
    ax.grid(alpha=0.3)

axes[0].set_ylabel("Normalized population")

# Keep the legend away from the first panel
axes[2].legend(loc="upper right")

fig.suptitle("Predator-Prey Model: Population vs Time for Different Coefficients")

plt.tight_layout()
plt.savefig(os.path.join(figure_dir, "task3_predator_prey_coefficient_timeseries.png"),dpi=300)
plt.show()

# Task 4: Lorenz model

# Parameters used for the Lorenz equations to calculate the rates of change for the Lorenz system
sigma = 10.0
b_lorenz = 8.0 / 3.0

def lorenz(t, state, sigma, r, b):
    x, y, z = state

    dxdt = sigma * (y - x)
    dydt = -x * z + r * x - y
    dzdt = x * y - b * z

    return np.array([dxdt, dydt, dzdt])

# RK45 solver for the Lorenz system to solve the Lorenz equations using RK45

def lorenz_rk45_solver(initial_state, t_start, t_end, dt, sigma, r, b):
    solver = ode(lorenz).set_integrator("dopri5")
    solver.set_initial_value(initial_state, t_start)
    solver.set_f_params(sigma, r, b)

    times = [t_start]
    states = [initial_state.copy()]

    while solver.successful() and solver.t < t_end:

        solver.integrate(min(solver.t + dt, t_end))

        times.append(solver.t)
        states.append(solver.y.copy())

    return np.array(times), np.array(states)

# Start with r = 23

r_lorenz = 23.0

lorenz_initial = np.array([1.0, 1.0, 1.0])

t_lorenz_start = 0.0
t_lorenz_end = 100.0
dt_lorenz = 0.01

# Run the original initial condition
t_lorenz, state_lorenz = lorenz_rk45_solver(
    lorenz_initial,
    t_lorenz_start,
    t_lorenz_end,
    dt_lorenz,
    sigma,
    r_lorenz,
    b_lorenz
)

print("\nLorenz model: r = 23")
print("Initial condition:", lorenz_initial)
print(f"Final x = {state_lorenz[-1, 0]:.6f}")
print(f"Final y = {state_lorenz[-1, 1]:.6f}")
print(f"Final z = {state_lorenz[-1, 2]:.6f}")

# Add a small perturbation to all three initial values
perturbation = 1e-5
lorenz_initial_perturbed = lorenz_initial + perturbation

# Run the perturbed initial condition
t_lorenz_pert, state_lorenz_pert = lorenz_rk45_solver(
    lorenz_initial_perturbed,
    t_lorenz_start,
    t_lorenz_end,
    dt_lorenz,
    sigma,
    r_lorenz,
    b_lorenz
)

print("\nLorenz model: r = 23, perturbed initial condition")
print("Initial condition:", lorenz_initial_perturbed)
print(f"Final x = {state_lorenz_pert[-1, 0]:.6f}")
print(f"Final y = {state_lorenz_pert[-1, 1]:.6f}")
print(f"Final z = {state_lorenz_pert[-1, 2]:.6f}")

# Difference between the two solutions at t = 100
final_difference = np.abs(
    state_lorenz_pert[-1] - state_lorenz[-1]
)

print("\nAbsolute difference at t = 100")
print(f"|dx| = {final_difference[0]:.6f}")
print(f"|dy| = {final_difference[1]:.6f}")
print(f"|dz| = {final_difference[2]:.6f}")

# Compare the original and perturbed trajectories for r = 23

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(
    t_lorenz,
    state_lorenz[:, 0],
    label="Original"
)

ax.plot(
    t_lorenz_pert,
    state_lorenz_pert[:, 0],
    "--",
    label="Perturbed"
)

ax.set_xlabel("Time(model time units)")
ax.set_ylabel("x")
ax.set_title("Lorenz Model: Sensitivity to Initial Conditions (r = 23)")
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(figure_dir, "task4_lorenz_r23_perturbation.png"),dpi=300)
plt.show()

# Repeat the perturbation experiment for r = 25

r_lorenz_25 = 25.0

# Original initial condition
t_lorenz_25, state_lorenz_25 = lorenz_rk45_solver(
    lorenz_initial,
    t_lorenz_start,
    t_lorenz_end,
    dt_lorenz,
    sigma,
    r_lorenz_25,
    b_lorenz
)

# Perturbed initial condition
t_lorenz_25_pert, state_lorenz_25_pert = lorenz_rk45_solver(
    lorenz_initial_perturbed,
    t_lorenz_start,
    t_lorenz_end,
    dt_lorenz,
    sigma,
    r_lorenz_25,
    b_lorenz
)

print("\nLorenz model: r = 25")
print("Original initial condition:", lorenz_initial)
print(f"Final x = {state_lorenz_25[-1, 0]:.6f}")
print(f"Final y = {state_lorenz_25[-1, 1]:.6f}")
print(f"Final z = {state_lorenz_25[-1, 2]:.6f}")

print("\nLorenz model: r = 25, perturbed initial condition")
print("Initial condition:", lorenz_initial_perturbed)
print(f"Final x = {state_lorenz_25_pert[-1, 0]:.6f}")
print(f"Final y = {state_lorenz_25_pert[-1, 1]:.6f}")
print(f"Final z = {state_lorenz_25_pert[-1, 2]:.6f}")

# Difference between the two solutions at t = 100
final_difference_25 = np.abs(
    state_lorenz_25_pert[-1] - state_lorenz_25[-1]
)

print("\nAbsolute difference at t = 100 for r = 25")
print(f"|dx| = {final_difference_25[0]:.6f}")
print(f"|dy| = {final_difference_25[1]:.6f}")
print(f"|dz| = {final_difference_25[2]:.6f}")

# Compare the original and perturbed trajectories for r = 25

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(
    t_lorenz_25,
    state_lorenz_25[:, 0],
    label="Original"
)

ax.plot(
    t_lorenz_25_pert,
    state_lorenz_25_pert[:, 0],
    "--",
    label="Perturbed"
)

ax.set_xlabel("Time(model time units)")
ax.set_ylabel("x")
ax.set_title("Lorenz Model: Sensitivity to Initial Conditions (r = 25)")
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(figure_dir,"task4_lorenz_r25_perturbation.png"),dpi=300)
plt.show()

# Test a range of initial conditions

lorenz_initial_cases = [
    np.array([1.0, 1.0, 1.0]),
    np.array([2.0, 2.0, 2.0]),
    np.array([5.0, 5.0, 5.0]),
    np.array([-1.0, -1.0, 1.0])
]

r_values = [23.0, 25.0]

print("\nLorenz model: range of initial conditions")

for r_test in r_values:

    print(f"\nr = {r_test}")

    for initial_test in lorenz_initial_cases:

        # Run the original initial condition
        t_original, state_original = lorenz_rk45_solver(
            initial_test,
            t_lorenz_start,
            t_lorenz_end,
            dt_lorenz,
            sigma,
            r_test,
            b_lorenz
        )

        # Add the same small perturbation to x, y, and z
        initial_perturbed = initial_test + perturbation

        t_perturbed, state_perturbed = lorenz_rk45_solver(
            initial_perturbed,
            t_lorenz_start,
            t_lorenz_end,
            dt_lorenz,
            sigma,
            r_test,
            b_lorenz
        )

        # Measure the distance between the two final states
        final_distance = np.linalg.norm(
            state_perturbed[-1] - state_original[-1]
        )

        print(
            f"IC = {initial_test}, "
            f"final difference = {final_distance:.6f}"
        )

# Validate the r = 23 result for IC = [5, 5, 5]
# Use tighter RK45 tolerances and several output time steps

validation_initial = np.array([5.0, 5.0, 5.0])
validation_perturbed = validation_initial + 1e-5

r_validation = 23.0

dt_validation_values = [0.05, 0.02, 0.01]


#Solve the Lorenz model with tighter RK45 tolerances
def lorenz_validation_solver(
    initial_condition,
    t_start,
    t_end,
    dt,
    sigma,
    r,
    b
):

    solver = ode(lorenz).set_integrator(
        "dopri5",
        rtol=1e-10,
        atol=1e-12
    )

    solver.set_initial_value(initial_condition, t_start)
    solver.set_f_params(sigma, r, b)

    times = [t_start]
    states = [initial_condition.copy()]

    while solver.successful() and solver.t < t_end:

        solver.integrate(min(solver.t + dt, t_end))

        times.append(solver.t)
        states.append(solver.y.copy())

    return np.array(times), np.array(states)


print("\nValidation: Lorenz r = 23, IC = [5, 5, 5]")

for dt_test in dt_validation_values:

    # Original trajectory
    t_original, state_original = lorenz_validation_solver(
        validation_initial,
        t_lorenz_start,
        t_lorenz_end,
        dt_test,
        sigma,
        r_validation,
        b_lorenz
    )

    # Perturbed trajectory
    t_perturbed, state_perturbed = lorenz_validation_solver(
        validation_perturbed,
        t_lorenz_start,
        t_lorenz_end,
        dt_test,
        sigma,
        r_validation,
        b_lorenz
    )

    # Distance between the two final states
    final_difference = np.linalg.norm(
        state_perturbed[-1] - state_original[-1]
    )

    print(
        f"dt = {dt_test}: "
        f"final difference = {final_difference:.6f}"
    )