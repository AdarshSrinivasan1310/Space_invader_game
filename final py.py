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
scr.tracer(0)

# Creating borders
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

create_border(-300, -300, 20, 600)  # Left border
create_border(280, -300, 20, 600)   # Right border

# Creating scoreboard
score = 0
scoreboard = turtle.Turtle()
scoreboard.color("yellow")
scoreboard.penup()
scoreboard.goto(0, 320)
scoreboard.write("Score: 0", align="center", font=("Arial", 24, "bold"))
scoreboard.hideturtle()

# Creating player
title = turtle.Turtle()
title.color("red")
title.penup()
title.goto(0, 350)
title.write("Space Invaders", align="center", font=("Arial", 24, "bold"))
title.hideturtle()

player = turtle.Turtle()
player.speed(0)
player.color("blue")
player.shape("player.gif")
player.penup()
player.goto(0, -275)

# Creating enemies
enemyspeed = 5
enemies = []
for _ in range(5):
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
bullet_speed = 20
bullet = turtle.Turtle()
bullet.speed(0)
bullet.color("yellow")
bullet.shape("triangle")
bullet.shapesize(0.5, 0.5)
bullet.setheading(90)
bullet.penup()
bullet.hideturtle()
bulletstate = "ready"

# Moving player right
def player_right():
    x = player.xcor()
    if x < 280:
        player.setx(x + 20)

# Moving player left
def player_left():
    x = player.xcor()
    if x > -280:
        player.setx(x - 20)

# Firing bullet
def firebullet():
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "fire"
        bullet.setposition(player.xcor(), player.ycor() + 10)
        bullet.showturtle()

# Collision detection
def iscollision(t1, t2):
    return t1.distance(t2) < 25

# Keyboard binding
scr.listen()
scr.onkeypress(player_right, "Right")
scr.onkeypress(player_left, "Left")
scr.onkeypress(firebullet, "space")

# Game loop
while True:
    for enemy in enemies:
        enemy.setx(enemy.xcor() + enemyspeed)

        # Enemy boundary check
        if enemy.xcor() > 280 or enemy.xcor() < -280:
            enemyspeed *= -1
            for e in enemies:
                e.sety(e.ycor() - 40)

        # Game over condition
        if enemy.ycor() < -275:
            scr.bgcolor("black")
            title.clear()
            title.write("Game Over", align="center", font=("Arial", 36, "bold"))
            scr.update()
            scr.bye()

        # Bullet-Enemy collision
        if iscollision(bullet, enemy):
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.goto(0, -400)
            enemy.goto(random.randint(-200, 200), random.randint(100, 250))
            score += 10
            scoreboard.clear()
            scoreboard.write("Score: {}".format(score), align="center", font=("Arial", 24, "bold"))

        # Player-Enemy collision
        if iscollision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            scr.bgcolor("black")
            title.clear()
            title.write("Game Over", align="center", font=("Arial", 36, "bold"))
            scr.update()
            scr.bye()

    # Bullet movement
    if bulletstate == "fire":
        bullet.sety(bullet.ycor() + bullet_speed)

    # Reset bullet
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

    scr.update()
