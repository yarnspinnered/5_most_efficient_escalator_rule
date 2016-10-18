import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import statistics
import random
import seaborn as sns

"""
This script simulates people riding the escalator according to two different scenarios. In one, the left lane is reserved for walkers and the right lane is 
reserved for people who stand still. The alternative scenario is that people just stay at whatever lane they arrive at, regardless of whether they walk or
stand still, potentially blocking people behind them. We assume 80% of people walk and walkers complete their journey in half the time a "stander" takes and 
then we model the number of people who finish an escalator ride under the two rules. We find there is little difference when the escalator is relatively empty
but the free-for-all rule quickly becomes more efficient as the escalator becomes busier. Interestingly, the disparity grows as the probability of a walker
diverges from 0.5. Intuitively, it's probably because half the escalator is being reserved for less than half of the riders which is clearly inefficient.
"""
walker_chance = 0.8
escalator_length = 20
esc_trip_count = 10
passenger_chance_list = [x * 0.1 for x in range(11)]

def simulate_trips(walker_rule):
    main = np.array([[0, 0] for x in range(escalator_length)])
    result = []
    #passenger chance denotes the chance of a passenger appearing on the currently empty bottom step
    
    for passenger_chance in passenger_chance_list:
        trip_list = []
        for one_sim in range(100):
            walker_count = 0
            still_count = 0
            for tick in range(escalator_length * esc_trip_count):
                for pos, x in np.ndenumerate(main):
                    main[pos] = 0
                    #255 indicates the walkers
                    if x == 255:
                        new_pos = list(pos)
                        new_pos[0] -= 2
                        other_col = 1
                        if pos[1] == 1: other_col = 0
                        
                        #Change walking rule based on whether walkers only stay on the left
                        if walker_rule == True:
                        #Check if they still are on the escalator and choose the most efficient path if they are a walker
                            if new_pos[0] >= 0:
                                if main[tuple(new_pos)] == 0:
                                    main[tuple(new_pos)] = 255
        #                         2 elifs implement the weave/in out rule
                                elif main[new_pos[0], other_col] == 0 and main[pos[0], other_col] == 0 \
                                                                      and main[new_pos[0] + 1, other_col] == 0:
                                    main[new_pos[0] + 1, other_col] = 255
                                elif main[new_pos[0], other_col] == 0 and main[new_pos[0] + 1, other_col] == 0:
                                    main[new_pos[0] + 1, other_col] = 255
                                else:
                                    new_pos[0] += 1
                                    main[tuple(new_pos)] = 255
                            else:
                                walker_count += 1
                        else:
                            if new_pos[0] >= 0:                            
                                if main[tuple(new_pos)] == 0:
                                    main[tuple(new_pos)] = 255
                                else:
                                    new_pos[0] += 1
                                    main[tuple(new_pos)] = 255
                            else:
                                walker_count += 1                            
                    elif x == 100:
                        new_pos = list(pos)
                        new_pos[0] = new_pos[0] - 1
                        if new_pos[0] >= 0:
                            main[new_pos[0], new_pos[1]] = 100
                        else:
                            still_count += 1
                #Add in new entrants (Completely random)
                new_entries = np.random.choice([255, 100, 0], 1 * 2, p=[passenger_chance * walker_chance,
                                                                        (1 - walker_chance) * passenger_chance, 
                                                                        1 - passenger_chance])
                #Implement walkers on left, standers on the right rule
                if walker_rule == True:
                    if np.array_equal(new_entries, np.array([100,255])): 
                        new_entries = np.array([255, 100])
                    elif np.array_equal(new_entries, np.array([100,0])) or np.array_equal(new_entries, np.array([100,100])): 
                        new_entries = np.array([0, 100])
                    elif np.array_equal(new_entries, np.array([0,255])) or np.array_equal(new_entries, np.array([255,255])):
                        new_entries = np.array([255, 0])
                        
                main = np.vstack([main[:-1], new_entries])
            trip_list.append(walker_count + still_count)
        result.append(sum(trip_list)/len(trip_list))
    return result

x1 = simulate_trips(True)
x2 = simulate_trips(False)

rule_plot, = plt.plot(passenger_chance_list, x1)
no_rule_plot, = plt.plot(passenger_chance_list, x2)
plt.legend([no_rule_plot, rule_plot], ["Free walking", "Walker's on right only"], loc=2)
plt.xlabel('Probability of a new arrival', fontsize=18) 
plt.ylabel('Number of people to complete journey', fontsize=18) 
plt.show()