import random
import re
import json

# Roll dice, using the following syntax:
#
#     pythfinder.roll("2d4")
#     pythfinder.roll("1d20+5")
#     pythfinder.roll("3d8+5+2")
def roll(roll_string = ""):
    # Parse roll string
    match = re.search("^[0-9]+d[0-9]+\+?[0-9]+$", roll_string)
    if match:
        roll = match.group(0)
    else:
        return None

    bonus = re.search("\+", roll)

    # Parse the string, including optional bonus
    roll_bonus = 0
    if bonus:
        # the number of dice comes before the "d", and the size of the 
        # dice comes right after, but before any plus signs
        roll_count = int(roll.split("d")[0])
        roll_size = int(roll.split("d")[1].split("+")[0])
        roll_bonus = int(roll.split("d")[1].split("+")[1])
    else:
        roll_split = roll.split("d")
        roll_count = int(roll_split[0])
        roll_size = int(roll_split[1])

    total = 0
    for _ in range(roll_count):
        if roll_size == 1:
            result = 1
        else:
            result = random.randrange(1,roll_size)
        total += result

    total += roll_bonus 

    return total
