import turtle
import time

# Screen
wn = turtle.Screen()
wn.title("Obstacle Jumping Game")
wn.bgcolor("lightgreen")
wn.setup(width=800, height=400)
wn.tracer(0)

# Player
player = turtle.Turtle()
player.shape("square")
player.color("blue")
player.penup()
player.goto(-300, -100)
player.dy = 0

# Obstacle
obstacle = turtle.Turtle()
obstacle.shape("square")
obstacle.color("red")
obstacle.penup()
obstacle.goto(400, -100)

# Gravity & jump
gravity = -0.6
jump_power = 12

def jump():
    if player.ycor() <= -100:   # ground check
        player.dy = jump_power

wn.listen()
wn.onkey(jump, "space")

# Game loop
while True:
    wn.update()
    time.sleep(0.02)

    # Player movement
    player.dy += gravity
    player.sety(player.ycor() + player.dy)

    # Ground collision
    if player.ycor() < -100:
        player.sety(-100)
        player.dy = 0

    # Obstacle movement
    obstacle.setx(obstacle.xcor() - 8)

    if obstacle.xcor() < -400:
        obstacle.goto(400, -100)

    # Collision detection
    if (abs(player.xcor() - obstacle.xcor()) < 20 and
        abs(player.ycor() - obstacle.ycor()) < 20):
        print("💥 Game Over!")
        break

wn.mainloop()
