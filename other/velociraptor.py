import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation


VELOCIRAPTOR_SPEED = 60 * (1000/3600) #mps
VELOCIRAPTPR_TURN_SPEED = 36*(math.pi**2) / 100 #radians per second

VELOCIRAPTOR_REACH = 1 #meter

PREY_SPEED = 50 * (1000/3600) #mps
PREY_TURN_SPEED = 36*(math.pi**2) / 100 #radians per second

class Move():
    def __init__(self, rotate, move):
        self.turn_speed = rotate
        self.move_speed = move


#######################HEURISTICS
def time_to_dinner(velociraptor_x, velociraptor_y, velociraptor_facing, prey_x, prey_y, prey_facing):
    x_distance_to_prey = math.abs(velociraptor_x - prey_x)
    y_distance_to_prey = math.abs(velociraptor_y - prey_y)
#################################




#########################STRATEGIES
#VELOCIRAPTOR STRATEGIES RETURN A LIST OF MOVES FOR EACH VELOCIRAPTOR
def dummy_velociraptor_strategy(seconds, velociraptors, prey_x, prey_y, prey_facing, move_count):
    strategies = []
    for velociraptor in velociraptors:
        strategies.append([Move(math.pi, 30) for move_index in range(move_count)])
    return strategies

#PREY STRATEGIES RETURN A LIST OF MOVES FOR THE PREY
#veliciraptors = (x, y, facing)
def dummy_prey_strategy(seconds, velociraptors, my_x, my_y, my_facing,move_count):
    return [Move(math.pi, 30) for move_index in range(move_count)]
###################################





#veliciraptors = (x, y, facing)
def move(trig_function, start_facing, start_x_or_y, seconds, move_speed, turn_speed):
    displacement = 0
    angle = 0
    if (turn_speed == 0):
        displacement = move_speed * seconds
        angle = start_facing
    else:
        r = move_speed/turn_speed
        a = turn_speed*seconds
        displacement = math.sqrt(2*r*r - 2 * r * r * math.cos(a))
        angle = start_facing + a / 2
    return start_x_or_y + displacement * trig_function(angle)

def x_move(start_facing, start_x, seconds, move_speed, turn_speed):
    return move(math.cos, start_facing, start_x, seconds, move_speed, turn_speed)
def y_move(start_facing, start_y, seconds, move_speed, turn_speed):
    return move(math.sin, start_facing, start_y, seconds, move_speed, turn_speed)

def turn(start_facing, seconds, turn_speed):
    return start_facing + seconds * turn_speed
def simulate_seconds(seconds,
                     velociraptors,
                     velociraptor_strategy,
                     prey_x,
                     prey_y,
                     prey_facing,
                     prey_strategy,
                     how_many_points):



    
    seconds_per_point = seconds/how_many_points

    prey_moves = prey_strategy(seconds, velociraptors, prey_x, prey_y, prey_facing, how_many_points)
    all_velociraptor_moves = velociraptor_strategy(seconds, velociraptors, prey_x, prey_y, prey_facing, how_many_points)

    prey_xs = [prey_x]
    prey_ys = [prey_y]
    prey_facings = [prey_facing]

    velociraptor_x_lists = [[velociraptor[0]] for velociraptor in velociraptors]
    velociraptor_y_lists = [[velociraptor[1]] for velociraptor in velociraptors]
    velociraptor_facing_lists = [[velociraptor[2]] for velociraptor in velociraptors]
    for time_step in range(1, how_many_points):
        prey_move = prey_moves[time_step-1]
        prey_xs.append(x_move(prey_facings[time_step-1],
                              prey_xs[time_step-1],
                              seconds_per_point,
                              prey_move.move_speed,
                              prey_move.turn_speed))
        prey_ys.append(y_move(prey_facings[time_step-1],
                              prey_ys[time_step-1],
                              seconds_per_point,
                              prey_move.move_speed,
                              prey_move.turn_speed))
        prey_facings.append(turn(prey_facings[time_step-1],
                                 seconds_per_point,
                                 prey_moves[time_step-1].turn_speed))

        for velociraptor_number in range(len(all_velociraptor_moves)):
            velociraptor_move = all_velociraptor_moves[velociraptor_number][time_step-1]
            previous_facing = velociraptor_facing_lists[velociraptor_number][time_step-1]
            previous_x = velociraptor_x_lists[velociraptor_number][time_step-1]
            velociraptor_x_lists[velociraptor_number].append(x_move(previous_facing,
                                                                    previous_x,
                                                                    seconds_per_point,
                                                                    velociraptor_move.move_speed,
                                                                    velociraptor_move.turn_speed))
            previous_y = velociraptor_y_lists[velociraptor_number][time_step-1]
            velociraptor_y_lists[velociraptor_number].append(y_move(previous_facing,
                                                                    previous_y,
                                                                    seconds_per_point,
                                                                    velociraptor_move.move_speed,
                                                                    velociraptor_move.turn_speed))
            velociraptor_facing_lists[velociraptor_number].append(turn(previous_facing,
                                                                       seconds_per_point,
                                                                       velociraptor_move.turn_speed))

    return prey_xs, prey_ys, prey_facings, velociraptor_x_lists, velociraptor_y_lists, velociraptor_facing_lists


def plot_game(points):
    fig = plt.figure()
    ax = plt.axes(xlim=(-200, 200), ylim=(-200, 200))

    velociraptor_x_lists = points[3]
    velociraptor_y_lists = points[4]
    prey_xs = points[0]
    prey_ys = points[1]

    velociraptor_lines = tuple([ax.plot([], [], lw=3)[0] for x_list in velociraptor_x_lists])
    prey_line, = ax.plot([], [])
    
    def init():
        for line in velociraptor_lines:
            line.set_data([], [])
        prey_line.set_data([], [])
        return velociraptor_lines + (prey_line,)

    def update(i):
        for j in range(len(velociraptor_lines)):
            line = velociraptor_lines[j]
            line.set_data(velociraptor_x_lists[j][:i], velociraptor_y_lists[j][:i])
        prey_line.set_data(prey_xs[:i], prey_ys[:i])
        return velociraptor_lines + (prey_line,)


    anim = animation.FuncAnimation(fig, update, interval=1, init_func=init, blit=True)

    plt.show()


def detect_dinner(points):
    for i in range(len(points[0])):
        prey_x = points[0][i]
        prey_y = points[1][i]
        prey_facing = points[2][i]
        all_velociraptor_xs = points[3]
        all_velociraptor_ys = points[4]
        all_velociraptor_facings = points[5]
        for velociraptor_i in range(len(all_velociraptor_xs)):
            velociraptor_x = all_velociraptor_xs[velociraptor_i][i]
            velociraptor_y = all_velociraptor_ys[velociraptor_i][i]
            velociraptor_facing = all_velociraptor_facings[velociraptor_i][i]
            difference_vector = (abs(prey_x-velociraptor_x), abs(prey_y-velociraptor_y))
            difference_angle = 



how_many_points = 1000
velociraptors = [(0, 50, 0),
                    (50, 0, 0),
                    (0, -50, 0)]
prey_x, prey_y, prey_facing = (0, 0, 0)
points=simulate_seconds(15,
                        velociraptors,
                        dummy_velociraptor_strategy,
                        prey_x,
                        prey_y,
                        prey_facing,
                        dummy_prey_strategy,
                        how_many_points)

if (detect_dinner(points)):
    print ("Eaten")
else:
    print ("Escaped!")

plot_game(points)
