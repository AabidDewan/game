from Move import Move

class Character:
    def __init__(self,
                 name,
                 age,
                 gender,
                 health=100,
                 speed=50,
                 strength=50,
                 durability=50,
                 ability=None,
                 is_enemy=False,
                 db=None,
                 user_id=None):
        self.name = name
        self.age = age
        # The character is male if the user types 1, female if 2
        if gender == 1:
            self.gender = "male"
        else:
            self.gender = "female"
        self.health = health

        # Base stats
        self.base_speed = speed
        self.base_strength = strength
        self.base_durability = durability

        # Current stats
        self.speed = speed
        self.strength = strength
        self.durability = durability

        # DB integration
        self.db = db
        self.user_id = user_id

        self.ability = ability  
        self.is_enemy = is_enemy

        # The starting moves for the character are Punch and Steal
        self.moves = [Move("Punch", 25), Move("Steal", 0)]

    def __str__(self):
        ab_name = self.ability.name if self.ability is not None else "None"
        return ("Name: " + self.name + "  Health: " + str(self.health) +
                "  Speed: " + str(self.speed) + "  Strength: " + str(self.strength) +
                "  Durability: " + str(self.durability) + "  Ability: " + ab_name)

    def use_ability(self):
        if self.ability is not None:
            if (not self.ability.active) and (not self.ability.in_penalty):
                self.ability.activate()
                if self.ability.stat_target == "speed":
                    self.speed = self.base_speed + self.ability.boost_value
                elif self.ability.stat_target == "strength":
                    self.strength = self.base_strength + self.ability.boost_value
                elif self.ability.stat_target == "durability":
                    self.durability = self.base_durability + self.ability.boost_value
            else:
                print("The ability is already active or the character is in a penalty.")
        else:
            print("There is no ability to use.")

    def update_ability(self):
        # Enemies do not receive penalties, only the player
        if self.ability is not None and not self.is_enemy:
            penalty_started = self.ability.update()
            if penalty_started:
                if self.ability.stat_target == "speed":
                    self.speed = self.base_speed - self.ability.penalty_value
                elif self.ability.stat_target == "strength":
                    self.strength = self.base_strength - self.ability.penalty_value
                elif self.ability.stat_target == "durability":
                    self.durability = self.base_durability - self.ability.penalty_value

            # Once everything is off/over, restore base stats
            if (not self.ability.active) and (not self.ability.in_penalty):
                if self.ability.stat_target == "speed":
                    self.speed = self.base_speed
                elif self.ability.stat_target == "strength":
                    self.strength = self.base_strength
                elif self.ability.stat_target == "durability":
                    self.durability = self.base_durability

    def steal_ability(self, enemy):
        if enemy.health <= 0 and enemy.ability is not None:
            # Record the borrow in the database
            if self.db and self.user_id:
                item = self.db.get_item_by_name(enemy.ability.name)
                try:
                    self.db.borrow_item(self.user_id, item["id"])
                except ValueError as e:
                    print(f"Could not steal: {e}")
                    return

            # Then perform the in-memory steal
            print(f"{self.name} steals {enemy.name}'s ability: {enemy.ability.name}")
            enemy.ability.active = False
            enemy.ability.in_penalty = False
            self.ability = enemy.ability
            self.moves.append(Move(self.ability.name, 0))
            enemy.ability = None
        else:
            print("You cannot steal the enemy's ability right now.")
