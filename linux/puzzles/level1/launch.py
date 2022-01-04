import sys

def do_launch():
    print ("rrrrrrrROOOOOOOooooooooom.....!  We're on our way!")
    sys.cmd("mv ../level1 ../level1_done")
    print ("Level 1 complete!")

password = input("Please enter password: ")
if password == "sagan_rules":
    do_launch()
else:
    print("That is not correct.")
