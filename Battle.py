from Move import Move

class Battle:
    def __init__(self, player, enemy, db=None, user_id=None):
        self.player = player
        self.enemy = enemy
        self.db = db
        self.user_id = user_id
        # determine who goes first based on speed
        self.player_turn = (self.player.speed >= self.enemy.speed)

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
        import random
        # dodge logic for Super Speed
        if (self.enemy.ability and self.enemy.ability.name == "Super Speed"
                and self.enemy.ability.active):
            if random.random() < 0.5:
                print(self.enemy.name + " has dodged the attack with Super Speed!")
                return

        # miss chance under penalty
        if (self.player.ability and self.player.ability.name == "Super Speed"
                and self.player.ability.in_penalty):
            if random.random() < 0.5:
                print(self.player.name + " missed the attack due to the Super Speed penalty!")
                return

        # calculate damage
        if move.name == "Punch":
            if (self.player.ability and self.player.ability.name == "Super Strength"
                    and self.player.ability.active):
                damage = 34
            else:
                bonus = 0
                if (self.player.ability and self.player.ability.name == "Super Strength"
                        and self.player.ability.active):
                    bonus = self.player.strength - self.player.base_strength
                damage = move.damage + bonus
        else:
            damage = move.damage

        self.enemy.health -= damage
        print(f"{self.player.name} uses {move.name} dealing {damage} damage.")
        print(f"{self.enemy.name} has {self.enemy.health} health left.")

    def enemy_attack(self):
        import random
        # player dodge with Super Speed
        if (self.player.ability and self.player.ability.name == "Super Speed"
                and self.player.ability.active):
            if random.random() < 0.5:
                print(self.player.name + " has dodged the attack with their Super Speed!")
                return

        # enemy activates their ability once at start
        if self.enemy.health > 0:
            if self.enemy.ability and not hasattr(self.enemy, 'ability_used'):
                print(f"{self.enemy.name} activates {self.enemy.ability.name}")
                self.enemy.use_ability()
                self.enemy.ability_used = True
            else:
                punch_move = self.enemy_moves()[1]
                if (self.enemy.ability and self.enemy.ability.name == "Super Strength"
                        and self.enemy.ability.active):
                    damage = 34
                else:
                    bonus = 0
                    if (self.enemy.ability and self.enemy.ability.name == "Super Strength"
                            and self.enemy.ability.active):
                        bonus = self.enemy.strength - self.enemy.base_strength
                    damage = punch_move.damage + bonus
                self.player.health -= damage
                print(f"{self.enemy.name} attacks with Punch dealing {damage} damage.")
                print(f"{self.player.name} has {self.player.health} health left.")

    def start_battle(self):
        print(f"Battle begins: {self.player.name} vs. {self.enemy.name}")
        while self.player.health > 0 and self.enemy.health > 0:
            if self.player_turn:
                self.player_turn_action()
                self.player.update_ability()
            else:
                self.enemy_attack()
            self.player_turn = not self.player_turn

        if self.player.health <= 0:
            print(f"{self.enemy.name} has won!")
        elif self.enemy.health <= 0:
            print(f"{self.player.name} has won!")
            self.allow_steal_ability()

    def player_turn_action(self):
        print("Your moves:")
        moves = self.player_moves()
        for i, m in enumerate(moves, start=1):
            print(f"{i}. {m.name}")
        try:
            choice = int(input("Enter the number of your move: ")) - 1
        except:
            print("Invalid input.")
            return self.player_turn_action()

        if 0 <= choice < len(moves):
            selected = moves[choice]
            if selected.name == "Steal":
                if self.enemy.health <= 0:
                    self.player.steal_ability(self.enemy)
                else:
                    print("Enemy is still alive; cannot steal ability.")
            elif selected.name in {"Super Speed", "Super Strength", "Super Durability"}:
                self.player.use_ability()
            else:
                self.player_attack(selected)
        else:
            print("Invalid move.")
            return self.player_turn_action()

        # handle toggling off ability and returning it
        if self.player.ability and self.player.ability.active:
            remaining = self.player.ability.get_turns_left()
            print(f"{self.player.ability.name} is active. Turns remaining: {remaining}")
            try:
                toggle = int(input("Turn off ability? (1=Yes, 2=No): "))
            except:
                toggle = 2

            if toggle == 1:
                # in-memory toggle
                self.player.ability.toggle_off()
                # DB return
                if self.db and self.user_id:
                    item = self.db.get_item_by_name(self.player.ability.name)
                    self.db.return_item(self.user_id, item["id"])
                # restore stat
                target = self.player.ability.stat_target
                if target == "speed":
                    self.player.speed = self.player.base_speed
                elif target == "strength":
                    self.player.strength = self.player.base_strength
                elif target == "durability":
                    self.player.durability = self.player.base_durability
            else:
                print("Ability remains active.")

    def allow_steal_ability(self):
        if self.enemy.health <= 0 and self.enemy.ability:
            try:
                choice = int(input("Steal enemy's ability? (1=Yes, 2=No): "))
            except:
                choice = 2
            if choice == 1:
                self.player.steal_ability(self.enemy)
                if self.player.ability:
                    print(f"Ability stolen: {self.player.ability.name}")
            else:
                print("Ability not stolen.")
