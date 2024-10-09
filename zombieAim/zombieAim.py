import time  # Module for tracking time and delays
import random  # Module for random number generation
import math  # Module for mathematical functions
import pygame  # Pygame module for game development
import sys  # System-specific parameters and functions

pygame.init()  # initialize pygame 
pygame.init()  # initialize pygame 
pygame.mixer.init()  # initialize the mixer for audio

start_screen_music = "numbersMason.ogg"
damned_music = "Damned.ogg"

start_screen_image = pygame.image.load("zombiesMenuScreen.png")  # loads start screen 

# Load and play background music


zombie_scream = pygame.mixer.Sound("zombiescream1.ogg")
shoot_sound = pygame.mixer.Sound("ogg_file.ogg")
shoot_sound.set_volume(2.0)

width = 1920 
height = 1080 
windowObj = pygame.display.set_mode((width, height))  # initialize a pygame window object 
pygame.display.set_caption("Da Aim Trainer")  # gives a name to our window 

pygame.mixer.set_num_channels(5)
# Load multiple zombie scream sounds into a list
zombie_screams = [
    pygame.mixer.Sound("zombiescream1.ogg"),
    pygame.mixer.Sound("zombiescream2.ogg"),
    pygame.mixer.Sound("zombiescream3.ogg"),
    pygame.mixer.Sound("zombiescream4.ogg"),
    
    
    
]
for scream in zombie_screams:
    scream.set_volume(1.0)  # Adjust volume as needed (0.0 to 1.0)


# Load zombie character images
character_images = [
    pygame.image.load("ZOMBIE.png"),
    pygame.image.load("zombie2.png"),
    pygame.image.load("zombie10.png"),
    pygame.image.load("zombie3.png"),
    pygame.image.load("zombie9.png"),
        
   
    
]

Raygun_Image = pygame.image.load(("raygunv4.png"))


# Constants for target display timing and event handling
target_inc = 500  # milliseconds until next target 
target_Event = pygame.USEREVENT  # Custom events for targets

# Constants for layout and design
target_Padding = 40  # pixels target is off edge of screen 
top_bar_height = 40  # top bar height in pixels 
FONT = pygame.font.SysFont("LL Akkura", 20) 
NumLives = 3

# Ammo variables
MAX_AMMO = 160  # Set a max ammo value
current_ammo = MAX_AMMO  # Initialize current ammo
kills = 0  # Track number of kills
MAX_AMMO_KILLS = 40  # Number of kills required for Max Ammo



