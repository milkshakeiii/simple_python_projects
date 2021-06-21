def answer(numbers):
    seen_pirates = []
    current_pirate = 0
    while current_pirate not in seen_pirates:
        seen_pirates.append(current_pirate)
        current_pirate = numbers[current_pirate]
    return len(seen_pirates[seen_pirates.index(current_pirate):])
