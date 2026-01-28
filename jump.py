import turtle
import time
import random

# ================= SCREEN =================
wn = turtle.Screen()
wn.title("Running Jump Game")
wn.bgcolor("skyblue")
wn.setup(width=900, height=400)
wn.tracer(0)

# ================= GROUND =================
ground = turtle.Turtle()
ground.hideturtle()
ground.shape("square")
ground.color("saddlebrown")
ground.penup()
ground.goto(0, -130)
ground.shapesize(stretch_wid=1, stretch_len=50)

# ================= PLAYER =================
player = turtle.Turtle()
player.shape("square")
player.color("darkblue")
player.penup()
player.goto(-350, -100)

player.dy = 0
gravity = -0.8
jump_power = 15
on_ground = True

# Running animation frames
run_frames = [(2, 2), (2.2, 1.8), (1.8, 2.2)]
frame_index = 0
frame_timer = 0

# ================= OBSTACLES =================
obstacles = []

def create_obstacle(x):
    obs = turtle.Turtle()
    obs.shape("square")
    obs.color("darkred")
    obs.penup()
    obs.goto(x, -100)
    obs.shapesize(stretch_wid=2, stretch_len=random.randint(1, 3))
    obstacles.append(obs)

create_obstacle(400)
create_obstacle(650)

speed = 8

# ================= SCORE =================
score = 0
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.goto(0, 150)
pen.write("Score: 0", align="center", font=("Arial", 18, "bold"))

# ================= JUMP =================
def jump():
    global on_ground
    if on_ground:
        player.dy = jump_power
        on_ground = False

wn.listen()
wn.onkey(jump, "space")

# ================= GAME LOOP =================
game_over = False

while not game_over:
    wn.update()
    time.sleep(0.02)

    # -------- RUNNING ANIMATION --------
    if on_ground:
        frame_timer += 1
        if frame_timer > 5:
            frame_index = (frame_index + 1) % len(run_frames)
            w, l = run_frames[frame_index]
            player.shapesize(stretch_wid=w, stretch_len=l)
            frame_timer = 0
    else:
        # Jump pose
        player.shapesize(stretch_wid=2.3, stretch_len=2.3)

    # -------- PHYSICS --------
    player.dy += gravity
    player.sety(player.ycor() + player.dy)

    if player.ycor() <= -100:
        player.sety(-100)
        player.dy = 0
        on_ground = True

    # -------- OBSTACLES --------
    for obs in obstacles:
        obs.setx(obs.xcor() - speed)

        if obs.xcor() < -450:
            obs.goto(450 + random.randint(0, 300), -100)
            score += 1
            speed += 0.3
            pen.clear()
            pen.write(f"Score: {score}", align="center",
                      font=("Arial", 18, "bold"))

        # Collision
        if (abs(player.xcor() - obs.xcor()) < 35 and
            abs(player.ycor() - obs.ycor()) < 45):
            game_over = True

# ================= GAME OVER =================
pen.goto(0, 0)
pen.write("💥 GAME OVER 💥", align="center",
          font=("Arial", 28, "bold"))

wn.mainloop()
