#!/bin/sh
#
# dbcleanup.sh
#
# Deletes and creates the pathfinder database for testing

psql postgres -c "DROP DATABASE pathfinder"
createdb pathfinder
psql pathfinder -f ./create_db.sql
