class Ability:
    def __init__(self, name, stat_target, boost_value, penalty_value, active_duration, penalty_duration=2):
        self.name = name
        self.stat_target = stat_target  
        self.boost_value = boost_value
        self.penalty_value = penalty_value
        self.active_duration = active_duration 
        self.penalty_duration = penalty_duration
        self.active = False
        self.active_rounds = 0
        self.in_penalty = False
        self.penalty_rounds = 0

    def activate(self):
        self.active = True
        self.active_rounds = 0
        self.in_penalty = False
        self.penalty_rounds = 0
        print(self.name + " has been activated")

    def update(self):
        if self.active:
            self.active_rounds = self.active_rounds + 1
            if self.active_rounds >= self.active_duration:
                self.active = False
                self.in_penalty = True
                self.penalty_rounds = 0
                print(self.name + " ended automatically. The penalty has been applied.")
                return True  
            #the penalty has started
        elif self.in_penalty:
            self.penalty_rounds = self.penalty_rounds + 1
            if self.penalty_rounds >= self.penalty_duration:
                self.in_penalty = False
                print(self.name + " penalty ended.")
        return False

    def toggle_off(self):
        #When the ability is turned off manually, the penalty is not applied. 
        if self.active:
            self.active = False
            self.in_penalty = False
            self.penalty_rounds = 0
            print(self.name + " has been turned off manually. No penalty recieved.")
            return True
        return False

    def get_turns_left(self):
        if self.active:
            return self.active_duration - self.active_rounds
        else:
            return 0
