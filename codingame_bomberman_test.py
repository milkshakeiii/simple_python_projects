
    #test
    position.display()
    sequenced_moves = [[Move(BOMB_MOVE, 1, 0, 1)],
                       [Move(BOMB_MOVE, 1, 1, 1)],
                       [Move(MOVE_MOVE, 1, 2, 1)],
                       [Move(MOVE_MOVE, 1, 1, 1)],
                       [Move(MOVE_MOVE, 2, 1, 1)],
                       [Move(BOMB_MOVE, 1, 1, 1)],
                       [Move(BOMB_MOVE, 0, 1, 1)],
                       [Move(MOVE_MOVE, 0, 2, 1)],
                       [Move(MOVE_MOVE, 0, 3, 1)],
                       [Move(MOVE_MOVE, 0, 2, 1)],
                       [Move(MOVE_MOVE, 1, 2, 1)],
                       [Move(MOVE_MOVE, 2, 2, 1)],
                       [Move(MOVE_MOVE, 3, 2, 1)],
                       [Move(MOVE_MOVE, 3, 1, 1)],
                       [Move(MOVE_MOVE, 4, 1, 1)],
                       [Move(BOMB_MOVE, 3, 1, 1)],
                       [Move(MOVE_MOVE, 3, 1, 1)],
                       [Move(MOVE_MOVE, 3, 1, 1)],
                       [Move(MOVE_MOVE, 3, 1, 1)],
                       [Move(MOVE_MOVE, 3, 1, 1)],
                       [Move(MOVE_MOVE, 3, 1, 1)],
                       [Move(MOVE_MOVE, 3, 1, 1)],
                       [Move(MOVE_MOVE, 3, 1, 1)],
                       [Move(MOVE_MOVE, 3, 1, 1)],
                       [Move(MOVE_MOVE, 3, 1, 1)],
                       [Move(MOVE_MOVE, 3, 0, 1)],
                       [Move(MOVE_MOVE, 4, 0, 1)],
                       [Move(MOVE_MOVE, 1, 2, 1)],
                       [Move(BOMB_MOVE, 1, 3, 1)],
                       [Move(MOVE_MOVE, 1, 2, 1)],
                       [Move(MOVE_MOVE, 1, 2, 1)],
                       [Move(MOVE_MOVE, 1, 2, 1)],
                       [Move(MOVE_MOVE, 1, 2, 1)],
                       [Move(MOVE_MOVE, 1, 2, 1)],
                       [Move(MOVE_MOVE, 1, 2, 1)],
                       [Move(MOVE_MOVE, 1, 2, 1)],
                       [Move(MOVE_MOVE, 1, 2, 1)]]

    new_position = copy.deepcopy(position)
    for moves in sequenced_moves:
        new_position = new_position.move_result(moves)
        new_position.display()
        print ("---")
    break
