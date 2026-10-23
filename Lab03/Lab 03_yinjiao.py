import numpy as np
import matplotlib.pyplot as plt
import os

# Task 1: Derive the N-layer atmospheric energy balance model
# Layer 1 is closest to the surface, and layer N is the uppermost layer.

# Assumptions:
# 1. The surface is a perfect blackbody (emissivity = 1).
# 2. All atmospheric layers have the same emissivity (epsilon).
# 3. Atmospheric layers are transparent to incoming solar radiation.
# 4. Each layer absorbs and emits longwave radiation in both directions.

# Define the absorbed solar flux:
# S = (1 - albedo) * S0 / 4

# Define the emitted longwave fluxes:
# F0 = sigma * Ts^4                    (surface)
# Fi = epsilon * sigma * Ti^4          (atmospheric layer i)

# Surface energy balance:
# F0 - sum[(1-epsilon)^(j-1) * Fj, j=1,...,N] = S

# Atmospheric layer i energy balance:
# 2*Fi = epsilon*(1-epsilon)^(i-1)*F0 + epsilon*sum[(1-epsilon)^(|i-j|-1)*Fj, j!=i]

# Matrix representation:
# A @ x = b
# x = [F0, F1, ..., FN]
# b = [S, 0, ..., 0]

# Matrix coefficients A[i,j]:
# i=0, j=0:      1
# i=0, j>0:     -(1-epsilon)^(j-1)
# i>0, j=0:     -epsilon*(1-epsilon)^(i-1)
# i=j>0:         2
# i!=j, i,j>0:  -epsilon*(1-epsilon)^(|i-j|-1)

# Physical constants
SIGMA = 5.6703e-8  # Stefan-Boltzmann constant (W/m^2/K^4)
S0_EARTH = 1350.0   # Solar irradiance (W/m^2)
ALBEDO_EARTH = 0.33

# Save figures in the Lab03 folder
FIGURE_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGURE_DIR, exist_ok=True)

# function to calculate the T in N-layer model
def n_layer_atmosphere(nlayers, solar_irradiance, emissivity, albedo, debug=False, nuclear_winter=False):
    """
    Calculate equilibrium temperatures for an N-layer atmosphere.

    Parameters:
    nlayers : Number of atmospheric layers.
    solar_irradiance : Incoming solar irradiance (W/m^2).
    emissivity : Atmospheric emissivity.
    albedo : Planetary albedo.
    debug : Print intermediate calculations when True.
    nuclear_winter : Absorb all incoming solar radiation in the top layer when True.
    temperatures : Surface and atmospheric temperatures in K and index 0 is the surface.
    """

    if nlayers < 1:
        raise ValueError("nlayers must be at least 1")
    if not 0 < emissivity <= 1:
        raise ValueError("emissivity must be greater than 0 and at most 1")

    # Initialize the (N+1) x (N+1) coefficient matrix and solar flux vector
    A = np.zeros([nlayers + 1, nlayers + 1])
    b = np.zeros(nlayers + 1)

    solar_flux = solar_irradiance * (1 - albedo) / 4
    # Solar radiation reaches the surface normally, but the top layer during nuclear winter.
    if nuclear_winter:
        b[nlayers] = solar_flux
    else:
        b[0] = solar_flux

    # Fill the surface and atmospheric energy balance equations
    for i in range(nlayers + 1):
        for j in range(nlayers + 1):
            if i == 0 and j == 0:
                A[i, j] = 1
            elif i == 0:
                A[i, j] = -(1 - emissivity)**(j - 1)
            elif j == 0:
                A[i, j] = -emissivity * (1 - emissivity)**(i - 1)
            elif i == j:
                A[i, j] = 2
            else:
                A[i, j] = -emissivity * (1 - emissivity)**(abs(i - j) - 1)

    # Solve the linear system without explicitly inverting A
    fluxes = np.linalg.solve(A, b)

    # Convert emitted fluxes to temperature
    temperatures = np.empty(nlayers + 1)
    temperatures[0] = (fluxes[0] / SIGMA)**0.25
    temperatures[1:] = (fluxes[1:] / (emissivity * SIGMA))**0.25

    if debug:
        print("Coefficient matrix A:")
        print(A)
        print("Solar flux vector b:")
        print(b)
        print("Emitted fluxes (W/m^2):")
        print(fluxes)
        print("Temperatures (K):")
        print(temperatures)

    return temperatures


# Task 2: Validate the model using a one-layer blackbody atmosphere

temperatures = n_layer_atmosphere(nlayers=1,solar_irradiance=S0_EARTH,emissivity=1.0,albedo=ALBEDO_EARTH,debug=True)

print("\nOne-layer validation")
print(f"Surface temperature: {temperatures[0]:.2f} K")
print(f"Atmospheric temperature: {temperatures[1]:.2f} K")

# Check the numerical solution against the analytical one-layer solution
solar_flux = S0_EARTH * (1 - ALBEDO_EARTH) / 4
expected_temps = np.array([(2 * solar_flux / SIGMA)**0.25, (solar_flux / SIGMA)**0.25])
assert np.allclose(temperatures, expected_temps)
print("One-layer validation passed.")

# Task 3: Earth's surface temperature and atmospheric properties

# Experiment 1: Surface temperature versus atmospheric emissivity
emissivities = np.linspace(0.01, 1.0, 100)
surface_temps = np.array([n_layer_atmosphere(1, S0_EARTH, e, ALBEDO_EARTH)[0] for e in emissivities])

