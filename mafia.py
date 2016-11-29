import random

print("How many town players?")
town_count = int(input())
print("How many scum players?")
scum_count = int(input())

day_results = [[[town_count, scum_count, (1, 1), 0, ""]]]
            #town remaining, scum remaining, weight, game state, lynch order
            #game state is 0 for in progress, -1 for scum win, 1 for town win
current_day = 0

while True:
    last_day_results = day_results[current_day]
    current_day += 1
    current_day_results = []
    for result in last_day_results:
        if result[3] == 0:
            current_town_count = result[0]
            current_scum_count = result[1]
            current_total = current_town_count + current_scum_count
            current_weight = result[2]
            lynch_order = result[4]

            town_lynch_result = [current_town_count-2,
                                 current_scum_count,
                                 (current_weight[0] * current_town_count, current_weight[1] * current_total),
                                 0,
                                 lynch_order + "town, "]
            if (town_lynch_result[0]<=town_lynch_result[1]):
                town_lynch_result[3] = -1

            scum_lynch_result = [current_town_count-1,
                                 current_scum_count-1,
                                 (current_weight[0] * current_scum_count, current_weight[1] * current_total),
                                 0,
                                 lynch_order + "scum, "]

            if (scum_lynch_result[1] == 0):
                scum_lynch_result[3] = 1

            current_day_results.append(town_lynch_result)
            current_day_results.append(scum_lynch_result)

    day_results.append(current_day_results)
    if len(current_day_results) == 0:
        break


for i in range(len(day_results)):
    print("Day " + str(i) + ":")
    for result in day_results[i]:
        print("    --")
        print("    With weight " + str(result[2][0]) + "/" + str(result[2][1]))
        print("    Lynch order: " + result[4])
        if result[3] == 0:
            print("    (Still playing)")
        if result[3] == 1:
            print("    !Town wins!")
        if result[3] == -1:
            print("    !Scum wins!")
print("    Game over!")
    
        
all_results = []
for day in day_results:
    all_results = all_results + day

town_win_chance = 0
scum_win_chance = 0
for result in all_results:
    if result[3] == 1:
        town_win_chance += result[2][0]/result[2][1]
    if result[3] == -1:
        scum_win_chance += result[2][0]/result[2][1]

print("Overall town win chance: " + str(town_win_chance*100)[:5] + "%")
print("Overall scum win chance: " + str(scum_win_chance*100)[:5] + "%")
    





#[Weight 1] Day 1:  7 town 2 scum living.
#[Weight 7/9] Day 2a:  5 town 2 scum living.
#[Weight 2/9] Day 2b:  6 town 1 scum living.
#[Weight 35/63] Day 3aa:  3 town 2 scum living.
#[Weight 14/63] Day 3ab:  4 town 1 scum living.
#[Weight 12/63] Day 3ba:  4 town 1 scum living.
#[Weight 2/63] Day 3bb:  Town wins!
#[Weight 105/315] Day 3aaa: Scum wins!
#[Weight 70/315] Day 3aab: 2 town 1 scum living.
#[Weight 56/315] Day 3aba: 2 town 1 scum living.
#[Weight 14/315] Day 3abb: Town wins!
#[Weight 48/315] Day 3baa: 2 town 1 scum living.
#[Weight 12/315] Day 3bab: Town wins!
#[Weight 140/945] Day 4aaba: Scum wins!
#[Weight 70/945] Day 4aabb: Town wins!
#[Weight 112/945] Day 4abaa: Scum wins!
#[Weight 56/945] Day 4abab: Town wins!
#[Weight 96/945] Day 4baaa: Scum wins!
#[Weight 48/945] Day 4baab: Town wins!
