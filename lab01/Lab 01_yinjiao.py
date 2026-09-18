import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch # used in the legend
import os

# keep results are same for each time
np.random.seed(42)
#save all figures
figure_dir = "figures"
os.makedirs(figure_dir, exist_ok=True)
# forest = 2, bare = 1, burning = 3

# Task 1.1: 3 × 3 validation
nx, ny=3, 3
prob_spread=1.0
prob_bare=0.0
prob_start=0.0
forest_history = []

forest = np.zeros([ny, nx]) +2
forest[ny//2, nx//2] = 3
#saved into the forest history
forest_history.append(forest.copy())
print("Task 1.1: Iteration 0")
print(forest)

for iteration in range(2):
    # new loop for new case
    new_forest = forest.copy()
    for i in range(nx):
        for j in range(ny):
            # is current cell burning or not?
            if forest[j, i] == 3:
                # old burning cell becomes burnt
                new_forest[j, i] = 1
                # does a right neighbor exist?
                if i+1 < nx:
                    # is the right neighbor forested?
                    if forest[j, i+1] == 2:
                        #does fire spread?
                        if np.random.rand() < prob_spread:
                            # new cell burning
                            new_forest[j, i+1] = 3
                # does a left neighbor exist?
                if i-1 >= 0:
                    # is the left neighbor forested?
                    if forest[j, i-1] == 2:
                        #does fire spread?
                        if np.random.rand() < prob_spread:
                            # new cell burning
                            new_forest[j, i-1] = 3
                # does a down neighbor exist?
                if j+1 < ny:
                    # is the down neighbor forested?
                    if forest[j+1, i] == 2:
                        #does fire spread?
                        if np.random.rand() < prob_spread:
                            # new cell burning
                            new_forest[j+1, i] = 3
                # does a up neighbor exist?
                if j-1 >= 0:
                    # is the up neighbor forested?
                    if forest[j-1, i] == 2:
                        #does fire spread?
                        if np.random.rand() < prob_spread:
                            # new cell burning
                            new_forest[j-1, i] = 3
    forest = new_forest
    forest_history.append(forest.copy())
    print(f"Task 1.1: Iteration {iteration +1}")
    print(forest)

# plotting
colors = ["grey", "green", "red"]
forest_cmap = ListedColormap(colors)
fig, axes=plt.subplots(1, 3, figsize=(13, 5))
fig.suptitle("Task 1.1: Forest Fire Spread Validation (3 × 3 Grid)")
for k in range(len(forest_history)):
    axes[k].pcolor(forest_history[k], cmap=forest_cmap, vmin=1, vmax=3)
    axes[k].set_title(f"Iteration {k}")
    axes[k].set_xlabel("Column")
    axes[k].set_ylabel("Row")
    axes[k].invert_yaxis()
legend_set = [Patch(facecolor="grey", label="Bare/Burnt"), Patch(facecolor="green", label="Forest"), Patch(facecolor="red", label="Burning")]
fig.legend(handles=legend_set, loc="lower center", ncol=3)
plt.tight_layout(rect=[0, 0.1, 1, 0.95])
plt.savefig(os.path.join(figure_dir, "task1_1_validation_3x3.png"),dpi=300,bbox_inches="tight")
plt.show()


# Task 1.2 (3*5)
nx, ny=5, 3
prob_spread=1.0
prob_bare=0.0
prob_start=0.0
forest_history = []

forest = np.zeros([ny, nx]) +2

forest[ny//2, nx//2] = 3
#saved into the forest history
forest_history.append(forest.copy())
print("Task 1: Iteration 0")
print(forest)

for iteration in range(2):   
    # new loop for new case
    new_forest = forest.copy()
    for i in range(nx):
        for j in range(ny):
            # is current cell burning or not?
            if forest[j, i] == 3:
                # old burning cell becomes burnt
                new_forest[j, i] = 1

                # does a right neighbor exist?
                if i+1 < nx:
                    # is the right neighbor forested?
                    if forest[j, i+1] == 2:
                        #does fire spread?
                        if np.random.rand() < prob_spread:
                            # new cell burning
                            new_forest[j, i+1] = 3

                # does a left neighbor exist?
                if i-1 >= 0:
                    # is the left neighbor forested?
                    if forest[j, i-1] == 2:
                        #does fire spread?
                        if np.random.rand() < prob_spread:
                            # new cell burning
                            new_forest[j, i-1] = 3

                # does a down neighbor exist?
                if j+1 < ny:
                    # is the down neighbor forested?
                    if forest[j+1, i] == 2:
                        #does fire spread?
                        if np.random.rand() < prob_spread:
                            # new cell burning
                            new_forest[j+1, i] = 3

                # does a up neighbor exist?
                if j-1 >= 0:
                    # is the left neighbor forested?
                    if forest[j-1, i] == 2:
                        #does fire spread?
                        if np.random.rand() < prob_spread:
                            # new cell burning
                            new_forest[j-1, i] = 3

    forest = new_forest
    forest_history.append(forest.copy())
    print(f"Task 1: Iteration {iteration +1}")
    print(forest)

# plotting
# set the color for each kind cell
colors = ["grey", "green", "red"]
forest_cmap = ListedColormap(colors)


# create figsize and title
fig, axes=plt.subplots(1, 3, figsize=(13, 5))
fig.suptitle("Task 1.2: Forest Fire Spread Validation (3 × 5 Grid)")
#create the loopy for plotting
for k in range(len(forest_history)):
    # plot matrix
    axes[k].pcolor(forest_history[k], cmap=forest_cmap, vmin = 1, vmax = 3)
    # set the title for each fig
    axes[k].set_title(f"Iteration {k}")
    axes[k].set_xlabel("Column")
    axes[k].set_ylabel("Row")
    axes[k].invert_yaxis()
# add the lengend
legend_set = [Patch(facecolor="grey", label="Bare/Burnt"), 
              Patch(facecolor="green", label="Forest"),
              Patch(facecolor="red", label="Burning"),]
fig.legend(handles=legend_set, loc="lower center", ncol=3) 
# adjust the legend location 
plt.tight_layout(rect=[0, 0.1, 1, 0.95])
plt.savefig(os.path.join(figure_dir, "task1_2_validation_3x5.png"),dpi=300,bbox_inches="tight")
plt.show()

# Task 2
nx = 50
ny = 50

def fire(nx, ny, prob_spread, prob_bare, prob_start):
    """
    Simulate wildfire spread on a 2-D grid and return
    burned fractions and the forest state history.
    """
    forest_history = []
    # create a new forest
    forest = np.zeros([ny, nx]) + 2

    # randomly create bare cells
    for i in range(nx):
        for j in range(ny):
            if np.random.rand() < prob_bare:
                forest[j, i] = 1

    #forest[ny//2, nx//2] = 3

    # randomly create additional initial burning cells
    for i in range(nx):
        for j in range(ny):
            # only forest cells can be ignited
            if forest[j, i] == 2:
                if np.random.rand() < prob_start:
                    forest[j, i] = 3
    initial_tree_cells = np.sum((forest == 2) | (forest == 3))

    #save initial state
    forest_history.append(forest.copy())

    #set the inital value
    iteration = 0
    while np.any(forest == 3):
        # new loop for new case
        new_forest = forest.copy()
        for i in range(nx):
            for j in range(ny):
                # is current cell burning or not?
                if forest[j, i] == 3:
                    # old burning cell becomes burnt
                    new_forest[j, i] = 1
                    # does a right neighbor exist?
                    if i+1 < nx:
                        # is the right neighbor forested?
                        if forest[j, i+1] == 2:
                            #does fire spread?
                            if np.random.rand() < prob_spread:
                                # new cell burning
                                new_forest[j, i+1] = 3

                    # does a left neighbor exist?
                    if i-1 >= 0:
                        # is the left neighbor forested?
                        if forest[j, i-1] == 2:
                            #does fire spread?
                            if np.random.rand() < prob_spread:
                                # new cell burning
                                new_forest[j, i-1] = 3

                    # does a down neighbor exist?
                    if j+1 < ny:
                        # is the down neighbor forested?
                        if forest[j+1, i] == 2:
                            #does fire spread?
                            if np.random.rand() < prob_spread:
                                # new cell burning
                                new_forest[j+1, i] = 3

                    # does a up neighbor exist?
                    if j-1 >= 0:
                        # is the left neighbor forested?
                        if forest[j-1, i] == 2:
                            #does fire spread?
                            if np.random.rand() < prob_spread:
                                # new cell burning
                                new_forest[j-1, i] = 3

        forest = new_forest
        iteration += 1
        forest_history.append(forest.copy())

    remaining_tree_cells = np.sum(forest == 2)
    burned_cells = initial_tree_cells - remaining_tree_cells
    burned_fraction = burned_cells/initial_tree_cells
    burned_area_fraction = burned_cells / (nx * ny)

    return burned_fraction, burned_area_fraction, forest_history

# Task 2 visualization
prob_spread = 0.5
prob_bare = 0.1
prob_start = 0.002

burned_fraction, burned_area_fraction, forest_history = fire(nx,ny,prob_spread,prob_bare,prob_start)

# choose initial, middle, and final forest
initial_forest = forest_history[0]
middle_forest = forest_history[len(forest_history)//2]
final_forest = forest_history[-1]

colors = ["grey", "green", "red"]
forest_cmap = ListedColormap(colors)

fig, axes=plt.subplots(1,3,figsize=(13,5))
axes[0].pcolor(initial_forest,cmap=forest_cmap,vmin=1,vmax=3)
axes[0].set_title("Initial Forest")
axes[1].pcolor(middle_forest,cmap=forest_cmap,vmin=1,vmax=3)
axes[1].set_title("During Fire")
axes[2].pcolor(final_forest,cmap=forest_cmap,vmin=1,vmax=3)
axes[2].set_title("Final Forest")

for ax in axes:
    ax.invert_yaxis()
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")

legend_set = [Patch(facecolor="grey",label="Bare/Burnt"),Patch(facecolor="green",label="Forest"),Patch(facecolor="red",label="Burning")]
fig.legend(handles=legend_set,loc="lower center",ncol=3)
plt.tight_layout(rect=[0,0.1,1,0.95])
plt.savefig(os.path.join(figure_dir,"task2_fire_visualization.png"),dpi=300,bbox_inches="tight")
plt.show()

# count each cell type for each iteration
forest_count = []
burning_count = []
burned_count = []

for forest in forest_history:
    forest_count.append(np.sum(forest == 2))
    burning_count.append(np.sum(forest == 3))
    burned_count.append(np.sum(forest == 1))

iterations = np.arange(len(forest_history))

plt.figure(figsize=(7,5))
plt.plot(iterations,forest_count,label="Forest")
plt.plot(iterations,burning_count,label="Burning")
plt.plot(iterations,burned_count,label="Bare/Burnt")
plt.xlabel("Iteration")
plt.ylabel("Number of Cells")
plt.title("Task 2: Forest Cell States Over Time")
plt.legend()
plt.savefig(os.path.join(figure_dir,"task2_forest_states_over_time.png"),dpi=300,bbox_inches="tight")
plt.show()

# Task 2.1
prob_spread = 1.0
prob_start = 0.002
#input the value
bare_values = np.arange(0.0, 1.01, 0.1)
mean_burned = []

# set diff prob_bare value
for prob_bare in bare_values:
    results = []
    #random 100
    for run in range(100):
        burned_fraction, burned_area_fraction, forest_history= fire(nx, ny, prob_spread, prob_bare, prob_start)
        results.append(burned_area_fraction)
    # compute the mean fraction
    mean_fraction = np.mean(results)
    mean_burned.append(mean_fraction)

    print(f"P_bare = {prob_bare:.1f}, Mean burned area fraction = {mean_fraction:.3f}")

# plot the fig
plt.figure(figsize=(7, 5))
plt.plot(bare_values, mean_burned, marker="o")
plt.xlabel("Probability of Bare Cells")
plt.ylabel("Mean Burned Area Fraction")
plt.title("Task 2.1: Effect of Bare Fraction on Wildfire Severity")
plt.ylim(0, 1.05)
plt.savefig(os.path.join(figure_dir, "task2_1_bare_fraction.png"),dpi=300,bbox_inches="tight")
plt.show()

# Task 2.2
prob_bare = 0.0
prob_start = 0.002
spread_values = np.arange(0.0, 1.01, 0.1)
mean_burned_spread = []

# set diff prob_spread value
for prob_spread in spread_values:
    results = []
    #random 100
    for run in range(100):
        burned_fraction, burned_area_fraction, forest_history = fire(nx, ny, prob_spread, prob_bare, prob_start)
        results.append(burned_area_fraction)
    # compute the mean fraction
    mean_fraction = np.mean(results)
    mean_burned_spread.append(mean_fraction)

    print(f"P_spread = {prob_spread:.1f}, Mean burned area fraction = {mean_fraction:.3f}")

# plot the fig
plt.figure(figsize=(7, 5))
plt.plot(spread_values, mean_burned_spread, marker="o")
plt.xlabel("Probability of Fire Spread")
plt.ylabel("Mean Burned Area Fraction")
plt.title("Task 2.2: Effect of Fire Spread Probability on Wildfire Severity")
plt.savefig(os.path.join(figure_dir, "task2_2_spread_probablity.png"),dpi=300,bbox_inches="tight")
plt.show()


# task 2.3
prob_bare = 0.0
prob_spread = 0.5

# different probabilities of initial ignition
start_values = np.arange(0.0, 0.021, 0.002)

mean_burned_start = []

# set different prob_start values
for prob_start in start_values:

    results = []

    # run 500 random simulations
    for run in range(500):

        burned_fraction, burned_area_fraction, forest_history = fire(nx,ny,prob_spread,prob_bare,prob_start)
        results.append(burned_area_fraction)
    # compute mean burned area fraction
    mean_fraction = np.mean(results)
    mean_burned_start.append(mean_fraction)
    print(f"P_start = {prob_start:.3f}, Mean burned area fraction = {mean_fraction:.3f}")

# plot the figure
plt.figure(figsize=(7, 5))
plt.plot(start_values,mean_burned_start,marker="o")
plt.xlabel("Probability of Initial Ignition")
plt.ylabel("Mean Burned Area Fraction")
plt.title("Task 2.3: Effect of Initial Ignition Probability on Wildfire Severity")
plt.ylim(0, 1.05)
plt.savefig(os.path.join(figure_dir, "task2_3_initial_ignition_probability.png"),dpi=300,bbox_inches="tight")
plt.show()

# Task 2.4: Controlled Burn Experiment
# fixed values
prob_spread = 0.5
prob_start = 0.002
# different levels of controlled burn / bare area
control_values = np.arange(0.0, 0.61, 0.1)
mean_burned_control = []
large_fire_probability = []
# number of repeated simulations
num_runs = 500
for prob_bare in control_values:
    burned_results = []
    for run in range(num_runs):

        burned_fraction, burned_area_fraction, forest_history = fire(nx,ny,prob_spread,prob_bare,prob_start)

        burned_results.append(burned_area_fraction)

    # average wildfire severity
    mean_fraction = np.mean(burned_results)
    mean_burned_control.append(mean_fraction)

    # define a large wildfire as burning more than 50% of the total area
    large_fire_count = np.sum(np.array(burned_results) > 0.5)

    # probability of a large wildfire
    large_fire_prob = large_fire_count / num_runs
    large_fire_probability.append(large_fire_prob)

    print(f"P_bare = {prob_bare:.1f}, Mean burned area = {mean_fraction:.3f}, Large fire probability = {large_fire_prob:.3f}")

# Plot
plt.figure(figsize=(7, 5))
plt.plot(control_values, mean_burned_control, marker="o")
plt.xlabel("Controlled Burn Fraction (P_bare)")
plt.ylabel("Mean Burned Area Fraction")
plt.title("Task 2.4.1: Effect of Controlled Burns on Wildfire Severity")
plt.ylim(0, 1.05)
plt.savefig(os.path.join(figure_dir, "task2_4_1_controlled_burns_severity.png"),dpi=300,bbox_inches="tight")
plt.show()

# Plot 
plt.figure(figsize=(7, 5))
plt.plot(control_values, large_fire_probability, marker="o")
plt.xlabel("Controlled Burn Fraction (P_bare)")
plt.ylabel("Probability of Large Wildfire")
plt.title("Task 2.4.2: Effect of Controlled Burns on Wildfire Likelihood")
plt.ylim(0, 1.05)
plt.savefig(os.path.join(figure_dir, "task2_4_2_controlled_burns_likelihood.png"),dpi=300,bbox_inches="tight")
plt.show()

# Task 3
# died = 0, survived/immune = 1, healthy = 2, sick = 3
nx = 50
ny = 50

def disease(nx, ny, prob_spread, prob_vaccinated, prob_start, prob_fatal):
    """
    Simulate disease spread on a 2-D grid and return
    final population fractions and the population history.
    """
    population_history = []
    # create a new population
    population = np.zeros([ny, nx]) + 2
    # randomly create vaccinated/immune people
    for i in range(nx):
        for j in range(ny):
            if np.random.rand() < prob_vaccinated:
                population[j, i] = 1

    # set the center person as sick
    population[ny//2, nx//2] = 3
    # randomly create additional initial sick people
    for i in range(nx):
        for j in range(ny):
            # only healthy people can become initially sick
            if population[j, i] == 2:
                if np.random.rand() < prob_start:
                    population[j, i] = 3

    population_history.append(population.copy())

    # continue until there are no sick people
    while np.any(population == 3):
        # create a copy for the new time step
        new_population = population.copy()
        for i in range(nx):
            for j in range(ny):
                # is current person sick?
                if population[j, i] == 3:
                    # determine whether the sick person dies or survives
                    if np.random.rand() < prob_fatal:
                        new_population[j, i] = 0
                    else:
                        new_population[j, i] = 1
                    # right
                    if i+1 < nx:
                        # is the right neighbor healthy?
                        if population[j, i+1] == 2:
                            # does disease spread?
                            if np.random.rand() < prob_spread:
                                new_population[j, i+1] = 3

                    # left
                    if i-1 >= 0:
                        # is the left neighbor healthy?
                        if population[j, i-1] == 2:
                            # does disease spread?
                            if np.random.rand() < prob_spread:
                                new_population[j, i-1] = 3

                    # down 
                    if j+1 < ny:
                        # is the down neighbor healthy?
                        if population[j+1, i] == 2:
                            # does disease spread?
                            if np.random.rand() < prob_spread:
                                new_population[j+1, i] = 3

                    # up
                    if j-1 >= 0:
                        # is the up neighbor healthy?
                        if population[j-1, i] == 2:
                            # does disease spread?
                            if np.random.rand() < prob_spread:
                                new_population[j-1, i] = 3

        # update the population
        population = new_population
        population_history.append(population.copy())
    # calculate final fractions
    dead_fraction = np.sum(population == 0) / (nx * ny)
    immune_fraction = np.sum(population == 1) / (nx * ny)
    healthy_fraction = np.sum(population == 2) / (nx * ny)

    return dead_fraction, immune_fraction, healthy_fraction, population_history

# Task 3 visualization
prob_spread = 0.5
prob_vaccinated = 0.1
prob_start = 0.002
prob_fatal = 0.5

dead_fraction, immune_fraction, healthy_fraction, population_history = disease(nx,ny,prob_spread,prob_vaccinated,prob_start,prob_fatal)

initial_population = population_history[0]
sick_numbers = [np.sum(population == 3) for population in population_history]
middle_population = population_history[np.argmax(sick_numbers)]
final_population = population_history[-1]

colors = ["black","blue","green","red"]
disease_cmap = ListedColormap(colors)

fig, axes=plt.subplots(1,3,figsize=(13,5))
axes[0].pcolor(initial_population,cmap=disease_cmap,vmin=0,vmax=3)
axes[0].set_title("Initial Population")
axes[1].pcolor(middle_population,cmap=disease_cmap,vmin=0,vmax=3)
axes[1].set_title("Peak Disease Spread")
axes[2].pcolor(final_population,cmap=disease_cmap,vmin=0,vmax=3)
axes[2].set_title("Final Population")

for ax in axes:
    ax.invert_yaxis()
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")

legend_set = [Patch(facecolor="black",label="Dead"),Patch(facecolor="blue",label="Immune"),Patch(facecolor="green",label="Healthy"),Patch(facecolor="red",label="Sick")]
fig.legend(handles=legend_set,loc="lower center",ncol=4)
plt.tight_layout(rect=[0,0.1,1,0.95])
plt.savefig(os.path.join(figure_dir,"task3_disease_visualization.png"),dpi=300,bbox_inches="tight")
plt.show()

# count each population state for each iteration
dead_count = []
immune_count = []
healthy_count = []
sick_count = []

for population in population_history:
    dead_count.append(np.sum(population == 0))
    immune_count.append(np.sum(population == 1))
    healthy_count.append(np.sum(population == 2))
    sick_count.append(np.sum(population == 3))

iterations = np.arange(len(population_history))

plt.figure(figsize=(7,5))
plt.plot(iterations,healthy_count,label="Healthy",color="green")
plt.plot(iterations,sick_count,label="Sick",color="red")
plt.plot(iterations,immune_count,label="Immune",color="blue")
plt.plot(iterations,dead_count,label="Dead",color="black")
plt.xlabel("Iteration")
plt.ylabel("Number of People")
plt.title("Task 3: Population States Over Time")
plt.legend()
plt.savefig(os.path.join(figure_dir,"task3_population_states_over_time.png"),dpi=300,bbox_inches="tight")
plt.show()

# Task 3.1
# Effect of fatality probability on mortality
prob_spread = 0.5
prob_vaccinated = 0.0
prob_start = 0.002

fatal_values = np.arange(0.0, 1.01, 0.1)
mean_dead = []

# set different fatality probabilities
for prob_fatal in fatal_values:
    results = []
    # run 100 random simulations
    for run in range(100):

        dead_fraction, immune_fraction, healthy_fraction, population_history = disease(nx,ny,prob_spread,prob_vaccinated,prob_start,prob_fatal)

        results.append(dead_fraction)

    # compute mean dead fraction
    mean_fraction = np.mean(results)
    mean_dead.append(mean_fraction)

    print(f"P_fatal = {prob_fatal:.1f}, Mean dead fraction = {mean_fraction:.3f}")


# plot the figure
plt.figure(figsize=(7, 5))
plt.plot(fatal_values, mean_dead, marker="o")
plt.xlabel("Probability of Fatality")
plt.ylabel("Mean Dead Fraction")
plt.title("Task 3.1: Effect of Fatality Probability on Mortality")
plt.savefig(os.path.join(figure_dir, "task3_1_fatality_probability.png"),dpi=300,bbox_inches="tight")
plt.ylim(0, 1.05)
plt.show()


# Task 3.2
# Effect of vaccination on mortality
prob_spread = 0.5
prob_start = 0.002
prob_fatal = 0.5

vaccinated_values = np.arange(0.0, 1.01, 0.1)
mean_dead_vaccine = []

# set different vaccination probabilities
for prob_vaccinated in vaccinated_values:
    results = []
    # run 100 random simulations
    for run in range(100):

        dead_fraction, immune_fraction, healthy_fraction, population_history = disease(nx,ny,prob_spread,prob_vaccinated,prob_start,prob_fatal)

        results.append(dead_fraction)

    # compute mean dead fraction
    mean_fraction = np.mean(results)
    mean_dead_vaccine.append(mean_fraction)

    print(f"P_vaccinated = {prob_vaccinated:.1f}, Mean dead fraction = {mean_fraction:.3f}")


# plot the figure
plt.figure(figsize=(7, 5))
plt.plot(vaccinated_values, mean_dead_vaccine, marker="o")
plt.xlabel("Probability of Vaccination")
plt.ylabel("Mean Dead Fraction")
plt.title("Task 3.2: Effect of Vaccination on Mortality")
plt.ylim(0, 1.05)
plt.savefig(os.path.join(figure_dir, "task3_2_vaccination.png"),dpi=300,bbox_inches="tight")
plt.show()