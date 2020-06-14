class Game():
    def __init__(self, x_size, y_size, z_size):
        board = []
        for x_pos in range(x_size):
            cut = []
            for y_pos in range(y_size):
                column = []
                for z_pos in range(z_size):
                    column.append(0)
                cut.append(column)
            board.apend(cut)
            
