def manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class EmitStone:
    def __init__(self, intensity, fade_distance, position):
        self.intensity = intensity
        self.fade_distance = fade_distance
        self.position = position

    def is_light(self):
        return intensity > 0

    def light_function(self, x, y):
        separation = manhattan(self.position, (x, y))
        shine = max(0, (1 - separation / self.fade_distance)) * self.intensity
        return shine

light_stones = []
light_stones.append(EmitStone(12, 3, (0, 0)))
light_stones.append(EmitStone(12, 3, (3, 3)))
dark_stones = []
dark_stones.append(EmitStone(-12, 3, (1, 0)))
dark_stones.append(EmitStone(-12, 3, (2, 3)))

width = 4
height = 4
intensities = [[0 for i in range(width)] for i in range(height)]
for i in range(width):
    for j in range(height):
        light_sum = sum([stone.light_function(i, j) for stone in light_stones])
        dark_sum = sum([stone.light_function(i, j) for stone in dark_stones])
        if abs(light_sum) > abs(dark_sum):
            intensities[j][i] = light_sum
        elif abs(light_sum) < abs(dark_sum):
            intensities[j][i] = dark_sum
        else:
            intensities[j][i] = 0

squares = []
for i in range(width):
    for j in range(height):
        squares.append((i, j))

square_pairs = []
for square1 in squares:
    (x, y) = square1
    for square2 in [(x + 1, y + 0), (x + 0, y + 1), (x - 1, y + 0), (x + 0, y - 1)]:
        (x, y) = square2
        in_bounds = x >= 0 and y >= 0 and x < width and y < height
        not_duplicate = ((square2, square1) not in square_pairs) and ((square1, square2) not in square_pairs)
        if in_bounds and not_duplicate:
            square_pairs.append((square1, square2))

score = 0
for pair in square_pairs:
    (x1, y1) = pair[0]
    (x2, y2) = pair[1]
    intense1 = intensities[y1][x1]
    intense2 = intensities[y2][x2]
    if (intense1 > 0) != (intense2 > 0):
        new_points = min(abs(intense1), abs(intense2))
        score += new_points

def pretty_print(board):
    for i in range(len(board)):
        print(''.join([(5 - len(str(int(value))))*' ' + str(int(value)) for value in board[i]]))

pretty_print(intensities)
print(score)
