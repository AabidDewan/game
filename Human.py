class Human:
    def __init__(self, name, age, gender, health, speed, strength, durability, ability):
        self.__name = name
        self.__age = age
        self.__gender = gender
        self.__health = health
        self.__speed = speed
        self.__strength = strength
        self.__durability = durability
        self.__ability = ability
        self.inventory = {}

    def name(self):
        print("My name is", self.__name)

    def age(self):
        print("My age is", self.__age)

    def gender(self):
        if self.__gender == 1:
            print("I am a male")
        elif self.__gender == 2:
            print("I am a female")
        
    def health(self):
        print("Health:", self.__health)

    def speed(self):
        print("Speed:", self.__speed)

    def strength(self):
        print("Strength:", self.__strength)

    def durability(self):
        print("Durability:", self.__durability)

    def ability(self):
        print("Ability:", self.__ability)

    # New methods for managing an inventory:
    def add_to_inventory(self, item, quantity=1):
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity
        print(f"Added {quantity} {item}(s) to inventory.")

    def remove_from_inventory(self, item, quantity=1):
        if item not in self.inventory:
            print("Item not in inventory.")
            return
        if quantity >= self.inventory[item]:
            del self.inventory[item]
            print(f"Removed {item} from inventory.")
        else:
            self.inventory[item] -= quantity
            print(f"Removed {quantity} {item}(s) from inventory.")

    def list_inventory(self):
        if not self.inventory:
            print("Inventory is empty.")
        else:
            for item, qty in self.inventory.items():
                print(f"{item}: {qty}")


