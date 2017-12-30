zodiac_animals = ["Bear", "Cat", "Dog", "Dolphin", "Antelope", "Gila Monster",
                  "Orangutan", "Rat", "Rooster", "Sheep", "Giraffe", "Puffin"]

print ("In which year were you born?")

year = None
while year == None:
    try:
        year = int(input())
    except:
        print ("Please enter an integer year.")

year_remainder = year%12

print ("Your Zodiac animal is the " + zodiac_animals[year_remainder] + ".")
