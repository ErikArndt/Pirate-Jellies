import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))

index = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("{0}: You quit the game".format(index))
            running = False
        elif event.type == pygame.KEYDOWN:
            print("{0}: You pressed {1:c}, key #{1}".format(index, event.key))
        elif event.type == pygame.KEYUP:
            print("{0}: You released {1:c}, key #{1}".format(index, event.key))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("{0}: You pressed mouse {1}".format(index, event.button))
        elif event.type == pygame.MOUSEBUTTONUP:
            print("{0}: You released mouse {1}".format(index, event.button))
        
pygame.quit()