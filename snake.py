import turtle
import time
import random
import math


window = turtle.Screen()
window.title("SNAKE ")
window.setup(width=700, height=700)
window.bgcolor("#000000")
window.tracer(0)

# ----------------------------
# Particle System for Effects
# ----------------------------
class Particle:
    def __init__(self, x, y, color, vx=None, vy=None):
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.color(color)
        self.t.penup()
        self.t.goto(x, y)
        self.t.shapesize(0.3, 0.3)
        self.vx = vx if vx else random.uniform(-3, 3)
        self.vy = vy if vy else random.uniform(-3, 3)
        self.life = 20
        
    def update(self):
        self.t.goto(self.t.xcor() + self.vx, self.t.ycor() + self.vy)
        self.vy -= 0.3  # Gravity
        self.life -= 1
        size = max(0.1, self.life / 40)
        self.t.shapesize(size, size)
        
    def is_dead(self):
        return self.life <= 0
    
    def destroy(self):
        self.t.hideturtle()
        del self.t

particles = []

# ----------------------------
# Animated Grid Background
# ----------------------------
grid = turtle.Turtle()
grid.speed(0)
grid.color("#1a1a3e")
grid.penup()
grid.width(1)
for i in range(-250, 251, 40):
    grid.goto(i, -250)
    grid.pendown()
    grid.goto(i, 250)
    grid.penup()
    grid.goto(-250, i)
    grid.pendown()
    grid.goto(250, i)
    grid.penup()
grid.hideturtle()

# Border glow effect
border = turtle.Turtle()
border.speed(0)
border.color("#ff00ff")
border.penup()
border.width(3)
border.goto(-240, -240)
border.pendown()
for _ in range(4):
    border.forward(480)
    border.left(90)
border.penup()
border.hideturtle()

# ----------------------------
# Professional UI Elements
# ----------------------------
def create_text_display(y_pos, color, size=18):
    display = turtle.Turtle()
    display.speed(0)
    display.color(color)
    display.penup()
    display.hideturtle()
    display.goto(0, y_pos)
    return display

score_display = create_text_display(260, "#00ff88", 22)
high_score_display = create_text_display(285, "#ffaa00", 18)
level_display = create_text_display(235, "#00ddff", 16)
combo_display = create_text_display(210, "#ff0088", 16)

# Game Over Screen
game_over_text = turtle.Turtle()
game_over_text.speed(0)
game_over_text.color("#ff0000")
game_over_text.penup()
game_over_text.hideturtle()
game_over_text.goto(0, 0)

instruction_text = turtle.Turtle()
instruction_text.speed(0)
instruction_text.color("#ffffff")
instruction_text.penup()
instruction_text.hideturtle()
instruction_text.goto(0, -50)

