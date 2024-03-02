import math


class Image:

    colors = {"white": "\033[97m",
              "red": "\033[31m",
              "bright red": "\033[91m",
              "green": "\033[32m",
              "yellow": "\033[33m",
              "blue": "\033[34m",
              "magenta": "\033[35m",
              "cyan": "\033[36m",
              "grey": "\033[37m",
              "dark grey": "\033[90m",
              "bright green": "\033[92m",
              }

    reset = "\033[39m"

    def __init__(self):
        self.rules = {}
        self.symb = "#" #█
        self.color = "\033[91m"
        self.fn = sample_fn

    def set_color(self, color):

        self.color = self.colors[color]

    def set_precise_color(self, col):
        self.color = col

    def set_fn(self, fn):
        self.fn = fn

    def __str__(self):
        return self.color + "y = " + str(self.fn) + "\033[97m"

    def compute_rules(self, values: dict, f, variables: dict):
        """
        Basically, goes through all the possible x values,
        and adds to the rules whichever y values have to be filled
        """
        self.rules = {}

        # Store num of successfully calculated values
        successful = 0


        # Init. values
        variables["x"] = values["origin"][0]
        try:
            successful += 1
            y1 = f(0, self.fn.calculate(variables))[0]
        except:
            successful = 0
            y1 = -5

        # Go through all the possible x values
        for i in range(values["width"]):

            variables["x"] += values["cell_w"]
            try:
                successful += 1
                y2 = f(0, self.fn.calculate(variables))[0]
            except:
                successful = 0
                y2 = -5

            self.rules[i] = []
            # If the y value can be displayed, add it to the dictionary
            if successful > 1:
                for j in range(max(min(y1, y2), 0), min(max(y1, y2), values["height"]-1) + 1):
                    self.rules[i].append(j)

            y1 = y2


def sample_fn(x):
    return math.sqrt(abs(1-x**2))
