import math

def answer(minions):
    #append minion number to ensure every minion is unique
    minions = [(minions[i][0], minions[i][1], minions[i][2], i) for i in range(len(minions))]
    
    #simply interrogate the minions with the highest chance-per-minute (lowest
    #minutes per chance) first. Since python sort is stable, this will
    #break ties in favor of the lower minion number (original index)
    return [minions.index(minion) for minion in sorted(minions, key=minutes_per_chance)]
    
def minutes_per_chance(minion):
    #minion[1] is chance numerator, minion[2] is chance denominator
    #minion[0] is minutes
    return float(minion[0]) / (float(minion[1])/minion[2])
