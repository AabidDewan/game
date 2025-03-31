class Move:
    def __init__(self, name, damage=0):
        self.name = name
        self.damage = damage

    def __str__(self):
        return self.name + " (Damage: " + str(self.damage) + ")"