# Find the emissivity corresponding to a surface temperature of 288 K
target_temp = 288.0
best_emissivity = 2 * (1 - (S0_EARTH * (1 - ALBEDO_EARTH) / 4) / (SIGMA * target_temp**4))

print("\nTask 3 - Experiment 1")
print(f"Emissivity for a surface temperature of 288 K: {best_emissivity:.3f}")

plt.figure(figsize=(7, 5))
plt.plot(emissivities, surface_temps, color="steelblue", label="One-layer model")
plt.axhline(target_temp, color="red", linestyle="--", label="Observed Earth temperature (288 K)")
plt.axvline(best_emissivity, color="gray", linestyle=":", label=f"Estimated emissivity = {best_emissivity:.3f}")
plt.xlabel("Atmospheric Emissivity")
plt.ylabel("Surface Temperature (K)")
plt.title("Earth Surface Temperature vs. Atmospheric Emissivity")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "Task3_Emissivity.png"), dpi=300)
plt.show()


# Experiment 2: Surface temperature versus number of atmospheric layers
epsilon = 0.255
layers = np.arange(1, 5)
profiles = [n_layer_atmosphere(n, S0_EARTH, epsilon, ALBEDO_EARTH) for n in layers]
surface_temps_layers = np.array([profile[0] for profile in profiles])
best_index = np.argmin(abs(surface_temps_layers - target_temp))
best_layers = layers[best_index]

print("\nTask 3 - Experiment 2")
for n, temp in zip(layers, surface_temps_layers):
    print(f"{n} layer(s): Surface temperature = {temp:.2f} K")
print(f"Closest to 288 K: {best_layers} layers ({surface_temps_layers[best_index]:.2f} K)")
print("None of the tested layer counts reaches 288 K.")

plt.figure(figsize=(7, 5))
for n, profile in zip(layers, profiles):
    plt.plot(profile, np.arange(n + 1), marker="o", label=f"{n} layer(s)")
plt.axvline(target_temp, color="red", linestyle="--", label="Observed Earth temperature (288 K)")
plt.xlabel("Temperature (K)")
plt.ylabel("Atmospheric Layer Index (0 = Surface)")
plt.title("Earth Atmospheric Temperature Profiles (Emissivity = 0.255)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "Task3_Temperature_Profiles.png"), dpi=300)
plt.show()


# Task 4: Estimate the number of atmospheric layers on Venus

S0_VENUS = 2600.0
ALBEDO_VENUS = 0.71
VENUS_TARGET = 700.0

# Estimate the required number of perfectly absorbing atmospheric layers
estimated_layers = 4 * SIGMA * VENUS_TARGET**4 / (S0_VENUS * (1 - ALBEDO_VENUS)) - 1

# Compare nearby integer layer counts using the numerical model
candidate_layers = np.arange(max(2, int(estimated_layers) - 2), int(estimated_layers) + 4)
venus_temps = np.array([n_layer_atmosphere(n, S0_VENUS, 1.0, ALBEDO_VENUS)[0] for n in candidate_layers])
best_index = np.argmin(abs(venus_temps - VENUS_TARGET))
best_layers_venus = candidate_layers[best_index]

print("\nTask 4 - Venus")
print(f"Estimated atmospheric layers: {estimated_layers:.2f}")
print(f"Best integer number of layers: {best_layers_venus}")
print(f"Modeled Venus surface temperature: {venus_temps[best_index]:.2f} K")

plt.figure(figsize=(7, 5))
plt.plot(candidate_layers, venus_temps, "o-", label="Venus atmosphere model")
plt.axhline(VENUS_TARGET, color="red", linestyle="--", label="Target temperature (700 K)")
plt.xlabel("Number of Atmospheric Layers")
plt.ylabel("Surface Temperature (K)")
plt.title("Venus Surface Temperature vs. Atmospheric Layers")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "Task4_Venus.png"), dpi=300)
plt.show()


# Task 5: Nuclear winter scenario
# All absorbed solar radiation heats the top atmospheric layer.
# No shortwave radiation reaches the surface.
# Compare normal conditions with a nuclear winter atmosphere
nlayers = 5
epsilon = 0.5

normal_temps = n_layer_atmosphere(nlayers, S0_EARTH, epsilon, ALBEDO_EARTH)
winter_temps = n_layer_atmosphere(nlayers, S0_EARTH, epsilon, ALBEDO_EARTH, nuclear_winter=True)

print("\nTask 5 - Nuclear Winter")
print(f"Normal surface temperature: {normal_temps[0]:.2f} K")
print(f"Nuclear winter surface temperature: {winter_temps[0]:.2f} K")
print(f"Surface cooling: {normal_temps[0] - winter_temps[0]:.2f} K")

# Plot vertical temperature profiles
plt.figure(figsize=(7, 5))
plt.plot(normal_temps, np.arange(nlayers + 1), "o-", label="Normal atmosphere")
plt.plot(winter_temps, np.arange(nlayers + 1), "s--", label="Nuclear winter")
plt.xlabel("Temperature (K)")
plt.ylabel("Atmospheric Layer Index (0 = Surface)")
plt.title("Atmospheric Temperature Profiles: Nuclear Winter")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "Task5_Nuclear_Winter.png"), dpi=300)
plt.show()
