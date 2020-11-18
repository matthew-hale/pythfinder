(Note: I went on a bit of a hiatus from development during the 4-5 months after the initial COVID lockdowns, so that's why this project looks like it's pretty dead. I'm getting back into it now, so development will continue very soon.)

# Pythfinder

A repository for an in-development Pathfinder 1e python app. The goal 
is to be able to keep track of multiple characters, and provide 
functionality such as rolling for attacks/skills, computing bonuses, 
etc.

NOTE: this is _very_ WIP, and is mostly for personal use at this time. 
It's got lots of rough edges.

## Requirements

+ python
+ a character sheet in JSON format

To get a character sheet, you can either copy the template in 
data/template.json, or generate a blank one using either the cli 
script, or by writing your own script using the 
`pythfinder.writeCharacter()` function to save the output of 
`pythfinder.Character()` to a file.

## Roadmap

+ Change skills to support multiple Craft, Profession, and Perform 
skills
+ Change all modifiers/bonuses to be named & typed (e.g. temporary 
bonuses to abilities/skills)
+ Add methods for adding/editing/removing bonuses/penalties
+ Change BAB to single int, and calculate multiple attacks from high 
BAB instead of tracking multiple BAB values
+ Change equipment to include a "location" value, in addition to an 
"on-person" flag for weight calculation
    + Rework the current "pack" flag to a "camp" flag, to mark items 
    as "camp items" to allow for quick toggle of the "on-person" flag 
    when you set up camp (e.g., "I set up camp; put down all the camp 
    items and leave them at camp")
+ Revisit use cases for the "notes" of every other property, and see if 
they could be better served with real properties and methods
+ Add roll capability to attacks:
    + Roll hit
    + Roll damage
    + Automatically re-roll to confirm criticals
    + Rework attacks to have specific hit and damage modifiers (e.g. dex to hit, str to damage
+ ~~Rework script arguments into subcommand + argument~~
+ ~~Basic tracking of, and output for:~~
    + ~~attacks~~
    + ~~feats~~
    + ~~traits~~
    + ~~spells~~
+ Functionality to edit/update values of:
    + ~~ability scores~~
        + Same as below; I need to create functions specifically for 
        adding/removing ability/skill modifiers, possibly by name. This 
        would necessitate reworking the structure of both, or maybe 
        adding a class for temporary/permanent effects, I'm not sure.
    + ~~skill ranks/class status/notes~~
        + This still needs a custom function to add/remove/change any 
        of the "misc" modifiers on skills, but otherwise it's 
        implemented fully
    + ~~items~~
    + ~~attacks~~
    + ~~feats~~
    + ~~traits~~
    + ~~spells~~
    + ~~special abilities~~
    + etc.
+ ~~New character creation walkthrough process (CLI)~~
    + There is now functionality to create a blank character sheet in 
    both the module and the CLI, but it's not interactive; that's good 
    enough for me, as most "interactive" processes would be much better 
    served in a gui.
+ ~~Character sheet JSON format enforcement~~
    + ~~This is partially done with the Character class, but I'll 
    eventually have classes for other complex objects within the 
    character, like items, attacks, spells, etc. Makes it easier to 
    import json; just grab values if they're there, if not use the 
    defaults, and for extra values just ignore them.~~ this is now 
    pretty much finished, nearly everything is an object
+ ~~add ability modifiers (for temp increases/damage)~~
+ ~~rework hp:~~
    + ~~add wounds, temp hp, temporary max hp increases~~
    + ~~essentially make current hp a calculated value~~
    + I'm not doing either of these, but I am adding nonlethal damage
+ add full armor class components
+ expand on attacks and armor class:
    + display all modifiers
    + show the rolls and modifiers for hits and damage
    + track enhancement bonus / masterwork status
    + ~~(AC) show touch/flat footed and all the modifiers~~
+ implement spells like equipment and attacks:
    + ~~spells get tracked in the character.spells list~~
    + damaging spells can get added to the spell attack list, like 
    weapon attacks
    + show damage, cast time, duration (if applicable)
+ ~~Refactor classes into single Character class~~
    + ~~Thinking about it more, it doesn't make sense for all of these 
    character properties to be their own classes; their constructors 
    and methods could just be Character() methods. It would greatly 
    simplify a lot of the structure of this package.~~ - complete
+ ~~Add name enforcement for list properties~~
+ Add tests:
    + `add_*` methods
    + `update_*` methods
    + `get_*` methods