# ----------------------------
# Advanced Snake Head with Realistic Eyes
# ----------------------------
class SnakeHead:
    def __init__(self):
        # Main head
        self.head = turtle.Turtle()
        self.head.shape("circle")
        self.head.color("#00ff88")
        self.head.penup()
        self.head.goto(0, 0)
        self.head.shapesize(1.8, 1.8)
        self.direction = "Stop"
        
        # Glow effect
        self.glow = turtle.Turtle()
        self.glow.shape("circle")
        self.glow.color("#00ff88")
        self.glow.penup()
        self.glow.shapesize(2.5, 2.5)
        
        # Eyes
        self.left_eye = self.create_eye()
        self.right_eye = self.create_eye()
        self.left_pupil = self.create_pupil()
        self.right_pupil = self.create_pupil()
        
        # Tongue
        self.tongue = turtle.Turtle()
        self.tongue.shape("square")
        self.tongue.color("#ff0066")
        self.tongue.penup()
        self.tongue.shapesize(0.1, 0.6)
        self.tongue.hideturtle()
        
    def create_eye(self):
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
    
    def update_position(self):
        self.glow.goto(self.head.xcor(), self.head.ycor())
        self.update_eyes()
        
    def update_eyes(self):
        x, y = self.head.xcor(), self.head.ycor()
        
        eye_offset = 10
        pupil_offset = 3
        
        if self.direction == "up":
            self.left_eye.goto(x - 8, y + 12)
            self.right_eye.goto(x + 8, y + 12)
            self.left_pupil.goto(x - 8, y + 14)
            self.right_pupil.goto(x + 8, y + 14)
            self.tongue.goto(x, y + 18)
            self.tongue.setheading(90)
        elif self.direction == "down":
            self.left_eye.goto(x - 8, y - 12)
            self.right_eye.goto(x + 8, y - 12)
            self.left_pupil.goto(x - 8, y - 14)
            self.right_pupil.goto(x + 8, y - 14)
            self.tongue.goto(x, y - 18)
            self.tongue.setheading(270)
        elif self.direction == "left":
            self.left_eye.goto(x - 12, y + 8)
            self.right_eye.goto(x - 12, y - 8)
            self.left_pupil.goto(x - 14, y + 8)
            self.right_pupil.goto(x - 14, y - 8)
            self.tongue.goto(x - 18, y)
            self.tongue.setheading(180)
        elif self.direction == "right":
            self.left_eye.goto(x + 12, y + 8)
            self.right_eye.goto(x + 12, y - 8)
            self.left_pupil.goto(x + 14, y + 8)
            self.right_pupil.goto(x + 14, y - 8)
            self.tongue.goto(x + 18, y)
            self.tongue.setheading(0)
        else:
            self.left_eye.goto(x - 8, y + 6)
            self.right_eye.goto(x + 8, y + 6)
            self.left_pupil.goto(x - 8, y + 6)
            self.right_pupil.goto(x + 8, y + 6)
            self.tongue.hideturtle()
            return
        
        # Show tongue when moving
        if random.random() > 0.95:
            self.tongue.showturtle()
        else:
            self.tongue.hideturtle()
    
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
# Power-up System
# ----------------------------
class PowerUp:
    def __init__(self, x, y, type_name):
        self.t = turtle.Turtle()
        self.t.shape("square")
        self.t.penup()
        self.t.goto(x, y)
        self.type = type_name
        self.life = 200  # Disappears after time
        
        if type_name == "speed":
            self.t.color("#00ffff")
            self.t.shapesize(0.8, 0.8)
        elif type_name == "slow":
            self.t.color("#ffff00")
            self.t.shapesize(0.8, 0.8)
        elif type_name == "shield":
            self.t.color("#0088ff")
            self.t.shapesize(1.0, 1.0)
        elif type_name == "bonus":
            self.t.color("#ff00ff")
            self.t.shapesize(0.9, 0.9)
    
    def update(self, count):
        self.life -= 1
        # Rotating animation
        self.t.setheading(count * 10)
        # Pulsing
        scale = 0.8 + 0.2 * math.sin(count * 0.3)
        if self.type == "shield":
            self.t.shapesize(scale + 0.2, scale + 0.2)
        else:
            self.t.shapesize(scale, scale)
    
    def is_expired(self):
        return self.life <= 0
    
    def destroy(self):
        self.t.hideturtle()

powerups = []

# ----------------------------
# Game State Variables
# ----------------------------
segments = []
score = 0
high_score = 0
level = 1
combo = 0
delay = 0.09
game_paused = False
game_over = False
invincible = False
invincible_timer = 0

# Rainbow gradient colors
rainbow_colors = [
    "#00ff88", "#00ffaa", "#00ffcc", "#00ffff",
    "#00ccff", "#00aaff", "#0088ff", "#0066ff",
    "#6600ff", "#8800ff", "#aa00ff", "#ff00ff",
    "#ff00aa", "#ff0088", "#ff0066"
]

