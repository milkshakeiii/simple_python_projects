import math, numpy
import random
import matplotlib.pyplot

NUMBER_OF_WALKS = 10000
POINTS_PER_WALK = 12
LENGTH_OF_STEP = 1

walks = []
spatial_walks = []
temporal_walks = []

for i in range(NUMBER_OF_WALKS):
    walk = [(0, 0)]
    for j in range(POINTS_PER_WALK-1):
        angle = random.random() * math.pi * 2
        next_step_one = (math.cos(angle)*LENGTH_OF_STEP, math.sin(angle)*LENGTH_OF_STEP)
        angle = random.random() * math.pi * 2
        next_step_two = (math.cos(angle)*LENGTH_OF_STEP, math.sin(angle)*LENGTH_OF_STEP)
        last_point = walk[-1]
        walk.append((last_point[0] + next_step_one[0] + next_step_two[0], last_point[1] + next_step_one[1] + next_step_two[1]))

    spatial_distances = [[0 for i in range(POINTS_PER_WALK)] for j in range(POINTS_PER_WALK)]
    temporal_distances = [[0 for i in range(POINTS_PER_WALK)] for j in range(POINTS_PER_WALK)]
    for i in range(POINTS_PER_WALK):
        for j in range(POINTS_PER_WALK):
            point_a = walk[i]
            point_b = walk[j]
            x_distance = point_a[0] - point_b[0]
            y_distance = point_a[1] - point_b[1]
            spatial_distances[i][j] = (math.sqrt(x_distance**2 + y_distance**2))
            temporal_distances[i][j] = (abs(i-j))

    spatial_walk = numpy.array(spatial_distances)
    spatial_walk = numpy.triu(spatial_walk)
    spatial_walk = spatial_walk.flatten()

    temporal_walk = numpy.array(temporal_distances)
    temporal_walk = numpy.triu(temporal_walk)
    temporal_walk = temporal_walk.flatten()

    spatial_walks.append(spatial_walk)
    temporal_walks.append(temporal_walk)
    walks.append(walk)

for i in range(10000):
    if (numpy.corrcoef(temporal_walks[i], spatial_walks[i])[0][1] < 0.55):
        x = []
        y = []
        for point in walks[i]:
            x.append(point[0])
            y.append(point[1])
        matplotlib.pyplot.plot(x, y)
        matplotlib.pyplot.show()


