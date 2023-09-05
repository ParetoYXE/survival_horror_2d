import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Define screen dimensions and colors
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Survival Horror Game")

# Load images
def load_images():
    images = {}
    images["tree"] = pygame.image.load("tree.png").convert_alpha()
    images["forest_house"] = pygame.image.load("Forest_House.png").convert_alpha()
    images["player"] = pygame.image.load("player.png").convert_alpha()
    images["hunter"] = pygame.image.load("hunter.png").convert_alpha()
    return images

# Initialize player variables
player_x = SCREEN_WIDTH // 4  # Adjust player spawn location
player_y = SCREEN_HEIGHT // 4  # Adjust player spawn location
player_speed = 0.25
player_width = 32
player_height = 50

# Initialize hunter variables
hunter_speed = 0.1  # Lower speed for testing
hunter_width = player_width
hunter_height = player_height



# Define objects on the screen
screens = {

    'screen 1': {'objects':[
        ("tree", (100, 100)),
        ("tree", (100, 300)),
        ("tree", (600, 200)),
        ("forest_house", (300, 200)),
        ("forest_house", (700, 200)),
        ("forest_house", (300, 500)),
        # Add more objects as needed
    ],

    'hunters':[
        {
            "x": SCREEN_WIDTH - player_width,
            "y": SCREEN_HEIGHT - player_height,
            "last_known_player_x": None,
            "last_known_player_y": None,
            "state": "wander",  # Initialize state as "wander"
            "patrol_direction": None,  # Initialize patrol direction
            "patrol_timer": 0,  # Initialize patrol timer
        },

        {
            "x": SCREEN_WIDTH - player_width,
            "y": SCREEN_HEIGHT - player_height,
            "last_known_player_x": None,
            "last_known_player_y": None,
            "state": "wander",  # Initialize state as "wander"
            "patrol_direction": None,  # Initialize patrol direction
            "patrol_timer": 0,  # Initialize patrol timer
        },
    ]}


}

# Render function
def render_screen(screen_data, images, player_x, player_y, hunters):
    screen.fill(BLACK)

    for object_name, (x, y) in screen_data:
        if object_name in images:
            screen.blit(images[object_name], (x, y))

    player_image = pygame.transform.scale(images["player"], (player_width, player_height))
    screen.blit(player_image, (player_x, player_y))

    for hunter in hunters:
        hunter_image = pygame.transform.scale(images["hunter"], (hunter_width, hunter_height))
        screen.blit(hunter_image, (hunter["x"], hunter["y"]))

    pygame.display.flip()

# Collision detection function
def check_collision(x, y, images,objects):
    for object_name, (obj_x, obj_y) in objects:
        obj_width = images[object_name].get_width()
        obj_height = images[object_name].get_height()

        if (
            x < obj_x + obj_width
            and x + player_width > obj_x
            and y < obj_y + obj_height
            and y + player_height > obj_y
        ):
            return True  # Collision detected

    return False  # No collision

# Push the object back when collision occurs
def push_back(x, y, dx, dy, images):
    while check_collision(x, y, images):
        x += dx
        y += dy
    return x, y


import random

