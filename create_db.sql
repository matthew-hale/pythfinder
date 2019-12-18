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

CREATE TABLE characters (
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

CREATE TABLE character_abilities (
    character text PRIMARY KEY references characters(name),
    strength int CHECK (strength > 0 AND strength < 99) DEFAULT 10,
    dexterity int CHECK (dexterity > 0 AND dexterity < 99) DEFAULT 10,
    constitution int CHECK (constitution > 0 AND constitution < 99) DEFAULT 10,
    intelligence int CHECK (intelligence > 0 AND intelligence < 99) DEFAULT 10,
    wisdom int CHECK (wisdom > 0 AND wisdom < 99) DEFAULT 10,
    charisma int CHECK (charisma > 0 AND charisma < 99) DEFAULT 10
);

CREATE TABLE skills (
    name text PRIMARY KEY,
    description text DEFAULT '',
    use_untrained boolean NOT NULL,
    modifier ability NOT NULL,
    ac_penalty boolean NOT NULL
);

INSERT INTO skills VALUES ('Acrobatics', '', true, 'dexterity', true);
INSERT INTO skills VALUES ('Appraise', '', true, 'intelligence', false);
INSERT INTO skills VALUES ('Bluff', '', true, 'charisma', false);
INSERT INTO skills VALUES ('Climb', '', true, 'strength', true);
INSERT INTO skills VALUES ('Craft', '', true, 'intelligence', false);
INSERT INTO skills VALUES ('Diplomacy', '', true, 'charisma', false);
INSERT INTO skills VALUES ('Disable Device', '', false, 'dexterity', true);
INSERT INTO skills VALUES ('Disguise', '', true, 'charisma', false);
INSERT INTO skills VALUES ('Escape Artist', '', true, 'dexterity', true);
INSERT INTO skills VALUES ('Fly', '', true, 'dexterity', true);
INSERT INTO skills VALUES ('Handle Animal', '', false, 'charisma', false);
INSERT INTO skills VALUES ('Heal', '', true, 'wisdom', false);
INSERT INTO skills VALUES ('Intimidate', '', true, 'charisma', false);
INSERT INTO skills VALUES ('Knowledge (arcana)', '', false, 'intelligence', false);
INSERT INTO skills VALUES ('Knowledge (dungeoneering)', '', false, 'intelligence', false);
INSERT INTO skills VALUES ('Knowledge (engineering)', '', false, 'intelligence', false);
INSERT INTO skills VALUES ('Knowledge (geography)', '', false, 'intelligence', false);
INSERT INTO skills VALUES ('Knowledge (history)', '', false, 'intelligence', false);
INSERT INTO skills VALUES ('Knowledge (local)', '', false, 'intelligence', false);
INSERT INTO skills VALUES ('Knowledge (nature)', '', false, 'intelligence', false);
INSERT INTO skills VALUES ('Knowledge (nobility)', '', false, 'intelligence', false);
INSERT INTO skills VALUES ('Knowledge (planes)', '', false, 'intelligence', false);
INSERT INTO skills VALUES ('Knowledge (religion)', '', false, 'intelligence', false);
INSERT INTO skills VALUES ('Linguistics', '', false, 'intelligence', false);
INSERT INTO skills VALUES ('Perception', '', true, 'wisdom', false);
INSERT INTO skills VALUES ('Perform', '', true, 'charisma', false);
INSERT INTO skills VALUES ('Profession', '', false, 'wisdom', false);
INSERT INTO skills VALUES ('Ride', '', true, 'dexterity', true);
INSERT INTO skills VALUES ('Sense Motive', '', true, 'wisdom', false);
INSERT INTO skills VALUES ('Sleight of Hand', '', false, 'dexterity', true);
INSERT INTO skills VALUES ('Spellcraft', '', false, 'intelligence', false);
INSERT INTO skills VALUES ('Stealth', '', true, 'dexterity', true);
INSERT INTO skills VALUES ('Survival', '', true, 'wisdom', false);
INSERT INTO skills VALUES ('Swim', '', true, 'strength', true);
INSERT INTO skills VALUES ('Use Magic Device', '', false, 'charisma', false);

CREATE TABLE character_skills (
    character text references characters(name),
    name text references skills(name),
    ranks integer CHECK (ranks >= 0) DEFAULT 0,
    is_class boolean DEFAULT false,
    profession_or_craft_type text DEFAULT ''
);

-- Traits are just names and descriptions, but can have multiple bonuses

CREATE TABLE traits (
    name text PRIMARY KEY,
    description text DEFAULT ''
);

CREATE TABLE character_traits (
    character text references characters(name),
    name text references traits(name),
    PRIMARY KEY(character, name)
);

CREATE TABLE feats (
    name text PRIMARY KEY,
    description text DEFAULT '',
    is_stackable boolean DEFAULT false
);

CREATE TABLE character_feats (
    character text references characters(name),
    name text references feats(name),
    count integer CHECK (count >= 1) DEFAULT 1,
    PRIMARY KEY(character, name)
);

CREATE FUNCTION feat_stack_check() RETURNS trigger AS $stack$
    BEGIN
        IF NEW.count > 1 AND (SELECT is_stackable FROM feats WHERE NEW.name = feats.name) IS TRUE THEN
            RAISE EXCEPTION 'this feat is not stackable';
        END IF;
        RETURN NEW;
    END;
$stack$ LANGUAGE plpgsql;

CREATE TRIGGER feat_stack_check BEFORE INSERT OR UPDATE ON character_feats
    FOR EACH ROW EXECUTE PROCEDURE feat_stack_check();

-- Demo data

-- Qofin Parora, new Carrion Crown character
INSERT INTO characters VALUES (
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
INSERT INTO character_abilities VALUES ('Qofin Parora', 17, 16, 16, 13, 10, 11);

-- Skills
INSERT INTO character_skills VALUES ('Qofin Parora', 'Acrobatics', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Appraise', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Bluff', 0, true, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Climb', 0, true, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Craft', 1, true, 'Weapons');
INSERT INTO character_skills VALUES ('Qofin Parora', 'Diplomacy', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Disable Device', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Disguise', 0, true, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Escape Artist', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Fly', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Handle Animal', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Heal', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Intimidate', 1, true, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Knowledge (arcana)', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Knowledge (dungeonering)', 0, true, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Knowledge (engineering)', 0, true, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Knowledge (geography)', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Knowledge (history)', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Knowledge (local)', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Knowledge (nature)', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Knowledge (nobility)', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Knowledge (planes)', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Knowledge (religion)', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Linguistics', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Perception', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Perform', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Profession', 1, true, 'smuggler');
INSERT INTO character_skills VALUES ('Qofin Parora', 'Ride', 0, true, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Sense Motive', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Sleight of Hand', 1, true, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Spellcraft', 0, false, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Stealth', 1, true, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Survival', 1, true, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Swim', 0, true, DEFAULT);
INSERT INTO character_skills VALUES ('Qofin Parora', 'Use Magic Device', 0, false, DEFAULT);

-- Traits

-- Feats
