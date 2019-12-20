CREATE TYPE alignment AS ENUM (
    'LG',
    'LN',
    'LE',
    'NG',
    'NN',
    'NE',
    'CG',
    'CN',
    'CE'
);

CREATE TYPE ability AS ENUM (
    'strength',
    'dexterity',
    'constitution',
    'intelligence',
    'wisdom',
    'charisma'
);

CREATE TYPE skill AS ENUM (
    'Acrobatics',
    'Appraise',
    'Bluff',
    'Climb',
    'Craft',
    'Diplomacy',
    'Disable Device',
    'Disguise',
    'Escape Artist',
    'Fly',
    'Handle Animal',
    'Heal',
    'Intimidate',
    'Knowledge (arcana)',
    'Knowledge (dungeoneering)',
    'Knowledge (engineering)',
    'Knowledge (geography)',
    'Knowledge (history)',
    'Knowledge (local)',
    'Knowledge (nature)',
    'Knowledge (nobility)',
    'Knowledge (planes)',
    'Knowledge (religion)',
    'Linguistics',
    'Perception',
    'Perform',
    'Profession',
    'Ride',
    'Sense Motive',
    'Sleight of Hand',
    'Spellcraft',
    'Stealth',
    'Survival',
    'Swim',
    'Use Magic Device'
);

CREATE TABLE character (
    name text PRIMARY KEY, 
    race text NOT NULL,
    class text NOT NULL,
    alignment alignment NOT NULL,
    level integer CHECK (level > 0) NOT NULL,
    gold numeric CHECK (gold >= 0.00) DEFAULT 0.00,
    max_health integer CHECK (max_health > 0) NOT NULL,
    base_attack_bonus integer DEFAULT 1
);

CREATE TABLE inventory (
    character text references characters(name),
    name text NOT NULL,
    description text DEFAULT '',
    unit_weight numeric(10,1) DEFAULT 0,
    count integer CHECK (count > 0) DEFAULT 1,
    is_camp boolean DEFAULT false,
    is_carrying boolean DEFAULT true,
    PRIMARY KEY(character, name)
);

CREATE TABLE character_ability (
    character text PRIMARY KEY references characters(name),
    strength int CHECK (strength > 0 AND strength < 99) DEFAULT 10,
    dexterity int CHECK (dexterity > 0 AND dexterity < 99) DEFAULT 10,
    constitution int CHECK (constitution > 0 AND constitution < 99) DEFAULT 10,
    intelligence int CHECK (intelligence > 0 AND intelligence < 99) DEFAULT 10,
    wisdom int CHECK (wisdom > 0 AND wisdom < 99) DEFAULT 10,
    charisma int CHECK (charisma > 0 AND charisma < 99) DEFAULT 10
);

CREATE TABLE skill (
    name skill PRIMARY KEY,
    description text DEFAULT '',
    use_untrained boolean NOT NULL,
    modifier ability NOT NULL,
    ac_penalty boolean NOT NULL
);

