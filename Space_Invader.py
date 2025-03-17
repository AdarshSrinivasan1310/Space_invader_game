import math
import turtle
import random

# Registering shapes to Turtle
turtle.register_shape("player.gif")
turtle.register_shape("invader.gif")

# Setup the screen
scr = turtle.Screen()
scr.title("Space Invaders")
scr.bgcolor("blue")
scr.bgpic("space_invaders_background.gif")
scr.setup(600, 800)

# Creating borders
borders = []

def create_border(x, y, width, height):
    border = turtle.Turtle()
    border.speed(0)
    border.color("blue")
    border.penup()
    border.goto(x, y)
    border.pendown()
    border.begin_fill()
    for _ in range(2):
        border.forward(width)
        border.left(90)
        border.forward(height)
        border.left(90)
    border.end_fill()
    border.hideturtle()
    borders.append(border)

create_border(-300, -300, 20, 600)  # Left border
create_border(280, -300, 20, 600)   # Right border

# Creating scoreboard
score = 0
scoreboard = turtle.Turtle()
scoreboard.color("yellow")
scoreboard.penup()
scoreboard.goto(0, 320)  # Adjusted position to make room for the title
scoreboard.pendown()
scoreboard.write("Score: 0", align="center", font=("Arial", 24, "bold"))
scoreboard.hideturtle()

# Creating title
title = turtle.Turtle()
title.color("red")
title.penup()
title.goto(0, 350)  # Adjusted position for the title
title.write("Space Invaders", align="center", font=("Arial", 24, "bold"))
title.hideturtle()

# Creating player turtle
player = turtle.Turtle()
player.speed(0)
player.color("blue")
player.shape("player.gif")
player.penup()
player.goto(0, -275)

# Creating enemy
enemyspeed = 5
enemies = []
no_enemies = 5
for _ in range(no_enemies):
    enemy = turtle.Turtle()
    enemy.speed(0)
    enemy.color("green")
    enemy.shape("invader.gif")
    enemy.penup()
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.goto(x, y)
    enemies.append(enemy)

# Creating bullet
bullet_speed = 20  # Set bullet speed
bullet = turtle.Turtle()
bullet.speed(0)
bullet.color("yellow")
bullet.shape("triangle")
bullet.shapesize(0.5, 0.5)
bullet.setheading(90)
bullet.penup()
bullet.goto(0, -400)  # Initial bullet position (off-screen)
bullet.hideturtle()

# Bullet state
bulletstate = "ready"

# Moving player right
def player_right():
    x = player.xcor()
    x += 20
    if x > 280:
        x = 280  # Make sure it's within the screen
    player.setx(x)

# Moving player left
def player_left():
    x = player.xcor()
    x -= 20
    if x < -280:
        x = -280  # Make sure it's within the screen
    player.setx(x)

# Firing bullet
def firebullet():
    global bulletstate
    if bulletstate == "ready":
        bullet.showturtle()
        bulletstate = "fire"
        x = player.xcor()
        y = player.ycor() + 10  # To avoid overlap
        bullet.goto(x, y)

# Keyboard binding
scr.listen()
scr.onkeypress(player_right, "Right")
scr.onkeypress(player_right, "d")
scr.onkeypress(player_left, "Left")
scr.onkeypress(player_left, "a")
scr.onkeypress(firebullet, "space")
scr.onkeypress(firebullet, "0")

# Collision detection
def iscollision(t1, t2):
    distance = math.sqrt((t1.xcor() - t2.xcor()) ** 2 + (t1.ycor() - t2.ycor()) ** 2)
    if distance < 25:
        return True
    else:
        return False

# Main game loop
while True:
    for enemy in enemies:
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        if x > 280 or x < -280:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1

        if enemy.ycor() < -275:
            scr.bgcolor("black")  # Change background color to black
            title.clear()  # Clear the title
            title.color("red")  # Set color to red
            title.write("Game Over", align="center", font=("Arial", 36, "bold"))  # Write "Game Over" message
            print("Game Over")
            exit()

        if iscollision(bullet, enemy):
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.goto(0, -400)  # Reset bullet position
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.goto(x, y)
            score += 10
            scoreboard.clear()
            scoreboard.write("Score: {}".format(score), align="center", font=("Arial", 24, "bold"))

        if iscollision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            scr.bgcolor("black")  # Change background color to black
            title.clear()  # Clear the title
            title.color("red")  # Set color to red
            title.write("Game Over", align="center", font=("Arial", 36, "bold"))  # Write "Game Over" message
            print("Game Over")
            exit()
            break

    # Moving bullet up
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

turtle.done()
