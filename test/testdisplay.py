import pygame, time, os, sys
from pygame.locals import *

drivers = [
	# unix
	'x11', 'dga', 'fbcon', 'directfb', 'ggi', 'vgl', 'svgalib', 'aalib',
	# windows
	'windib', 'directx'
	]

found = False
for driver in drivers:
    if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
    try:
        pygame.display.init()
        print 'Driver: {0} success.'.format(driver)
    except pygame.error:
        print 'Driver: {0} failed.'.format(driver)
        continue
    found = True

    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.display.init()
    # set up the pygame window
    screen = pygame.display.set_mode((640,480),0)
    #screen = pygame.display.set_mode((480, 480),1)
    font1 = pygame.font.Font(None, 40)
    text1 = font1.render("Driver: " + format(driver), True, (255,255, 255), (0, 0, 0))
    rect1 = text1.get_rect()
    rect1.centerx = screen.get_rect().centerx
    rect1.centery = screen.get_rect().centery
    font2 = pygame.font.Font(None, 20)
    text2 = font2.render("pygame.image.get_extended: " + str(pygame.image.get_extended()), True, (123,123,123), (0, 0, 0))
    rect2 = text2.get_rect()
    rect2.centerx = screen.get_rect().centerx
    rect2.centery = screen.get_rect().centery + 20
    screen.blit(text1, rect1)
    screen.blit(text2, rect2)
    image1 = pygame.image.load("image.png")
    screen.blit(image1, (290,300))
    pygame.display.update()
    time.sleep(2)
    pygame.display.quit()
    pygame.quit()
    break

if not found:
   raise Exception('No suitable video driver found!')

sys.exit()
