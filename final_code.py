#
#   Program Name:   final_code.py
#
#   Author(s):      Yuan Zhong, Jason Feng, Yuxin Liu, William Sun
#
#   Date:           04-29-2025
#
#   Description:
#   A CLI-based turn-based RPG game. Players control a custom character through 
#   a series of randomly generated battles with story progression. Features include:
#   - Character skills with energy and accuracy systems
#   - Melee and ranged attack types
#   - Basic and skill-based combat options
#   - Health and energy management
#   - Victory and defeat outcomes with narrative events
#

import random
from enum import Enum

#
#   Class Name:   AttackType
#
#   Description:
#   Enumeration to specify the type of an attack: melee or ranged.
#
class AttackType(Enum):
    MELEE = 1
    RANGED = 2

#
#   Class Name:   Skill
#
#   Author:      
#
#   Description:
#   Defines a combat skill, which can be offensive or healing. Includes properties 
#   such as power, energy cost, attack type, and accuracy. Applies effects during battle.
#
class Skill:
    #
    #   Function/Method Name:   __William Sun__
    #
    #   Author:      
    #
    #   Parameters:  self, name (str), power (int), cost (int), attack_type (AttackType), accuracy (float)
    #
    #   Return Value: None
    #
    #   Description:
    #   Initializes a new skill with the given attributes.
    #
    def __init__(self, name, power, cost, attack_type, accuracy=0.8):
        self.name = name
        self.power = power
        self.cost = cost
        self.attack_type = attack_type
        self.accuracy = accuracy

    #
    #   Function/Method Name:   apply
    #
    #   Author:      
    #
    #   Parameters:  self, user (Character), target (Character)
    #
    #   Return Value: Integer indicating damage dealt or healing applied
    #
    #   Description:
    #   Executes the skill's effect. If offensive, calculates and applies damage based on 
    #   attack type and target defense. If healing, restores HP. Can miss based on accuracy.
    #
    def apply(self, user, target):
        if random.random() > self.accuracy:
            print(f"{user.name}'s {self.name} missed!")
            return 0
        
        if self.power >= 0:  # Attack skill
            if self.attack_type == AttackType.MELEE:
                damage = max(0, user.attack + self.power - target.defense)
            else:  # Ranged attack
                damage = max(0, (user.attack * 0.7) + self.power - (target.defense * 0.5))
                
            target.take_damage(damage)
            return damage
        else:  # Healing skill
            healing = min(-self.power, user.max_hp - user.current_hp)
            user.current_hp += healing
            print(f"{user.name} healed for {healing} HP.")
            return -healing

#
#   Class Name:   Character
#
#   Author:      
#
#   Description:
#   Represents a game character with attributes like HP, attack, defense, energy, 
#   and skills. Supports actions like attacking, defending, healing, and status display.
#
class Character:
    def __init__(self, name, max_hp, attack, defense, skills, energy, story=""):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.skills = skills
        self.energy = energy
        self.story = story

    def is_alive(self):
        return self.current_hp > 0

    def take_damage(self, amount):
        self.current_hp = max(0, self.current_hp - amount)

    def cost_energy(self, cost):
        self.energy = max(0, self.energy - cost)

    def display_status(self):
        print(f"{self.name}: HP {self.current_hp}/{self.max_hp} | Energy: {self.energy}")

    def display_skills(self):
        print(f"\n{self.name}'s Actions:")
        print(f"1. Attack (Power: {self.attack}, Cost: 0)")
        print(f"2. Defend (Reduces damage by 50%, Cost: 0)")

        for i, skill in enumerate(self.skills):
            print(f"{i+3}. {skill.name} (Power: {skill.power}, Cost: {skill.cost}, Type: {skill.attack_type.name}, Accuracy: {skill.accuracy*100}%)")

        print(f"{len(self.skills)+3}. Skip Turn (Recover 1 energy)")

