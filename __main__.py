import random
from matplotlib import pyplot

class villager:
    def __init__(self, type="villager"):
        self.type = type
        self.alive = True
    
    def check_death(self):
        return self.alive
    
    def check_type(self):
        return self.type

    def kill(self):
        self.alive = False

def check_winner(survivors):
    if len(survivors["Villagers"]) <= 2:
        return "Werewolves"
    elif len(survivors["Werewolves"]) == 0:
        return "Villagers"
    else:
        return "No winner yet"

def display_message(message):
    #print(message)
    pass

def initilase_townfolk(num_of_villagers=25, num_of_werewolves=2):
    town_folk = {"Villagers":[], "Werewolves":[]}

    # Initilase all the villagers
    for i in range(num_of_villagers):
        person = villager()
        town_folk["Villagers"].append(person)

    # Initilase all the werewolves
    for i in range(num_of_werewolves):
        wolf = villager("werewolf")
        town_folk["Werewolves"].append(wolf)
    return town_folk

def run_game(num_of_villagers=5, num_of_werewolves=2, num_of_runs=100, win_counter={"Werewolves":0, "Villagers":0}):
    for i in range(num_of_runs):
        survivors = initilase_townfolk(num_of_villagers, num_of_werewolves)
        num_of_villagers_remaining = num_of_villagers
        num_of_werewolves_remaining = num_of_werewolves
        won = False
        winner = ""
        display_message("New game!")
        while not won:
            display_message("New day!")
            # First execute a villager
            chosen_victim = random.randint(0, num_of_villagers_remaining-1)
            # Kill the villager
            victim = survivors["Villagers"].pop(chosen_victim -1)
            victim.kill()
            num_of_villagers_remaining -= 1

            # Now check if anyone won
            winner = check_winner(survivors)
            if winner == "Werewolves":
                win_counter["Werewolves"] += 1
                won = True

            if not won:
                # Now execute a random person (Villager or Werewolf)
                chosen_victim = random.randint(0, num_of_villagers_remaining + num_of_werewolves_remaining -1)
                if chosen_victim > num_of_villagers_remaining -1:
                    # A wolf is being killed
                    victim = survivors["Werewolves"].pop(chosen_victim - num_of_villagers_remaining -1)
                    victim.kill()
                    num_of_werewolves_remaining -= 1
                    display_message("A werewolf has been killed")
                else:
                    # A villager is chosen
                    victim = survivors["Villagers"].pop(chosen_victim-1)
                    victim.kill()
                    num_of_villagers_remaining -= 1
                    display_message("A villager has been killed")
                
                # Now check if anyone won
                winner = check_winner(survivors)
                if winner == "Werewolves":
                    win_counter["Werewolves"] += 1
                    won = True
                elif winner == "Villagers":
                    win_counter["Villagers"] += 1
                    won = True
    return (win_counter["Werewolves"], win_counter["Villagers"])

def plot_readings(number_of_townfolk=[], win_rate_of_villagers=[]):
    # Plot the number of townfolk on the bottom to the win rate of the villagers along the top
    pyplot.plot(number_of_townfolk, win_rate_of_villagers)
    # Label the axes
    pyplot.xlabel("Number of townsfolk")
    pyplot.ylabel("Winrate of villagers")
    pyplot.title("Werewolf Simulation")
    pyplot.show()

def run_simulations(min_num_of_townsfolk=10, max_num_of_townsfolk=100, step=1, number_of_werewolves=2, simulations_per_step=1000):
    number_of_townfolk = []
    win_rate_of_villagers = []

    # Run the sim
    for num_of_townsfolk in range(min_num_of_townsfolk, max_num_of_townsfolk, step):
        # Create the simulation
        win_counter = run_game(num_of_townsfolk, number_of_werewolves, simulations_per_step)
        # Record the number of townsfolk
        number_of_townfolk.append(num_of_townsfolk)
        # Record the success rate of the townsfolk
        success_rate = 100 * win_counter[1] / (win_counter[0] + win_counter[1])
        win_rate_of_villagers.append(success_rate)
    # Plot the graph
    plot_readings(number_of_townfolk, win_rate_of_villagers)

def main(min_num_of_townsfolk=1, max_num_of_townsfolk=100, step=1, number_of_werewolves=2, simulations_per_step=10000):
    run_simulations(min_num_of_townsfolk, max_num_of_townsfolk, step, number_of_werewolves, simulations_per_step)

main()