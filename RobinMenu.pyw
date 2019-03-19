""" 
 Prototype for AdaFruit 128x64 OLED Screen Menu
"""

# Import required libraries
import pygame

# Initialize PyGame
pygame.init()

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# Placeholder for Trig functions
PI = 3.141592653

# Set the height and width of the screen
# Uncomment multipliers for debugging
WD = 128 #* 2
HT = 64  #* 2
size = (WD, HT)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Robin Pi Menu")

#Loop until the user clicks the close button.
done  = False
BUSY  = False
SCRUP = False
SCROD = False
SCRHT = 0
VCENT = int((HT/4 - int(HT/5))/2)
HCENT = 0
LMARG = int(WD / 10)
clock = pygame.time.Clock()

BOX1 = 0
BOX2 = HT / 4
BOX3 = BOX2 * 2
BOX4 = BOX2 * 3
BOX5 = BOX2 * 4
BOX6 = BOX2 * 5

MAIN_MENU = ["MAIN MENU", "SUBMENU 1" , "SUBMENU 2" , "SUBMENU 3" , "SUBMENU 4" , "SUBMENU 5"]

font = pygame.font.SysFont('Lucida Console', int(HT/5), True, False)
       
# Loop as long as done == False
while not done:

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if BUSY == False:
                if event.key == pygame.K_UP:
                    BUSY = True
                    SCRUP = True
                elif event.key == pygame.K_DOWN:
                    BUSY = True
                    SCROD = True
                
    # All drawing code happens after the for loop and but
    # inside the main while not done loop.
    
    # Clear the screen and set the screen background
    screen.fill(WHITE)
   
    # Draw a rectangle

    ## for OPTION in MAIN_MENU[1:]:
    ## then overwrite with MAIN_MENU[0]
    
    pygame.draw.rect(screen, BLACK, [0, BOX2, WD -1, HT / 4], 2)
    pygame.draw.rect(screen, BLACK, [0, BOX3, WD -1, HT / 4], 2)
    pygame.draw.rect(screen, BLACK, [0, BOX4, WD -1, HT / 4], 2)
    pygame.draw.rect(screen, BLACK, [0, BOX5, WD -1, HT / 4], 2)

    screen.blit(font.render("SubMenu 1", True, BLACK), [LMARG, BOX2 + VCENT])
    screen.blit(font.render("SubMenu 2", True, BLACK), [LMARG, BOX3 + VCENT])
    screen.blit(font.render("SubMenu 3", True, BLACK), [LMARG, BOX4 + VCENT])
    screen.blit(font.render("SubMenu 4", True, BLACK), [LMARG, BOX5 + VCENT])

    pygame.draw.rect(screen, WHITE, [0, BOX1, WD   , HT / 4])
    pygame.draw.rect(screen, BLACK, [0, BOX1, WD -1, HT / 4], 2)

    header = font.render("MAIN MENU", True, BLACK)
    screen.blit(header, [(WD - font.size("MAIN MENU")[0])/2, BOX1 + VCENT])

    if BUSY == True:
        if SCRHT == (int(HT/4)):
            BUSY = False
            SCRUP = False
            SCROD = False
            SCRHT = 0
        elif SCRUP == True:
            BOX2 = (BOX2 + 1) % HT
            BOX3 = (BOX3 + 1) % HT
            BOX4 = (BOX4 + 1) % HT
            BOX5 = (BOX5 + 1) % HT
            SCRHT = SCRHT + 1
        elif SCROD == True:
            BOX2 = (BOX2 - 1) % HT
            BOX3 = (BOX3 - 1) % HT
            BOX4 = (BOX4 - 1) % HT
            BOX5 = (BOX5 - 1) % HT
            SCRHT = SCRHT + 1
            
        # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(120)
 
# Be IDLE friendly
pygame.quit()
