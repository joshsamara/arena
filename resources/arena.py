import random
from common import *
from fight import *

def goto_arena(character):
    clear()
    print "Welcome to the:"
    print color("""
     _
    / \\   _ __ ___ _ __   __ _
   / _ \\ | '__/ _ \\ '_ \\ / _` |
  / ___ \\| | |  __/ | | | (_| |
 /_/   \\_\\_|  \\___|_| |_|\\__,_|
 """, "red")
    character.print_useful()
    arena_options = [make_option('Fight!', 'F', time=1, hp='?'),
                     make_option('Return to Town', 'T')]

    print nav_menu(arena_options)

    val = get_val("ft")

    clear()
    if val == "f":
        fight(character)
    elif val == "t":
        character.move("town", False)
    else:
        character.save_prompt()
        print "ERROR IN ARENA SELECT"
    return
        

def fight(character):
    if character.requires(0, 1):
        character.time_pass(1)
        enemy = Enemy(pick_diff(character.lvl))
        battle(character, enemy)
    character.move("town")
    return

def victory(character, enemy):
    print "You win!"
    character.stat("xp", enemy.calc_exp())
    character.stat("gold", enemy.calc_gold())
    character.check_lvlup()
    character.move("town")
    return

def battle(character, enemy, message="\n>" * 4):
    battle_display(character, enemy, message)
    val = get_val("ar")
    clear()
    if val == "a":
        enemy, message = attack(character, enemy)
        if character.not_dead():
            if enemy.not_dead():
                battle(character, enemy, message)
            else:
                victory(character, enemy)
        else:
            print "Error in battle"
    elif val == "r":
        character.move("town")
    else:
        character.save_prompt()
        raise Exception ("ERROR IN BATTLE SELECT")
    return

def battle_display(character, enemy, message):
    print "-" * 40
    print "Enemy: %s" % enemy.type
    print "Level: %s" % enemy.lvl
    ticks = min(
        int(math.ceil(enemy.hp / (enemy.lvl * 250.0) * 25.0)),
        25)
    healthbar = color(" " * ticks, "redh") + " " * (25 - ticks)
    print "HP: [%s]" % healthbar
    print "-" * 40
    print message
    print_bar(2)
    print "Options:"
    print "Attack!                   (A)"
    print "Run!                      (R)"
    print_bar(2)
    print "\n"
    print "-" * 40
    your_ticks = min(
        int(math.ceil(float(character.hp) / character.vit * 25.0)),
        25)
    your_healthbar = color(" " * your_ticks, "greenh") + " " * (25 - your_ticks)
    print "You:"
    print "Level: %s" % character.lvl
    print "HP: [%s] %s/%s" % (your_healthbar, character.hp, character.vit)
    print "-" * 40
    return

def attack(character, enemy):
    my_damage = character.damage_calc()
    enemy_damage = enemy.damage_calc()
    damage_to_me = character.damage_reduce(enemy_damage)
    damage_to_enemy = enemy.damage_reduce(my_damage)
    character.hp -= damage_to_me
    character.hp = max(character.hp, 0)  # SAFEGAURD AGAINST NEGATIVE HP
    enemy.hp -= damage_to_enemy
    enemy.hp = max(enemy.hp, 0)
    you_deal = color("You deal:    %s damage", "green") % damage_to_enemy
    enemy_deal = color("Enemy deals: %s damage", "red") % damage_to_me
    message = """
>
> %s
> %s
> """ % (you_deal, enemy_deal)
    return enemy, message