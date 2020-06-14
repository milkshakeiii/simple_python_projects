class Stone:
    def __init__(self, weight = 2, ability = "lug"):
        self.character = "."
        self.weight = weight #kg
        self.ability = ability


class Player:
    def __init__(self, stones = [Stone(), Stone(), Stone()]):
        self.stones = stones
        

def make_hexgrid(radius):
    hexgrid = {}
    hexgrid[0, 0] = None
    for i in range(radius+1):
        for j in range(0, i*8):
            hexgrid[i, j] = None
    return hexgrid


def hexgrid_string(hexgrid, radius):
    printsize = radius*4+1
    lines = [list(" "*(printsize)) for i in range(printsize)]
    center = (printsize//2, printsize//2)
    lines[center[1]][center[0]] = hexgrid[(0, 0)].character if hexgrid[(0, 0)] else "_"

    for i in range(1, radius+1):
        n = 0
        x = center[0] - i*2
        y = center[1]
        for direction in [(1, -1), (1, 1), (-1, 1), (-1, -1)]:
            for j in range(i*2):
                if hexgrid[i, n]:
                    lines[y][x] = hexgrid[i, n].character
                else:
                    lines[y][x] = "_"
                    
                x += direction[0]
                y += direction[1]
                n += 1

    return('\n'.join([''.join(line) for line in lines]))


def print_hexgrid(hexgrid, radius):
    print(hexgrid_string(hexgrid, radius))


def place_stone(hexgrid, stone, radius, position):
    hexgrid[radius, position] = stone
    do_ability(hexgrid, stone, radius, position)


def do_ability(hexgrid, stone, radius, position):
    


def place_stone_command(radius_input, position_input, stone_input, hexgrid, player):
    radius = 0
    radius = int(radius_input)
    position = int(position_input)
    stone_index = int(stone_input)
    stone = player.stones.pop(stone_index)
    place_stone(hexgrid, stone, radius, position)
    return hexgrid_string(hexgrid, 3)


def inventory_command(player):
    inventory_string = []
    for stone in player.stones:
        inventory_string.append(str(stone))
    return '\n'.join(inventory_string)

    
hexgrid = make_hexgrid(3)
player = Player()
while (True):
    command = input().split()
    if len(command) == 0:
        continue
    
    command_name = command[0]

    if command_name == "place":
        if len(command) != 4:
            print("Wrong number of arguments")
            continue
        print (place_stone_command(command[1], command[2], command[3], hexgrid, player))
        continue

    if (command_name == "inventory") or (command_name == "i"):
        print (inventory_command(player))
        continue

    if (command_name == "look"):
        print(hexgrid_string(hexgrid, 3))
        continue