INSERT INTO skill VALUES ('Acrobatics', '', true, 'dexterity', true);
INSERT INTO skill VALUES ('Appraise', '', true, 'intelligence', false);
INSERT INTO skill VALUES ('Bluff', '', true, 'charisma', false);
INSERT INTO skill VALUES ('Climb', '', true, 'strength', true);
INSERT INTO skill VALUES ('Craft', '', true, 'intelligence', false);
INSERT INTO skill VALUES ('Diplomacy', '', true, 'charisma', false);
INSERT INTO skill VALUES ('Disable Device', '', false, 'dexterity', true);
INSERT INTO skill VALUES ('Disguise', '', true, 'charisma', false);
INSERT INTO skill VALUES ('Escape Artist', '', true, 'dexterity', true);
INSERT INTO skill VALUES ('Fly', '', true, 'dexterity', true);
INSERT INTO skill VALUES ('Handle Animal', '', false, 'charisma', false);
INSERT INTO skill VALUES ('Heal', '', true, 'wisdom', false);
INSERT INTO skill VALUES ('Intimidate', '', true, 'charisma', false);
INSERT INTO skill VALUES ('Knowledge (arcana)', '', false, 'intelligence', false);
INSERT INTO skill VALUES ('Knowledge (dungeoneering)', '', false, 'intelligence', false);
INSERT INTO skill VALUES ('Knowledge (engineering)', '', false, 'intelligence', false);
INSERT INTO skill VALUES ('Knowledge (geography)', '', false, 'intelligence', false);
INSERT INTO skill VALUES ('Knowledge (history)', '', false, 'intelligence', false);
INSERT INTO skill VALUES ('Knowledge (local)', '', false, 'intelligence', false);
INSERT INTO skill VALUES ('Knowledge (nature)', '', false, 'intelligence', false);
INSERT INTO skill VALUES ('Knowledge (nobility)', '', false, 'intelligence', false);
INSERT INTO skill VALUES ('Knowledge (planes)', '', false, 'intelligence', false);
INSERT INTO skill VALUES ('Knowledge (religion)', '', false, 'intelligence', false);
INSERT INTO skill VALUES ('Linguistics', '', false, 'intelligence', false);
INSERT INTO skill VALUES ('Perception', '', true, 'wisdom', false);
INSERT INTO skill VALUES ('Perform', '', true, 'charisma', false);
INSERT INTO skill VALUES ('Profession', '', false, 'wisdom', false);
INSERT INTO skill VALUES ('Ride', '', true, 'dexterity', true);
INSERT INTO skill VALUES ('Sense Motive', '', true, 'wisdom', false);
INSERT INTO skill VALUES ('Sleight of Hand', '', false, 'dexterity', true);
INSERT INTO skill VALUES ('Spellcraft', '', false, 'intelligence', false);
INSERT INTO skill VALUES ('Stealth', '', true, 'dexterity', true);
INSERT INTO skill VALUES ('Survival', '', true, 'wisdom', false);
INSERT INTO skill VALUES ('Swim', '', true, 'strength', true);
INSERT INTO skill VALUES ('Use Magic Device', '', false, 'charisma', false);

CREATE TABLE character_skill (
    character text references characters(name),
    name text references skills(name),
    ranks integer CHECK (ranks >= 0) DEFAULT 0,
    is_class boolean DEFAULT false,
    profession_or_craft_type text DEFAULT ''
);

-- Traits are just names and descriptions, but can have multiple bonuses

CREATE TABLE trait (
    name text PRIMARY KEY,
    description text DEFAULT ''
);

CREATE TABLE character_trait (
    character text references characters(name),
    name text references traits(name),
    PRIMARY KEY(character, name)
);

CREATE TABLE feat (
    name text PRIMARY KEY,
    description text DEFAULT '',
    is_stackable boolean DEFAULT false
);

CREATE TABLE character_feat (
    character text references characters(name),
    name text references feats(name),
    count integer CHECK (count >= 1) DEFAULT 1,
    PRIMARY KEY(character, name)
);

CREATE FUNCTION feat_stack_check() RETURNS trigger AS $stack$
    BEGIN
        IF NEW.count > 1 AND (SELECT is_stackable FROM feats WHERE NEW.name = feat.name) IS TRUE THEN
            RAISE EXCEPTION 'this feat is not stackable';
        END IF;
        RETURN NEW;
    END;
$stack$ LANGUAGE plpgsql;

CREATE TRIGGER feat_stack_check BEFORE INSERT OR UPDATE ON character_feat
    FOR EACH ROW EXECUTE PROCEDURE feat_stack_check();

-- Demo data

-- Qofin Parora, new Carrion Crown character
INSERT INTO character VALUES (
    'Qofin Parora',
    'Half-elf',
    'Fighter',
    'NE',
    1,
    0.00,
    13,
    1
);

-- Ability scores
INSERT INTO character_abilitie VALUES ('Qofin Parora', 17, 16, 16, 13, 10, 11);

