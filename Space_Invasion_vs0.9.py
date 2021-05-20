import pygame, sys, random

pygame.init()
win = pygame.display.set_mode((1250, 650))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 60)
score = 0
heals_timer = 0
heals_active = False
font = pygame.font.SysFont(None, 30)
font1 = pygame.font.SysFont(None, 150)
font2 = pygame.font.SysFont(None, 100)
meteors_hit = 0
laser_timer = 0
laser_active = False

bg = pygame.image.load('bg.jpg')
earth_bg = pygame.image.load('Earth_bg.jpg')
mars_bg = pygame.image.load('Mars_bg.jpg')
jupiter_bg = pygame.image.load('Jupiter_bg.jpg')
saturn_bg = pygame.image.load('Saturn_bg.jpg')
neptune_bg = pygame.image.load('Neptune_bg.jpg')
uranus_bg = pygame.image.load('Uranus_bg.jpg')
sun = pygame.image.load('Sun.png')
earth = pygame.image.load('earth.png')
mars = pygame.image.load('mars.png')
jupiter = pygame.image.load('jupiter.png')
saturn = pygame.image.load('saturn.png')
uranus = pygame.image.load('uranus.png')
neptune = pygame.image.load('Neptune.png')

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def txt_obj(text, font):
    txt_surface = font.render(text, True, (0,0,0))
    return txt_surface, txt_surface.get_rect()

class SpaceShip(pygame.sprite.Sprite):

    def __init__(self, path, x, y):
        super().__init__()
        self.uncharged = pygame.image.load(path)
        self.image = self.uncharged
        self.rect = self.image.get_rect(center = (x,y))
        self.health_surface = pygame.image.load('Health.png')
        self.health = 5
    
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.border()
        self.display_health()

    def display_health(self):
        for index, shield in enumerate(range(self.health)):
            win.blit(self.health_surface,(index * 50, 10))
    
    def border(self):
        if self.rect.right >= 1800:
            self.rect.right = 1800
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 1000:
            self.rect.bottom = 1000

    def damage(self,damage_amount):
        self.health -= damage_amount

class Meteor(pygame.sprite.Sprite):
    def __init__(self, path, x, y, xvel, yvel):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x,y))
        self.xvel = xvel
        self.yvel = yvel

    def update(self):
        self.rect.centerx +=  self.xvel
        self.rect.centery += self.yvel

        if self.rect.centery >= 800:
            self.kill()
        if self.rect.centerx >= 1300:
            self.kill()
        if self.rect.centerx <= -10:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, path, vel, x, y):
        super().__init__()
        self.image = pygame.image.load(path)
        self.vel = vel
        self.rect = self.image.get_rect(center = (x,y))

    def update(self):
        self.rect.centery -= self.vel

        if self.rect.centery <= -10:
            self.kill()

class Laser_right(pygame.sprite.Sprite):
    def __init__(self, path, vel, x, y):
        super().__init__()
        self.image = pygame.image.load(path)
        self.vel = vel
        self.rect = self.image.get_rect(center = (x,y))

    def update(self):
        self.rect.centery -= self.vel
        self.rect.centerx += self.vel / 5

        if self.rect.centery <= -10:
            self.kill()

class Laser_left(pygame.sprite.Sprite):
    def __init__(self, path, vel, x, y):
        super().__init__()
        self.image = pygame.image.load(path)
        self.vel = vel
        self.rect = self.image.get_rect(center = (x,y))

    def update(self):
        self.rect.centery -= self.vel
        self.rect.centerx -= self.vel / 5

        if self.rect.centery <= -10:
            self.kill()

def game():
    global score
    global meteors_hit
    global laser_timer
    global laser_active
    laser_group.draw(win)
    spaceship_group.draw(win)
    meteor_group.draw(win)

    laser_group.update()
    spaceship_group.update()
    meteor_group.update()

    if pygame.sprite.spritecollide(spaceship_group.sprite, meteor_group, True):
        spaceship_group.sprite.damage(1)

    for laser in laser_group:
        if pygame.sprite.spritecollide(laser, meteor_group, True):
            meteors_hit += 1
    
    if pygame.time.get_ticks() - laser_timer >= 500:
        laser_active = True
    
    return 1

def game_over():
    win.blit(bg, (0,0))

    game_over_surface = game_font.render('GAME OVER - CLICK TO GO TO MENU',True,(255,255,255))
    game_over_rect = game_over_surface.get_rect(center = (635,400))
    win.blit(game_over_surface, game_over_rect)

    score_surface = game_font.render(f'SCORE: {score}',True,(255,255,255))
    score_rect = score_surface.get_rect(center = (625, 275))
    win.blit(score_surface, score_rect)

    meteor_hit_surface = game_font.render(f'METEORS HIT: {meteors_hit}',True,(255,255,255))
    meteor_hit_rect = meteor_hit_surface.get_rect(center = (625, 330))
    win.blit(meteor_hit_surface, meteor_hit_rect)

