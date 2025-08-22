from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 300
SPACE_SIZE = 50
BODY_PARTS = 3

# Available fruit emojis (all red shades)
FOOD_OPTIONS = ["🍎", "🍒", "🍓", "🍅", "🌶️", "🍉"]

BACKGROUND_COLOR_TOP = "#000000"     # gradient top color
BACKGROUND_COLOR_BOTTOM = "#434343"  # gradient bottom color


class Snake:

    def __init__(self, color):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.color = color

        for i in range(0, BODY_PARTS):
            self.coordinates.append([i * SPACE_SIZE, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                                             fill=self.color, tag="snake")
            self.squares.append(square)


class Food:

    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]

        self.food_icon = random.choice(FOOD_OPTIONS)

        # Draw "neon glow" effect: outer shadow + main emoji
        for offset in range(3, 0, -1):  # 3 layers of glow
            canvas.create_text(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2,
                               text=self.food_icon,
                               font=("Arial", SPACE_SIZE // 2 + offset),
                               fill="#FF0033",  # neon red glow
                               tag="food")
        # Actual emoji (front)
        canvas.create_text(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2,
                           text=self.food_icon,
                           font=("Arial", SPACE_SIZE // 2),
                           tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                                     fill=snake.color)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 80,
                       font=('consolas', 30), text="Press R to Restart", fill="white", tag="restart")
    window.bind('<r>', restart_game)


def restart_game(event):
    global score, direction, snake, food
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    canvas.delete(ALL)
    draw_gradient_background()
    snake = Snake(SNAKE_COLOR)
    food = Food()
    next_turn(snake, food)


def draw_gradient_background():
    """Draw vertical gradient background"""
    r1, g1, b1 = window.winfo_rgb(BACKGROUND_COLOR_TOP)
    r2, g2, b2 = window.winfo_rgb(BACKGROUND_COLOR_BOTTOM)
    r_ratio = (r2 - r1) / GAME_HEIGHT
    g_ratio = (g2 - g1) / GAME_HEIGHT
    b_ratio = (b2 - b1) / GAME_HEIGHT

    for i in range(GAME_HEIGHT):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
        canvas.create_line(0, i, GAME_WIDTH, i, fill=color)


# ---------------- Main Program ----------------
window = Tk()
window.title("Snake Game - Neon Edition")
window.resizable(False, False)

# Ask user to pick snake color randomly from cyberpunk palette
SNAKE_COLOR = random.choice(["#00FF00", "#FFD700", "#1E90FF", "#FF1493", "#FF8C00"])

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Center window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind keys
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Start game
draw_gradient_background()
snake = Snake(SNAKE_COLOR)
food = Food()
next_turn(snake, food)

window.mainloop()
#byDishantBhere