# ----------------------------
# Food System with Multiple Types
# ----------------------------
class Food:
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.penup()
        self.t.shapesize(1.3, 1.3)
        
        # Glow rings
        self.rings = []
        for i in range(3):
            ring = turtle.Turtle()
            ring.shape("circle")
            ring.penup()
            ring.color("#ff006e")
            self.rings.append(ring)
        
        # Sparkles
        self.sparkles = []
        for i in range(6):
            sparkle = turtle.Turtle()
            sparkle.shape("circle")
            sparkle.color("#ffff00")
            sparkle.penup()
            sparkle.shapesize(0.25, 0.25)
            self.sparkles.append(sparkle)
        
        self.type = "normal"
        self.respawn()
    
    def respawn(self):
        x = random.randint(-220, 220)
        y = random.randint(-220, 220)
        x = (x // 20) * 20
        y = (y // 20) * 20
        self.t.goto(x, y)
        
        # Random food type
        rand = random.random()
        if rand < 0.7:
            self.type = "normal"
            self.t.color("#ff006e")
        elif rand < 0.85:
            self.type = "golden"
            self.t.color("#ffd700")
        else:
            self.type = "super"
            self.t.color("#00ffff")
    
    def update(self, count):
        # Pulsing animation
        scale = 1.1 + 0.3 * math.sin(count * 4)
        self.t.shapesize(scale, scale)
        
        # Glow rings
        for i, ring in enumerate(self.rings):
            ring_scale = scale + 0.5 + i * 0.3
            ring.shapesize(ring_scale, ring_scale)
            ring.goto(self.t.xcor(), self.t.ycor())
        
        # Orbiting sparkles
        for i, sparkle in enumerate(self.sparkles):
            angle = count * 8 + (i * 60)
            radius = 30 + 5 * math.sin(count * 3 + i)
            x = self.t.xcor() + radius * math.cos(math.radians(angle))
            y = self.t.ycor() + radius * math.sin(math.radians(angle))
            sparkle.goto(x, y)
            
            # Color based on food type
            if self.type == "golden":
                sparkle.color("#ffaa00")
            elif self.type == "super":
                sparkle.color("#00ffff")
            else:
                sparkle.color("#ffff00")

food = Food()

# ----------------------------
# Explosion Effect
# ----------------------------
def create_explosion(x, y, color):
    for _ in range(15):
        angle = random.uniform(0, 360)
        speed = random.uniform(2, 8)
        vx = speed * math.cos(math.radians(angle))
        vy = speed * math.sin(math.radians(angle))
        particles.append(Particle(x, y, color, vx, vy))

# ----------------------------
# Trail Effect
# ----------------------------
class TrailSegment:
    def __init__(self, x, y, color):
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.color(color)
        self.t.penup()
        self.t.goto(x, y)
        self.life = 10
        self.size = 0.5
        self.t.shapesize(self.size, self.size)
    
    def update(self):
        self.life -= 1
        self.size *= 0.9
        self.t.shapesize(self.size, self.size)
    
    def is_dead(self):
        return self.life <= 0
    
    def destroy(self):
        self.t.hideturtle()

trails = []

# ----------------------------
# Update Score Display
# ----------------------------
def update_ui():
    score_display.clear()
    score_display.write(f"SCORE: {score}", align="center", font=("Courier", 24, "bold"))
    
    high_score_display.clear()
    high_score_display.write(f"HIGH SCORE: {high_score}", align="center", font=("Courier", 18, "bold"))
    
    level_display.clear()
    level_display.write(f"LEVEL: {level}", align="center", font=("Courier", 16, "bold"))
    
    if combo > 1:
        combo_display.clear()
        combo_display.write(f"COMBO x{combo}!", align="center", font=("Courier", 16, "bold"))
    else:
        combo_display.clear()

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
    if random.random() < 0.3 and len(powerups) < 2:
        x = random.randint(-220, 220)
        y = random.randint(-220, 220)
        x = (x // 20) * 20
        y = (y // 20) * 20
        
        types = ["speed", "slow", "shield", "bonus"]
        powerup_type = random.choice(types)
        powerups.append(PowerUp(x, y, powerup_type))

# ----------------------------
# Level Up System
# ----------------------------
def level_up():
    global level, delay
    level += 1
    delay = max(0.04, delay - 0.008)
    create_explosion(0, 0, "#00ff88")

# ----------------------------
# Reset Game
# ----------------------------
def reset_game():
    global score, delay, level, combo, invincible, invincible_timer, game_over
    
    # Flash effect
    for _ in range(3):
        snake.head.color("#ff0000")
        window.update()
        time.sleep(0.1)
        snake.head.color("#00ff88")
        window.update()
        time.sleep(0.1)
    
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
    delay = 0.09
    invincible = False
    invincible_timer = 0
    
    food.respawn()
    update_ui()
    
    game_over_text.clear()
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
    game_over_text.write("GAME OVER!", align="center", font=("Courier", 48, "bold"))
    instruction_text.write("Press 'R' to Restart", align="center", font=("Courier", 20, "normal"))

# ----------------------------
# Main Game Loop
# ----------------------------
update_ui()
count = 0

print("=" * 50)
print("🐍 ULTRA REALISTIC NEON SNAKE 🐍")
print("=" * 50)
print("CONTROLS:")
print("  Arrow Keys / WASD - Move")
print("  SPACE - Pause")
print("  R - Restart (after game over)")
print("\nPOWER-UPS:")
print("  🔵 Shield - Temporary invincibility")
print("  ⚡ Speed - Move faster")
print("  🐢 Slow - Move slower")
print("  💎 Bonus - Extra points")
print("\nFOOD TYPES:")
print("  🔴 Normal - 10 points")
print("  🟡 Golden - 25 points")
print("  💠 Super - 50 points")
print("=" * 50)
print("Good luck! 🎮\n")

while True:
    window.update()
    count += 0.2
    
    if not game_paused and not game_over:
        # Update food animation
        food.update(count)
        
        # Update particles
        for particle in particles[:]:
            particle.update()
            if particle.is_dead():
                particle.destroy()
                particles.remove(particle)
        
        # Update trail effects
        for trail in trails[:]:
            trail.update()
            if trail.is_dead():
                trail.destroy()
                trails.remove(trail)
        
        # Add trail when moving
        if snake.direction != "Stop" and random.random() > 0.5:
            color = rainbow_colors[len(segments) % len(rainbow_colors)]
            trails.append(TrailSegment(snake.head.xcor(), snake.head.ycor(), color))
        
        # Update and spawn power-ups
        if random.random() < 0.005:
            spawn_powerup()
        
        for powerup in powerups[:]:
            powerup.update(count)
            if powerup.is_expired():
                powerup.destroy()
                powerups.remove(powerup)
            elif snake.head.distance(powerup.t) < 25:
                if powerup.type == "speed":
                    delay = max(0.03, delay - 0.02)
                elif powerup.type == "slow":
                    delay = min(0.15, delay + 0.03)
                elif powerup.type == "shield":
                    invincible = True
                    invincible_timer = 100
                    snake.head.color("#0088ff")
                elif powerup.type == "bonus":
                    score += 50
                    combo += 1
                
                create_explosion(powerup.t.xcor(), powerup.t.ycor(), powerup.t.color()[0])
                powerup.destroy()
                powerups.remove(powerup)
                update_ui()
        
        # Update invincibility
        if invincible:
            invincible_timer -= 1
            # Blinking effect
            if invincible_timer % 10 < 5:
                snake.head.color("#0088ff")
            else:
                snake.head.color("#00ffff")
            
            if invincible_timer <= 0:
                invincible = False
                snake.head.color("#00ff88")
        
        # Check if snake ate food
        if snake.head.distance(food.t) < 25:
            # Points based on food type
            if food.type == "normal":
                points = 10
            elif food.type == "golden":
                points = 25
            else:  # super
                points = 50
            
            score += points * max(1, combo)
            combo += 1
            
            # Explosion effect
            create_explosion(food.t.xcor(), food.t.ycor(), food.t.color()[0])
            
            # Respawn food
            food.respawn()
            
            # Create new body segment
            new_seg = turtle.Turtle()
            new_seg.speed(0)
            new_seg.shape("circle")
            
            # Rainbow gradient
            color_index = len(segments) % len(rainbow_colors)
            new_seg.color(rainbow_colors[color_index])
            new_seg.penup()
            
            # Tapering - segments get smaller
            size = max(0.6, 1.5 - (len(segments) * 0.012))
            new_seg.shapesize(size, size)
            segments.append(new_seg)
            
            # Update score
            if score > high_score:
                high_score = score
            
            # Level up every 100 points
            if score // 100 > (score - points) // 100:
                level_up()
            
            update_ui()
        
        # Move body segments
        for i in range(len(segments) - 1, 0, -1):
            segments[i].goto(segments[i - 1].xcor(), segments[i - 1].ycor())
        
        if len(segments) > 0:
            segments[0].goto(snake.head.xcor(), snake.head.ycor())
        
        # Move head
        snake.move()
        
        # Check wall collision
        if abs(snake.head.xcor()) > 240 or abs(snake.head.ycor()) > 240:
            if not invincible:
                create_explosion(snake.head.xcor(), snake.head.ycor(), "#ff0000")
                show_game_over()
            else:
                # Bounce back
                if abs(snake.head.xcor()) > 240:
                    snake.head.setx(230 if snake.head.xcor() > 0 else -230)
                if abs(snake.head.ycor()) > 240:
                    snake.head.sety(230 if snake.head.ycor() > 0 else -230)
        
        # Check self collision
        for segment in segments[3:]:  # Skip first 3 to avoid false collision
            if segment.distance(snake.head) < 18:
                if not invincible:
                    create_explosion(snake.head.xcor(), snake.head.ycor(), "#ff0000")
                    show_game_over()
                    break
    
    time.sleep(delay)