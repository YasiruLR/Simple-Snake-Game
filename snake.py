import turtle
import time
import random
import math

window = turtle.Screen()
window.title("🐍 ULTRA REALISTIC SNAKE - 3D Edition")
window.setup(width=800, height=800)
window.bgcolor("#0a0a0a")
window.tracer(0)

# ----------------------------
# Enhanced Particle System with Physics
# ----------------------------
class Particle:
    def __init__(self, x, y, color, vx=None, vy=None, particle_type="normal"):
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.color(color)
        self.t.penup()
        self.t.goto(x, y)
        self.t.shapesize(0.4, 0.4)
        self.vx = vx if vx is not None else random.uniform(-4, 4)
        self.vy = vy if vy is not None else random.uniform(-4, 4)
        self.life = 30
        self.type = particle_type
        self.rotation = random.uniform(0, 360)

    def update(self):
        self.t.goto(self.t.xcor() + self.vx, self.t.ycor() + self.vy)
        self.vy -= 0.4  # gravity
        self.vx *= 0.98  # air resistance
        self.vy *= 0.98
        self.life -= 1

        size = max(0.05, self.life / 50)
        self.t.shapesize(size, size)

        self.rotation += 15
        self.t.setheading(self.rotation)

    def is_dead(self):
        return self.life <= 0 or self.t.ycor() < -300

    def destroy(self):
        self.t.hideturtle()
        del self.t


particles = []

# ----------------------------
# 3D-Style Animated Grid Background
# ----------------------------
def create_3d_grid():
    grid = turtle.Turtle()
    grid.speed(0)
    grid.penup()
    grid.hideturtle()

    for i in range(-280, 281, 35):
        grid.color("#1a1a4e" if i % 70 == 0 else "#0f0f2e")
        grid.width(2 if i % 70 == 0 else 1)

        grid.goto(i, -280)
        grid.pendown()
        grid.goto(i, 280)
        grid.penup()

        grid.goto(-280, i)
        grid.pendown()
        grid.goto(280, i)
        grid.penup()


create_3d_grid()

# Animated neon border with glow
border_layers = []
for layer in range(3):
    border = turtle.Turtle()
    border.speed(0)
    border.penup()
    border.hideturtle()
    border.width(3 - layer)
    offset = layer * 5

    if layer == 0:
        border.color("#ff00ff")
    elif layer == 1:
        border.color("#ff44ff")
    else:
        border.color("#ff88ff")

    border.goto(-270 + offset, -270 + offset)
    border.pendown()
    for _ in range(4):
        border.forward(540 - offset * 2)
        border.left(90)
    border.penup()
    border_layers.append(border)

# ----------------------------
# Professional UI Elements with Shadows
# ----------------------------
def create_text_with_shadow(y_pos, color, shadow_color, size=18):
    shadow = turtle.Turtle()
    shadow.speed(0)
    shadow.color(shadow_color)
    shadow.penup()
    shadow.hideturtle()
    shadow.goto(2, y_pos - 2)

    display = turtle.Turtle()
    display.speed(0)
    display.color(color)
    display.penup()
    display.hideturtle()
    display.goto(0, y_pos)

    return display, shadow


score_display, score_shadow = create_text_with_shadow(295, "#00ff88", "#003322", 22)
high_score_display, high_shadow = create_text_with_shadow(325, "#ffaa00", "#442200", 18)
level_display, level_shadow = create_text_with_shadow(265, "#00ddff", "#002244", 16)
combo_display, combo_shadow = create_text_with_shadow(235, "#ff0088", "#330022", 16)

# Game Over Screen with glow
game_over_text = turtle.Turtle()
game_over_text.speed(0)
game_over_text.color("#ff0000")
game_over_text.penup()
game_over_text.hideturtle()
game_over_text.goto(0, 0)

game_over_shadow = turtle.Turtle()
game_over_shadow.speed(0)
game_over_shadow.color("#440000")
game_over_shadow.penup()
game_over_shadow.hideturtle()
game_over_shadow.goto(3, -3)

instruction_text = turtle.Turtle()
instruction_text.speed(0)
instruction_text.color("#ffffff")
instruction_text.penup()
instruction_text.hideturtle()
instruction_text.goto(0, -60)

# FPS Counter
fps_display = turtle.Turtle()
fps_display.speed(0)
fps_display.color("#888888")
fps_display.penup()
fps_display.hideturtle()
fps_display.goto(-350, 320)

