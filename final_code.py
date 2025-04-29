"""
final_code.py
Author: Yuan Zhong, Jason Feng, Yuxin Liu, William Sun
Date: 04-29-2025

A CLI turn-based RPG game featuring:
- Multiple character skills with energy cost system
- Melee and ranged attack types with accuracy mechanics
- Progressive level system with 5-9 randomly generated battles
- Story-driven gameplay with victory/defeat conditions
"""

import random
from enum import Enum

class AttackType(Enum):
    MELEE = 1
    RANGED = 2

class Skill:
    def __init__(self, name, power, cost, attack_type, accuracy=0.8):
        self.name = name
        self.power = power
        self.cost = cost
        self.attack_type = attack_type
        self.accuracy = accuracy

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
            print(f"🎉 {self.player.name} wins!")
            self.print_separator("Story Continues")
            print("You have overcome this challenge, but your journey continues...")
        else:
            print(f"💀 {self.enemy.name} wins!")
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
                        print("⚠️ Not enough energy to use this skill!")
                        continue
                    damage = selected_skill.apply(self.player, self.enemy)
                    if damage > 0:
                        self.player.cost_energy(selected_skill.cost)
                        print(f"⚔️ {self.player.name} used {selected_skill.name} and dealt {damage} damage!")
                    break
                elif choice == len(self.player.skills):
                    damage = max(0, self.player.attack - self.enemy.defense)
                    self.enemy.take_damage(damage)
                    print(f"👊 {self.player.name} performs a basic attack and deals {damage} damage!")
                    break
                elif choice == len(self.player.skills)+1:
                    self.player.defense *= 1.5
                    print(f"🛡️ {self.player.name} takes a defensive stance!")
                    break
                elif choice == len(self.player.skills)+2:
                    self.player.energy += 1
                    print(f"⏳ {self.player.name} skips turn and recovers 1 energy!")
                    break
                else:
                    print("❌ Invalid choice. Try again or type '?' for help.")
            except ValueError:
                print("❌ Please enter a valid number or '?' for help.")
    
    def enemy_turn(self):
        print(f"\n{self.enemy.name}'s turn!")
        # Enemy AI: prioritize skills it can afford
        affordable_skills = [s for s in self.enemy.skills if s.cost <= self.enemy.energy]
        if affordable_skills:
            selected_skill = random.choice(affordable_skills)
            damage = selected_skill.apply(self.enemy, self.player)
            if damage > 0:
                self.enemy.cost_energy(selected_skill.cost)
                print(f"{self.enemy.name} used {selected_skill.name} and dealt {damage} damage to {self.player.name}!")
        else:
            # Basic attack if no skills can be used
            damage = max(0, self.enemy.attack - self.player.defense)
            self.player.take_damage(damage)
            print(f"{self.enemy.name} attacks and deals {damage} damage!")

def main():
    # Create skills
    slash = Skill("Slash", 8, 2, AttackType.MELEE, 0.9)
    fireball = Skill("Fireball", 12, 4, AttackType.RANGED, 0.7)
    heal = Skill("Heal", -15, 3, AttackType.MELEE, 1.0)
    
    # Create player with backstory
    player_story = """
    You are a wandering knight on a quest to save your kingdom from darkness.
    You must survive through multiple battles to find the hidden treasure.
    """
    player = Character("Sir Lancelot", 60, 12, 6, [slash, fireball, heal], 3, player_story)
    
    # Game progression
    total_levels = random.randint(5, 9)
    current_level = 0
    
    while player.is_alive() and current_level < total_levels:
        current_level += 1
        print(f"\n=== Level {current_level}/{total_levels} ===")
        
        # Create enemy based on current level
        enemy_hp = 30 + (current_level * 5)
        enemy_attack = 6 + current_level
        enemy_defense = 3 + (current_level // 2)
        
        enemy = Character(f"Level {current_level} Goblin", enemy_hp, enemy_attack, enemy_defense,
                        [Skill("Bite", 4 + current_level, 0, AttackType.MELEE, 0.8), 
                         Skill("Stone Throw", 3 + current_level, 0, AttackType.RANGED, 0.6)], 
                        current_level // 2)
        
        # Start battle
        battle = Battle(player, enemy)
        battle.start()
        
        if player.is_alive():
            # Recover some HP and energy between battles
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
