import pygame
from random import randint

def setup():
    global size, width, height, screen, tile_size, image_size, clock, running, pacman, pacmanrect, pacmanfood, pacmanfoodrect
    global score, level, fps, level_reqs, speeds, speed, velocity_left, velocity_right, velocity_up, velocity_down, velocity
    global scoring_sound

    pygame.init()
    size = width, height = 1280, 720
    tile_size = 40
    image_size = (tile_size, tile_size)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True

    pacman = pygame.image.load("pacmantemp.png").convert()
    pacman = pygame.transform.scale(pacman, image_size) # resize image
    pacmanrect = pacman.get_rect()

    pacmanfood = pygame.image.load("pacmanfood.png").convert()
    pacmanfood = pygame.transform.scale(pacmanfood, image_size) # resize image
    pacmanfoodrect = pacmanfood.get_rect()
    pacmanfoodrect.left = width/2 - tile_size
    pacmanfoodrect.top = height/2 - tile_size

    scoring_sound = pygame.mixer.Sound("eaten.mp3")

    # score_level_text = 1

    # game initial stats
    score = 0
    level = 1
    speeds = [5, 8, 10, 20, 40]
    level_reqs = [5, 15, 30, 50]
    set_velocities(level) # initial speed is 5 (to the right)
    fps = 60
    

def main():
    global size, width, height, screen, tile_size, image_size, clock, running, pacman, pacmanrect, pacmanfood, pacmanfoodrect
    global score, level, fps, level_reqs, speeds, speed, velocity_left, velocity_right, velocity_up, velocity_down, velocity
    global scoring_sound
    setup()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # get user input and change pacman direction accordingly
        keys = pygame.key.get_pressed()
        control_pacman(keys)

        # move pacman
        for _ in range(tile_size // speed):
            pacmanrect = pacmanrect.move(velocity)
            enforce_boundaries()
            clock.tick(fps)

            # Update the screen with new game state
            screen.fill("white")
            screen.blit(pacmanfood, pacmanfoodrect)
            screen.blit(pacman, pacmanrect)
            pygame.display.flip()

        # if there is a collision between pacman and pacmanfood, update score and change pacmanfood position
        if pacmanrect.left == pacmanfoodrect.left and pacmanrect.top == pacmanfoodrect.top:
            pygame.mixer.Sound.play(scoring_sound)
            score += 1
            pacmanfoodrect.left = randint(0, width // tile_size - 1) * 40
            pacmanfoodrect.top = randint(0, height // tile_size - 1) * 40

            if score in level_reqs:
                level += 1
                set_velocities(level)

            # Update the screen with new game state
            screen.fill("white")
            screen.blit(pacmanfood, pacmanfoodrect)
            screen.blit(pacman, pacmanrect)
            pygame.display.flip()


# set speed/velocities everytime level changes
def set_velocities(level):
    global speeds, speed, velocity_left, velocity_right, velocity_up, velocity_down, velocity

    if level > 1:
        prev_speed = speed          # to be used later
    else:
        prev_speed = speeds[0]      # filler

    speed = speeds[level - 1]       # speeds = [5, 10, 20, 40]
    velocity_left = [-speed, 0]
    velocity_right = [speed, 0]
    velocity_up = [0, -speed]
    velocity_down = [0, speed]
    if level == 1:
        velocity = velocity_right
    else:
        velocity[0] = (velocity[0] // prev_speed) * speed
        velocity[1] = (velocity[1] // prev_speed) * speed


# ensure pacman stays within boundaries
def enforce_boundaries():
    global pacmanrect, velocity
    
    if pacmanrect.left < 0:
        pacmanrect.left = 0
    elif pacmanrect.right > width:
        pacmanrect.right = width
    if pacmanrect.top < 0:
        pacmanrect.top = 0
    elif pacmanrect.bottom > height:
        pacmanrect.bottom = height


# allow user to control direction of pacman
def control_pacman(keys):
    global pacmanrect, velocity, velocity_left, velocity_right, velocity_up, velocity_down
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if pacmanrect.left > 0:
            velocity = velocity_left
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if pacmanrect.right < width:
            velocity = velocity_right
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if pacmanrect.top > 0:
            velocity = velocity_up
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if pacmanrect.bottom < height:
            velocity = velocity_down

main()
pygame.quit()