# ----------------------------
# Advanced 3D Snake Head with Realistic Features (SMALLER)
# ----------------------------
class SnakeHead:
    def __init__(self):
        self.shadow = turtle.Turtle()
        self.shadow.shape("circle")
        self.shadow.color("#001100")
        self.shadow.penup()
        self.shadow.shapesize(1.6, 1.6)

        self.head = turtle.Turtle()
        self.head.shape("circle")
        self.head.color("#00ff88")
        self.head.penup()
        self.head.goto(0, 0)
        self.head.shapesize(1.6, 1.6)
        self.direction = "Stop"

        self.glow_layers = []
        for i in range(3):
            glow = turtle.Turtle()
            glow.shape("circle")
            glow.penup()

            if i == 0:
                glow.color("#00ff88")
            elif i == 1:
                glow.color("#00dd77")
            else:
                glow.color("#00bb66")

            size = 2.0 + (i * 0.35)
            glow.shapesize(size, size)
            self.glow_layers.append(glow)

        self.left_eye_white = self.create_eye_white()
        self.right_eye_white = self.create_eye_white()
        self.left_pupil = self.create_pupil()
        self.right_pupil = self.create_pupil()
        self.left_highlight = self.create_highlight()
        self.right_highlight = self.create_highlight()

        self.tongue = turtle.Turtle()
        self.tongue.shape("square")
        self.tongue.color("#ff0066")
        self.tongue.penup()
        self.tongue.shapesize(0.15, 0.8)
        self.tongue.hideturtle()

        self.tongue_fork1 = turtle.Turtle()
        self.tongue_fork1.shape("square")
        self.tongue_fork1.color("#ff0066")
        self.tongue_fork1.penup()
        self.tongue_fork1.shapesize(0.1, 0.3)
        self.tongue_fork1.hideturtle()

        self.tongue_fork2 = turtle.Turtle()
        self.tongue_fork2.shape("square")
        self.tongue_fork2.color("#ff0066")
        self.tongue_fork2.penup()
        self.tongue_fork2.shapesize(0.1, 0.3)
        self.tongue_fork2.hideturtle()

        self.scales = []
        for _ in range(4):
            scale = turtle.Turtle()
            scale.shape("circle")
            scale.color("#00dd77")
            scale.penup()
            scale.shapesize(0.25, 0.25)
            self.scales.append(scale)

        self.tongue_extend = 0
        self.blink_timer = 0

    def create_eye_white(self):
        eye = turtle.Turtle()
        eye.shape("circle")
        eye.color("#ffffff")
        eye.penup()
        eye.shapesize(0.5, 0.5)
        return eye

    def create_pupil(self):
        pupil = turtle.Turtle()
        pupil.shape("circle")
        pupil.color("#000000")
        pupil.penup()
        pupil.shapesize(0.25, 0.25)
        return pupil

    def create_highlight(self):
        highlight = turtle.Turtle()
        highlight.shape("circle")
        highlight.color("#ffffff")
        highlight.penup()
        highlight.shapesize(0.12, 0.12)
        return highlight

    def update_position(self):
        self.shadow.goto(self.head.xcor() + 3, self.head.ycor() - 3)

        for i, glow in enumerate(self.glow_layers):
            offset = i * 0.5
            glow.goto(self.head.xcor() + offset, self.head.ycor() + offset)

        self.update_eyes()
        self.update_scales()

    def update_scales(self):
        x, y = self.head.xcor(), self.head.ycor()
        scale_positions = [
            (x - 6, y + 8), (x + 6, y + 8),
            (x - 6, y - 8), (x + 6, y - 8)
        ]
        for i, scale in enumerate(self.scales):
            scale.goto(scale_positions[i][0], scale_positions[i][1])

    def update_eyes(self):
        x, y = self.head.xcor(), self.head.ycor()

        self.blink_timer -= 1
        if self.blink_timer <= 0:
            self.blink_timer = random.randint(100, 300)

        is_blinking = self.blink_timer < 5
        if is_blinking:
            self.left_eye_white.hideturtle()
            self.right_eye_white.hideturtle()
            self.left_pupil.hideturtle()
            self.right_pupil.hideturtle()
            self.left_highlight.hideturtle()
            self.right_highlight.hideturtle()
            return
        else:
            self.left_eye_white.showturtle()
            self.right_eye_white.showturtle()
            self.left_pupil.showturtle()
            self.right_pupil.showturtle()
            self.left_highlight.showturtle()
            self.right_highlight.showturtle()

        self.tongue_extend = max(0, self.tongue_extend - 1)

        if self.direction == "up":
            self.left_eye_white.goto(x - 8, y + 12)
            self.right_eye_white.goto(x + 8, y + 12)
            self.left_pupil.goto(x - 8, y + 14)
            self.right_pupil.goto(x + 8, y + 14)
            self.left_highlight.goto(x - 6, y + 15)
            self.right_highlight.goto(x + 6, y + 15)

            if self.tongue_extend > 0:
                tongue_y = y + 16 + self.tongue_extend
                self.tongue.goto(x, tongue_y)
                self.tongue.setheading(90)
                self.tongue.showturtle()
                self.tongue_fork1.goto(x - 3, tongue_y + 7)
                self.tongue_fork2.goto(x + 3, tongue_y + 7)
                self.tongue_fork1.setheading(75)
                self.tongue_fork2.setheading(105)
                self.tongue_fork1.showturtle()
                self.tongue_fork2.showturtle()
            else:
                self.tongue.hideturtle()
                self.tongue_fork1.hideturtle()
                self.tongue_fork2.hideturtle()

        elif self.direction == "down":
            self.left_eye_white.goto(x - 8, y - 12)
            self.right_eye_white.goto(x + 8, y - 12)
            self.left_pupil.goto(x - 8, y - 14)
            self.right_pupil.goto(x + 8, y - 14)
            self.left_highlight.goto(x - 6, y - 13)
            self.right_highlight.goto(x + 6, y - 13)

            if self.tongue_extend > 0:
                tongue_y = y - 16 - self.tongue_extend
                self.tongue.goto(x, tongue_y)
                self.tongue.setheading(270)
                self.tongue.showturtle()
                self.tongue_fork1.goto(x - 3, tongue_y - 7)
                self.tongue_fork2.goto(x + 3, tongue_y - 7)
                self.tongue_fork1.setheading(255)
                self.tongue_fork2.setheading(285)
                self.tongue_fork1.showturtle()
                self.tongue_fork2.showturtle()
            else:
                self.tongue.hideturtle()
                self.tongue_fork1.hideturtle()
                self.tongue_fork2.hideturtle()

        elif self.direction == "left":
            self.left_eye_white.goto(x - 12, y + 8)
            self.right_eye_white.goto(x - 12, y - 8)
            self.left_pupil.goto(x - 14, y + 8)
            self.right_pupil.goto(x - 14, y - 8)
            self.left_highlight.goto(x - 13, y + 10)
            self.right_highlight.goto(x - 13, y - 6)

            if self.tongue_extend > 0:
                tongue_x = x - 16 - self.tongue_extend
                self.tongue.goto(tongue_x, y)
                self.tongue.setheading(180)
                self.tongue.showturtle()
                self.tongue_fork1.goto(tongue_x - 7, y + 3)
                self.tongue_fork2.goto(tongue_x - 7, y - 3)
                self.tongue_fork1.setheading(165)
                self.tongue_fork2.setheading(195)
                self.tongue_fork1.showturtle()
                self.tongue_fork2.showturtle()
            else:
                self.tongue.hideturtle()
                self.tongue_fork1.hideturtle()
                self.tongue_fork2.hideturtle()

        elif self.direction == "right":
            self.left_eye_white.goto(x + 12, y + 8)
            self.right_eye_white.goto(x + 12, y - 8)
            self.left_pupil.goto(x + 14, y + 8)
            self.right_pupil.goto(x + 14, y - 8)
            self.left_highlight.goto(x + 15, y + 10)
            self.right_highlight.goto(x + 15, y - 6)

            if self.tongue_extend > 0:
                tongue_x = x + 16 + self.tongue_extend
                self.tongue.goto(tongue_x, y)
                self.tongue.setheading(0)
                self.tongue.showturtle()
                self.tongue_fork1.goto(tongue_x + 7, y + 3)
                self.tongue_fork2.goto(tongue_x + 7, y - 3)
                self.tongue_fork1.setheading(15)
                self.tongue_fork2.setheading(345)
                self.tongue_fork1.showturtle()
                self.tongue_fork2.showturtle()
            else:
                self.tongue.hideturtle()
                self.tongue_fork1.hideturtle()
                self.tongue_fork2.hideturtle()
        else:
            self.left_eye_white.goto(x - 8, y + 7)
            self.right_eye_white.goto(x + 8, y + 7)
            self.left_pupil.goto(x - 8, y + 7)
            self.right_pupil.goto(x + 8, y + 7)
            self.left_highlight.goto(x - 6, y + 9)
            self.right_highlight.goto(x + 6, y + 9)
            self.tongue.hideturtle()
            self.tongue_fork1.hideturtle()
            self.tongue_fork2.hideturtle()

        if self.direction != "Stop" and random.random() > 0.98:
            self.tongue_extend = 10

    def move(self):
        if self.direction == "up":
            self.head.sety(self.head.ycor() + 20)
        elif self.direction == "down":
            self.head.sety(self.head.ycor() - 20)
        elif self.direction == "left":
            self.head.setx(self.head.xcor() - 20)
        elif self.direction == "right":
            self.head.setx(self.head.xcor() + 20)
        self.update_position()


