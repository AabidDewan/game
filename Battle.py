import random
from Move import Move

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        if self.player.speed >= self.enemy.speed:
            self.player_turn = True
        else:
            self.player_turn = False

    def enemy_moves(self):
        if self.enemy.ability is not None:
            ab_move = Move(self.enemy.ability.name, 0)
        else:
            ab_move = Move("No Ability", 0)
        punch_move = Move("Punch", 25)
        return [ab_move, punch_move]

    def player_moves(self):
        return self.player.moves

    def player_attack(self, move):
        #Using the random module, the super speed enemy has a 50% change to dodge the attack 
        if (self.enemy.ability is not None and self.enemy.ability.name == "Super Speed" and 
            self.enemy.ability.active):
            if random.random() < 0.5:
                print(self.enemy.name + " has dodged the attack with Super Speed!")
                return
        #Using the random module the player has a 50% chance to miss their attack agaisnt the super speed enemy, also if the player is under the speed penalty, they also have a 50% chance of missing thir attack
        if (self.player.ability is not None and self.player.ability.name == "Super Speed" and 
            self.player.ability.in_penalty):
            if random.random() < 0.5:
                print(self.player.name + " missed the attack due to the Super Speed penalty!")
                return

        #Damage for the punch move, if the super strength abiltiy is active, the punch move does 34 daamge, otherwise it does 25 damage
        if move.name == "Punch":
            if (self.player.ability is not None and self.player.ability.name == "Super Strength" and 
                self.player.ability.active):
                damage = 34
            else:
                bonus = 0
                if (self.player.ability is not None and self.player.ability.name == "Super Strength" and 
                    self.player.ability.active):
                    bonus = self.player.strength - self.player.base_strength
                damage = move.damage + bonus
        else:
            damage = move.damage

        self.enemy.health = self.enemy.health - damage
        print(self.player.name + " uses " + move.name + " dealing " + str(damage) + " damage.")
        print(self.enemy.name + " has " + str(self.enemy.health) + " health left.")

    def enemy_attack(self):
        #If the player has super speed ability acitvated, they have a 50% chance to dodge the enemies attack
        if (self.player.ability is not None and self.player.ability.name == "Super Speed" and 
            self.player.ability.active):
            if random.random() < 0.5:
                print(self.player.name + " has dodged the attack with their Super Speed!")
                return

        #The enemy turns on their ability at the start of the battle
        if self.enemy.health > 0:
            if self.enemy.ability is not None and not hasattr(self.enemy, 'ability_used'):
                print(self.enemy.name + " activates " + self.enemy.ability.name)
                self.enemy.use_ability()
                self.enemy.ability_used = True
            #since the ability has now been turned on at the start, the next moves from the enemy will be a loop of punches
            #if the enemy is the super strength enemy they wil do 34 damag,e otherwise they will do 20 damage
            else:
                punch_move = self.enemy_moves()[1]
                if (self.enemy.ability is not None and self.enemy.ability.name == "Super Strength" and 
                    self.enemy.ability.active):
                    damage = 34
                else:
                    bonus = 0
                    if (self.enemy.ability is not None and self.enemy.ability.name == "Super Strength" and 
                        self.enemy.ability.active):
                        bonus = self.enemy.strength - self.enemy.base_strength
                    damage = punch_move.damage + bonus
                self.player.health = self.player.health - damage
                print(self.enemy.name + " attacks with Punch dealing " + str(damage) + " damage.")
                print(self.player.name + " has " + str(self.player.health) + " health left.")

    def start_battle(self):
        print("Battle begins: " + self.player.name + " vs. " + self.enemy.name)
        #this while loop runs as long as the enemy and platyer have a health greater than zero, it allows the player to choose theur move and/or deactivate their active ability. 
        while self.player.health > 0 and self.enemy.health > 0:
            if self.player_turn:
                self.player_turn_action()
                self.player.update_ability()
            else:
                self.enemy_attack()
            self.player_turn = not self.player_turn
            #print("-----")
        if self.player.health <= 0:
            print(self.enemy.name + " has won!")
        elif self.enemy.health <= 0:
            print(self.player.name + " has won!")
            self.allow_steal_ability()

    #Displays character's moves, includes all logic for moving, stealing abilites, activating abilites, turning off abilities. 
    def player_turn_action(self):
        print("Your moves:")
        moves = self.player_moves()
        for i in range(len(moves)):
            print(str(i + 1) + ". " + moves[i].name)
        try:
            choice = int(input("Enter the number of your move: ")) - 1
        except:
            print("Invalid input.")
            self.player_turn_action()
            return
        if choice >= 0 and choice < len(moves):
            selected = moves[choice]
            if selected.name == "Steal":
                if self.enemy.health <= 0:
                    self.player.steal_ability(self.enemy)
                else:
                    print("Enemy is still alive cannot steal ability.")
            elif (selected.name == "Super Speed" or 
                  selected.name == "Super Strength" or 
                  selected.name == "Super Durability"):
                self.player.use_ability()
            else:
                self.player_attack(selected)
        else:
            print("Invalid move.")
            self.player_turn_action()

        if self.player.ability is not None and self.player.ability.active:
            remaining = self.player.ability.get_turns_left()
            print(self.player.ability.name + " is active. Turns remaining: " + str(remaining))
            try:
                toggle = int(input("Turn off ability? (Type 1 for Yes, Type 2 for No): "))
            except:
                toggle = 2
            if toggle == 1:
                self.player.ability.toggle_off()
                if self.player.ability.stat_target == "speed":
                    self.player.speed = self.player.base_speed
                elif self.player.ability.stat_target == "strength":
                    self.player.strength = self.player.base_strength
                elif self.player.ability.stat_target == "durability":
                    self.player.durability = self.player.base_durability
            else:
                print("Ability remains active.")

    #the player can steal the enemies move
    def allow_steal_ability(self):
        if self.enemy.health <= 0 and self.enemy.ability is not None:
            try:
                choice = int(input("Steal enemy's ability? (Type 1 for Yes, Type 2 for No): "))
            except:
                choice = 2
            if choice == 1:
                self.player.steal_ability(self.enemy)
                print("Ability stolen: " + self.player.ability.name)
            else:
                print("Ability not stolen.")

