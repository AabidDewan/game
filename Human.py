#This class is to describe the stats of all the characters in the game
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
        print("speed:", self.__speed)

    def strength(self):
        print("Strength:", self.__strength)

    def durability(self):
        print("Durability:", self.__durability)

    def ability(self):
        print("Ability:", self.__ability)