import pygame,pygame_textinput
import random
import os


os.chdir(os.path.dirname(__file__))
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
font_type = 'Consolas'


def inputsize():
    pygame.key.set_repeat(200, 25)
    manager = pygame_textinput.TextInputManager(validator=lambda input:(True if input.isdigit() else input == ''))
    textinput=pygame_textinput.TextInputVisualizer(manager=manager,font_object=pygame.font.SysFont(font_type, 30),antialias=True,font_color=black,cursor_color=black)
    clock = pygame.time.Clock()
    invalid=0
    while True:
        screen.fill((225, 225, 225))
        events = pygame.event.get()
        textinput.update(events)
        screen.blit(textinput.surface, (10, 10))
        if invalid:
            screen.blit(pygame.font.SysFont(font_type,30).render("Input is invalid!",1,black),(10,50))
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if textinput.value != '' and int(textinput.value)>3 and int(textinput.value)<=50:
                    return int(textinput.value)
                else:
                    invalid=1
            if event.type == pygame.QUIT:
                exit()
        pygame.display.update()
        clock.tick(30)


pygame.init()
screen = pygame.display.set_mode([400, 100])
pygame.display.set_caption("Minesweeper:Input Size(>3,<=50)")
pygame.display.set_icon(pygame.image.load("Bomb.png"))
size = inputsize()
block = 14 * 50 // size
screen = pygame.display.set_mode([size*block, size*block+50])
pygame.display.set_caption("Minesweeper")
smallfont = pygame.font.SysFont(font_type, 40)
font = pygame.font.SysFont(font_type, block)
largefont = pygame.font.SysFont(font_type, size * block // 5)
bombimg = pygame.transform.scale(pygame.image.load("Bomb.png"), (block, block))
flagimg = pygame.transform.scale(pygame.image.load("Flag.png"), (block, block))



def fill0():
    for i in range(size + 1):
        a.append([])
        clicked.append([])
        flag.append([])
        for j in range(size + 1):
            a[i].append(0)
            clicked[i].append(0)
            flag[i].append(0)


def mapgen(firstclick):
    cnt = 0
    while(cnt < size * size / 8):
        x = random.randint(0, size-1)
        y = random.randint(0, size - 1)
        if(a[x][y] != -1 and firstclick != [x, y]):
            flag = True
            for k in range(8):
                tx = x+dirs[k][0]
                ty = y+dirs[k][1]
                if(tx < 0 or tx > size - 1 or ty < 0 or ty > size - 1):
                    continue
                if(firstclick == [tx, ty]):
                    flag = False
            if(flag):
                a[x][y] = -1
                cnt += 1
    for i in range(size):
        for j in range(size):
            if(a[i][j] == 0):
                for k in range(8):
                    tx = i+dirs[k][0]
                    ty = j+dirs[k][1]
                    if(tx < 0 or tx > size - 1 or ty < 0 or ty > size - 1):
                        continue
                    if(a[tx][ty] == -1):
                        a[i][j] += 1


def drawmap():
    screen.fill(blue)
    pygame.draw.rect(screen, white, (0, size*block, size*block, 50), 0)
    for i in range(size):
        for j in range(size):
            if(clicked[i][j]):
                pygame.draw.rect(screen, white, (i*block, j*block, block, block), 0)
                if(a[i][j] > 0):
                    screen.blit(font.render(str(a[i][j]), 1, black), [
                                i*block+block//5, j*block+block//20])
                if(a[i][j] == -1):
                    screen.blit(bombimg, [i*block, j*block])
            elif(flag[i][j]):
                screen.blit(flagimg, [i*block, j*block])
    for i in range(size):
        pygame.draw.line(screen, black, (i*block-1, 0), (i*block-1, size * block), 2)
    for i in range(size+1):
        pygame.draw.line(screen, black, (0, i*block-1), (size * block, i*block-1), 2)
    pygame.draw.rect(screen, red, (size*block-300, size*block, 300, 50), 0)
    screen.blit(smallfont.render("Play Again", 1, black), [size*block-250, size*block+5])


def click(x, y):
    if(a[x][y] == 0):
        clicked[x][y] = 1
        for i in range(8):
            tx = x+dirs[i][0]
            ty = y+dirs[i][1]
            if(tx < 0 or tx > size - 1 or ty < 0 or ty > size - 1 or clicked[tx][ty]):
                continue
            click(tx, ty)
    else:
        clicked[x][y] = 1


def showwin():
    drawmap()
    screen.blit(largefont.render("You Win", 1, black), [size * block // 8 + 5, size * block // 8 * 3 + 5])
    screen.blit(largefont.render("You Win", 1, red), [size * block // 8, size * block // 8 * 3])
    pygame.display.update()
    while(1):
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            spot = pygame.mouse.get_pos()
            if(spot[1]>=size*block):
                if(spot[0]>=size*block-300):
                    pygame.quit()
                    os.system("python "+__file__)
                    exit()


def showlose():
    for i in range(size):
        for j in range(size):
            if(a[i][j] == -1):
                 clicked[i][j] = 1
    drawmap()
    screen.blit(largefont.render("You Lose", 1, black), [size * block // 16 + 5, size * block // 8 * 3 + 5])
    screen.blit(largefont.render("You Lose", 1, red), [size * block // 16, size * block // 8 * 3])
    pygame.display.update()
    while(1):
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            spot = pygame.mouse.get_pos()
            if(spot[1]>=size*block):
                if(spot[0]>=size*block-300):
                    pygame.quit()
                    os.system("python "+__file__)
                    exit()


def first():
    f = True
    mousedown = [False, False, False, False, False, False]
    fill0()
    firstclick = [0, 0]
    while f:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                exit()
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                mousedown[event.button] = True
            elif (event.type == pygame.MOUSEBUTTONUP):
                mousedown = [False, False, False, False, False, False]
        if(mousedown[1]):
            spot = pygame.mouse.get_pos()
            if(spot[1]>=size*block):
                if(spot[0]>=size*block-300):
                    pygame.quit()
                    os.system("python "+__file__)
                    exit()
            else:
                firstclick=[spot[0]//block,spot[1]//block]
                f = False
                mapgen(firstclick)
                click(firstclick[0],firstclick[1])
        if(mousedown[3]):
            spot = pygame.mouse.get_pos()
            flag[spot[0]//block][spot[1]//block] = 1
        drawmap()
        pygame.display.update()


def main():
    mousedown = [False, False, False, False, False, False]
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
        for i in range(size):
            for j in range(size):
                if(clicked[i][j] == 0 and a[i][j] != -1):
                    win = 0
        if(win):
            showwin()
            f = False
        if(mousedown[1]):
            spot = pygame.mouse.get_pos()
            if(spot[1]>=size*block):
                if(spot[0]>=size*block-300):
                    pygame.quit()
                    os.system("python "+__file__)
                    exit()
            else:
                if(a[spot[0]//block][spot[1]//block] == -1):
                    showlose()
                    f = False
                else:
                    click(spot[0]//block, spot[1]//block)
        if(mousedown[3]):
            spot = pygame.mouse.get_pos()
            flag[spot[0]//block][spot[1]//block] = 1
        if(mousedown[2]):
            spot = pygame.mouse.get_pos()
            cnt = 0
            for i in range(8):
                tx = spot[0]//block+dirs[i][0]
                ty = spot[1]//block+dirs[i][1]
                if(tx < 0 or tx > size - 1 or ty < 0 or ty > size - 1 or clicked[tx][ty]):
                    continue
                if(flag[tx][ty] == 1):
                    cnt += 1
            if(cnt == a[spot[0]//block][spot[1]//block]):
                lose = False
                for i in range(8):
                    tx = spot[0]//block+dirs[i][0]
                    ty = spot[1]//block+dirs[i][1]
                    if(tx < 0 or tx > size - 1 or ty < 0 or ty > size - 1 or clicked[tx][ty]):
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


first()
main()
pygame.quit()
