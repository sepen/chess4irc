import os, sys, pygame, time

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
    # display results
    pygame.init()
    font1 = pygame.font.Font(None, 40)
    text1 = font1.render("Driver: " + format(driver), True, (255,255, 255), (0, 0, 0))
    rect1 = text1.get_rect()
    screen = pygame.display.set_mode((480, 480),1)
    rect1.centerx = screen.get_rect().centerx
    rect1.centery = screen.get_rect().centery
    screen.blit(text1, rect1)
    pygame.display.update()
    time.sleep(3)
    pygame.display.quit()
    pygame.quit()
    break

if not found:
   raise Exception('No suitable video driver found!')

sys.exit()