# NPC AI function
def npc_ai(hunter, player_x, player_y, images,objects):
    # Extract hunter information
    hunter_x = hunter["x"]
    hunter_y = hunter["y"]
    last_known_player_x = hunter["last_known_player_x"]
    last_known_player_y = hunter["last_known_player_y"]
    state = hunter["state"]
    patrol_direction = hunter.get("patrol_direction", None)
    patrol_timer = hunter.get("patrol_timer", 0)
    collision_count = hunter.get("collision_count", 0)

    # Calculate the direction from the hunter to the player
    dx = player_x - hunter_x
    dy = player_y - hunter_y

    # Calculate the distance between the hunter and the player
    distance = pygame.math.Vector2(dx, dy).length()

    if distance > 0:
        # Normalize the direction vector
        dx /= distance
        dy /= distance

    # Check if there is a clear line of sight to the player
    line_of_sight = True

    # Check for collision with objects along the line of sight
    step = 5  # Adjust the step size for checking
    for i in range(0, int(distance), step):
        check_x = hunter_x + dx * i
        check_y = hunter_y + dy * i

        if check_collision(check_x, check_y, images,objects):
            line_of_sight = False
            break

    if line_of_sight:
        # If there is a clear line of sight, sprint towards the player
        new_x = hunter_x + dx * (hunter_speed + 0.15)  # Increase speed slightly
        new_y = hunter_y + dy * (hunter_speed + 0.15)  # Increase speed slightly

        # Check for collision with objects
        if not check_collision(new_x, new_y, images,objects):
            hunter_x = new_x
            hunter_y = new_y
            # Update last known player location
            hunter["last_known_player_x"] = player_x
            hunter["last_known_player_y"] = player_y
            collision_count = 0
    else:
        # If no line of sight, patrol in a chosen direction
        if patrol_direction is None:
            # Randomly choose a patrol direction
            patrol_direction = random.choice(["left", "right", "up", "down"])
            hunter["patrol_direction"] = patrol_direction
            # Reset the patrol timer
            patrol_timer = 0

        # Move in the chosen patrol direction
        if patrol_direction == "left":
            new_x = hunter_x - hunter_speed
            new_y = hunter_y
        elif patrol_direction == "right":
            new_x = hunter_x + hunter_speed
            new_y = hunter_y
        elif patrol_direction == "up":
            new_x = hunter_x
            new_y = hunter_y - hunter_speed
        elif patrol_direction == "down":
            new_x = hunter_x
            new_y = hunter_y + hunter_speed

        # Check for collision with objects
        if not check_collision(new_x, new_y, images,objects):
            hunter_x = new_x
            hunter_y = new_y
            collision_count = 0

        # Update the patrol timer
        patrol_timer += 1

        # If patrol timer exceeds a certain value, randomly choose a new patrol direction
        if patrol_timer >= 2000:  # Adjust the timer value as needed
            patrol_direction = random.choice(["left", "right", "up", "down"])
            hunter["patrol_direction"] = patrol_direction
            # Reset the patrol timer
            patrol_timer = 0

    # Check for collision with objects and change direction if stuck
    if check_collision(hunter_x, hunter_y, images,objects):
        collision_count += 1

        if collision_count >= 5:  # Adjust the collision count threshold as needed
            # Change direction randomly
            patrol_direction = random.choice(["left", "right", "up", "down"])
            hunter["patrol_direction"] = patrol_direction
            collision_count = 0

    # Update the hunter's position in the object
    hunter["x"] = hunter_x
    hunter["y"] = hunter_y
    hunter["patrol_timer"] = patrol_timer
    hunter["collision_count"] = collision_count

    return hunter


# ... (Previous code remains unchanged)
# ... (Previous code remains unchanged)

# Initialize the game-over and win states
game_over = False
win = False

# Main game loop
def main():
    global player_x, player_y, win, game_over
    images = load_images()

    current_screen = "screen 1"
    objects = screens[current_screen]['objects']
    hunters = screens[current_screen]['hunters']

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()

        new_x = player_x
        new_y = player_y

        if keys[pygame.K_a]:
            new_x -= player_speed
        if keys[pygame.K_d]:
            new_x += player_speed
        if keys[pygame.K_w]:
            new_y -= player_speed
        if keys[pygame.K_s]:
            new_y += player_speed

        # Check for collision before updating the player's position
        if not check_collision(new_x, new_y, images, objects):
            player_x = new_x
            player_y = new_y

        # Check if the player reaches the bottom right corner
        if player_x >= SCREEN_WIDTH - player_width and player_y >= SCREEN_HEIGHT - player_height:
            win = True  # Set win to True

        # NPC AI for each hunter
        for hunter in hunters:
            hunter = npc_ai(hunter, player_x, player_y, images, objects)

        # Check for collision between player and hunters
        for hunter in hunters:
            hunter_rect = pygame.Rect(hunter["x"], hunter["y"], hunter_width, hunter_height)
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

            if hunter_rect.colliderect(player_rect):
                game_over = True  # Set game over to True on collision

        # Render win screen if win is True
        if win:
            # Display "You Win" on the screen
            win_font = pygame.font.Font(None, 100)
            win_text = win_font.render("You Win", True, (0, 255, 0))
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            screen.fill(BLACK)
            screen.blit(win_text, win_rect)
            pygame.display.flip()
        # Render game-over screen if game over is True
        elif game_over:
            # Display "Condemned" on the screen
            game_over_font = pygame.font.Font(None, 100)
            game_over_text = game_over_font.render("Condemned", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            screen.fill(BLACK)
            screen.blit(game_over_text, game_over_rect)
            pygame.display.flip()
        else:
            render_screen(objects, images, player_x, player_y, hunters)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
