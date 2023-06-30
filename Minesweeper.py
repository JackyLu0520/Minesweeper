import pygame
import random


pygame.init()
screen = pygame.display.set_mode([400, 400])
pygame.display.set_caption("Minesweeper")
dirs = [[1, 0], [0, 1], [-1, 0], [0, -1],
        [1, 1], [1, -1], [-1, 1], [-1, -1]]
a = []
clicked = []
flag = []
blue = (0, 0, 255)
cyan = (0, 255, 255)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
font = pygame.font.SysFont("Consolas", 50)
largefont = pygame.font.SysFont("Consolas", 80)
bombimg = pygame.image.load("Bomb.png")
flagimg = pygame.image.load("Flag.png")


def fill0():
    for i in range(9):
        a.append([])
        clicked.append([])
        flag.append([])
        for j in range(9):
            a[i].append(0)
            clicked[i].append(0)
            flag[i].append(0)


def mapgen(firstclick):
    cnt = 0
    while(cnt < 8):
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        if(a[x][y] != -1 and firstclick != [x, y]):
            a[x][y] = -1
            cnt += 1
    for i in range(8):
        for j in range(8):
            if(a[i][j] == 0):
                for k in range(8):
                    tx = i+dirs[k][0]
                    ty = j+dirs[k][1]
                    if(tx < 0 or tx > 7 or ty < 0 or ty > 7):
                        continue
                    if(a[tx][ty] == -1):
                        a[i][j] += 1


def drawmap():
    screen.fill(blue)
    for i in range(8):
        for j in range(8):
            if(clicked[i][j]):
                pygame.draw.rect(screen, white, (i*50, j*50, 50, 50), 0)
                if(a[i][j] > 0):
                    screen.blit(font.render(str(a[i][j]), 1, black), [
                                i*50+12, j*50+3])
                if(a[i][j] == -1):
                    screen.blit(bombimg, [i*50, j*50])
            elif(flag[i][j]):
                screen.blit(flagimg, [i*50, j*50])
    for i in range(8):
        pygame.draw.line(screen, black, (i*50-1, 0), (i*50-1, 800), 2)
    for i in range(8):
        pygame.draw.line(screen, black, (0, i*50-1), (800, i*50-1), 2)


def click(x, y):
    if(a[x][y] == 0):
        clicked[x][y] = 1
        for i in range(8):
            tx = x+dirs[i][0]
            ty = y+dirs[i][1]
            if(tx < 0 or tx > 7 or ty < 0 or ty > 7 or clicked[tx][ty]):
                continue
            click(tx, ty)
    else:
        clicked[x][y] = 1


def showwin():
    drawmap()
    screen.blit(largefont.render("You Win", 1, black), [55, 155])
    screen.blit(largefont.render("You Win", 1, red), [50, 150])
    pygame.display.update()
    while(1):
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break


def showlose():
    for i in range(8):
        for j in range(8):
            if(a[i][j] == -1):
                 clicked[i][j] = 1
    drawmap()
    screen.blit(largefont.render("You Lose", 1, black), [30, 155])
    screen.blit(largefont.render("You Lose", 1, red), [25, 150])
    pygame.display.update()
    while(1):
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break


f = True
mousedown = [False, False, False, False, False, False]
fill0()
firstclick = [0, 0]
while f:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            f = False
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            mousedown[event.button] = True
        elif (event.type == pygame.MOUSEBUTTONUP):
            mousedown = [False, False, False, False, False, False]
    if(mousedown[1]):
        spot = pygame.mouse.get_pos()
        firstclick=[spot[0]//50,spot[1]//50]
        f = False
    if(mousedown[3]):
        spot = pygame.mouse.get_pos()
        flag[spot[0]//50][spot[1]//50] = 1
    drawmap()
    pygame.display.update()
mapgen(firstclick)
click(firstclick[0],firstclick[1])
f = True
while f:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            f = False
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            mousedown[event.button] = True
        elif (event.type == pygame.MOUSEBUTTONUP):
            mousedown = [False, False, False, False, False, False]
    win = 1
    for i in range(8):
        for j in range(8):
            if(clicked[i][j] == 0 and a[i][j] != -1):
                win = 0
    if(win):
        showwin()
        f = False
    if(mousedown[1]):
        spot = pygame.mouse.get_pos()
        if(a[spot[0]//50][spot[1]//50] == -1):
            showlose()
            f = False
        else:
            click(spot[0]//50, spot[1]//50)
    if(mousedown[3]):
        spot = pygame.mouse.get_pos()
        flag[spot[0]//50][spot[1]//50] = 1
    if(mousedown[2]):
        spot = pygame.mouse.get_pos()
        cnt = 0
        for i in range(8):
            tx = spot[0]//50+dirs[i][0]
            ty = spot[1]//50+dirs[i][1]
            if(tx < 0 or tx > 7 or ty < 0 or ty > 7 or clicked[tx][ty]):
                continue
            if(flag[tx][ty] == 1):
                cnt += 1
        if(cnt == a[spot[0]//50][spot[1]//50]):
            lose = False
            for i in range(8):
                tx = spot[0]//50+dirs[i][0]
                ty = spot[1]//50+dirs[i][1]
                if(tx < 0 or tx > 7 or ty < 0 or ty > 7 or clicked[tx][ty]):
                    continue
                if(flag[tx][ty] == 0):
                    click(tx, ty)
                    if(a[tx][ty] == -1):
                        lose = True
            if(lose):
                showlose()
                f = False
                        
    drawmap()
    pygame.display.update()
pygame.quit()
