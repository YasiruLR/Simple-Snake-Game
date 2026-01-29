import turtle
import time
import random

# ==========================================
# 🐍 SIMPLE SNAKE GAME (For Kids - Sinhala)
# ==========================================

# ✅ Screen (Game Window)
win = turtle.Screen()
win.title("🐍 Snake Game - Kids Version")
win.bgcolor("black")
win.setup(width=600, height=600)
win.tracer(0)  # screen auto update off (speed up)

# ✅ Score Writer
score = 0
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0", align="center", font=("Arial", 18, "bold"))

# ✅ Snake Head (Main snake circle)
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"  # start with not moving

# ✅ Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(100, 100)

# ✅ Snake Body parts list
segments = []

# ✅ Speed (delay time)
delay = 0.12


# ==========================================
# 🔼🔽◀️▶️ Move functions (Keyboard)
# ==========================================

def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"


# ✅ Connect keyboard to functions
win.listen()
win.onkeypress(go_up, "Up")
win.onkeypress(go_down, "Down")
win.onkeypress(go_left, "Left")
win.onkeypress(go_right, "Right")

# Also W A S D keys
win.onkeypress(go_up, "w")
win.onkeypress(go_down, "s")
win.onkeypress(go_left, "a")
win.onkeypress(go_right, "d")


# ==========================================
# 🚶 Snake move logic
# ==========================================
def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)


# ==========================================
# 🎮 Main Game Loop
# ==========================================
while True:
    win.update()

    # ✅ If snake hits the wall -> reset game
    if head.xcor() > 280 or head.xcor() < -280 or head.ycor() > 280 or head.ycor() < -280:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        # hide all body parts
        for seg in segments:
            seg.hideturtle()
        segments.clear()

        # reset score
        score = 0
        pen.clear()
        pen.write("Score: 0", align="center", font=("Arial", 18, "bold"))

    # ✅ If snake eats food
    if head.distance(food) < 20:
        # move food to random place
        x = random.randint(-260, 260)
        y = random.randint(-260, 260)
        # make it align to 20 grid
        x = (x // 20) * 20
        y = (y // 20) * 20
        food.goto(x, y)

        # add a new body segment
        new_seg = turtle.Turtle()
        new_seg.speed(0)
        new_seg.shape("circle")
        new_seg.color("green")
        new_seg.penup()
        segments.append(new_seg)

        # increase score
        score += 10
        pen.clear()
        pen.write(f"Score: {score}", align="center", font=("Arial", 18, "bold"))

    # ✅ Move body parts (from back to front)
    for i in range(len(segments) - 1, 0, -1):
        segments[i].goto(segments[i - 1].xcor(), segments[i - 1].ycor())

    # ✅ First segment follows head
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    # ✅ Move snake head
    move()

    # ✅ If snake hits its own body -> reset
    for seg in segments:
        if seg.distance(head) < 15:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"
            for s in segments:
                s.hideturtle()
            segments.clear()
            score = 0
            pen.clear()
            pen.write("Score: 0", align="center", font=("Arial", 18, "bold"))
            break

    time.sleep(delay)