#
#   Class Name:   Battle
#
#   Author:      
#
#   Description:
#   Manages a turn-based combat loop between the player and an enemy. Handles action 
#   selection, turn order, skill usage, enemy AI, and win/loss outcomes.
#
class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 0

    def print_separator(self, title=""):
        if title:
            print(f"\n=== {title} ===")
        else:
            print("\n" + "=" * 40)

    def start(self):
        self.print_separator("Story")
        print(self.player.story)
        self.print_separator(f"Battle Start: {self.player.name} vs {self.enemy.name}")

        while self.player.is_alive() and self.enemy.is_alive():
            self.turn += 1
            self.player.energy += 1
            self.print_separator(f"Turn {self.turn}")

            self.player.display_status()
            self.enemy.display_status()

            self.player_turn()

            if not self.enemy.is_alive():
                self.print_separator(f"{self.enemy.name} Defeated")
                break

            self.enemy_turn()

            if not self.player.is_alive():
                self.print_separator(f"{self.player.name} Defeated")
                break

        self.print_separator("Battle Results")
        if self.player.is_alive():
            print(f"\U0001f389 {self.player.name} wins!")
            self.print_separator("Story Continues")
            print("You have overcome this challenge, but your journey continues...")
        else:
            print(f"\U0001f480 {self.enemy.name} wins!")
            self.print_separator("Game Over")

    def player_turn(self):
        self.print_separator(f"{self.player.name}'s Turn")
        self.player.display_status()
        self.player.display_skills()

        while True:
            try:
                choice = input("\nChoose an action (number): ")
                if choice.lower() == '?':
                    self.player.display_skills()
                    continue

                choice = int(choice) - 1
                total_options = len(self.player.skills) + 3

                if 0 <= choice < len(self.player.skills):
                    selected_skill = self.player.skills[choice]
                    if selected_skill.cost > self.player.energy:
                        print("\u26a0\ufe0f Not enough energy to use this skill!")
                        continue
                    damage = selected_skill.apply(self.player, self.enemy)
                    if damage > 0:
                        self.player.cost_energy(selected_skill.cost)
                        print(f"\u2694\ufe0f {self.player.name} used {selected_skill.name} and dealt {damage} damage!")
                    break
                elif choice == len(self.player.skills):
                    damage = max(0, self.player.attack - self.enemy.defense)
                    self.enemy.take_damage(damage)
                    print(f"\U0001f44a {self.player.name} performs a basic attack and deals {damage} damage!")
                    break
                elif choice == len(self.player.skills)+1:
                    self.player.defense *= 1.5
                    print(f"\U0001f6e1\ufe0f {self.player.name} takes a defensive stance!")
                    break
                elif choice == len(self.player.skills)+2:
                    self.player.energy += 1
                    print(f"\u23f3 {self.player.name} skips turn and recovers 1 energy!")
                    break
                else:
                    print("\u274c Invalid choice. Try again or type '?' for help.")
            except ValueError:
                print("\u274c Please enter a valid number or '?' for help.")

    def enemy_turn(self):
        print(f"\n{self.enemy.name}'s turn!")
        affordable_skills = [s for s in self.enemy.skills if s.cost <= self.enemy.energy]
        if affordable_skills:
            selected_skill = random.choice(affordable_skills)
            damage = selected_skill.apply(self.enemy, self.player)
            if damage > 0:
                self.enemy.cost_energy(selected_skill.cost)
                print(f"{self.enemy.name} used {selected_skill.name} and dealt {damage} damage to {self.player.name}!")
        else:
            damage = max(0, self.enemy.attack - self.player.defense)
            self.player.take_damage(damage)
            print(f"{self.enemy.name} attacks and deals {damage} damage!")

def main():
    #
    #   Function/Method Name:   main
    #
    #   Author:      
    #
    #   Parameters:  None
    #
    #   Return Value: None
    #
    #   Description:
    #   Initializes the game. Creates the player and generates a series of enemy battles.
    #   Handles overall game progression and final outcome based on player's survival.
    #
    slash = Skill("Slash", 8, 2, AttackType.MELEE, 0.9)
    fireball = Skill("Fireball", 12, 4, AttackType.RANGED, 0.7)
    heal = Skill("Heal", -15, 3, AttackType.MELEE, 1.0)

    player_story = """
    You are a wandering knight on a quest to save your kingdom from darkness.
    You must survive through multiple battles to find the hidden treasure.
    """
    player = Character("Sir Lancelot", 60, 12, 6, [slash, fireball, heal], 3, player_story)

    total_levels = random.randint(5, 9)
    current_level = 0

    while player.is_alive() and current_level < total_levels:
        current_level += 1
        print(f"\n=== Level {current_level}/{total_levels} ===")

        enemy_hp = 30 + (current_level * 5)
        enemy_attack = 6 + current_level
        enemy_defense = 3 + (current_level // 2)

        enemy = Character(f"Level {current_level} Goblin", enemy_hp, enemy_attack, enemy_defense,
                        [Skill("Bite", 4 + current_level, 0, AttackType.MELEE, 0.8), 
                         Skill("Stone Throw", 3 + current_level, 0, AttackType.RANGED, 0.6)], 
                        current_level // 2)

        battle = Battle(player, enemy)
        battle.start()

        if player.is_alive():
            player.current_hp = min(player.max_hp, player.current_hp + 10)
            player.energy = min(5, player.energy + 2)
            print(f"\nAfter the battle, {player.name} recovers some HP and energy!")
            player.display_status()

    if player.is_alive():
        print("\n=== Congratulations! ===")
        print("You have survived all the battles and found the hidden treasure!")
        print("Your kingdom will be saved from darkness!")
    else:
        print("\n=== Game Over ===")
        print("You failed to complete your quest...")

if __name__ == "__main__":
    main()