-- Skills
INSERT INTO character_skill VALUES ('Qofin Parora', 'Acrobatics', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Appraise', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Bluff', 0, true, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Climb', 0, true, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Craft', 1, true, 'Weapons');
INSERT INTO character_skill VALUES ('Qofin Parora', 'Diplomacy', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Disable Device', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Disguise', 0, true, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Escape Artist', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Fly', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Handle Animal', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Heal', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Intimidate', 1, true, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Knowledge (arcana)', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Knowledge (dungeoneering)', 0, true, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Knowledge (engineering)', 0, true, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Knowledge (geography)', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Knowledge (history)', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Knowledge (local)', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Knowledge (nature)', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Knowledge (nobility)', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Knowledge (planes)', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Knowledge (religion)', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Linguistics', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Perception', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Perform', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Profession', 1, true, 'smuggler');
INSERT INTO character_skill VALUES ('Qofin Parora', 'Ride', 0, true, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Sense Motive', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Sleight of Hand', 1, true, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Spellcraft', 0, false, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Stealth', 1, true, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Survival', 1, true, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Swim', 0, true, DEFAULT);
INSERT INTO character_skill VALUES ('Qofin Parora', 'Use Magic Device', 0, false, DEFAULT);

-- Traits

INSERT INTO trait VALUES ('On the Payroll', 'Benefit: You begin play with an additional 150 gp in starting wealth.');
INSERT INTO trait VALUES ('Ordinary','The only thing extraordinary about your appearance is its ordinariness. You carry yourself in an understated way, and many people who see your face soon forget it. Benefit: You gain a +4 trait bonus on Stealth checks whenever you attempt to hide in a crowd.');

INSERT INTO character_trait VALUES ('Qofin Parora','On the Payroll');
INSERT INTO character_trait VALUES ('Qofin Parora','Ordinary');

-- Feats

INSERT INTO feat VALUES ('Skill Focus (Sleight of Hand)', 'Choose a skill. You are particularly adept at that skill. Benefit: You get a +3 bonus on all checks involving the chosen skill. If you have 10 or more ranks in that skill, this bonus increases to +6. Special: You can ain this feat multiple times. Its effects do not stack. Each time you take the feat, it applies to a new skill.', false);
INSERT INTO feat VALUES ('Deft Hands', 'You have exceptional manual dexterity. Benefit: You get a +2 bonus on Disable Device and Sleight of Hand skill checks. If you have 10 or more ranks in one of these skills, the bonus increases to +4 for that skill.', false);

INSERT INTO character_feat VALUES ('Qofin Parora', 'Skill Focus (Sleight of Hand)', DEFAULT);
INSERT INTO character_feat VALUES ('Qofin Parora', 'Deft Hands', DEFAULT);

-- Items

INSERT INTO inventory VALUES ('Qofin Parora', 'Tent, hanging', '', 15, 1, true, true);
INSERT INTO inventory VALUES ('Qofin Parora', 'Outfit, traveler''s', '', 5, 1, false, true);
INSERT INTO inventory VALUES ('Qofin Parora', 'Backpack, masterwork', '', 4, 1, false, true);
INSERT INTO inventory VALUES ('Qofin Parora', 'Bedroll', '', 5, 1, true, true);
INSERT INTO inventory VALUES ('Qofin Parora', 'Blanket', '', 3, 1, true, true);
INSERT INTO inventory VALUES ('Qofin Parora', 'Fishing tackle', '+1 Circumstance bonus to Survical checks to gather food aroun dbodies of water that contain fish.', 5, 1, true, true);
INSERT INTO inventory VALUES ('Qofin Parora', 'Crowbar', '+2 Circumstance bonus to Strength checks to force open a door or chest.', 5, 1, false, true);
INSERT INTO inventory VALUES ('Qofin Parora', 'Pouch, belt', 'Can hold 1/5 cubic feet of material.', 5, 1, false, true);
INSERT INTO inventory VALUES ('Qofin Parora', 'Scarf, pocketed', '+4 bonus on Sleight of Hand checks made to hide objects on your body.', 0.5, 1, false, true);
INSERT INTO inventory VALUES ('Qofin Parora', 'Flint and steel', 'Lighting a torch with a flint and steel is a full-round action.', 0, 1, false, true);
INSERT INTO inventory VALUES ('Qofin Parora', 'Pot, cooking, iron', 'Holds 1 gallon.', 2, 1, true, true);
INSERT INTO inventory VALUES ('Qofin Parora', 'Kit, mess', '', 1, 1, true, true);
INSERT INTO inventory VALUES ('Qofin Parora', 'Tools, artisan''s', '', 5, 1, true, true);
INSERT INTO inventory VALUES ('Qofin Parora', 'Rope, hemp', '', 0, 1, false, true);
