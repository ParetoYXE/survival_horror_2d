import pygame
import sys
import random
import pygame.mixer  # Import the mixer module
# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer
# Define screen dimensions and colors
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Survival Horror Game")



def load_images(scale_factor=1.2):
    images = {}
    original_tree = pygame.image.load("tree.png").convert_alpha()
    images["tree"] = pygame.transform.scale(original_tree, (int(original_tree.get_width() * scale_factor), int(original_tree.get_height() * scale_factor)))

    original_forest_house = pygame.image.load("Forest_House.png").convert_alpha()
    images["forest_house"] = pygame.transform.scale(original_forest_house, (int(original_forest_house.get_width() * scale_factor), int(original_forest_house.get_height() * scale_factor)))

    original_player = pygame.image.load("player.png").convert_alpha()
    images["player"] = pygame.transform.scale(original_player, (int(original_player.get_width() * scale_factor), int(original_player.get_height() * scale_factor)))

    original_hunter = pygame.image.load("hunter.png").convert_alpha()
    images["hunter"] = pygame.transform.scale(original_hunter, (int(original_hunter.get_width() * scale_factor), int(original_hunter.get_height() * scale_factor)))

    original_sign = pygame.image.load("sign_1.png").convert_alpha()
    images["sign_1"] = pygame.transform.scale(original_sign, (int(original_sign.get_width() * scale_factor), int(original_sign.get_height() * scale_factor)))

    original_apartment = pygame.image.load("Apartment.png").convert_alpha()
    images['apartment'] = pygame.transform.scale(original_apartment, (int(original_apartment.get_width() * scale_factor), int(original_apartment.get_height() * scale_factor)))

    original_light = pygame.image.load("light.png").convert_alpha()
    images["light"] = pygame.transform.scale(original_light, (int(original_light.get_width() * scale_factor), int(original_light.get_height() * scale_factor)))

    return images

# Initialize player variables
player_x = SCREEN_WIDTH // 4  # Adjust player spawn location
player_y = SCREEN_HEIGHT // 4  # Adjust player spawn location
player_speed = 2
player_width = 32
player_height = 50
player_inventory = []

# Initialize hunter variables
hunter_speed = 1.5  # Lower speed for testing
hunter_width = player_width
hunter_height = player_height

# Define objects on the screen as dictionaries
screens = {
    'screen 1': {
        'objects': [
            {"name": "tree", "position": (100, 100), "collide": True, 'render_layer':0},
            {"name": "tree", "position": (100, 300), "collide": True, 'render_layer':0},
            {"name": "tree", "position": (600, 200), "collide": True, 'render_layer':0},
            {"name": "forest_house", "position": (300, 200), "collide": True, 'render_layer':0},
            {"name": "forest_house", "position": (700, 200), "collide": True, 'render_layer':0},
            {"name": "forest_house", "position": (300, 500), "collide": True, 'render_layer':0},
            {"name": "sign_1", "position": (530, 300), "collide": False, 'render_layer':2},
            {"name": "light", "position": (530, 400), "collide": False, 'render_layer':2},
            # Add more objects as needed
        ],
        'hunters': [
        ],
        'transitions': {
            'North': None,  # No transition to the north
            'East': 'screen 2',  # Transition to 'screen 2' when moving east
            'South': 'screen 3',  # No transition to the south
            'West': None,  # No transition to the west
        },
    },
     'screen 2': {
        'objects': [
            {"name": "tree", "position": (300, 100), "collide": True, 'render_layer':0},
            {"name": "tree", "position": (400, 200), "collide": True, 'render_layer':0},
            {"name": "forest_house", "position": (100, 200), "collide": True, 'render_layer':0},
            {"name": "apartment", "position": (600, 0), "collide": True, 'render_layer':0},
        ],
        'hunters': [
            {
                "x":800,
                "y": 700,
                "last_known_player_x": None,
                "last_known_player_y": None,
                "state": "wander",  # Initialize state as "wander"
                "patrol_direction": None,  # Initialize patrol direction
                "patrol_timer": 0,  # Initialize patrol timer
            },
            {
                "x": 700,
                "y": 700,
                "last_known_player_x": None,
                "last_known_player_y": None,
                "state": "wander",  # Initialize state as "wander"
                "patrol_direction": None,  # Initialize patrol direction
                "patrol_timer": 0,  # Initialize patrol timer
            },
            {
                "x": 730,
                "y": 700,
                "last_known_player_x": None,
                "last_known_player_y": None,
                "state": "wander",  # Initialize state as "wander"
                "patrol_direction": None,  # Initialize patrol direction
                "patrol_timer": 0,  # Initialize patrol timer
            },
            {
                "x": 730,
                "y": 800,
                "last_known_player_x": None,
                "last_known_player_y": None,
                "state": "wander",  # Initialize state as "wander"
                "patrol_direction": None,  # Initialize patrol direction
                "patrol_timer": 0,  # Initialize patrol timer
            },
        ],
        'transitions': {
            'North': None,  # No transition to the north
            'East': None,  # No transition to the east
            'South': None,  # No transition to the south
            'West': 'screen 1',  # Transition to 'screen 1' when moving west
        },
    },
     'screen 3': {
        'objects': [
            {"name": "forest_house", "position": (100, 200), "collide": True, 'render_layer':0},
            {"name": "forest_house", "position": (100, 500), "collide": True, 'render_layer':0},
            {"name": "tree", "position": (500, 100), "collide": True, 'render_layer':0},
            {"name": "tree", "position": (600, 200), "collide": True, 'render_layer':0},
            {"name": "tree", "position": (600, 400), "collide": True, 'render_layer':0},
        ],
        'hunters': [
            {
                "x": 300,
                "y": 450,
                "last_known_player_x": None,
                "last_known_player_y": None,
                "state": "wander",  # Initialize state as "wander"
                "patrol_direction": None,  # Initialize patrol direction
                "patrol_timer": 0,  # Initialize patrol timer
            },
        ],
        'transitions': {
            'North': 'screen 1',  # Add a transition to screen 1 to the north
            'East': None,
            'South': None,
            'West': None,
        },
    }
}


