# Initial (Startup Requirements)

## Classes

### Creature Class

#### Variables of Interest

| var name | data type | info |
|---|----|---|
|name|str|name of creature|
|size|named tuple|creature size-type (tiny to colossal) as int|
|type|str|undead,celestial,etc...|
|alignment|tuple|{(lawful,neutral,chaotic),(good,neutral,evil)}|
|AC|int|armor class of creature|
|Max HP|int|max hitpoints of creature|
|Current HP|int|current hitpoints of creature|
|Speed|int|ft movable by creature|
|Attributes|class|Strength,Dex,Con,Int,Wis,Cha|
|Saving Throws|static set|derived from proficiency and attributes|
|Skills|static set|perception,investigation,etc. derived from attributes and proficiency|
|Resistances|list str|resistances to damage types|
|Sulnerabilities|list str|vulnerabilities to damage types|
|Senses|list str|dark vision,etc.|
|Languages|list str|common,etc.|

#### Possible Functions

### Monster <- Creature
#### Variables of Interest
#### Possible Functions

### Character <- Creature
#### Variables of Interest
#### Possible Functions

### Player <- Character
#### Variables of Interest
#### Possible Functions

### Non-Player <- Character, Monster
#### Variables of Interest
#### Possible Functions