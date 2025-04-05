from Move import Move
from Ability import Ability

class Character:
    def __init__(self, name, age, gender, health=100, speed=50, strength=50, durability=50, ability=None, is_enemy=False):
        self.name = name
        self.age = age
        #The character is male if the user types 1 and 2 if female
        if gender == 1:
            self.gender = "male"
        else:
            self.gender = "female"
        self.health = health

        #Base stats
        self.base_speed = speed
        self.base_strength = strength
        self.base_durability = durability

        #Current stats
        self.speed = speed
        self.strength = strength
        self.durability = durability

        self.ability = ability  
        self.is_enemy = is_enemy

        #the starting moves for the character are punch and steal
        self.moves = [Move("Punch", 25), Move("Steal", 0)]

    def __str__(self):
        ab_name = self.ability.name if self.ability is not None else "None"
        return ("Name: " + self.name + " Health: " + str(self.health) +
                " Speed: " + str(self.speed) + " Strength: " + str(self.strength) +
                " Durability: " + str(self.durability) + " Ability: " + ab_name)

    def use_ability(self):
        if self.ability is not None:
            if (self.ability.active == False) and (self.ability.in_penalty == False):
                self.ability.activate()
                if self.ability.stat_target == "speed":
                    self.speed = self.base_speed + self.ability.boost_value
                elif self.ability.stat_target == "strength":
                    self.strength = self.base_strength + self.ability.boost_value
                elif self.ability.stat_target == "durability":
                    self.durability = self.base_durability + self.ability.boost_value
            else:
                print("the ability is already active or the character is in a penalty")
        else:
            print("There is no ability to use")

    def update_ability(self):
        #The enenmy should not receive any penatlys only the platyer
        if self.ability is not None and self.is_enemy == False:
            penalty_started = self.ability.update()
            if penalty_started:
                if self.ability.stat_target == "speed":
                    self.speed = self.base_speed - self.ability.penalty_value
                elif self.ability.stat_target == "strength":
                    self.strength = self.base_strength - self.ability.penalty_value
                elif self.ability.stat_target == "durability":
                    self.durability = self.base_durability - self.ability.penalty_value
            if (self.ability.active == False) and (self.ability.in_penalty == False):
                #restores stat to normal once ability is worn off / turned off
                if self.ability.stat_target == "speed":
                    self.speed = self.base_speed
                elif self.ability.stat_target == "strength":
                    self.strength = self.base_strength
                elif self.ability.stat_target == "durability":
                    self.durability = self.base_durability

    def steal_ability(self, enemy):
        if enemy.health <= 0 and enemy.ability is not None:
            print(self.name + " steals " + enemy.name + "'s ability: " + enemy.ability.name)
            enemy.ability.active = False
            enemy.ability.in_penalty = False
            self.ability = enemy.ability
            self.moves.append(Move(self.ability.name, 0))
            enemy.ability = None
        else:
            print("You cannot steal the enemy's ability. The enemy is still alive.")
