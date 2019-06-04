        g = pygame.transform.scale(grassTile, (100, 100))
        for i in range(0, 1200, 100):#from 0 to 1000 in multiples of 100
            for j in range(400, 1100, 100):
                s.blit(g, (i, j))
                
        c = pygame.transform.scale(concreteTile, (100, 100))
        for i in range(0, 1200, 100):
            for j in range(0, 400, 100):
                s.blit(c, (i, j))
            if i in (0, 200, 300, 500, 700, 800, 900, 1200):
                s.blit(c, (i, 400))
            if i in (100, 300, 400, 700, 900, 1000, 1100):
                s.blit(c, (i, 500))
            if i in (100, 400, 600, 900):
                s.blit(c, (i, 600))

        t = pygame.transform.scale(tree, (200, 300))
        s.blit(t, (0, 700))
        s.blit(t, (1000, 700))

        b = pygame.transform.scale(bush, (50, 50))
        s.blit(b, (150, 600))
        s.blit(b, (150, 650))
        s.blit(b, (1000, 600))
        s.blit(b, (1000, 650))

        r = pygame.transform.scale(rock, (100, 100))
        for i in range(50, 1200, 100):
            if i != 550:
                s.blit(r, (i, 1000))

        cr = pygame.transform.scale(crate, (50, 50))
        s.blit(cr, (0, 450))
        s.blit(cr, (0, 500))
        s.blit(cr, (0, 550))
        s.blit(cr, (0, 600))
        s.blit(cr, (0, 650))
        s.blit(cr, (1150, 450))
        s.blit(cr, (1150, 500))
        s.blit(cr, (1150, 550))
        s.blit(cr, (1150, 600))
        s.blit(cr, (1150, 650))

        h = pygame.transform.scale(house, (300, 300))
        s.blit(h, (-100, 150))
        s.blit(h, (1000, 150))
        s.blit(h, (200, -100))
        s.blit(h, (700, -100))
