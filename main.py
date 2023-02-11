# Import all required modules
import random
import pgzrun
from pgzhelper import *

# Set up the game Screen
TITLE = 'Flappy Bird'
WIDTH = 640
HEIGHT = 488

# Ground
ground = Actor('ground')
ground.x = 320
ground.y = 465

# Bird
bird = Actor('bird1')
bird.x = 75
bird.y = 100
bird.images = ['bird1', 'bird2', 'bird3', 'bird4']
bird.fps = 10

# Game Over
gameover = Actor('gameover')
gameover.x = 320
gameover.y = 200
gameover.scale = 3

# Pipes
top_pipe = Actor('top')
bottom_pipe = Actor('bottom')
top_pipe.x = WIDTH
top_pipe.y = -100
gap = 100
bottom_pipe.x = WIDTH
bottom_pipe.y = top_pipe.height + gap

# Set up game variables
gravity = 0.3 # How fast the bird falls towards the ground
bird.speed = 1 # How fast the bird moves up/down
bird.alive = True
scroll_speed = -4 # Speed at which the pipes move across the screen
score = 0

# What happens when either mouse button is pressed
def on_mouse_down():
    global score

    if bird.alive:
        bird.speed = -6.5 # Make the bird fly up a little
        sounds.wing.play()
    else:
        bird.alive = True # Restarts the game
        score = 0

def update():
    global score

    # Bird
    bird.animate()
    bird.y += bird.speed  # Move the bird down the y-axis at the set speed
    bird.speed += gravity  # The longer the bird falls, the faster it will fall

    # End the game if the bird hits the top or bottom of the screen
    if bird.y > HEIGHT - 40 or bird.y < 0:
        bird.alive = False
        sounds.die.play()

    # Scroll the pipes across the screen
    top_pipe.x += scroll_speed
    bottom_pipe.x += scroll_speed

    # When the pipes hit the left side of the page
    if top_pipe.x < -50:
        offset = random.uniform(-100, -200)
        gap = 150
        top_pipe.midleft = (WIDTH, offset)
        bottom_pipe.midleft = (WIDTH, offset + top_pipe.height + gap)
        score += 1
        sounds.point.play()

    # End of the game if the bird collides with the pipes
    if bird.colliderect(top_pipe) or bird.colliderect(bottom_pipe):
        bird.alive = False
        sounds.hit.play()

def draw():
    screen.blit('bg', (0, 0))  # blit means to draw an image on the page at the given coordinates

    # What happens when the game is playing
    if bird.alive:
        # Draw the actors into the game
        top_pipe.draw()
        bottom_pipe.draw()
        bird.draw()
        ground.draw()

    # What happens when the bird crashes
    else:
        screen.draw.text("Click, your mouse to play again", color='white', center=(320, 300), shadow=(0.5, 0.5), scolor="black", fontsize=30)
        gameover.draw()
        bird.x = 75
        bird.y = 100
        gravity = 0
        bird.speed = 0
        top_pipe.x = WIDTH
        bottom_pipe.x = WIDTH

    screen.draw.text("Score: " + str(score), color='white', midtop=(50, 10), shadow=(0.5, 0.5), scolor="black", fontsize=30)

# For running the pygame zero app
pgzrun.go()
