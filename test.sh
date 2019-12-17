#!/bin/sh
#
# test.sh
#
# Script for testing out the database

skills=$(psql pathfinder --csv -c "SELECT name, ranks, is_class, profession_or_craft_type FROM character_skills WHERE character = 'Qofin Parora'" | tail -n +2)

out="Current skill bonuses:\n"

IFS="
"
for skill in $skills; do
    skillName=$(echo "$skill" | cut -d "," -f 1)
    ranks=$(echo "$skill" | cut -d "," -f 2)
    isClass=$(echo "$skill" | cut -d "," -f 3)
    isCraftOrProfession=$(echo "$skill" | cut -d "," -f 4)
    if [ "$isClass" = "t" ]; then
        if [ "$ranks" -ge 1 ]; then
            bonus=$(( ranks + 3 ))
        else
            bonus="$ranks"
        fi
    else
        bonus="$ranks"
    fi
    if [ -n "$isCraftOrProfession" ]; then
        skillName="${skillName} (${isCraftOrProfession})"
    fi
    out="${out}${skillName}: ${bonus}\n"
done

env printf "$out"
