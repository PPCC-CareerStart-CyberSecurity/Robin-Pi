""" 
 Simple graphics demo
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

"""

# Import a library of functions called 'pygame'
import pygame

# Initialize the game engine
pygame.init()

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

PI = 3.141592653

# Set the height and width of the screen
WD = 256
HT = 128
size = (WD, HT)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Robin Pi Menu")

#Loop until the user clicks the close button.
done = False
BUSY = False
SCRUP = False
SCROD = False
SCRHT = 0
clock = pygame.time.Clock()

BOX1 = 0
BOX2 = HT / 4
BOX3 = BOX2 * 2
BOX4 = BOX2 * 3
BOX5 = BOX2 * 4
BOX6 = BOX2 * 5

font = pygame.font.SysFont('Calibri', 12, True, False)

#def scroll_down():
#    for x in range (int(HT/4)):
#        BOX2 = (BOX2 - 1) % HT
#        BOX3 = (BOX3 - 1) % HT
#        BOX4 = (BOX4 - 1) % HT
#        BOX5 = (BOX5 - 1) % HT

#def scroll_up():
#    for x in range (int(HT/4)):
#        BOX2 = (BOX2 + 1) % HT
#        BOX3 = (BOX3 + 1) % HT
#        BOX4 = (BOX4 + 1) % HT
#        BOX5 = (BOX5 + 1) % HT        
        
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

    # Draw on the screen a line from (0,0) to (100,100) 
    # 5 pixels wide.
    #pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)

    # Draw on the screen several lines from (0,10) to (100,110) 
    # 5 pixels wide using a loop
    #for y_offset in range(0, 100, 10):
        #pygame.draw.line(screen, RED, [0, 10 + y_offset], [100, 110 + y_offset], 5)


    # Draw a rectangle
    
    pygame.draw.rect(screen, BLACK, [0, BOX2, WD -1, HT / 4], 2)
    pygame.draw.rect(screen, BLACK, [0, BOX3, WD -1, HT / 4], 2)
    pygame.draw.rect(screen, BLACK, [0, BOX4, WD -1, HT / 4], 2)
    pygame.draw.rect(screen, BLACK, [0, BOX5, WD -1, HT / 4], 2)

    text = font.render("My text", True, BLACK)
    screen.blit(text, [5, BOX2 +2])

    pygame.draw.rect(screen, WHITE, [0, BOX1, WD   , HT / 4])
    pygame.draw.rect(screen, BLACK, [0, BOX1, WD -1, HT / 4], 2)

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
            
    #scroll_up()
    
    # Draw an ellipse, using a rectangle as the outside boundaries
    #pygame.draw.ellipse(screen, BLACK, [20, 20, 250, 100], 2) 

    # Draw an arc as part of an ellipse. 
    # Use radians to determine what angle to draw.
    #pygame.draw.arc(screen, BLACK, [20, 220, 250, 200], 0, PI / 2, 2)
    #pygame.draw.arc(screen, GREEN, [20, 220, 250, 200], PI / 2, PI, 2)
    #pygame.draw.arc(screen, BLUE, [20, 220, 250, 200], PI, 3 * PI / 2, 2)
    #pygame.draw.arc(screen, RED, [20, 220, 250, 200], 3 * PI / 2, 2 * PI, 2)
    
    # This draws a triangle using the polygon command
    #pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)

    # Select the font to use, size, bold, italics
    
    # Render the text. "True" means anti-aliased text. 
    # Black is the color. This creates an image of the 
    # letters, but does not put it on the screen
    

    # Put the image of the text on the screen at 250x250
    

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)
    

# Be IDLE friendly
pygame.quit()
