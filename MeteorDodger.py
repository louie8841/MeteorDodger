import pygame, sys
from random import randint
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE

pygame.init()
SURFACE = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Meteor Dodger")
FPSCLOCK = pygame.time.Clock()

def runGame():
    global score
    game_over = False
    score = 0
    speed = 25
    stars = []
    keymap = []
    ship = [0, 0]

    scope_image = pygame.image.load("scope.png")
    rock_image = pygame.image.load("rock.png")

    scorefont = pygame.font.SysFont(None, 32)
    sysfont = pygame.font.SysFont(None, 72)
    message_over = sysfont.render("GAME OVER!!", True, (0, 255, 255))
    message_rect = message_over.get_rect()
    message_rect.center = (400 ,400)
    
    pygame.mixer.music.load("background2.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0)

    while len(stars) < 200:
        stars.append({"pos" : [randint(-1600, 1600),
                               randint(-1600, 1600),
                               randint(0, 4095)],
                      "theta" : randint(0, 360)})

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key not in keymap:
                    keymap.append(event.key)
            
            elif event.type == KEYUP:
                if event.key in keymap:
                    keymap.remove(event.key)


        if not game_over:
            score += 1
            if score % 10 == 0:
                speed += 1
            
            if K_LEFT in keymap:
                ship[0] -= 30
            
            elif K_RIGHT in keymap:
                ship[0] += 30

            elif K_UP in keymap:
                ship[1] -= 30
            
            elif K_DOWN in keymap:
                ship[1] += 30
            
            ship[0] = max(-800, min(800, ship[0]))
            ship[1] = max(-800, min(800, ship[1]))

            for star in stars:
                star["pos"][2] -= speed
                if star["pos"][2] < 64:
                    if abs(star["pos"][0] - ship[0]) < 50 and abs(star["pos"][1] - ship[1]) < 50:
                        game_over = True
                    star["pos"] = [randint(-1600, 1600),
                                   randint(-1600, 1600),
                                           4095]

        SURFACE.fill((0, 0, 0)) 
        stars = sorted(stars, key=lambda x: x["pos"][2], reverse=True) 
        for star in stars:
            zpos = star["pos"][2]
            xpos = ((star["pos"][0] - ship[0]) << 9) / zpos + 400
            ypos = ((star["pos"][1] - ship[1]) << 9) / zpos + 400
            size = (50 << 9) / zpos
            rotated = pygame.transform.rotozoom(rock_image, star["theta"], size / 145)
            SURFACE.blit(rotated, (xpos, ypos))
        
        SURFACE.blit(scope_image, (0, 0))

        if game_over:
            pygame.mixer.music.stop()
            restart()
        
        score_str = str(score).zfill(6)
        score_image = scorefont.render(score_str, True, (0, 255, 0))
        SURFACE.blit(score_image, (700, 50))

        pygame.display.update()
        FPSCLOCK.tick(20)

def main():
    font = pygame.font.SysFont(None, 40)
    pygame.mixer.music.load("background1.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0)
    while True:
        SURFACE.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                pygame.mixer.music.stop()
                runGame()
        txt = font.render("Press space to start", True, (255, 255, 255))
        SURFACE.blit(txt, (250, 300))
        pygame.display.update()
        FPSCLOCK.tick(15)

def getBest(score):
    global best
    with open('data.dat', 'r') as f:
        if f.read != "":
            bestf = f.read()
            if score > int(bestf):
                best = score
            else:
                best = bestf
        else:
            best = score
    with open('data.dat', 'w') as f:
        f.write(str(best))

def restart():
    global score, best
    pygame.mixer.music.load("background1.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0)
    font = pygame.font.SysFont(None, 40)
    while True:
        SURFACE.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                pygame.mixer.music.stop()
                runGame()
        getBest(score)
        txt = font.render("Press space to restart", True, (255, 255, 255))
        txt2 = font.render(f"Your score is {score}", True, (255, 255, 255))
        txt3 = font.render(f"Your best score is {best}", True, (255, 255, 255))
        txtrect = txt.get_rect()
        txtrect.center = (400, 350)
        SURFACE.blit(txt, txtrect.topleft)
        txtrect.center = (400, 400)
        SURFACE.blit(txt2, txtrect.topleft)
        txtrect.center = (400, 450)
        SURFACE.blit(txt3, txtrect.topleft)
        pygame.display.update()
        FPSCLOCK.tick(20)

if __name__ == '__main__':
    main()