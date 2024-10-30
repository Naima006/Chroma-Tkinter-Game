class Difficulty:
    def __init__(self, label, timeleft, difficulty_multiplier, colors):
        self.label = label
        self.timeleft = timeleft
        self.difficulty_multiplier = difficulty_multiplier #score multiplier
        self.colors = colors