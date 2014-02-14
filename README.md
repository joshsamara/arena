##Arena

###Table of contents
1. About
2. How To
3. Game Basics 
  - Stats
  - Areas
4. Notes

###1. About

This is a Gladiator arena battle and development text based rpg game
Currently being designed and worked on by Josh Samara

###2. How To
Open a terminal and run:

`git clone https://github.com/joshsamara/arena.git ~/arena`

`cd ~/arena`

`python main.py`

The game is played from a terminal window.
You can create and load a single local save file
Most input is immediately responsive, ie takes effect 
as soon as you hit the key, unless otherwise prompted

###3. Game basics
You start the game by naming your character. Your goal is to 
train the character and fight in the arena

####Stats
Your character has the following stats
- _level_: The character level
- _xp_: Experience, needed to gain levels
- _gold_: Gold, needed for purchases
- _hp_: current life, lose all of this and you faint
- _str_: Strength, helps in battle and others
- _int_: Intelligence, helps in battle and others
- _agi_: Agility, helps in battle and others
- _luck_: Luck, helps in battle and others
- _vit_: Vitality, maximum hp possible
- _wep_: Weapon, flat damage multiplier
- _def_: Defence, a flat battle damage resistance 

####Areas
You can go to the following areas
- _Town_: Main hub, can go places and save
- _Tavern_: Bar, can train luck, work, sleep, and more
- _Library_: Can train int and more
- _Fields_:  Can train agi, str, and more
- _Blacksmith_: Can train vit, upgrade weapon and armor
- _Arena_: Can fight enemies to gain exp

###4. Notes
Game is currently incomplete:
- Not yet balanced
- Not fully tested
- No end game condition
- Needs additional documentation
