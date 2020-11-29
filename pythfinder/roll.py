import random
import re

# Roll dice, using the following syntax:
#
#     pythfinder.roll("2d4")
#     pythfinder.roll("1d20+5")
#     pythfinder.roll("3d8+5+2")
#     pythfinder.roll("2d6+4-7+12-9")
#
# Returns integer value of final result
def roll(roll_string = ""):
    # regex strings
    dice_regex = "[0-9]+d[0-9]+"
    modifier_regex = "\+[0-9]+|\-[0-9]+"

    # Parse roll string, getting dice and all modifiers
    dice = re.findall(dice_regex, roll_string)
    modifiers = re.findall(modifier_regex, roll_string)

    if not dice:
        raise ValueError("roll: improper dice format")

    subtotal = 0
    natural_rolls = []
    for die in dice:
        dice_count = int(re.search("^[0-9]*", die).group(0))
        dice_size = int(re.search("[0-9]*$", die).group(0))
    
        # Sum each dice roll
        for d in range(dice_count):
            result = random.randrange(1,dice_size+1)
            subtotal += result
            natural_rolls.append((dice_size, result))
    # Sum each modifier
    if modifiers:
        for m in modifiers:
            subtotal += int(m)

    return {
        "natural_rolls": natural_rolls,
        "total": subtotal
    }
