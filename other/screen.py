if __name__ == "__main__":
    import keyinput, image, time, math, cursor, function
else:
    import other.keyinput as keyinput, other.image as image, time, math, cursor, other.function as function


scale = 0.03
class Screen:
    def __init__(self, width=0, height=0):
        # Set width and height, as specified
        self.width = width if width > 0 else get_setting("width")
        self.height = height if height > 0 else get_setting("height")

        # Create grid
        self.out = ""
        self.grid = [['–' for i in range(self.width)] for j in range(self.height)]

        # Compile original output to be projected on the screen
        self.compile_output()

        # Store variables for ratios
        self.ratio = get_setting("height_s")/get_setting("width_s")

        d = ((self.width/2)/10)*self.ratio
        self.origin = [-5, d]
        self.cell_h = 2*d / self.height
        self.cell_w = 20 / self.width

        save_setting("info", str(self.origin))

        self.images = []

        # Variable that stores all the variables for the funciotns
        self.variables = {"x": 0}


    def compile_output(self):
        """
        Create an output string, that basically joins together
        all the strings in the grid, so that it can all be outputted
        all at once
        """
        self.out = ''
        for row in self.grid:
            self.out += ''.join(row) + "\n"

    def __str__(self):
        return self.out

    def clear_screen(self, ch=" "):
        self.grid = [[ch for i in range(self.width)] for j in range(self.height)]

    def screen_prompt(self, ask: str):
        print("\033c", end='')
        print(self, end="")
        return input(ask + " ")

    def functions_prompt(self, ask: str):
        """
        Prints the main screen with the functions and variables
        """
        print("\033c", end='')
        out = "\n\nFunctions\n\n"
        for i in range(len(self.images)):
            out += str(i+1) + ". " + str(self.images[i]) + "\n\n"

        if len(self.variables) > 1:
            out += "\n\nVariables\n\n"
        for i in self.variables:
            if i != "x":
                out += i + " = " + str(self.variables[i]) + "\n"
        print(out)

        return input(ask + " ")

    def screen_info(self, ask: str):
        print("\033c", end='')
        print(str(self) + ask, end="")

    def determine_size(self):
        """
        Helps determine what size screen we want, by prompting user to give
        suggestions
        """
        self.screen_prompt("We will first determine your screen size (Enter)")
        # # Ask user if they want to change screen dimensions
        # if self.screen_prompt("Would you like to change the dimensions of the screen (y/n)?") != 'y':
        #     return
        #
        # self.screen_prompt("First, we'll be changing the width (Enter)")
        #
        # c = self.screen_prompt("Would you like to increase (1) or decrease (2) the width?")
        #
        # if c == "1":
        #     c = self.screen_prompt("Press enter to increase width by 1. If next line reached press something else")
        #     while c == "":
        #         self.width += 1
        #         self.clear_screen(ch="–")
        #         self.compile_output()
        #         c = self.screen_prompt( "Press enter to increase width by 1. If next line reached press something else")
        #     self.width -= 1
        #     self.grid = [['–' for i in range(self.width)] for j in range(self.height)]
        #     self.compile_output()
        # elif c == "2":
        #     c = self.screen_prompt("Press enter to decrease width by 1. Press something else when done")
        #     while c == "":
        #         self.width = self.width -1 if self.width > 0 else 0
        #         self.clear_screen(ch="–")
        #         self.compile_output()
        #         c = self.screen_prompt( "Press enter to decrease width by 1. Press something else when done")
        #
        # self.screen_prompt( "Next, we'll be changing the height (Enter)")
        #
        # c = self.screen_prompt( "Would you like to increase (1) or decrease (2) the height?")
        #
        # if c == "1":
        #     c = self.screen_prompt(
        #                       "Press enter to increase height by 1. If the first line is lines, press something else")
        #     while c == "":
        #         self.height += 1
        #         self.clear_screen(ch="–")
        #         self.compile_output()
        #         c = self.screen_prompt(
        #                           "Press enter to increase height by 1. If the first line is lines, press something else")
        #     self.width -= 1
        #     self.grid = [['–' for i in range(self.width)] for j in range(self.height)]
        #     self.compile_output()
        # elif c == "2":
        #     c = self.screen_prompt( "Press enter to decrease height by 1. Press something else when done")
        #     while c == "":
        #         self.height = self.height - 1 if self.height > 0 else 0
        #         self.clear_screen(ch="–")
        #         self.compile_output()
        #         c = self.screen_prompt( "Press enter to decrease height by 1. Press something else when done")
        self.screen_info("Use the arrow keys to resize the screen. Press enter when done.")
        inp = keyinput.get_input()
        # Loop to keep asking user

        while inp != "enter":
            if inp == "down":
                self.height += 1
            elif inp == "up" and 0 < self.height:
                self.height -= 1
            elif inp == "right":
                self.width += 1
            elif inp == "left" and 0 < self.width:
                self.width -= 1
            self.clear_screen(ch='-')
            self.compile_output()

            self.screen_info("Use the arrow keys to resize the screen. Press enter when done.")
            inp = keyinput.get_input()

        self.screen_prompt( "We are done! (Enter) ")

        save_setting("height", self.height)
        save_setting("width", self.width)

    def determine_ratio(self):
        self.screen_prompt("The ratio of your font will now be determined by asking you if you see a square 💀")

        # Setting height and width for the square
        height = min(self.height//2, self.height)
        width = min(self.width//3, self.width)

        # Code to draw a square
        self.clear_screen()
        for i in range(height):
            for j in range(width):
                self.grid[i][j] = "#"
        self.compile_output()

        self.screen_info("Use the arrow keys to resize the rectangle into a square. Press enter when done.")
        inp = keyinput.get_input()

        # Loop to keep asking user

        while inp != "enter":
            if inp == "down" and height < self.height:
                height += 1
            elif inp == "up" and 0 < height:
                height -= 1
            elif inp == "right" and width < self.width:
                width += 1
            elif inp == "left" and 0 < width:
                width -= 1
            self.clear_screen()
            for i in range(height):
                for j in range(width):
                    self.grid[i][j] = "#"
            self.compile_output()

            self.screen_info("Use the arrow keys to resize the rectangle into a square. Press enter when done.")
            inp = keyinput.get_input()

        # Save info
        save_setting("width_s", width)
        save_setting("height_s", height)

    def get_row_col(self, x, y):
        return int((self.origin[1] - y)/self.cell_h), int((x - self.origin[0])/self.cell_w)

    def get_values_dict(self):
        return {"width": self.width, "height": self.height, "origin": self.origin, "cell_w": self.cell_w,
                "cell_h": self.cell_h}

    def create_graphs(self):
        """
        Actually apply the images to the screen
        """
        self.clear_screen()

        # Find row for 0 point
        x_axis, y_axis = self.get_row_col(0, 0)

        k = 0

        # Draw axes
        if 0 <= x_axis < self.height:
            k += 1
            for i in range(self.width):
                self.grid[x_axis][i] = "–"
        if 0 <= y_axis < self.width:
            k += 1
            for i in range(self.height):
                self.grid[i][y_axis] = "|"
        if k == 2:
            self.grid[x_axis][y_axis] = "+"

        # Get rules for all the images, and draw
        for i in self.images:
            i.compute_rules(self.get_values_dict(), self.get_row_col, self.variables)
            for x in i.rules:
                for y in i.rules[x]:
                    self.grid[y][x] = i.color + i.symb + "\033[00m"

    def transformation(self):
        """
        Deals with the movement of the camera
        """
        self.screen_info("Use Arrow Keys and +- to Navigate (Press Enter to Finish)" +
                         "\n(" + str(self.origin[0]) + "< x < " + str(self.origin[0] + self.width*self.cell_w) + ") (" + str(self.origin[1] - self.height*self.cell_h) + "< y < " + str(self.origin[1] ) + ")")
        time_since_change = 4
        translate = [0, 0]
        time.sleep(0.1)
        c = keyinput.get_press()
        while "enter" not in c:
            time.sleep(0.1)

            if c:
                msg = []
                if "right" in c:
                    translate[0] = lerp(translate[0], 15, 0.1)
                    msg.append("Panning Right")
                elif "left" in c:
                    translate[0] = lerp(translate[0], -15, 0.1)
                    msg.append("Panning Left")
                if "up" in c:
                    translate[1] = lerp(translate[1], 15, 0.1)
                    msg.append("Panning Up")
                elif "down" in c:
                    translate[1] = lerp(translate[1], -15, 0.1)
                    msg.append("Panning Down")
                if "+" in c:
                    self.origin[0] += scale * self.width * self.cell_w
                    self.origin[1] -= scale * self.height * self.cell_h
                    self.cell_w *= 1 - 2*scale
                    self.cell_h *= 1 - 2 * scale
                    msg.append("Zooming In")
                elif "-" in c:
                    self.cell_w /= 1 - 2*scale
                    self.cell_h /= 1 - 2*scale
                    self.origin[0] -= scale * self.width * self.cell_w
                    self.origin[1] += scale * self.height * self.cell_h
                    msg.append("Zooming Out")

                time_since_change = 0

                # Update origin
                self.origin[0] += math.trunc(translate[0]) * self.cell_w
                self.origin[1] += math.trunc(translate[1] * self.ratio) * self.cell_h

                # Create graph
                self.create_graphs()
                self.compile_output()
                self.screen_info(', '.join(msg))

            else:
                if time_since_change == 4:
                    self.screen_info("Use Arrow Keys and +- to Navigate (Press Enter to Finish)" +
                                     "\n(" + str(self.origin[0]) + "< x < " + str(self.origin[0] + self.width*self.cell_w) + ") (" + str(self.origin[1] - self.height*self.cell_h) + "< y < " + str(self.origin[1] ) + ")")
                if time_since_change <= 10:
                    time_since_change += 1
                translate[0] = lerp(translate[0], 0, 0.7)
                translate[1] = lerp(translate[0], 0, 0.7)

            c = keyinput.get_press()














def get_setting(setting):
    """
    <setting> is the title of the setting we're looking for
    returns the value associated with setting
    """
    if __name__ == "__main__":
        f = open("settings.txt", "r")
    else:
        f = open("other/settings.txt", "r")
    result = ""
    for line in f:
        s = line.strip().split()
        if s[0] == setting:
            result = int(s[1])

    f.close()
    return result


def save_setting(setting, value):
    """
    <setting> is the setting we want to change
    <value> is the value that we want to add to the settings
    """
    if __name__ == "__main__":
        f = open("settings.txt", "r+")
    else:
        f = open("other/settings.txt", "r+")
    data = f.readlines()
    f.close()
    if __name__ == "__main__":
        f = open("settings.txt", "w")
    else:
        f = open("other/settings.txt", "w")

    # Go through data and replace data
    for i in range(len(data)):
        if setting + " " in data[i]:
            data[i] = setting + " " + str(value) + "\n"
    f.writelines(data)
    f.close()


def lerp(a, b, t):
    return (b-a)*t + a

if __name__ == "__main__":
    sample = Screen()

    i1 = image.Image()
    i2 = image.Image()

    i1.set_color("blue")
    i2.set_color("red")

    def f1(x): return -x**2
    def f2(x): return (x-2)*(x-5)*(x+4)
    f2, var = function.get_fn("sinx/cosx/tanx/cosx")
    f1, var = function.get_fn("x^2^x")
    i1.set_fn(f1)
    i2.set_fn(f2)

    sample.images = [i2, i1]

    sample.create_graphs()
    sample.compile_output()
    sample.screen_prompt("Testing axes")
    # sample.transformation()
    sample.functions_prompt("hello")

