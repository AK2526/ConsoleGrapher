import screen, function, image, keyinput

view = screen.Screen()
print("\033c", end='')
while True:
    fn = input("Please enter a function: ")
    try:
        f, var = function.get_fn(fn)
        img = image.Image()
        img.set_fn(f)
        # Add new variables to variables
        for i in var:
            if i != "x":
                inp = input("Please enter a value for variable " + str(i) + ": ")
                if inp != "":
                    view.variables[i] = float()

        color = input("\nPlease enter a color from the following: \n" + ", ".join(list(image.Image.colors.keys())) + "\n\n")
        if color in list(image.Image.colors.keys()):
            img.set_color(color)

        view.images.append(img)
        break


    except:
            print("Please try again\n\n")

view.create_graphs()
view.compile_output()
view.functions_prompt("Continue...")

def fns_screen():
    while True:
        inp = view.functions_prompt("Choose between (g)raphing, (a)dding a function, (m)odifying a function, (r)emoving a function, (e)xiting:")

        if inp[0:1] == "a":
            add_fn()
        elif inp[0:1] == "m":
            modify_fn()
        elif inp[0:1] == "r":
            inp = view.functions_prompt("\nPlease enter the number of the function you'd like to remove:")
            try:
                view.images.pop(int(inp)-1)
            except:
                input("\nSorry, that is not valid...")
        elif inp[0:1] == "e":
            exit(0)
        else:
            view.create_graphs()
            view.compile_output()
            return

def graph_screen():
    while True:
        print("", end="")
        inp = view.screen_prompt("Choose between (m)oving around, (s)howing functions, (e)xiting:")

        if inp[0:1] == "m":
            view.transformation()
        elif inp[0:1] == "e":
            exit()
        else:
            fns_screen()


def add_fn():
    fn = input("Please enter a function: ")

    try:
        f, var = function.get_fn(fn)
        img = image.Image()
        img.set_fn(f)
        # Add new variables to variables
        for i in var:
            if i != "x":
                inp = input("Please enter a value for variable " + str(i) + ": ")
                if inp != "":
                    view.variables[i] = float()

        color = input(
            "\nPlease enter a color from the following: \n" + ", ".join(list(image.Image.colors.keys())) + "\n\n")
        if color in list(image.Image.colors.keys()):
            img.set_color(color)

        view.images.append(img)

        view.create_graphs()
        view.compile_output()

    except:
        input("Sorry, please try again...\n\n")

def modify_fn():
    inp = view.functions_prompt("Please enter the number of the function you'd like to modify:")
    try:
        temp = view.images.pop(int(inp) - 1)

        keyinput.write_eqn(str(temp.fn))
        fn = input("Please modify the function: ")

        f, var = function.get_fn(fn)
        img = image.Image()
        img.set_fn(f)
        # Add new variables to variables
        for i in var:
            if i != "x":
                inp = input("Please enter a value for variable " + str(i) + ": ")
                if inp != "":
                    view.variables[i] = float()

        color = input(
            "\nPlease enter a color from the following: \n" + ", ".join(list(image.Image.colors.keys())) + "\n\n")
        if color in list(image.Image.colors.keys()):
            img.set_color(color)
        else:
            img.set_precise_color(temp.color)

        view.images.insert(int(inp) - 1, img)

    except:
        input("\nSorry, that is not valid...")

graph_screen()