# Load font
font = pygame.font.Font(None, 20)

def center_text(text):
    # Get the text's rect and center it on the screen
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    return text_rect

def intro(screen):
    # Define the intro text
    intro_text = [
        "I shouldn't be here. This area of the 'city' fell to the rot and into the hand of gangs close to a decade ago.",
        "I'm stuck though. Those bastard wise guys dropped me outside of town with no money and I need to hike my ass East.",
        "Least until I can reach the 'core' and to my apartment.",
        "I'm pretty sure this is 'pagan' turf. I'll need to watch out for those fucking psychos.",
        ""
    ]

    # Initialize variables
    text_color = WHITE
    line_spacing = 40

    intro_complete = False
    current_line = 1

    while not intro_complete:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                current_line += 1
                if current_line == len(intro_text):
                    intro_complete = True

        screen.fill(BLACK)

        # Render each line of the intro text centered on the screen
        text_surface = font.render(intro_text[0], True, text_color)
        text_rect = center_text(text_surface)
        text_rect.y += 0 * line_spacing
        screen.blit(text_surface, text_rect)

        for i in range(1,current_line):
            text_surface = font.render(intro_text[i], True, text_color)
            text_rect = center_text(text_surface)
            text_rect.y += i * line_spacing
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        pygame.time.delay(100)
        pygame.mixer.music.load("bgmusic.mp3")  # Load your background music file
        pygame.mixer.music.set_volume(0.5)  # Set the volume (adjust as needed)
        pygame.mixer.music.play(-1)  # Play the music indefinitely (-1)

# Render function
def render_screen(screen_data, images, player_x, player_y, hunters):
    screen.fill(BLACK)

    # Create a list to store objects based on render layers
    layers = [[] for _ in range(3)]  # 3 layers (0, 1, 2)

    for obj in screen_data:
        object_name = obj["name"]
        obj_x, obj_y = obj["position"]
        obj_render_layer = obj["render_layer"]

        if object_name in images:
            # Append the object to the corresponding layer
            layers[obj_render_layer].append((object_name, (obj_x, obj_y)))

    # Render objects from lower to higher layers
    count = 0
    for layer in layers:
        if(count == 1):
            # Render player and hunters on the same layer (layer 1)
            player_image = pygame.transform.scale(images["player"], (player_width, player_height))
            screen.blit(player_image, (player_x, player_y))

            for hunter in hunters:
                hunter_image = pygame.transform.scale(images["hunter"], (hunter_width, hunter_height))
                screen.blit(hunter_image, (hunter["x"], hunter["y"]))
        for object_name, (x, y) in layer:
            screen.blit(images[object_name], (x, y))
        count +=1

    pygame.display.flip()