def minimap(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def circle(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


#Spaceship
spaceship = SpaceShip('Spaceship.png',635,550)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

#Add to sprite groups
meteor_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()


def menu():
    run = True
    while run:

        win.blit(bg, (0,0))
        draw_text('main menu', font, (255, 255, 255), win, 1100, 20)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()

        start_btn = pygame.Rect(475, 225, 300, 75)
        start_btn_text = pygame.font.Font('freesansbold.ttf', 50)
        txt_surf1, txt_rect1 = txt_obj("Start", start_btn_text)
        txt_rect1.center = ((475+(300/2)), (225+(75/2)))

        levelmenu_btn = pygame.Rect(475, 350, 300, 75)
        levelmenu_btn_text = pygame.font.Font('freesansbold.ttf', 50)
        txt_surf2, txt_rect2 = txt_obj("Level Menu", levelmenu_btn_text)
        txt_rect2.center = ((475+(300/2)), (350+(75/2)))

        if start_btn.collidepoint((mx, my)):
            if click:
                level1()
        
        if levelmenu_btn.collidepoint((mx, my)):
            if click:
                levels_menu()
        
        pygame.draw.rect(win, (255, 255, 255), start_btn)
        win.blit(txt_surf1, txt_rect1)

        pygame.draw.rect(win, (255, 255, 255), levelmenu_btn)
        win.blit(txt_surf2, txt_rect2)

        pygame.display.update()
        clock.tick(120)

def levels_menu():
    run = True
    while run:
        win.blit(bg, (0,0))

        draw_text('Levels menu', font, (255, 255, 255), win, 1100, 20)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()

        #level 1
        level1_btn = pygame.Rect(400, 200, 75, 75)
        level1_btn_text = pygame.font.Font('freesansbold.ttf', 50)
        txt_surf1, txt_rect1 = txt_obj("1", level1_btn_text)
        txt_rect1.center = ((400+(75/2)), (200+(75/2)))

        if level1_btn.collidepoint((mx, my)):
            if click:
                level1()

        pygame.draw.rect(win, (255, 255, 255), level1_btn)
        win.blit(txt_surf1, txt_rect1)

        #level 2
        level2_btn = pygame.Rect(500, 200, 75, 75)
        level2_btn_text = pygame.font.Font('freesansbold.ttf', 50)
        txt_surf2, txt_rect2 = txt_obj("2", level2_btn_text)
        txt_rect2.center = ((500+(75/2)), (200+(75/2)))

        if level2_btn.collidepoint((mx, my)):
            if click:
                level2()

        pygame.draw.rect(win, (255, 255, 255), level2_btn)
        win.blit(txt_surf2, txt_rect2)

        #level 3
        level3_btn = pygame.Rect(600, 200, 75, 75)
        level3_btn_text = pygame.font.Font('freesansbold.ttf', 50)
        txt_surf3, txt_rect3 = txt_obj("3", level3_btn_text)
        txt_rect3.center = ((600+(75/2)), (200+(75/2)))

        if level3_btn.collidepoint((mx, my)):
            if click:
                level3()

        pygame.draw.rect(win, (255, 255, 255), level3_btn)
        win.blit(txt_surf3, txt_rect3)

        #level 4
        level4_btn = pygame.Rect(700, 200, 75, 75)
        level4_btn_text = pygame.font.Font('freesansbold.ttf', 50)
        txt_surf4, txt_rect4 = txt_obj("4", level4_btn_text)
        txt_rect4.center = ((700+(75/2)), (200+(75/2)))

        if level4_btn.collidepoint((mx, my)):
            if click:
                level4()

        pygame.draw.rect(win, (255, 255, 255), level4_btn)
        win.blit(txt_surf4, txt_rect4)

        #level5
        level5_btn = pygame.Rect(800, 200, 75, 75)
        level5_btn_text = pygame.font.Font('freesansbold.ttf', 50)
        txt_surf5, txt_rect5 = txt_obj("5", level5_btn_text)
        txt_rect5.center = ((800+(75/2)), (200+(75/2)))

        if level5_btn.collidepoint((mx, my)):
            if click:
                level5()

        pygame.draw.rect(win, (255, 255, 255), level5_btn)
        win.blit(txt_surf5, txt_rect5)

        #level6
        level6_btn = pygame.Rect(900, 200, 75, 75)
        level6_btn_text = pygame.font.Font('freesansbold.ttf', 50)
        txt_surf6, txt_rect6 = txt_obj("6", level6_btn_text)
        txt_rect6.center = ((900+(75/2)), (200+(75/2)))

        if level6_btn.collidepoint((mx, my)):
            if click:
                level6()

        pygame.draw.rect(win, (255, 255, 255), level6_btn)
        win.blit(txt_surf6, txt_rect6)

        pygame.display.update()
        clock.tick(120)

def level1():
    global score
    global meteors_hit
    global laser_timer
    global laser_active
    score = 0
    spaceship_group.sprite.health = 5
    meteor_group.empty()
    meteors_hit = 0

    run = True
    while run:
        win.blit(earth_bg,(0,0))

        draw_text('Level 1', font, (255, 255, 255), win, 1100, 20)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            METEOR_EVENT = pygame.USEREVENT
            pygame.time.set_timer(METEOR_EVENT, 500)

            if event.type == pygame.MOUSEBUTTONDOWN and laser_active:
                new_laser = Laser('Laser.png', 15, event.pos[0], event.pos[1])
                laser_group.add(new_laser)
                laser_active = False
                laser_timer = pygame.time.get_ticks()

            if event.type == METEOR_EVENT:
                meteor_path = random.choice(('Meteor1.png', 'Meteor2.png', 'Meteor3.png'))
                random_x = random.randrange(0,1300)
                random_y = random.randrange(-10,-5)
                random_xvel = random.randrange(-1,1)
                random_yvel = random.randrange(2,5)
                meteor = Meteor(meteor_path,random_x,random_y,random_xvel,random_yvel)
                meteor_group.add(meteor)

            if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.health <= 0:
                menu()

        minimap(win, (255, 255, 255, 50), (0,440, 600,210))
        win.blit(sun, (-100,450))
        win.blit(earth, (100, 525))
        win.blit(mars, (175, 525))
        win.blit(jupiter, (250, 525))
        win.blit(saturn, (325, 535))
        win.blit(uranus, (400, 525))
        win.blit(neptune, (500,510))

        circle(win, (255,0,0, 175),(137, 563), 35)

        mx, my = pygame.mouse.get_pos()

        back_btn = pygame.Rect(1085, 560, 150, 75)
        back_btn_text = pygame.font.Font('freesansbold.ttf', 50)
        txt_surf, txt_rect = txt_obj("Back", back_btn_text)
        txt_rect.center = ((1085+(150/2)), (560+(75/2)))

        if back_btn.collidepoint((mx, my)):
            if click:
                menu()

        pygame.draw.rect(win, (255, 255, 255), back_btn)
        win.blit(txt_surf, txt_rect)

        score_surface = game_font.render(f'SCORE: {score}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (125, 100))
        win.blit(score_surface, score_rect)

        meteor_hit_surface = game_font.render(f'METEORS HIT: {meteors_hit}',True,(255,255,255))
        meteor_hit_rect = meteor_hit_surface.get_rect(center = (165, 150))
        win.blit(meteor_hit_surface, meteor_hit_rect)

        if spaceship_group.sprite.health > 0:
            score += game()
        else:
            game_over()

        if score >= 2000:
            win.blit(bg, (0,0))

            game_over_surface1 = game_font.render('YOU REACHED 2000 POINTS AND DEFEATED EARTH',True, (255,255,255))
            game_over_surface2 = game_font.render('YOU WILL NOW MOVE ON TO MARS', True, (255,255,255))
            game_over_surface3 = game_font.render('CLICK "MARS" TO MOVE ON!', True, (255,255,255))

            game_over_rect1 = game_over_surface1.get_rect(center = (625,205))
            game_over_rect2 = game_over_surface2.get_rect(center = (625,250))
            game_over_rect3 = game_over_surface3.get_rect(center = (625,300))

            win.blit(game_over_surface1, game_over_rect1)
            win.blit(game_over_surface2, game_over_rect2)
            win.blit(game_over_surface3, game_over_rect3)

            mx, my = pygame.mouse.get_pos()

            button2 = pygame.Rect(475, 400, 300, 75)
            button2_text = pygame.font.Font('freesansbold.ttf', 50)
            txt_surf2, txt_rect2 = txt_obj("MARS", button2_text)
            txt_rect2.center = ((475+(300/2)), (400+(75/2)))

            pygame.draw.rect(win, (255, 255, 255), button2)
            win.blit(txt_surf2, txt_rect2)

            if button2.collidepoint((mx, my)):
                if click:
                    level2()
            
        pygame.display.update()
        clock.tick(120)

def level2():
    global score
    global meteors_hit
    global laser_active
    global laser_timer
    score = 0
    spaceship_group.sprite.health = 5
    meteor_group.empty()
    meteors_hit = 0

    run = True
    while run:
        win.blit(mars_bg,(0,0))

        draw_text('Level 2', font, (255, 255, 255), win, 1110, 20)

        click = False        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            METEOR_EVENT = pygame.USEREVENT
            pygame.time.set_timer(METEOR_EVENT, 100)

            if event.type == pygame.MOUSEBUTTONDOWN and laser_active:
                new_laser1 = Laser('Laser.png', 15, event.pos[0]+15, event.pos[1])
                laser_group.add(new_laser1)

                new_laser2 = Laser('Laser.png', 15, event.pos[0]-15, event.pos[1])
                laser_group.add(new_laser2)

                laser_active = False
                laser_timer = pygame.time.get_ticks()

            if event.type == METEOR_EVENT:
                meteor_path = random.choice(('Meteor1.png', 'Meteor2.png', 'Meteor3.png'))
                random_x = random.randrange(0,1300)
                random_y = random.randrange(-500,-50)
                random_xvel = random.randrange(-1,1)
                random_yvel = random.randrange(3,7)
                meteor = Meteor(meteor_path,random_x,random_y,random_xvel,random_yvel)
                meteor_group.add(meteor)

            if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.health <= 0:
                menu()

        minimap(win, (255, 255, 255, 50), (0,440, 600,210))
        win.blit(sun, (-100,450))
        win.blit(earth, (100, 525))
        win.blit(mars, (175, 525))
        win.blit(jupiter, (250, 525))
        win.blit(saturn, (325, 535))
        win.blit(uranus, (400, 525))
        win.blit(neptune, (500,510))

        circle(win, (0,0,0, 175),(137, 563), 35)
        circle(win, (255,0,0, 175),(212, 563), 37)

        draw_text('x', font1, (255,0,0), win, 110, 510)

        mx, my = pygame.mouse.get_pos()

        back_btn = pygame.Rect(1085, 560, 150, 75)
        back_btn_text = pygame.font.Font('freesansbold.ttf', 50)
        txt_surf, txt_rect = txt_obj("Back", back_btn_text)
        txt_rect.center = ((1085+(150/2)), (560+(75/2)))

        if back_btn.collidepoint((mx, my)):
            if click:
                menu()

        pygame.draw.rect(win, (255, 255, 255), back_btn)
        win.blit(txt_surf, txt_rect)

        score_surface = game_font.render(f'SCORE: {score}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (125, 100))
        win.blit(score_surface, score_rect)

        meteor_hit_surface = game_font.render(f'METEORS HIT: {meteors_hit}',True,(255,255,255))
        meteor_hit_rect = meteor_hit_surface.get_rect(center = (165, 150))
        win.blit(meteor_hit_surface, meteor_hit_rect)

        if spaceship_group.sprite.health > 0:
            score += game()
        else:
            game_over()

        if score >= 2500:
            win.blit(bg, (0,0))

            game_over_surface1 = game_font.render('YOU REACHED 2500 POINTS AND DEAFETED MARS',True, (255,255,255))
            game_over_surface2 = game_font.render('YOU WILL NOW MOVE ON TO SATURN', True, (255,255,255))
            game_over_surface3 = game_font.render('CLICK "SATURN" TO MOVE ON!', True, (255,255,255))

            game_over_rect1 = game_over_surface1.get_rect(center = (625,205))
            game_over_rect2 = game_over_surface2.get_rect(center = (625,250))
            game_over_rect3 = game_over_surface3.get_rect(center = (625,300))

            win.blit(game_over_surface1, game_over_rect1)
            win.blit(game_over_surface2, game_over_rect2)
            win.blit(game_over_surface3, game_over_rect3)

            mx, my = pygame.mouse.get_pos()

            button3 = pygame.Rect(475, 400, 300, 75)
            button3_text = pygame.font.Font('freesansbold.ttf', 50)
            txt_surf3, txt_rect3 = txt_obj("SATURN", button3_text)
            txt_rect3.center = ((475+(300/2)), (400+(75/2)))

            pygame.draw.rect(win, (255, 255, 255), button3)
            win.blit(txt_surf3, txt_rect3)

            if button3.collidepoint((mx, my)):
                if click:
                    level3()

        pygame.display.update()
        clock.tick(120)

def level3():
    global score
    global meteors_hit
    global laser_active
    global laser_timer
    score = 0
    spaceship_group.sprite.health = 5
    meteor_group.empty()
    meteors_hit = 0

    run = True
    while run:
        win.blit(jupiter_bg,(0,0))

        draw_text('Level 3', font, (255, 255, 255), win, 1110, 20)

        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            METEOR_EVENT = pygame.USEREVENT
            pygame.time.set_timer(METEOR_EVENT, 85)

            if event.type == pygame.MOUSEBUTTONDOWN and laser_active:
                new_laser1 = Laser('Laser.png', 15, event.pos[0], event.pos[1])
                laser_group.add(new_laser1)
                
                new_laser2 = Laser_right('Laser_right.png', 15, event.pos[0]+25, event.pos[1])
                laser_group.add(new_laser2)

                new_laser3 = Laser_left('Laser_left.png', 15, event.pos[0]-25, event.pos[1])
                laser_group.add(new_laser3)

                laser_active = False
                laser_timer = pygame.time.get_ticks()


            if event.type == METEOR_EVENT:
                meteor_path = random.choice(('Meteor1.png', 'Meteor2.png', 'Meteor3.png'))
                random_x = random.randrange(0,1300)
                random_y = random.randrange(-500,-50)
                random_xvel = random.randrange(-1,1)
                random_yvel = random.randrange(5,9)
                meteor = Meteor(meteor_path,random_x,random_y,random_xvel,random_yvel)
                meteor_group.add(meteor)

            if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.health <= 0:
                menu()

        minimap(win, (255, 255, 255, 50), (0,440, 600,210))
        win.blit(sun, (-100,450))
        win.blit(earth, (100, 525))
        win.blit(mars, (175, 525))
        win.blit(jupiter, (250, 525))
        win.blit(saturn, (325, 535))
        win.blit(uranus, (400, 525))
        win.blit(neptune, (500,510))

        circle(win, (0,0,0, 175),(137, 563), 35)
        circle(win, (0,0,0, 175),(212, 563), 37)
        circle(win, (255,0,0, 175),(289, 563), 32)

        draw_text('x', font1, (255,0,0), win, 110, 510)
        draw_text('x', font1, (255,0,0), win, 185, 510)

        mx, my = pygame.mouse.get_pos()

        back_btn = pygame.Rect(1085, 560, 150, 75)
        back_btn_text = pygame.font.Font('freesansbold.ttf', 50)
        txt_surf, txt_rect = txt_obj("Back", back_btn_text)
        txt_rect.center = ((1085+(150/2)), (560+(75/2)))

        if back_btn.collidepoint((mx, my)):
            if click:
                menu()

        pygame.draw.rect(win, (255, 255, 255), back_btn)
        win.blit(txt_surf, txt_rect)

        score_surface = game_font.render(f'SCORE: {score}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (125, 100))
        win.blit(score_surface, score_rect)

        meteor_hit_surface = game_font.render(f'METEORS HIT: {meteors_hit}',True,(255,255,255))
        meteor_hit_rect = meteor_hit_surface.get_rect(center = (165, 150))
        win.blit(meteor_hit_surface, meteor_hit_rect)

        if spaceship_group.sprite.health > 0:
            score += game()
        else:
            game_over()

        if score >= 3000:
            win.blit(bg, (0,0))

            game_over_surface1 = game_font.render('YOU REACHED 3000 POINTS AND DEFEATED JUPITER',True, (255,255,255))
            game_over_surface2 = game_font.render('YOU WILL NOW MOVE ON TO SATURN', True, (255,255,255))
            game_over_surface3 = game_font.render('CLICK "SATURN" TO MOVE ON!', True, (255,255,255))

            game_over_rect1 = game_over_surface1.get_rect(center = (625,205))
            game_over_rect2 = game_over_surface2.get_rect(center = (625,250))
            game_over_rect3 = game_over_surface3.get_rect(center = (625,300))

            win.blit(game_over_surface1, game_over_rect1)
            win.blit(game_over_surface2, game_over_rect2)
            win.blit(game_over_surface3, game_over_rect3)

            mx, my = pygame.mouse.get_pos()

            button3 = pygame.Rect(475, 400, 300, 75)
            button3_text = pygame.font.Font('freesansbold.ttf', 50)
            txt_surf3, txt_rect3 = txt_obj("SATURN", button3_text)
            txt_rect3.center = ((475+(300/2)), (400+(75/2)))

            pygame.draw.rect(win, (255, 255, 255), button3)
            win.blit(txt_surf3, txt_rect3)

            if button3.collidepoint((mx, my)):
                if click:
                    level4()

        pygame.display.update()
        clock.tick(120)

def level4():
    global score
    global meteors_hit
    global laser_active
    global laser_timer
    score = 0
    spaceship_group.sprite.health = 5
    meteor_group.empty()
    meteors_hit = 0

    run = True
    while run:
        win.blit(saturn_bg,(0,0))

        draw_text('Level 4', font, (255, 255, 255), win, 1110, 20)

        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            METEOR_EVENT = pygame.USEREVENT
            pygame.time.set_timer(METEOR_EVENT, 80)

            if event.type == pygame.MOUSEBUTTONDOWN and laser_active:
                new_laser1 = Laser('Laser.png', 15, event.pos[0], event.pos[1])
                laser_group.add(new_laser1)
                
                new_laser2 = Laser_right('Laser_right.png', 15, event.pos[0]+15, event.pos[1])
                laser_group.add(new_laser2)

                new_laser3 = Laser_left('Laser_left.png', 15, event.pos[0]-15, event.pos[1])
                laser_group.add(new_laser3)

                laser_active = False
                laser_timer = pygame.time.get_ticks()


            if event.type == METEOR_EVENT:
                meteor_path = random.choice(('Meteor1.png', 'Meteor2.png', 'Meteor3.png'))
                random_x = random.randrange(0,1300)
                random_y = random.randrange(-500,-50)
                random_xvel = random.randrange(-1,1)
                random_yvel = random.randrange(6,11)
                meteor = Meteor(meteor_path,random_x,random_y,random_xvel,random_yvel)
                meteor_group.add(meteor)

            if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.health <= 0:
                menu()

        minimap(win, (255, 255, 255, 50), (0,440, 600,210))
        win.blit(sun, (-100,450))
        win.blit(earth, (100, 525))
        win.blit(mars, (175, 525))
        win.blit(jupiter, (250, 525))
        win.blit(saturn, (325, 535))
        win.blit(uranus, (400, 525))
        win.blit(neptune, (500,510))

        circle(win, (0,0,0, 175),(137, 563), 35)
        circle(win, (0,0,0, 175),(212, 563), 37)
        circle(win, (0,0,0, 175),(289, 563), 32)
        circle(win, (255,0,0, 175),(363, 562), 18)

        draw_text('x', font1, (255,0,0), win, 110, 510)
        draw_text('x', font1, (255,0,0), win, 185, 510)
        draw_text('x', font1, (255,0,0), win, 260, 510)

        mx, my = pygame.mouse.get_pos()

        back_btn = pygame.Rect(1085, 560, 150, 75)
        back_btn_text = pygame.font.Font('freesansbold.ttf', 50)
        txt_surf, txt_rect = txt_obj("Back", back_btn_text)
        txt_rect.center = ((1085+(150/2)), (560+(75/2)))

        if back_btn.collidepoint((mx, my)):
            if click:
                menu()

        pygame.draw.rect(win, (255, 255, 255), back_btn)
        win.blit(txt_surf, txt_rect)

        score_surface = game_font.render(f'SCORE: {score}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (125, 100))
        win.blit(score_surface, score_rect)

        meteor_hit_surface = game_font.render(f'METEORS HIT: {meteors_hit}',True,(255,255,255))
        meteor_hit_rect = meteor_hit_surface.get_rect(center = (165, 150))
        win.blit(meteor_hit_surface, meteor_hit_rect)

        if spaceship_group.sprite.health > 0:
            score += game()
        else:
            game_over()

        if score >= 3000:
            win.blit(bg, (0,0))

            game_over_surface1 = game_font.render('YOU REACHED 3000 POINTS AND DEFEATED SATURN',True, (255,255,255))
            game_over_surface2 = game_font.render('YOU WILL NOW MOVE ON TO URANUS', True, (255,255,255))
            game_over_surface3 = game_font.render('CLICK "URANUS" TO MOVE ON!', True, (255,255,255))

            game_over_rect1 = game_over_surface1.get_rect(center = (625,205))
            game_over_rect2 = game_over_surface2.get_rect(center = (625,250))
            game_over_rect3 = game_over_surface3.get_rect(center = (625,300))

            win.blit(game_over_surface1, game_over_rect1)
            win.blit(game_over_surface2, game_over_rect2)
            win.blit(game_over_surface3, game_over_rect3)

            mx, my = pygame.mouse.get_pos()

            button4 = pygame.Rect(475, 400, 300, 75)
            button4_text = pygame.font.Font('freesansbold.ttf', 50)
            txt_surf4, txt_rect4 = txt_obj("URANUS", button4_text)
            txt_rect4.center = ((475+(300/2)), (400+(75/2)))

            pygame.draw.rect(win, (255, 255, 255), button4)
            win.blit(txt_surf4, txt_rect4)

            if button4.collidepoint((mx, my)):
                if click:
                    level5()

        pygame.display.update()
        clock.tick(120)

def level5():
    global score
    global meteors_hit
    global arc_time
    global laser_active
    global laser_timer
    score = 0
    spaceship_group.sprite.health = 5
    meteor_group.empty()
    meteors_hit = 0
    arc_time = 0

    run = True
    while run:
        win.blit(uranus_bg,(0,0))

        draw_text('Level 4', font, (255, 255, 255), win, 1110, 20)

        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            METEOR_EVENT = pygame.USEREVENT
            pygame.time.set_timer(METEOR_EVENT, 75)

            if event.type == pygame.MOUSEBUTTONDOWN and laser_active:
                new_laser = Laser('arc_laser.png', 15, event.pos[0], event.pos[1])
                laser_group.add(new_laser)

                laser_active = False
                laser_timer = pygame.time.get_ticks()

            if event.type == METEOR_EVENT:
                meteor_path = random.choice(('Meteor1.png', 'Meteor2.png', 'Meteor3.png'))
                random_x = random.randrange(0,1300)
                random_y = random.randrange(-500,-50)
                random_xvel = random.randrange(-1,1)
                random_yvel = random.randrange(6,13)
                meteor = Meteor(meteor_path,random_x,random_y,random_xvel,random_yvel)
                meteor_group.add(meteor)

            if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.health <= 0:
                menu()

        minimap(win, (255, 255, 255, 50), (0,440, 600,210))
        win.blit(sun, (-100,450))
        win.blit(earth, (100, 525))
        win.blit(mars, (175, 525))
        win.blit(jupiter, (250, 525))
        win.blit(saturn, (325, 535))
        win.blit(uranus, (400, 525))
        win.blit(neptune, (500,510))

        circle(win, (0,0,0, 175),(137, 563), 35)
        circle(win, (0,0,0, 175),(212, 563), 37)
        circle(win, (0,0,0, 175),(289, 563), 32)
        circle(win, (0,0,0, 175),(363, 563), 18)
        circle(win, (255,0,0, 175),(438, 563), 37)

        draw_text('x', font1, (255,0,0), win, 110, 510)
        draw_text('x', font1, (255,0,0), win, 185, 510)
        draw_text('x', font1, (255,0,0), win, 260, 510)
        draw_text('x', font1, (255,0,0), win, 335, 510)

        mx, my = pygame.mouse.get_pos()

        back_btn = pygame.Rect(1085, 560, 150, 75)
        back_btn_text = pygame.font.Font('freesansbold.ttf', 50)
        txt_surf, txt_rect = txt_obj("Back", back_btn_text)
        txt_rect.center = ((1085+(150/2)), (560+(75/2)))

        if back_btn.collidepoint((mx, my)):
            if click:
                menu()

        pygame.draw.rect(win, (255, 255, 255), back_btn)
        win.blit(txt_surf, txt_rect)

        score_surface = game_font.render(f'SCORE: {score}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (125, 100))
        win.blit(score_surface, score_rect)

        meteor_hit_surface = game_font.render(f'METEORS HIT: {meteors_hit}',True,(255,255,255))
        meteor_hit_rect = meteor_hit_surface.get_rect(center = (165, 150))
        win.blit(meteor_hit_surface, meteor_hit_rect)

        if spaceship_group.sprite.health > 0:
            score += game()
        else:
            game_over()

        if score >= 3000:
            win.blit(bg, (0,0))

            game_over_surface1 = game_font.render('YOU REACHED 3000 POINTS AND DEFEATED SATURN',True, (255,255,255))
            game_over_surface2 = game_font.render('YOU WILL NOW MOVE ON TO URANUS', True, (255,255,255))
            game_over_surface3 = game_font.render('CLICK "URANUS" TO MOVE ON!', True, (255,255,255))

            game_over_rect1 = game_over_surface1.get_rect(center = (625,205))
            game_over_rect2 = game_over_surface2.get_rect(center = (625,250))
            game_over_rect3 = game_over_surface3.get_rect(center = (625,300))

            win.blit(game_over_surface1, game_over_rect1)
            win.blit(game_over_surface2, game_over_rect2)
            win.blit(game_over_surface3, game_over_rect3)

            mx, my = pygame.mouse.get_pos()

            button4 = pygame.Rect(475, 400, 300, 75)
            button4_text = pygame.font.Font('freesansbold.ttf', 50)
            txt_surf4, txt_rect4 = txt_obj("URANUS", button4_text)
            txt_rect4.center = ((475+(300/2)), (400+(75/2)))

            pygame.draw.rect(win, (255, 255, 255), button4)
            win.blit(txt_surf4, txt_rect4)

            if button4.collidepoint((mx, my)):
                if click:
                    level6()

        pygame.display.update()
        clock.tick(120)

def level6():
    global score
    global meteors_hit
    global laser_active
    global laser_timer
    score = 0
    spaceship_group.sprite.health = 5
    meteor_group.empty()
    meteors_hit = 0

    run = True
    while run:
        win.blit(neptune_bg,(0,0))

        draw_text('Level 4', font, (255, 255, 255), win, 1110, 20)

        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            METEOR_EVENT = pygame.USEREVENT
            pygame.time.set_timer(METEOR_EVENT, 80)

            if event.type == pygame.MOUSEBUTTONDOWN and laser_active:
                new_laser1 = Laser_left('arc_laser_tilt1.png', 15, event.pos[0]-10, event.pos[1])
                laser_group.add(new_laser1)

                new_laser2 = Laser_right('arc_laser_tilt2.png', 15, event.pos[0]+10, event.pos[1])
                laser_group.add(new_laser2)

                new_laser3 = Laser('arc_laser.png', 15, event.pos[0]+10, event.pos[1])
                laser_group.add(new_laser3)

                laser_active = False
                laser_timer = pygame.time.get_ticks()


            if event.type == METEOR_EVENT:
                meteor_path = random.choice(('Meteor1.png', 'Meteor2.png', 'Meteor3.png'))
                random_x = random.randrange(0,1300)
                random_y = random.randrange(-500,-50)
                random_xvel = random.randrange(-1,1)
                random_yvel = random.randrange(6,15)
                meteor = Meteor(meteor_path,random_x,random_y,random_xvel,random_yvel)
                meteor_group.add(meteor)

            if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.health <= 0:
                menu()

        minimap(win, (255, 255, 255, 50), (0,440, 600,210))
        win.blit(sun, (-100,450))
        win.blit(earth, (100, 525))
        win.blit(mars, (175, 525))
        win.blit(jupiter, (250, 525))
        win.blit(saturn, (325, 535))
        win.blit(uranus, (400, 525))
        win.blit(neptune, (500,510))

        circle(win, (0,0,0, 175),(137, 563), 35)
        circle(win, (0,0,0, 175),(212, 563), 37)
        circle(win, (0,0,0, 175),(289, 563), 32)
        circle(win, (0,0,0, 175),(363, 563), 18)
        circle(win, (0,0,0, 175),(438, 563), 37)
        circle(win, (255,0,0, 175),(550, 558), 49)

        draw_text('x', font1, (255,0,0), win, 110, 510)
        draw_text('x', font1, (255,0,0), win, 185, 510)
        draw_text('x', font1, (255,0,0), win, 260, 510)
        draw_text('x', font1, (255,0,0), win, 335, 510)
        draw_text('x', font1, (255,0,0), win, 410, 510)

        mx, my = pygame.mouse.get_pos()

        back_btn = pygame.Rect(1085, 560, 150, 75)
        back_btn_text = pygame.font.Font('freesansbold.ttf', 50)
        txt_surf, txt_rect = txt_obj("Back", back_btn_text)
        txt_rect.center = ((1085+(150/2)), (560+(75/2)))

        if back_btn.collidepoint((mx, my)):
            if click:
                menu()

        pygame.draw.rect(win, (255, 255, 255), back_btn)
        win.blit(txt_surf, txt_rect)

        score_surface = game_font.render(f'SCORE: {score}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (125, 100))
        win.blit(score_surface, score_rect)

        meteor_hit_surface = game_font.render(f'METEORS HIT: {meteors_hit}',True,(255,255,255))
        meteor_hit_rect = meteor_hit_surface.get_rect(center = (165, 150))
        win.blit(meteor_hit_surface, meteor_hit_rect)

        if spaceship_group.sprite.health > 0:
            score += game()
        else:
            game_over()

        if score >= 3000:
            win.blit(bg, (0,0))

            game_over_surface1 = game_font.render('YOU REACHED 3000 POINTS AND DEFEATED SATURN',True, (255,255,255))
            game_over_surface2 = game_font.render('YOU WILL NOW MOVE ON TO URANUS', True, (255,255,255))
            game_over_surface3 = game_font.render('CLICK "URANUS" TO MOVE ON!', True, (255,255,255))

            game_over_rect1 = game_over_surface1.get_rect(center = (625,205))
            game_over_rect2 = game_over_surface2.get_rect(center = (625,250))
            game_over_rect3 = game_over_surface3.get_rect(center = (625,300))

            win.blit(game_over_surface1, game_over_rect1)
            win.blit(game_over_surface2, game_over_rect2)
            win.blit(game_over_surface3, game_over_rect3)

            mx, my = pygame.mouse.get_pos()

            button4 = pygame.Rect(475, 400, 300, 75)
            button4_text = pygame.font.Font('freesansbold.ttf', 50)
            txt_surf4, txt_rect4 = txt_obj("URANUS", button4_text)
            txt_rect4.center = ((475+(300/2)), (400+(75/2)))

            pygame.draw.rect(win, (255, 255, 255), button4)
            win.blit(txt_surf4, txt_rect4)

            if button4.collidepoint((mx, my)):
                if click:
                    pass

        pygame.display.update()
        clock.tick(120)

menu()
