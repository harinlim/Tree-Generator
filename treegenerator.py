"""My turtle scene creates a unique randomized tree on randomized ground height and with randomized color birds.

Most of it is softcoded for your personal leisure. With this program, you will be able to generate a tree bird scenery that is unique and randomized every time
you run the program. I wanted to explore the idea of randomness and use the power of coding to further what would just be an artistic portrait of a bird-tree
so I created this to do that. I wrote comments in the main function for variables that you can change to tweak the program.

For the tree leaves, I used a loop to randomly generate a set sum of triangle shaped leaves in a set rectangular space. 
I called this tree leaf clump function multiple times through a simple while loop. I also used while loops to randomly 
generate my birds. Marker and fill color are specified in the bird body circle functions. 
"""

from turtle import Turtle, colormode, done, tracer, update, Screen, TurtleScreen
import random


colormode(255)


def main() -> None:
    """Welcome to the turtle scene. Here, we call all of our components and set up the background."""
    tracer(0, 0)
    bob: Turtle = Turtle()
    bob.hideturtle()

    width: float = 800
    height: float = 800

    # Creates screen and fills with sky gradient
    screen: TurtleScreen = Screen()
    skycolors: list[tuple[int, int, int]] = [(112, 168, 196), (84, 151, 184), (62, 144, 184), (38, 119, 158), (13, 82, 115), (17, 68, 92), (146, 192, 214), (222, 173, 126)]
    screen.bgcolor(random.choice(skycolors))
    screen.screensize(int(width), int(height))
    
    # VARIABLES USED WITH HARD CODE: Do not change.
    startx: int = 0
    starty: int = 175
    startedtree: bool = False
    treecoords: list[tuple[float, float]] = []
    branchcoords: list[tuple[float, float]] = []
    originy: float = starty
    originx: float = startx

    # COLOR LISTS: uncomment the commented colors line and comment the other colors line for a different theme! Line 47 contains a cherry blossom theme, line 46 has a regular tree theme.
    # colors: list[tuple[int, int, int]] = [(40, 120, 44), (13, 89, 17), (45, 87, 47), (22, 122, 62), (81, 148, 108)]
    colors: list[tuple[int, int, int]] = [(227, 157, 192), (184, 99, 141), (219, 184, 202), (224, 218, 221), (143, 61, 102)]
    branchcolor: list[tuple[int, int, int]] = [(102, 64, 46), (102, 60, 46), (100, 65, 47)]

    # Softcoded variables. You may change these at your leisure.
    leafsize: int = 20  # length of leaf triangle side
    leafpensize: int = 10  # leaf pen size
    leafamount: int = 200  # amount of leaf triangles in a clump of leaves
    leafspace: int = 30  # length of space between each consecutive leaf drawn. Recommend do not change.
    leafrect: int = 150  # half the length of the side of the rectangle space leaves can be drawn in for a clump
    clumpcount: int = 5  # Amount of clumps in a tree. You may change this freely. Recommended between 4 and 8.

    # You can change birdamount, but keep less than clumpamount. Uncomment the code below the variable for some random fun!
    birdamount: int = clumpcount
    # birdamount = random.randint(1, birdamount)

    # Creates a sky color gradient of blue.
    skyshade(bob, skycolors, height)

    # Creates the ground!
    ground(bob, height, width, colors)

    # Drawing the branches of the tree
    i: int = 0
    while i < clumpcount:
        while startedtree is True:
            originx = random.randint(-leafrect * clumpcount // 3, leafrect * clumpcount // 3)
            originy = random.randint(starty - 100, starty)
            if checkclumps(originx, originy, treecoords, leafrect):
                startedtree = False
        bob.penup()
        bob.goto(originx, originy)
        bob.pendown()
        treecoords.append((originx, originy))
        branches(starty, bob, originx, originy, i, branchcolor)
        branchcoords.append((bob.xcor(), bob.ycor()))
        startedtree = True
        i += 1

    # Draws the trunk of the tree
    trunk(branchcoords, bob, branchcolor)

    # Draws our leaves for the tree
    i = 0
    while i < clumpcount:
        leaves(bob, treecoords[i][0], treecoords[i][1], leafsize, leafamount, leafspace, leafrect, leafpensize, colors)
        i += 1

    # Draws our birds on the tree.
    birdcoords: list[tuple[float, float]] = []
    i = 0
    while i < birdamount:
        notunique: bool = True
        number: int = 0
        while notunique is True:
            number = random.randint(0, len(treecoords) - 1)
            if checkbirds(number, treecoords, birdcoords):
                notunique = False
        birdcoords.append(treecoords[number])
        bird(bob, treecoords, number)
        i += 1
    
    update()
    done()


def skyshade(turtle: Turtle, colors: list[tuple[int, int, int]], height: float) -> None:
    """Draws a circular pattern in the sky."""
    turtle.penup()
    turtle.goto(0, -height)
    turtle.pendown()

    i: int = 0
    while i < len(colors):
        turtle.color(colors[i])
        turtle.begin_fill()
        turtle.setheading(0)
        turtle.circle(int((len(colors) - i) * (height // len(colors))))
        turtle.end_fill()
        i += 1


def ground(turtle: Turtle, height: float, width: float, colors: list[tuple[int, int, int]]) -> None:
    """Creates a random color grass ground with random marker color using a rectangle."""
    groundy: int = random.randint(int(height) // 8, int(height) // 3)

    turtle.penup()
    turtle.goto(-(width / 2), -groundy)
    turtle.pendown()
    turtle.pencolor(random.choice(colors))
    turtle.fillcolor(random.choice(colors))
    turtle.pensize(20)
    turtle.begin_fill()
    turtle.setheading(0)

    i: int = 0
    while i < 4:
        if i % 2 == 0:
            turtle.forward(width)
            turtle.right(90)
        else:
            turtle.forward(height - groundy)
            turtle.right(90)
        i += 1
    
    turtle.end_fill()
    turtle.pensize(1)


def branches(starty: int, turtle: Turtle, originx: float, originy: float, trunknumber: int, color: list[tuple[int, int, int]]) -> None:
    """Draws trunk connecting leaf clump starting points to the ground point with a branch bend."""
    groundy: int = starty - 150
    branchbend: int = starty - 100
    ydiff: int = abs(starty - int(originy))

    turtle.pensize(30)

    degree: int = 0
    while turtle.ycor() > branchbend:
        turtle.color(random.choice(color))
        if originx <= 0:
            originx -= trunknumber * 10
            degree = random.randint(270, 300)
            turtle.setheading(degree)
            turtle.forward(50)
        elif originx > 0:
            originx += trunknumber * 10
            degree = random.randint(240, 270)
            turtle.setheading(degree)
            turtle.forward(50)

    turtle.goto(turtle.xcor() // 2, groundy - ydiff)
    turtle.goto(turtle.xcor() // 2, turtle.ycor() - ydiff)


def checkclumps(originx: float, originy: float, treecoords: list[tuple[float, float]], leafrect: int) -> bool:
    """Checks that the clump of leaves being made is not too close to the other clumps."""
    i: int = 0
    xdiff: int = 0
    ydiff: int = 0

    while i < len(treecoords):
        xdiff = abs(int(originx - treecoords[i][0]))
        ydiff = abs(int(originy - treecoords[i][1]))
        if xdiff < leafrect and ydiff < (leafrect // 4):
            return False
        i += 1
    return True


def trunk(coords: list[tuple[float, float]], turtle: Turtle, color: list[tuple[int, int, int]]) -> None:
    """Draws the trunk connecting the branches to the ground with some randomness, and in order of branches going down."""
    i: int = 0
    k: int = 0
    holder: list[tuple[float, float]] = []
    branchcoords: list[tuple[float, float]] = coords
    lentree: int = len(coords)

    while i < lentree:
        k = 0
        while k <= (lentree - i - 2):
            if (branchcoords[k][1] > branchcoords[k + 1][1]):
                holder.append(branchcoords[k])
                branchcoords[k] = branchcoords[k + 1]
                branchcoords[k + 1] = holder[-1]
            k = k + 1
        i += 1

    # Creates more variety by joining the highest three branches together.        
    firstmeet: list[tuple[float, float]] = [(0, branchcoords[2][1] - 100)]

    i = 0
    while i < 3:
        turtle.color(random.choice(color))
        turtle.penup()
        turtle.goto(branchcoords[i])
        turtle.pendown()
        turtle.goto(firstmeet[0])
        i += 1

    # Draws the rest of the branches down to a point.
    while i < lentree:
        turtle.color(random.choice(color))
        turtle.goto(branchcoords[i])    
        i += 1
    
    turtle.penup()
    turtle.goto(branchcoords[0])

    # Draws the full trunk by starting from the two lowest branch points based on which one is more to the left.
    state: bool = False
    turtle.color(random.choice(color))
    if branchcoords[0][0] > branchcoords[1][0]:
        turtle.goto(branchcoords[1])
        state = True
    turtle.pendown()
    turtle.begin_fill()
    turtle.setheading(270)
    turtle.goto(turtle.xcor(), branchcoords[0][1] - 50)
    turtle.right(random.randint(20, 60))
    turtle.forward(100)
    turtle.setheading(0)
    turtle.forward(125)
    turtle.left(random.randint(90, 150))
    turtle.forward(50)
    if state:
        turtle.goto(branchcoords[0])
    else:
        turtle.goto(branchcoords[1])
    turtle.end_fill()


def leaves(turtle: Turtle, x: float, y: float, trisize: int, amount: int, space: int, rect: int, pensize: int, leaf_colors: list[tuple[int, int, int]]) -> None:
    """Drawing the tree leaves starting at coords (x,y) w/turtle, with leaves of trisize, length of space between leaves, and a number amount of triangles within a rectangle."""
    turtle.pensize(pensize)
    
    xmin: int = int(x) - rect
    xmax: int = int(x) + rect
    ymin: int = int(y) - (rect // 2)
    ymax: int = int(y) + rect

    turtle.penup()
    turtle.goto(x, y) 
    turtle.pendown()

    i: int = 0
    while i < amount:
        turtle.color(random.choice(leaf_colors))
        inspace: bool = False
        while not inspace:
            degree: int = random.randint(0, 359)
            if checkleaves(turtle, space, xmin, xmax, ymax, ymin, degree):
                inspace = True
        turtle.forward(space)
        leaf(turtle, trisize)
        i += 1

    
def checkleaves(turtle: Turtle, space: int, xmin: int, xmax: int, ymax: int, ymin: int, degree: int) -> bool:
    """Checks if leaf starting point will be within the rectangle."""
    turtle.penup()
    turtle.right(degree)
    turtle.forward(space)

    if turtle.xcor() > xmin and turtle.xcor() < xmax and turtle.ycor() > ymin and turtle.ycor() < ymax:
        turtle.backward(space)
        turtle.pendown()
        return True
    else:
        turtle.backward(space)
        turtle.pendown()
        return False


def leaf(turtle: Turtle, trisize: int) -> None:
    """Draws the singular triangle leaf for the iteration."""
    turtle.right(random.randint(-150, 150))
    i: int = 0
    dir: int = random.choice([0, 1])
    turtle.begin_fill()

    if dir == 0:
        while (i < 3):
            turtle.forward(trisize)
            turtle.left(120)
            i = i + 1
    if dir == 1:
        while (i < 3):
            turtle.forward(trisize)
            turtle.right(120)
            i = i + 1

    turtle.end_fill()


def bird(turtle: Turtle, treecoords: list[tuple[float, float]], number: int) -> None:
    """Draws in a little random color birdie onto a random leaf clump point."""
    birdcolors: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = [((27, 142, 250), (18, 88, 153)), ((214, 164, 245), (115, 46, 158)), ((222, 140, 210), (168, 86, 156)), ((255, 181, 8), (184, 141, 40)), ((245, 12, 47), (107, 10, 24))]
    colorindex: int = random.randint(0, len(birdcolors) - 1)

    birdx: float = treecoords[number][0]
    birdy: float = treecoords[number][1]

    birdcircle(turtle, birdx, birdy, birdcolors, colorindex, 1, 0, 30)
    birdcircle(turtle, birdx, birdy + 50, birdcolors, colorindex, 1, 1, 25)
    birdeyes(turtle, birdx - 15, birdy + 80, 2)
    birdeyes(turtle, birdx + 15, birdy + 80, 2)
    birdbeak(turtle, birdx, birdy + 70, 10)


def birdcircle(turtle: Turtle, x: float, y: float, colors: list[tuple[tuple[int, int, int], tuple[int, int, int]]], colorindex: int, pencolor: int, fillcolor: int, radius: int) -> None:
    """Creates a bird body part circle with specified color outline and fill."""
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()

    turtle.setheading(0)
    turtle.pensize(10)
    turtle.pencolor(colors[colorindex][pencolor])
    turtle.fillcolor(colors[colorindex][fillcolor])

    turtle.begin_fill()
    turtle.circle(radius)
    turtle.end_fill()


def birdeyes(turtle: Turtle, x: float, y: float, radius: int) -> None:
    """Draws a black eye with white highlight."""
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()

    turtle.setheading(0)
    turtle.pensize(10)
    turtle.pencolor((0, 0, 0))
    turtle.circle(radius)

    turtle.penup()
    turtle.goto(x + 3, y + 5)
    turtle.pendown()

    turtle.pensize(3)
    turtle.pencolor((255, 255, 255))
    turtle.circle(radius // 2)


def birdbeak(turtle: Turtle, x: float, y: float, size: int) -> None:
    """A peckish yellow beak for our birdie at the coords and size we choose."""
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.setheading(0)
    turtle.pensize(10)
    turtle.color((189, 144, 60))

    turtle.begin_fill()
    turtle.forward(size)
    turtle.goto(x, y - (size // 3))
    turtle.goto(x - size, y)
    turtle.goto(x, y)
    turtle.end_fill()

    turtle.begin_fill()
    turtle.color((255, 207, 36))
    turtle.forward(size)
    turtle.goto(x, y + (size // 2))
    turtle.goto(x - size, y)
    turtle.goto(x, y)
    turtle.end_fill()


def checkbirds(number: int, treecoords: list[tuple[float, float]], birdcoords: list[tuple[float, float]]) -> bool:
    """Checks that there are no duplicate bird locations."""
    k: int = 0
    while k < len(birdcoords):
        if treecoords[number] == birdcoords[k]:
            return False
        k += 1
    return True


if __name__ == "__main__":
    main()