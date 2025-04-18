class Skill:
    # skill could be use
    def __init__(self, name, power, cost):
        self.name = name
        self.power = power
        self.cost = cost

    # how many damage could be made
    def apply(self, user, target):
        damage = max(0, user.attack + self.power - target.defense)
        target.take_damage(damage)
        return damage


class Character:
    # def of a character
    def __init__(self, name, max_hp, attack, defense, skills):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.skills = skills

    # alive or not
    def is_alive(self):
        return self.current_hp > 0

    # how many damage receive
    def take_damage(self, amount):
        self.current_hp = max(0, self.current_hp - amount)
        
    # display character status
    def display_status(self):
        print(f"{self.name}: HP {self.current_hp}/{self.max_hp}")
        
    # display available skills
    def display_skills(self):
        print(f"\n{self.name}'s Skills:")
        for i, skill in enumerate(self.skills):
            print(f"{i+1}. {skill.name} (Power: {skill.power}, Cost: {skill.cost})")


class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 0
        
    def start(self):
        print(f"\n--- Battle Start: {self.player.name} vs {self.enemy.name} ---\n")
        
        while self.player.is_alive() and self.enemy.is_alive():
            self.turn += 1
            print(f"\n--- Turn {self.turn} ---")
            
            # Display status
            self.player.display_status()
            self.enemy.display_status()
            
            # Player's turn
            self.player_turn()
            
            # Check if enemy is defeated
            if not self.enemy.is_alive():
                print(f"\n{self.enemy.name} has been defeated!")
                break
                
            # Enemy's turn
            self.enemy_turn()
            
            # Check if player is defeated
            if not self.player.is_alive():
                print(f"\n{self.player.name} has been defeated!")
                break
        
        print("\n--- Battle End ---")
        if self.player.is_alive():
            print(f"{self.player.name} wins!")
        else:
            print(f"{self.enemy.name} wins!")
    
    def player_turn(self):
        print(f"\n{self.player.name}'s turn!")
        self.player.display_skills()
        
        while True:
            try:
                choice = int(input("\nChoose a skill (number): ")) - 1
                if 0 <= choice < len(self.player.skills):
                    selected_skill = self.player.skills[choice]
                    damage = selected_skill.apply(self.player, self.enemy)
                    print(f"{self.player.name} used {selected_skill.name} and dealt {damage} damage to {self.enemy.name}!")
                    break
                else:
                    print("Invalid skill number. Try again.")
            except ValueError:
                print("Please enter a number.")
    
    def enemy_turn(self):
        print(f"\n{self.enemy.name}'s turn!")
        # Simple AI: enemy randomly selects a skill
        import random
        selected_skill = random.choice(self.enemy.skills)
        damage = selected_skill.apply(self.enemy, self.player)
        print(f"{self.enemy.name} used {selected_skill.name} and dealt {damage} damage to {self.player.name}!")


# Example usage
def main():
    # Create skills
    slash = Skill("Slash", 5, 0)
    fireball = Skill("Fireball", 8, 3)
    heal = Skill("Heal", -5, 2)  # Negative power for healing
    
    # Create player and enemy
    player = Character("Hero", 50, 10, 5, [slash, fireball, heal])
    enemy = Character("Goblin", 30, 8, 3, [Skill("Bite", 4, 0), Skill("Scratch", 3, 0)])
    
    # Start battle
    battle = Battle(player, enemy)
    battle.start()


if __name__ == "__main__":
    main()
