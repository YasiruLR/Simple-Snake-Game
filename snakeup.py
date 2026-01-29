import turtle
import time
import random

win = turtle.Screen()
win.title("Snake Game ")
win.bgcolor("black")
win.setup(width=600, height=600)
win.tracer(0)  

score = 0
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0", align="center", font=("Arial", 18, "bold"))

head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"  

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(100, 100)

segments = []
delay = 0.12

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

win.listen()
win.onkeypress(go_up, "Up")
win.onkeypress(go_down, "Down")
win.onkeypress(go_left, "Left")
win.onkeypress(go_right, "Right")

win.onkeypress(go_up, "w")
win.onkeypress(go_down, "s")
win.onkeypress(go_left, "a")
win.onkeypress(go_right, "d")

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

while True:
    win.update()

    if head.xcor() > 280 or head.xcor() < -280 or head.ycor() > 280 or head.ycor() < -280:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        for seg in segments:
            seg.hideturtle()
        segments.clear()

        score = 0
        pen.clear()
        pen.write("Score: 0", align="center", font=("Arial", 18, "bold"))

    if head.distance(food) < 20:
        
        x = random.randint(-260, 260)
        y = random.randint(-260, 260)
      
        x = (x // 20) * 20
        y = (y // 20) * 20
        food.goto(x, y)

        new_seg = turtle.Turtle()
        new_seg.speed(0)
        new_seg.shape("circle")
        new_seg.color("green")
        new_seg.penup()
        segments.append(new_seg)

        score += 10
        pen.clear()
        pen.write(f"Score: {score}", align="center", font=("Arial", 18, "bold"))

    for i in range(len(segments) - 1, 0, -1):
        segments[i].goto(segments[i - 1].xcor(), segments[i - 1].ycor())

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

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
