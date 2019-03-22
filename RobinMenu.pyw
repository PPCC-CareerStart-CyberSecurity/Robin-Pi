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
WD = 128 *4#* 2
HT = 64  *4#* 2
BOX =  (WD, int(HT/4))
size = (WD, HT)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Robin Pi Menu")

#Loop until the user clicks the close button.
done  = False
BUSY  = False
SCRUP = False
SCROD = False
SCRIT = False
SCREL = False
SCRHT = 0
SCRWD = 0
VCENT = int((HT/4 - int(HT/5))/2)
HCENT = 0
LMARG = int(WD / 10)
DEPTH = 0
clock = pygame.time.Clock()

#BOX1 = 0
#BOX2 = HT / 4
#BOX3 = BOX2 * 2
#BOX4 = BOX2 * 3
#BOX5 = BOX2 * 4
#BOX6 = BOX2 * 5


# Menu adjusts to elements in this list; first element is always the title bar.
MAIN_MENU   = ("MAIN MENU","GAMES","TOOLS","PAYLOADS","LOOT","SETTINGS","SHUT DOWN",)
GAMES       = ("Asteroids","Pong")
TOOLS       = ("Wireshark","Kismet","Bad USB")
PAYLOADS    = ("One","Two","Three","Four","Five","Six")
LOOT        = ("passwd","shadow","rc.local")
SHUT_DOWN   = ("SHUT DOWN","RESTART","CANCEL")


#(("MAIN MENU","MAIN MENU"), ("GAMES",("Asteroids","Pong")), ("TOOLS",("Wireshark","Kismet","Bad USB")), ("PAYLOADS",("P1","P2","P3")), ("LOOT",("passwd","shadow","rc.local")), ("SETTINGS",()), ("SHUT DOWN",("YES","No")))

MMHT = int(HT/4) * (len(MAIN_MENU) -1)

font = pygame.font.SysFont('Lucida Console', int(HT/5), True, False)
       
# Loop as long as done == False
while not done:

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # scroll the menu.
            if BUSY == False:
                if event.key == pygame.K_UP:
                    BUSY = True
                    SCRUP = True
                    SCROD = False
                    SCRIT = False
                    SCREL = False
                elif event.key == pygame.K_DOWN:
                    BUSY = True
                    SCRUP = False
                    SCROD = True
                    SCRIT = False
                    SCREL = False
                elif (event.key == pygame.K_RIGHT) and (DEPTH < 1):
                    BUSY = True
                    SCRUP = False
                    SCROD = False
                    SCRIT = True
                    SCREL = False
                    DEPTH = DEPTH + 1
                elif (event.key == pygame.K_LEFT) and (DEPTH > 0):
                    BUSY = True
                    SCRUP = False
                    SCROD = False
                    SCRIT = False
                    SCREL = True
                    DEPTH = DEPTH - 1
                    
                
    # All drawing code happens after the for loop and but
    # inside the main while not done loop.
    
    # Clear the screen and set the screen background
    screen.fill(WHITE)
   
    # Draw a rectangle

    ## for OPTION in MAIN_MENU[1:]:
    ## then overwrite with MAIN_MENU[0]

    for x in MAIN_MENU[1:]:
        #pygame.draw.rect(screen, BLACK, [0, ((BOX[1] * MAIN_MENU.index(x)) + SCRHT) % MMHT, WD -1, HT / 4], 2)
        screen.blit(font.render(x, True, BLACK), [SCRWD + LMARG, ((BOX[1] * MAIN_MENU.index(x)) + SCRHT + VCENT) % MMHT])
        # (SCRWD +  
        
    #pygame.draw.rect(screen, BLACK, [0, BOX2, WD -1, HT / 4], 2)
    #pygame.draw.rect(screen, BLACK, [0, BOX3, WD -1, HT / 4], 2)
    #pygame.draw.rect(screen, BLACK, [0, BOX4, WD -1, HT / 4], 2)
    #pygame.draw.rect(screen, BLACK, [0, BOX5, WD -1, HT / 4], 2)

    #screen.blit(font.render("SubMenu 1", True, BLACK), [LMARG, BOX2 + VCENT])
    #screen.blit(font.render("SubMenu 2", True, BLACK), [LMARG, BOX3 + VCENT])
    #screen.blit(font.render("SubMenu 3", True, BLACK), [LMARG, BOX4 + VCENT])
    #screen.blit(font.render("SubMenu 4", True, BLACK), [LMARG, BOX5 + VCENT])

    pygame.draw.rect(screen, BLACK, [0, 0, WD   , HT / 4])
    pygame.draw.rect(screen, BLACK, [0, 0, WD -1, HT / 4], 2)
    pygame.draw.polygon(screen, BLACK, [(WD/32,5*HT/16),(WD/32,7*HT/16),(WD/16,6*HT/16)])

    header = font.render(MAIN_MENU[DEPTH], True, WHITE)
    screen.blit(header, [(WD - font.size(MAIN_MENU[DEPTH])[0])/2, 0 + VCENT])

    if BUSY == True:
        if SCRUP == True:
            SCRHT = (SCRHT + 1) % MMHT
        elif SCROD == True:
            SCRHT = (SCRHT - 1) % MMHT
        elif SCRIT == True:
            SCRWD = SCRWD - 4
        elif SCREL == True:
            SCRWD = SCRWD + 4
            
        if (SCRHT % (int(HT/4)) == 0) and (SCRWD % WD == 0):
            BUSY = False
        #elif SCRWD % WD == 0:
        #    BUSY = False
        
    else:
        SCRUP = False
        SCROD = False
        SCRIT = False
        SCREL = False
            
        # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(120)
 
# Be IDLE friendly
pygame.quit()
