#!/bin/sh
#
# test.sh
#
# Script for testing out the database

skills=$(psql pathfinder --csv -c "SELECT name, ranks, is_class, profession_or_craft_type FROM character_skills WHERE character = 'Qofin Parora'" | tail -n +2)
echo "$skills"
