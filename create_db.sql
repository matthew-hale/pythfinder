CREATE TYPE ability AS ENUM (
    'strength',
    'dexterity',
    'constitution',
    'intelligence',
    'wisdom',
    'charisma'
);

CREATE TYPE bonus AS ENUM (
    'alchemical',
    'armor',
    'circumstance',
    'competence',
    'deflection',
    'dodge',
    'enhancement',
    'inherent',
    'insight',
    'luck',
    'morale',
    'natural armor',
    'profane',
    'racial',
    'resistance',
    'sacred',
    'shield',
    'size',
    'trait'
);

CREATE TABLE characters (
    name text PRIMARY KEY, 
    race text NOT NULL,
    class text NOT NULL,
    level integer CHECK (level > 0) NOT NULL,
    gold numeric CHECK (gold >= 0.00) DEFAULT 0.00,
    max_health integer CHECK (max_health > 0) NOT NULL,
    base_attack_bonus integer DEFAULT 1
);

CREATE TABLE bonuses (
    name bonus PRIMARY KEY,
    is_self_stackable boolean NOT NULL
);

INSERT INTO bonuses VALUES ('alchemical', false);
INSERT INTO bonuses VALUES ('armor', false);
INSERT INTO bonuses VALUES ('circumstance', true);
INSERT INTO bonuses VALUES ('competence', false);
INSERT INTO bonuses VALUES ('deflection', false);
INSERT INTO bonuses VALUES ('dodge', true);
INSERT INTO bonuses VALUES ('enhancement', false);
INSERT INTO bonuses VALUES ('inherent', false);
INSERT INTO bonuses VALUES ('insight', false);
INSERT INTO bonuses VALUES ('luck', false);
INSERT INTO bonuses VALUES ('morale', false);
INSERT INTO bonuses VALUES ('natural armor', false);
INSERT INTO bonuses VALUES ('profane', false);
INSERT INTO bonuses VALUES ('racial', true);
INSERT INTO bonuses VALUES ('resistance', false);
INSERT INTO bonuses VALUES ('sacred', false);
INSERT INTO bonuses VALUES ('shield', false);
INSERT INTO bonuses VALUES ('size', false);
INSERT INTO bonuses VALUES ('trait', false);

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

-- Bonuses that come from traits will reference traits by name
CREATE TABLE trait_bonuses (
    name text references traits(name),
    description text DEFAULT '',
    is_conditional boolean NOT NULL,
    bonus_value integer DEFAULT 1,
    bonus_type bonus DEFAULT 'trait'
);

CREATE TABLE feats (
    name text PRIMARY KEY,
    description text DEFAULT '',
    is_stackable boolean DEFAULT false,
    has_bonus boolean DEFAULT false
);

CREATE TABLE inventory (
    character text references characters(name),
    name text references items(name),
    description text DEFAULT '',
    unit_weight numeric(10,1) DEFAULT 0
    count integer CHECK (count > 0) DEFAULT 1,
    is_camp boolean DEFAULT false,
    is_carrying boolean DEFAULT true,
    PRIMARY KEY(character, name)
);

CREATE TABLE character_traits (
    character text references characters(name),
    trait_name text references traits(name),
    count integer CHECK (count >= 1) DEFAULT 1
);

CREATE TABLE character_feats (
    character text references characters(name),
    feat_name text references feats(name),
    count integer CHECK (count >= 1) DEFAULT 1
);

