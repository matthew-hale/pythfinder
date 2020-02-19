# Pythfinder

A repository for an in-development Pathfinder 1e python app. The goal 
is to be able to keep track of multiple characters, and provide 
functionality such as rolling for attacks/skills, computing bonuses, 
etc.

NOTE: this is _very_ WIP, and is mostly for personal use at this time. 
It's got lots of rough edges.

## Requirements

+ python
+ a character sheet in JSON format (copy the template to get started; 
future versions will have character sheet generators, as well as format 
enforcement)

## Roadmap

+ ~~Rework script arguments into subcommand + argument~~
+ ~~Add interactive flag for old behavior~~
    I'm going to get rid of this for now; it might end up being too 
    much effort to implement an interactive prompt with the new 
    argument structure. Will revisit in the future.
+ ~~Basic tracking of, and output for:~~
    + ~~attacks~~
    + ~~feats~~
    + ~~traits~~
    + ~~spells~~
+ Functionality to edit/update values of:
    + ~~ability scores~~

        Same as below; I need to create functions specifically for 
        adding/removing ability/skill modifiers, possibly by name. This 
        would necessitate reworking the structure of both, or maybe 
        adding a class for temporary/permanent effects, I'm not sure.

    + ~~skill ranks/class status/notes~~

        This still needs a custom function to add/remove/change any of 
        the "misc" modifiers on skills, but otherwise it's implemented 
        fully

    + ~~items~~
    + ~~attacks~~
    + ~~feats~~
    + ~~traits~~
    + ~~spells~~
    + ~~special abilities~~
    + etc.
+ New character creation walkthrough process (CLI)
+ ~~Character sheet JSON format enforcement~~
    + ~~This is partially done with the Character class, but I'll 
    eventually have classes for other complex objects within the 
    character, like items, attacks, spells, etc. Makes it easier to 
    import json; just grab values if they're there, if not use the 
    defaults, and for extra values just ignore them.~~ this is now 
    pretty much finished, nearly everything is an object
+ ~~add ability modifiers (for temp increases/damage)~~
+ rework hp:
    + ~~add wounds, temp hp, temporary max hp increases~~
    + ~~essentially make current hp a calculated value~~

    I'm not doing either of these, but I am adding nonlethal damage

+ add full armor class components
+ expand on attacks and armor class:
    + display all modifiers
    + show the rolls and modifiers for hits and damage
    + track enhancement bonus / masterwork status
    + (AC) show touch/flat footed and all the modifiers
+ implement spells like equipment and attacks:
    + ~~spells get tracked in the character.spells list~~
    + damaging spells can get added to the spell attack list, like 
    weapon attacks
    + show damage, cast time, duration (if applicable)
+ Refactor classes into single Character class

    Thinking about it more, it doesn't make sense for all of these 
    character properties to be their own classes; their constructors 
    and methods could just be Character() methods. It would greatly 
    simplify a lot of the structure of this package.

+ Eventually:
    + Decoupling of input and data processing, converting outputs to 
    json format
    + Option to have outputs be served via restful API (in addition to 
    CLI)
    + Web app frontend for restful API