def check_collision(x, y, images, objects, tolerance=0):
    for obj in objects:
        object_name = obj["name"]
        obj_x, obj_y = obj["position"]
        obj_collide = obj["collide"]

        # Check if the object allows collision
        if obj_collide:
            obj_width = images[object_name].get_width()
            obj_height = images[object_name].get_height()

            # Define the collision boundaries with tolerance
            left_boundary = obj_x - tolerance
            right_boundary = obj_x + obj_width + tolerance
            top_boundary = obj_y - tolerance
            bottom_boundary = obj_y + obj_height + tolerance

            if (
                x < right_boundary
                and x + player_width > left_boundary
                and y < bottom_boundary
                and y + player_height > top_boundary
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
def npc_ai(hunter, player_x, player_y, images, objects, screen_width, screen_height):
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

        if check_collision(check_x, check_y, images, objects):
            line_of_sight = False
            break

    if line_of_sight:
        # If there is a clear line of sight, sprint towards the player
        new_x = hunter_x + dx * (hunter_speed + 0.5)  # Increase speed slightly
        new_y = hunter_y + dy * (hunter_speed + 0.5)  # Increase speed slightly

        # Check for collision with objects
        if not check_collision(new_x, new_y, images, objects):
            # Perform bounds checking to keep the NPC within the screen boundaries
            new_x = max(0, min(new_x, screen_width - hunter_width))
            new_y = max(0, min(new_y, screen_height - hunter_height))

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
        if not check_collision(new_x, new_y, images, objects):
            # Perform bounds checking to keep the NPC within the screen boundaries
            new_x = max(0, min(new_x, screen_width - hunter_width))
            new_y = max(0, min(new_y, screen_height - hunter_height))

            hunter_x = new_x
            hunter_y = new_y
            collision_count = 0
            if(new_x <= 0 + hunter_width or new_x >= screen_width - hunter_width):
                patrol_direction = random.choice(["left", "right", "up", "down"])
                hunter["patrol_direction"] = patrol_direction
                collision_count+=1
            if(new_y <= 0 + hunter_height or new_y >= screen_height - hunter_height):
                patrol_direction = random.choice(["left", "right", "up", "down"])
                hunter["patrol_direction"] = patrol_direction
                collision_count+=1
        else:
            # Change direction randomly
            patrol_direction = random.choice(["left", "right", "up", "down"])
            hunter["patrol_direction"] = patrol_direction
            collision_count+=1
        # Update the patrol timer
        patrol_timer += 1

        # If patrol timer exceeds a certain value, randomly choose a new patrol direction
        if patrol_timer >= 2000:  # Adjust the timer value as needed
            patrol_direction = random.choice(["left", "right", "up", "down"])
            hunter["patrol_direction"] = patrol_direction
            # Reset the patrol timer
            patrol_timer = 0


    # Update the hunter's position in the object
    hunter["x"] = hunter_x
    hunter["y"] = hunter_y
    hunter["patrol_timer"] = patrol_timer
    hunter["collision_count"] = collision_count

    return hunter






# Initialize the game-over and win states
game_over = False
win = False


FPS = 60

# Create a clock object to control the frame rate
clock = pygame.time.Clock()




# Main game loop
def main():
    global player_x, player_y, win, game_over,screen_width, screen_height
    images = load_images()

    current_screen = "screen 1"

    running = True
    intro_complete = False


    while running:
        if not intro_complete:
            intro(screen)
            intro_complete = True



        objects = screens[current_screen]['objects']
        hunters = screens[current_screen]['hunters']
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

          # Check for transitions
        for direction, target_screen in screens[current_screen]['transitions'].items():
            if target_screen is not None:
                if direction == 'North' and player_y < 0:
                    current_screen = target_screen
                    player_y = SCREEN_HEIGHT - player_height  # Place player at the bottom
                elif direction == 'East' and player_x > SCREEN_WIDTH:
                    current_screen = target_screen
                    player_x = 0  # Place player at the left
                elif direction == 'South' and player_y > SCREEN_HEIGHT:
                    current_screen = target_screen
                    player_y = 0  # Place player at the top
                elif direction == 'West' and player_x < 0:
                    current_screen = target_screen
                    player_x = SCREEN_WIDTH - player_width  # Place player at the right

        # NPC AI for each hunter
        for hunter in hunters:
            hunter = npc_ai(hunter, player_x, player_y, images, objects, SCREEN_WIDTH, SCREEN_HEIGHT)

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



        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
