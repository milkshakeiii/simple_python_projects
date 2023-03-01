
# >>> try_out_lure_set({(5, 1, 1, 1)}, 1)
# 160000
# >>> (9*10//2)*10**3*3+(4*5//2+5*6//2)*10**3
# 160000

# brute force
def try_out_lure_set(lure_set, try_increment):
    total_pointwise_distance_for_all_fish = 0
    for r in range(1, 11, try_increment):
        for g in range(1, 11, try_increment):
            for b in range(1, 11, try_increment):
                for a in range(1, 11, try_increment):
                    best_lure_pointwise_distance = 400
                    for lure in lure_set:
                        best_lure_pointwise_distance = min(best_lure_pointwise_distance, compute_pointwise_distance(lure, r, g, b, a))
                    total_pointwise_distance_for_all_fish += best_lure_pointwise_distance
    return total_pointwise_distance_for_all_fish

# merely force
def try_out_lure_set_2(lure_set, coord_value_max):
    rz = set([lure[0] for lure in lure_set])
    gz = set([lure[1] for lure in lure_set])
    bz = set([lure[2] for lure in lure_set])
    az = set([lure[3] for lure in lure_set])
    
    distance_sums = 0
    for xz in [rz, gz, bz, az]:
        xz_min = min(xz)
        xz_max = max(xz)
        xz_up = [float('inf')]*coord_value_max
        xz_down = [float('inf')]*coord_value_max
        up_step = xz_min
        distance = 0
        while (up_step <= coord_value_max):
            xz_up[up_step-1] = distance
            up_step += 1
            distance += 1
            if (up_step in xz):
                distance = 0
        down_step = xz_max
        distance = 0
        while (down_step >= 1):
            xz_down[down_step-1] = distance
            down_step -= 1
            distance += 1
            if (down_step in xz):
                distance = 0
        distances = [min(step_distances) for step_distances in zip(xz_up, xz_down)]
        print(distances)
        distance_sums += sum(distances)*coord_value_max**3
    return distance_sums


def compute_pointwise_distance(lure, r, g, b, a):
    distance = 0
    distance += abs(lure[0]-r)
    distance += abs(lure[1]-g)
    distance += abs(lure[2]-b)
    distance += abs(lure[3]-a)
    return distance

def exhaustive_lure_set(increment):
    lure_set = set()
    for r in range(increment, 100, increment):
        for g in range(increment, 100, increment):
            for b in range(increment, 100, increment):
                for a in range(increment, 100, increment):
                    lure_set.add((r, g, b, a))
    return lure_set

def try_many_lure_sets(increment, set_size):
    selection_indices = [0]*set_size
    all_lures = list(sorted(exhaustive_lure_set(increment)))
    best_set = None
    best_set_distance = float('inf')
    for i in range(len(all_lures)**set_size-1):
        increment_index = 0
        selection_indices[increment_index] += 1
        while selection_indices[increment_index] == len(all_lures):
            selection_indices[increment_index] = 0
            increment_index += 1
            selection_indices[increment_index] += 1
        try_us = set()
        for index in selection_indices:
            try_us.add(all_lures[index])
        distance = try_out_lure_set(try_us, 5)
        if distance < best_set_distance:
            best_set_distance = distance
            best_set = try_us
        if (i%100==0):
            print(best_set)
            print(best_set_distance)
            print(selection_indices)
    return (best_set, best_set_distance)