snake = SnakeHead()

# ----------------------------
# Enhanced Power-up System with Animations
# ----------------------------
class PowerUp:
    def __init__(self, x, y, type_name):
        self.t = turtle.Turtle()
        self.t.shape("square")
        self.t.penup()
        self.t.goto(x, y)
        self.type = type_name
        self.life = 250

        self.glow = turtle.Turtle()
        self.glow.shape("circle")
        self.glow.penup()
        self.glow.goto(x, y)

        if type_name == "speed":
            self.t.color("#00ffff")
            self.glow.color("#008888")
            self.t.shapesize(0.9, 0.9)
            self.glow.shapesize(1.5, 1.5)
        elif type_name == "slow":
            self.t.color("#ffff00")
            self.glow.color("#888800")
            self.t.shapesize(0.9, 0.9)
            self.glow.shapesize(1.5, 1.5)
        elif type_name == "shield":
            self.t.color("#0088ff")
            self.glow.color("#004488")
            self.t.shapesize(1.1, 1.1)
            self.glow.shapesize(1.8, 1.8)
        elif type_name == "bonus":
            self.t.color("#ff00ff")
            self.glow.color("#880088")
            self.t.shapesize(1.0, 1.0)
            self.glow.shapesize(1.6, 1.6)

    def update(self, count):
        self.life -= 1
        self.t.setheading(count * 12)

        pulse = 0.9 + 0.3 * math.sin(count * 0.4)
        glow_pulse = 1.3 + 0.4 * math.sin(count * 0.4)

        if self.type == "shield":
            self.t.shapesize(pulse + 0.2, pulse + 0.2)
            self.glow.shapesize(glow_pulse + 0.4, glow_pulse + 0.4)
        else:
            self.t.shapesize(pulse, pulse)
            self.glow.shapesize(glow_pulse, glow_pulse)

        base_y = self.t.ycor()
        offset = 3 * math.sin(count * 0.5)
        self.t.sety(base_y + offset * 0.1)
        self.glow.goto(self.t.xcor(), self.t.ycor())

    def is_expired(self):
        return self.life <= 0

    def destroy(self):
        self.t.hideturtle()
        self.glow.hideturtle()


