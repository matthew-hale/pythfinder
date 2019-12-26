# Pathfinder

A repository for an in-development Pathfinder 1e python app. The goal is to be 
able to keep track of multiple characters, and provide functionality such as 
rolling for attacks/skills, computing bonuses, etc.

NOTE: this is _very_ WIP, and is mostly for personal use at this time. It's 
got lots of rough edges.

## Requirements

+ python
+ a character sheet in JSON format (like the one I'm currently running in my carrion crown campaign, where this all started; future versions will have character sheet generators, as well as format enforcement)

## Roadmap

+ Basic tracking of, and output for:
    + ~~attacks~~
    + ~~feats~~
    + ~~traits~~
    + spells
+ Add/edit functionality for:
    + ability scores
    + skill ranks/class status/notes
    + items
    + attacks
    + feats
    + traits
    + spells
+ New character creation walkthrough process
+ Eventually:
    + Decoupling of input and data processing, converting outputs to json format
    + Option to have outputs be served via restful API (in addition to CLI)
    + Web app frontend for restful API
