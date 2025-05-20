import pygame as pg
import numpy
import random

pg.init()
screen = pg.display.set_mode((580, 720))
clock = pg.time.Clock()

WHITE = (221, 226, 226)
COLORS = ["red", "green", "blue", "aqua", "pink", "grey", "purple", "orange", "black", "brown"]
CENTER = (290, 360)
S_ANGLE = 3 * numpy.pi / 2

class Ball():
    def __init__(self, lst):
        # base
        self.ticks = 0
        self.radius = 8.5
        self.cList = lst
        self.color = self.pick_color(lst)
        self.x = CENTER[0]
        self.y = CENTER[1]

        # motion
        self.speed = 0
        self.const_accel = 0.8
        self.bHeight = 14

        # collision
        self.bounce = False

    def pick_color(self, list):
        return list[random.randint(0, len(list)-1)]

    def update(self):
        self.ticks += 1

        #  motion
        self.speed += self.const_accel
        self.y += self.speed

        #if self.ticks % 60 == 0:
        #    self.const_accel += 0.01

        # collision
        self.bounce = False
        if self.y > 500:
            self.bounce = True
            self.y = 500
            self.speed = -self.bHeight




    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Platform():
    def __init__(self, thta, n, order, plat):
        # other objects
        self.platforms = plat

        # base
        self.ticks = 0
        self.n = n
        self.color = self.pick_color()
        self.order = order
        self.mag = 150
        self.thta = thta
        self.size = (60, 8)
        self.pos = [CENTER[0] - self.size[0] / 2, CENTER[1] - self.size[1] / 2]

        # img
        self.image = pg.Surface((self.size[0], self.size[1])).convert_alpha()
        self.copy_img = self.image

        # animation
        self.queue = []
        self.sTime = 0
        self.mov = False
        self.rate = 0.2
        self.dRight = None

        print(self.color)


    def pick_color(self):
        color = random.randint(0, len(COLORS)-1)
        dupe = False
        if self.n > len(COLORS):
            return COLORS[color]
        for p in self.platforms:
            if p.color == COLORS[color]:
                dupe = True
        if dupe:
            strColor = self.pick_color()
            return strColor
        return COLORS[color]
    
    def cThta(self, right):
        if right:
            amt = (2 * numpy.pi / self.n) / (self.rate * 60)
            self.thta += amt
        else:
            amt = (2 * numpy.pi / self.n) / (self.rate * 60)
            self.thta -= amt

    def create_rect(self):
        rect = pg.rect.Rect((0, 0), (self.size))
        pg.draw.rect(self.copy_img, self.color, rect)
    
    def rotate(self):        
        self.copy_img = pg.transform.rotate(self.copy_img, 90 + self.thta * 180 / numpy.pi)
    
    def revolve(self):
        # finalize center
        tmp = self.copy_img.get_size()
        self.pos = [CENTER[0] - (tmp[0] / 2), CENTER[1] - (tmp[1] / 2)]

        # transform coordinates
        dx = self.mag * numpy.cos(self.thta)
        dy = self.mag * numpy.sin(self.thta)
        self.pos[0] += dx
        self.pos[1] -= dy

    def update(self, events):
        self.ticks += 1

        # change theta
        for ev in events:
            if ev.type == pg.KEYDOWN:
                #if ev.key == pg.K_LEFT:
                    #self.queue.append((0, self.ticks))
                    #self.order -= 1
                    #self.order %= self.n
                if ev.key == pg.K_RIGHT:
                    self.queue.append((1, self.ticks))
                    self.order += 1
                    self.order %= self.n

        pops = 0
        for i in range(len(self.queue)):
            if self.ticks - self.queue[i][1] < self.rate * 60:
                if self.queue[i][0] == 0:
                    self.cThta(False)
                if self.queue[i][0] == 1:
                    self.cThta(True)
            else:
                pops += 1

        for i in range(pops):
            self.queue.pop(0)

        # spin
        self.copy_img = self.image
        self.create_rect()
        self.rotate()
        self.revolve()

    def draw(self, screen):
        screen.blit(self.copy_img, self.pos)

def draw_text(screen, pos, size, text):
    temp = pg.font.SysFont("Arial", size)
    temp = temp.render(text, False, "black")
    screen.blit(temp, (pos))

def create_platforms(n):
    for i in range(n):
        platforms.append(Platform(S_ANGLE + 2 * numpy.pi * i / n, n, i, platforms))

def checkLoss(n):
    if obj.bounce == True:
        for p in platforms:
            if p.order == 0:
                if obj.color != p.color:
                    print("lose \n" + str(n))
                    obj.color = obj.pick_color(obj.cList)
                    return n+1
                obj.color = obj.pick_color(obj.cList)
    return n

def compileColors():
    return [p.color for p in platforms]

def drawPos():
    for p in platforms:
        draw_text(screen, (p.pos), 20, f"{p.order}")



platforms = []
create_platforms(50)

obj = Ball(compileColors())

n=0
lose = False
running = True
while running:
    events = pg.event.get()
    for ev in events:
        if ev.type == pg.QUIT:
            running = False

    screen.fill(WHITE)

    obj.update()
    obj.draw(screen)

    for p in platforms:
        p.update(events)
        p.draw(screen)

    drawPos()
    n = checkLoss(n)
    draw_text(screen, (100, 100), 12, f"Acceleration: {obj.const_accel}")

    pg.display.flip()
    clock.tick(60)
    


    