powerups = []

# ----------------------------
# Game State Variables
# ----------------------------
segments = []
score = 0
high_score = 0
level = 1
combo = 0
delay = 0.085
game_paused = False
game_over = False
invincible = False
invincible_timer = 0

rainbow_colors = [
    "#00ff88", "#00ffaa", "#00ffcc", "#00ffff",
    "#00ddff", "#00ccff", "#00aaff", "#0088ff",
    "#0066ff", "#0044ff", "#4400ff", "#6600ff",
    "#8800ff", "#aa00ff", "#cc00ff", "#ff00ff",
    "#ff00dd", "#ff00bb", "#ff0099", "#ff0077"
]

# ----------------------------
# Advanced Food System with 3D Effects (SMALLER)
# ----------------------------
class Food:
    def __init__(self):
        self.shadow = turtle.Turtle()
        self.shadow.shape("circle")
        self.shadow.color("#220011")
        self.shadow.penup()
        self.shadow.shapesize(1.1, 1.1)

        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.penup()
        self.t.shapesize(1.0, 1.0)

        self.rings = []
        for _ in range(4):
            ring = turtle.Turtle()
            ring.shape("circle")
            ring.penup()
            ring.color("#ff006e")
            self.rings.append(ring)

        self.sparkles = []
        for i in range(8):
            sparkle = turtle.Turtle()
            sparkle.shape("circle")
            sparkle.color("#ffff00")
            sparkle.penup()
            size = 0.2 + (i % 3) * 0.1
            sparkle.shapesize(size, size)
            self.sparkles.append(sparkle)

        self.type = "normal"
        self.respawn()

    def respawn(self):
        x = random.randint(-240, 240)
        y = random.randint(-240, 240)
        x = (x // 20) * 20
        y = (y // 20) * 20
        self.t.goto(x, y)
        self.shadow.goto(x + 4, y - 4)

        rand = random.random()
        if rand < 0.65:
            self.type = "normal"
            self.t.color("#ff006e")
        elif rand < 0.85:
            self.type = "golden"
            self.t.color("#ffd700")
        else:
            self.type = "super"
            self.t.color("#00ffff")

    def update(self, count):
        scale = 0.9 + 0.25 * math.sin(count * 0.5)
        self.t.shapesize(scale, scale)

        for i, ring in enumerate(self.rings):
            ring_scale = scale + 0.45 + i * 0.28
            phase_shift = i * 0.5
            ring_scale += 0.2 * math.sin(count * 0.3 + phase_shift)
            ring.shapesize(ring_scale, ring_scale)
            ring.goto(self.t.xcor(), self.t.ycor())

        for i, sparkle in enumerate(self.sparkles):
            angle = count * (10 + i * 2) + (i * 45)
            radius = 28 + 6 * math.sin(count * 0.4 + i)
            height_offset = 3 * math.sin(count * 0.6 + i * 0.5)

            x = self.t.xcor() + radius * math.cos(math.radians(angle))
            y = self.t.ycor() + radius * math.sin(math.radians(angle)) + height_offset
            sparkle.goto(x, y)

            if self.type == "golden":
                colors = ["#ffaa00", "#ffdd00", "#ffff00"]
                sparkle.color(colors[i % 3])
            elif self.type == "super":
                colors = ["#00ffff", "#00ddff", "#00aaff"]
                sparkle.color(colors[i % 3])
            else:
                colors = ["#ffff00", "#ffdd00", "#ffaa00"]
                sparkle.color(colors[i % 3])


food = Food()

# ----------------------------
# Enhanced Explosion Effect
# ----------------------------
def create_explosion(x, y, color, intensity=15):
    for _ in range(intensity):
        angle = random.uniform(0, 360)
        speed = random.uniform(3, 10)
        vx = speed * math.cos(math.radians(angle))
        vy = speed * math.sin(math.radians(angle))
        particles.append(Particle(x, y, color, vx, vy))

    for i in range(8):
        angle = i * 45
        speed = 6
        vx = speed * math.cos(math.radians(angle))
        vy = speed * math.sin(math.radians(angle))
        particles.append(Particle(x, y, color, vx, vy, "ring"))

# ----------------------------
# Enhanced Trail Effect with Fading
# ----------------------------
class TrailSegment:
    def __init__(self, x, y, color):
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.color(color)
        self.t.penup()
        self.t.goto(x, y)
        self.life = 15
        self.size = 0.7
        self.t.shapesize(self.size, self.size)

    def update(self):
        self.life -= 1
        self.size *= 0.88
        self.t.shapesize(self.size, self.size)

    def is_dead(self):
        return self.life <= 0 or self.size < 0.05

    def destroy(self):
        self.t.hideturtle()


trails = []

# ----------------------------
# Update Score Display with Shadows
# ----------------------------
def update_ui():
    score_shadow.clear()
    score_shadow.write(f"SCORE: {score}", align="center", font=("Courier", 24, "bold"))
    score_display.clear()
    score_display.write(f"SCORE: {score}", align="center", font=("Courier", 24, "bold"))

    high_shadow.clear()
    high_shadow.write(f"HIGH SCORE: {high_score}", align="center", font=("Courier", 18, "bold"))
    high_score_display.clear()
    high_score_display.write(f"HIGH SCORE: {high_score}", align="center", font=("Courier", 18, "bold"))

    level_shadow.clear()
    level_shadow.write(f"LEVEL: {level}", align="center", font=("Courier", 16, "bold"))
    level_display.clear()
    level_display.write(f"LEVEL: {level}", align="center", font=("Courier", 16, "bold"))

    if combo > 1:
        combo_shadow.clear()
        combo_shadow.write(f"COMBO x{combo}! 🔥", align="center", font=("Courier", 16, "bold"))
        combo_display.clear()
        combo_display.write(f"COMBO x{combo}! 🔥", align="center", font=("Courier", 16, "bold"))
    else:
        combo_display.clear()
        combo_shadow.clear()

# ----------------------------
# Movement Functions
# ----------------------------
def go_up():
    if snake.direction != "down":
        snake.direction = "up"

def go_down():
    if snake.direction != "up":
        snake.direction = "down"

def go_left():
    if snake.direction != "right":
        snake.direction = "left"

def go_right():
    if snake.direction != "left":
        snake.direction = "right"

def toggle_pause():
    global game_paused
    if not game_over:
        game_paused = not game_paused

def restart_game():
    global game_over, game_paused
    if game_over:
        reset_game()
        game_over = False
        game_paused = False

# ----------------------------
# Spawn Power-up
# ----------------------------
def spawn_powerup():
    if random.random() < 0.25 and len(powerups) < 3:
        x = random.randint(-240, 240)
        y = random.randint(-240, 240)
        x = (x // 20) * 20
        y = (y // 20) * 20

        types = ["speed", "slow", "shield", "bonus"]
        powerup_type = random.choice(types)
        powerups.append(PowerUp(x, y, powerup_type))

# ----------------------------
# Level Up System with Effects
# ----------------------------
def level_up():
    global level, delay
    level += 1
    delay = max(0.035, delay - 0.007)
    create_explosion(0, 0, "#00ff88", 25)

    for _ in range(2):
        window.bgcolor("#002200")
        window.update()
        time.sleep(0.05)
        window.bgcolor("#0a0a0a")
        window.update()
        time.sleep(0.05)

# ----------------------------
# Reset Game
# ----------------------------
def reset_game():
    global score, delay, level, combo, invincible, invincible_timer

    for _ in range(5):
        snake.head.color("#ff0000")
        window.update()
        time.sleep(0.08)
        snake.head.color("#00ff88")
        window.update()
        time.sleep(0.08)

    snake.head.goto(0, 0)
    snake.direction = "Stop"

    for seg in segments:
        seg.hideturtle()
    segments.clear()

    for powerup in powerups:
        powerup.destroy()
    powerups.clear()

    score = 0
    level = 1
    combo = 0
    delay = 0.085
    invincible = False
    invincible_timer = 0

    food.respawn()
    update_ui()

    game_over_text.clear()
    game_over_shadow.clear()
    instruction_text.clear()

# ----------------------------
# Keyboard Bindings
# ----------------------------
window.listen()
window.onkey(go_up, "Up")
window.onkey(go_down, "Down")
window.onkey(go_left, "Left")
window.onkey(go_right, "Right")
window.onkey(go_up, "w")
window.onkey(go_down, "s")
window.onkey(go_left, "a")
window.onkey(go_right, "d")
window.onkey(toggle_pause, "space")
window.onkey(restart_game, "r")

# ----------------------------
# Show Game Over Screen
# ----------------------------
def show_game_over():
    global game_over
    game_over = True
    game_over_shadow.write("GAME OVER!", align="center", font=("Courier", 52, "bold"))
    game_over_text.write("GAME OVER!", align="center", font=("Courier", 52, "bold"))
    instruction_text.write("Press 'R' to Restart | Space to Pause", align="center", font=("Courier", 18, "normal"))

# ----------------------------
# Main Game Loop with FPS Counter
# ----------------------------
update_ui()
count = 0
frame_count = 0
fps_timer = time.time()

print("=" * 60)
print("🐍 ULTRA REALISTIC NEON SNAKE - 3D EDITION 🐍")
print("=" * 60)
print("CONTROLS:")
print("  ⬆️ ⬇️ ⬅️ ➡️  Arrow Keys / W A S D - Move")
print("  SPACE - Pause/Resume")
print("  R - Restart (after game over)")
print("\n🎁 POWER-UPS:")
print("  🔵 Shield - Temporary invincibility (120 ticks)")
print("  ⚡ Speed Boost - Move faster temporarily")
print("  🐢 Slow Motion - Slow down time")
print("  💎 Bonus Points - Instant +50 points")
print("\n🍎 FOOD TYPES:")
print("  🔴 Normal Food - 10 points")
print("  🟡 Golden Food - 25 points")
print("  💠 Super Food - 50 points")
print("\n✨ FEATURES:")
print("  • Realistic 3D snake with animated eyes and tongue")
print("  • Physics-based particle system")
print("  • Dynamic trail effects")
print("  • Combo multiplier system")
print("  • Progressive difficulty levels")
print("  • Blinking eyes and tongue flicks")
print("  • Layered glow effects")
print("=" * 60)
print("Good luck! May your combo be infinite! 🎮🔥\n")

while True:
    window.update()
    count += 0.25
    frame_count += 1

    # FPS Counter
    if time.time() - fps_timer >= 1.0:
        fps_display.clear()
        fps_display.write(f"FPS: {frame_count}", align="left", font=("Courier", 10, "normal"))
        frame_count = 0
        fps_timer = time.time()

    if not game_paused and not game_over:
        food.update(count)

        for particle in particles[:]:
            particle.update()
            if particle.is_dead():
                particle.destroy()
                particles.remove(particle)

        for trail in trails[:]:
            trail.update()
            if trail.is_dead():
                trail.destroy()
                trails.remove(trail)

        if snake.direction != "Stop" and random.random() > 0.3:
            color = rainbow_colors[len(segments) % len(rainbow_colors)]
            trails.append(TrailSegment(snake.head.xcor(), snake.head.ycor(), color))

        if random.random() < 0.006:
            spawn_powerup()

        for powerup in powerups[:]:
            powerup.update(count)
            if powerup.is_expired():
                powerup.destroy()
                powerups.remove(powerup)
            elif snake.head.distance(powerup.t) < 24:  # smaller pickup radius
                if powerup.type == "speed":
                    delay = max(0.025, delay - 0.025)
                elif powerup.type == "slow":
                    delay = min(0.18, delay + 0.04)
                elif powerup.type == "shield":
                    invincible = True
                    invincible_timer = 120
                    snake.head.color("#0088ff")
                elif powerup.type == "bonus":
                    score += 50
                    combo += 1

                create_explosion(powerup.t.xcor(), powerup.t.ycor(), powerup.t.color()[0], 20)
                powerup.destroy()
                powerups.remove(powerup)
                update_ui()

        if invincible:
            invincible_timer -= 1
            blink_colors = ["#0088ff", "#00aaff", "#00ccff", "#00ffff"]
            color_index = (invincible_timer // 5) % len(blink_colors)
            snake.head.color(blink_colors[color_index])

            if invincible_timer <= 0:
                invincible = False
                snake.head.color("#00ff88")

        # smaller eat radius
        if snake.head.distance(food.t) < 22:
            if food.type == "normal":
                points = 10
            elif food.type == "golden":
                points = 25
            else:
                points = 50

            score += points * max(1, combo)
            combo += 1

            create_explosion(food.t.xcor(), food.t.ycor(), food.t.color()[0], 25)
            food.respawn()

            new_seg = turtle.Turtle()
            new_seg.speed(0)
            new_seg.shape("circle")

            color_index = len(segments) % len(rainbow_colors)
            new_seg.color(rainbow_colors[color_index])
            new_seg.penup()

            # SMALLER body segments
            size = max(0.4, 1.3 - (len(segments) * 0.01))
            new_seg.shapesize(size, size)
            segments.append(new_seg)

            if score > high_score:
                high_score = score

            if score // 100 > (score - points) // 100:
                level_up()

            update_ui()

        for i in range(len(segments) - 1, 0, -1):
            segments[i].goto(segments[i - 1].xcor(), segments[i - 1].ycor())

        if len(segments) > 0:
            segments[0].goto(snake.head.xcor(), snake.head.ycor())

        snake.move()

        if abs(snake.head.xcor()) > 270 or abs(snake.head.ycor()) > 270:
            if not invincible:
                create_explosion(snake.head.xcor(), snake.head.ycor(), "#ff0000", 30)
                show_game_over()
            else:
                create_explosion(snake.head.xcor(), snake.head.ycor(), "#00ffff", 15)
                if abs(snake.head.xcor()) > 270:
                    snake.head.setx(260 if snake.head.xcor() > 0 else -260)
                if abs(snake.head.ycor()) > 270:
                    snake.head.sety(260 if snake.head.ycor() > 0 else -260)

        for segment in segments[4:]:
            if segment.distance(snake.head) < 16:  # smaller collision radius
                if not invincible:
                    create_explosion(snake.head.xcor(), snake.head.ycor(), "#ff0000", 30)
                    show_game_over()
                    break

    time.sleep(delay)
