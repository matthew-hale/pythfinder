CREATE TABLE characters (
    name text PRIMARY KEY, 
    race text NOT NULL,
    class text NOT NULL,
    level integer CHECK (level > 0) NOT NULL,
    max_health integer CHECK (max_health > 0) NOT NULL,
    base_attack_bonus integer DEFAULT 1
);

CREATE TABLE abilities (
    character text PRIMARY KEY references characters(name),
    strength int CHECK (strength > 0 AND strength < 99) DEFAULT 10,
    dexterity int CHECK (dexterity > 0 AND dexterity < 99) DEFAULT 10,
    constitution int CHECK (constitution > 0 AND constitution < 99) DEFAULT 10,
    intelligence int CHECK (intelligence > 0 AND intelligence < 99) DEFAULT 10,
    wisdom int CHECK (wisdom > 0 AND wisdom < 99) DEFAULT 10,
    charisma int CHECK (charisma > 0 AND charisma < 99) DEFAULT 10
);

CREATE TABLE items (
    name text PRIMARY KEY,
    description text DEFAULT '',
    unit_weight numeric(10,1) DEFAULT 0,
    bonus_value integer DEFAULT 0,
    bonus_type text DEFAULT '',
    bonus_reference text DEFAULT ''
);

CREATE TABLE traits (
    name text PRIMARY KEY,
    description text DEFAULT '',
    bonus_value integer DEFAULT 0,
    bonus_type text DEFAULT '',
    bonus_reference text DEFAULT ''
);

CREATE TABLE feats (
    name text PRIMARY KEY,
    description text DEFAULT '',
    bonus_value integer DEFAULT 0,
    bonus_type text DEFAULT '',
    bonus_reference text DEFAULT ''
);

CREATE TABLE inventory (
    character text references characters(name),
    gold numeric CHECK (gold >= 0.00) DEFAULT 0.00,
    item_name text references items(name),
    count integer CHECK (count > 0) DEFAULT 1,
    is_camp boolean DEFAULT false,
    is_carrying boolean DEFAULT true
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

INSERT INTO feats VALUES (
    'Test feat',
    'This is a test feat.',
    1,
    'skill',
    'acrobatics'
);