class Target:
    DaMaxSize = 150  # maximum size of target
    DaGrowthRate = 0.3  # growth rate of the target 

    def __init__(self, x, y, image):  # Constructor to initialize target position and size
        self.x = x  # X-coordinate of the target
        self.y = y  # Y-coordinate of the target
        self.image = image  # Image representing the target
        self.size = 0  # Size of the target until it hits max size 
        self.grow = True  # Whether the target is growing or shrinking 

    def update(self):  # Update target size
        if self.grow: 
            self.size += self.DaGrowthRate  # Increase size if growing
            if self.size >= self.DaMaxSize:  # Stop growing at max size
                self.size = self.DaMaxSize
                self.grow = False  # Switch to shrinking
        else: 
            self.size -= self.DaGrowthRate  # Decrease size if shrinking
            if self.size <= 0:
                self.size = 0
                self.grow = True  # Start growing again when it shrinks completely

    def draw(self, win):  # Draw the target image
        if self.size > 0:  
            scaled_image = pygame.transform.scale(self.image, (int(self.size), int(self.size)))  # Scale image based on size
            win.blit(scaled_image, (self.x - self.size // 2, self.y - self.size // 2))  # Draw image at target position

    def collide(self, x, y):  # Check for collisions
        distance = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)  # Calculate distance from mouse to target
        return distance <= self.size  # Return True if the mouse is within the target

background_image = pygame.image.load("gunholding.jpg")


def draw_raygun(windowObj, mouse_pos):
    raygun_width, raygun_height = Raygun_Image.get_size()
    
    # Calculate position based on mouse position
    x_position = (width - raygun_width) // 2  # Center horizontally
    y_position = height - raygun_height + 20   # 20 pixels to put it to bottom of screen 

   
   
    offset_x = (mouse_pos[0] - width / 2) // 10  #  # Adjust horizontal position of ragun based on mouse movement
    x_position += offset_x

    windowObj.blit(Raygun_Image, (x_position, y_position))   # Draw raygun

def draw(windowObj, targets):  # Draw all targets
    windowObj.blit(background_image, (0, 0))  # Draw background image
    for target in targets: 
        target.draw(windowObj)  # Draw each target

def timeFormat(secs):  # Format time into a string
    seconds = int(secs)  # Convert seconds to an integer
    return f"{seconds:02d} seconds"  # Return formatted string

def draw_top_bar_above_stats(windowObj, timeElapsed, targetsHit, NumMisses):  # Draw the top statistics bar
    pygame.draw.rect(windowObj, "Black", (0, 0, width, top_bar_height))  # Create a black top bar
    time_label = FONT.render(f"Time: {timeFormat(timeElapsed)}", 1, "White") 
    hits_label = FONT.render(f"Hits: {targetsHit}", 1, "White")
    misses_label = FONT.render(f"Misses: {NumMisses}", 1, "White")
    lives_label = FONT.render(f"Lives: {NumLives - NumMisses}", 1, "White") 

    windowObj.blit(time_label, (5, 5))  # Display labels
    windowObj.blit(hits_label, (200, 5)) 
    windowObj.blit(misses_label, (400, 5))
    windowObj.blit(lives_label, (600, 5))
    



def game_over_screen(windowObj, timeElapsed, targetsHit, NumClicks):  # Game over screen
    pygame.mixer.music.stop() #stops 115 song and zombie screams 
    pygame.mixer.stop()
    windowObj.fill("Black")
    
     # Load the game over image
    game_over_image = pygame.image.load("gameOVER.jpg")
    game_over_image_rect = game_over_image.get_rect(center=(width / 2, height / 2))  # Center the image

    game_over_sound = pygame.mixer.Sound("byebye.mp3")  
    game_over_sound.play()


    time_label = FONT.render(f"Time: {timeFormat(timeElapsed)}", 1, "White") 
    hits_label = FONT.render(f"Hits: {targetsHit}", 1, "White")
    accuracy_percent = round(targetsHit / NumClicks * 100, 1)
    accuracy_Label = FONT.render(f"Accuracy: {accuracy_percent}%", 1, "White")

    windowObj.blit(time_label, (get_middle(time_label), 100))
    windowObj.blit(hits_label, (get_middle(hits_label), 200))
    windowObj.blit(accuracy_Label, (get_middle(accuracy_Label), 400))


    windowObj.blit(game_over_image, game_over_image_rect)

    pygame.display.update() 

    run = True  # this is to quit and u do it by closing the command window which i should have added a key for that now that im thinking about it 
    while run:  
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit() # Exit the game

def get_middle(surface): # Helper function to get the horizontal center for an object
    return width / 2 - surface.get_width() / 2 

def draw(windowObj, targets, mouse_pos):  # Draw all targets and the raygun
    windowObj.blit(background_image, (0, 0))  # Draw background image
    for target in targets: 
        target.draw(windowObj)  # Draw each target
    draw_raygun(windowObj, mouse_pos)  # Draw the raygun



def Start_Screen():
    # Load and play "Damned.ogg" indefinitely
    pygame.mixer.music.load(damned_music)
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1)  # Play "Damned.ogg" indefinitely

    # Load and play "numbersMason.ogg" as a sound
    start_screen_sound = pygame.mixer.Sound(start_screen_music)
    start_screen_sound.set_volume(0.25)
    start_screen_sound.play()  # Play "numbersMason.ogg"





    run = True
    while run:
        windowObj.blit(start_screen_image, (0, 0))  
        
        # Render "Press ENTER to start" text
        FONT = pygame.font.SysFont("LL Akkura", 40)
        start_label = FONT.render("Press ENTER to start", True, "Red")
        label_rect = start_label.get_rect(center=(width // 2, height - 100))  # Center the text near the bottom
        windowObj.blit(start_label, label_rect)  # Blit the text to the window


        pygame.display.update()  

        for event in pygame.event.get(): # Loop through all the events that have occurred
            if event.type == pygame.QUIT:  # Check if the user has clicked the window close button
                pygame.quit()  # Quit Pygame (closes the window)
                sys.exit()   # Exit the program (closes the command window and stops the script)
            if event.type == pygame.KEYDOWN:  # Check if a key was pressed on the keyboard
                if event.key == pygame.K_RETURN:  # Check if the Enter key (RETURN) was pressed
                    run = False # Set 'run' to False, which will stop the game loop and exit the start screen
                    start_screen_sound.stop()  # Stop numbersMason sound
                    pygame.mixer.music.stop()  # Stop the Damned music

                    # Load and play the game start sound once
                    game_start_sound = pygame.mixer.Sound("fetchME.mp3")
                    game_start_sound.set_volume(0.25)
                    game_start_sound.play()  # Play the game start sound once

                    # Wait for the game start sound to finish
                    while pygame.mixer.get_busy():  # Wait until game_start_sound finishes
                        pygame.time.delay(100)

                    # After the game start sound finishes, load and play the gameplay music
                    pygame.mixer.music.load("115.mp3")  
                    pygame.mixer.music.set_volume(0.35)  
                    pygame.mixer.music.play(-1)  # Play gameplay music
                    

def main(): 
    Start_Screen()  # Show the start screen
    run = True 
    targets = []
    clock = pygame.time.Clock()  # Create a clock object to manage frame rate
    pygame.time.set_timer(target_Event, target_inc)  # Set timer for target event
   
    target_hit = 0
    NumClicks = 0
    start_time = 0
    NumMisses = 0
    startTime = time.time()  # Record start time
    
    next_scream_time = time.time() + random.uniform(10, 20)  # gives us an interval of when the zombie rnadomly screams 

    while run: 
        mouse_pos = pygame.mouse.get_pos() 
        NumClicks = False
        
        timeElapsed = time.time() - startTime  # Calculate elapsed time
         # Event handling loop
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:   # Quit the game if the window close button is clicked
                run = False 
                break  
            
            if event.type == target_Event:  # deals with custom target event
                x = random.randint(target_Padding, width - target_Padding)  
                y = random.randint(target_Padding + top_bar_height, height - target_Padding)  
                image = random.choice(character_images)  # Select a random character image
                target = Target(x, y, image)  # Create a new target with an image
                targets.append(target)  # Add target to the list 
                
            if event.type == pygame.MOUSEBUTTONDOWN:   # Detect a mouse click event
                NumClicks = True
                NumClicks += 1  # Increment click count
                shoot_sound.play()
        # Check if it's time to play a zombie scream
        if time.time() >= next_scream_time:
            scream_sound = random.choice(zombie_screams)  # Choose a random scream
            scream_sound.play()  # Play the chosen scream
            next_scream_time = time.time() + random.uniform(10, 20)  # Set a new random time for the next scream
                

                
        for target in targets:   # Update each target in the list
            target.update()   # Update the target's size and behavior
            
            if target.size <= 0:   # Remove the target if its size is 0 
                targets.remove(target)
                NumMisses += 1   # Increment the number of missed targets
            
            if NumClicks and target.collide(*mouse_pos):   # Check if the player clicked and hit a target
               targets.remove(target)  # Remove the target if it's hit
               target_hit += 1  # Increment the hit counter

        if NumMisses >= NumLives:  # If  player misses too many targets show the game over screen
               game_over_screen(windowObj, timeElapsed, target_hit, NumMisses)  # Display game over screen
            


        draw(windowObj, targets, mouse_pos)  # Draw all targets 
        draw_top_bar_above_stats(windowObj, timeElapsed, target_hit, NumMisses)  # Draw the top bar 
        
        pygame.display.update() 
        clock.tick(60)  # Set our FPS to 60

    pygame.quit()  # Clean up and close the game window

if __name__ == "__main__":
    main()  # Call the main function to start the game

