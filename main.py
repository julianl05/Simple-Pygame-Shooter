import pygame, sys, random, math
from pygame import Color, Surface

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
# asset credits
# Heart Icon: NicoleMarieProductions https://opengameart.org/content/heart-1616
# Zombie and Fast Zombie: Riley Gombart https://opengameart.org/content/animated-top-down-zombie https://opengameart.org/content/top-down-animated-zombie-set
# Player Avatar: Square Pug https://opengameart.org/content/top-down-shooter-character
# Tank/Target Zombie: Sean Noonan https://opengameart.org/content/top-down-cultist-creature
# Grass Background: hassekf https://opengameart.org/content/tower-defense-grass-background
# Bullet: Kenny.nl https://opengameart.org/content/space-shooter-redux
# Blood Splatters: PWl https://opengameart.org/content/blood-splats

def progress_bar(amount, cap, length, width, xpos, ypos):
    pygame.draw.rect(screen, DARK_GRAY, ((xpos, ypos), (length, width)))
    for i in range(amount):
        score = amount * (length/cap)
        if score <= length:
            pygame.draw.rect(screen, BLUE, ((xpos, ypos), (score, width)))
        else:
            return True

class Player(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def update(self):
        #self.rect.center = pygame.mouse.get_pos()
        self.screen_constrain()

    def screen_constrain(self):
        if self.rect.right >= 1280:
            self.rect.right = 1280
        if self.rect.left <= 0:
            self.rect.left = 0


class SlowZombie(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, x_speed, y_speed, health):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.penalty = 0
        self.health = health

    def update(self):
        progress_bar(self.health, 3, 100, 10, self.rect.centerx - 50, self.rect.centery - 50)
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

    def damage(self,amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return 1

    def slow(self, amount):
        self.rect.centery -= amount



class FastZombie(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, x_speed, y_speed, health):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.health = health

    def update(self):
        progress_bar(self.health, 1, 100, 10, self.rect.centerx - 50, self.rect.centery - 50)
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

    def damage(self,amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return 2



class TargetZombie(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, x_speed, y_speed, health):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.health = health
        self.penalty = 0

    def update(self):
        # if self.rect.centerx > player.rect.centerx:
        #     self.rect.centerx -= self.x_speed
        # else:
        #     self.rect.centerx += self.x_speed
        # if self.rect.centery > player.rect.centery:
        #     self.rect.centery -= self.y_speed
        # else:
        #     self.rect.centery += self.y_speed
        progress_bar(self.health, 5, 100, 10, self.rect.centerx - 50, self.rect.centery - 50)
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

    def damage(self,amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return 3

    def slow(self, amount):
        self.rect.centery -= amount


class Bullet(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos,y_pos))
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.centery <= -100:
            self.kill()

    def screen_constrain(self):
        if self.rect.centery <= -1:
            self.kill()


class Blood(pygame.sprite.Sprite):
    def __init__(self, path, xpos, ypos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(xpos,ypos))
        self.fade_timer = 0


    def update(self):
        self.fade_timer += 1
        if self.fade_timer >= 15:
            self.kill()


pygame.init()  # initiate pygame
screen = pygame.display.set_mode((1280, 720))  # Create display surface
clock = pygame.time.Clock()  # Create clock object

lose_color = Color(255, 0, 0, 5)
win_color = Color(255, 255, 255, 5)
game_over = pygame.Surface((1280,720), flags=pygame.SRCALPHA)

grass_bg = pygame.image.load('grass_template2.png')
blur_bg = pygame.image.load('blur.png')

BLUE = (0,80,160)
DARK_GRAY = (30,30,30)

game_font = pygame.font.Font('BLOODY.TTF', 80)
game_font2 = pygame.font.Font('ka1.TTF', 60)

player = Player('shooting.png', 640, 650)
player_group = pygame.sprite.GroupSingle()
player_group.add(player)

bullet_group = pygame.sprite.Group()
acid_group = pygame.sprite.Group()

fzombie_group = pygame.sprite.Group()
szombie_group = pygame.sprite.Group()
tzombie_group = pygame.sprite.Group()
damage_blood = pygame.sprite.Group()

zombie_yspeed = 1
zombie_xspeed = 0

ZOMBIE_EVENT = pygame.USEREVENT
pygame.time.set_timer(ZOMBIE_EVENT, 900)

SZOMBIE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SZOMBIE_EVENT, 900)

score_count = 0

zombie_count = 0

move = 256

alternate_fire = 0

running = True
win = False
fail = False
lose = False

zombie_list = []
pos_list = []

timer = 0
while True:  # Game loop
    if running:
        for event in pygame.event.get():  # Check for events / Player input
            if event.type == pygame.QUIT:  # Close the game
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if alternate_fire == 0:
                        new_bullet = Bullet('Laser.png', player.rect.centerx + 35, player.rect.centery, 15)
                        bullet_group.add(new_bullet)
                        alternate_fire = 1
                    elif alternate_fire == 1:
                        new_bullet = Bullet('Laser.png', player.rect.centerx - 35, player.rect.centery, 15)
                        bullet_group.add(new_bullet)
                        alternate_fire = 0

                if event.key == pygame.K_LEFT:
                    if player.rect.centerx != 128:
                        player.rect.centerx -= 256
                if event.key == pygame.K_RIGHT:
                    if player.rect.centerx != 1152:
                        player.rect.centerx += 256
                if event.key == pygame.K_a:
                    if player.rect.centerx != 128:
                        player.rect.centerx -= 256
                if event.key == pygame.K_d:
                    if player.rect.centerx != 1152:
                        player.rect.centerx += 256

            if event.type == ZOMBIE_EVENT:
                zombie_path = 'skeleton-attack_0.png'
                random_x_pos = random.choice((128, 384, 640, 896, 1152))
                y_pos = -50
                szombie = SlowZombie(zombie_path, random_x_pos, y_pos, zombie_xspeed, zombie_yspeed, 3)
                szombie_group.add(szombie)
                zombie_count += 1

            if event.type == ZOMBIE_EVENT and zombie_count % 4 == 0:
                zombie_path = 'run0001.png'
                random_x_pos = random.choice((128, 384, 640, 896, 1152))
                y_pos = -10
                fzombie_yspeed = zombie_xspeed + random.choice((2,3,4))
                fzombie = FastZombie(zombie_path, random_x_pos, y_pos, zombie_xspeed, fzombie_yspeed, 1)
                fzombie_group.add(fzombie)
                zombie_count += 1

            if event.type == ZOMBIE_EVENT and zombie_count % 5 == 0:
                zombie_path = 'cultist.png'
                random_x_pos = random.choice((128, 384, 640, 896, 1152))
                y_pos = -10
                tzombie_yspeed = 1
                tzombie = TargetZombie(zombie_path, random_x_pos, y_pos, zombie_xspeed, tzombie_yspeed, 5)
                tzombie_group.add(tzombie)
                zombie_count += 1

        for fzombie in fzombie_group:
            if pygame.sprite.spritecollide(fzombie, bullet_group, True):
                zombie_list.append(fzombie.damage(1))
                pos = fzombie.rect.center
                pos_list.append(pos)
            if fzombie.rect.centery >= 720:
                fail = True
                lose = True
                running = False

        for szombie in szombie_group:
            if pygame.sprite.spritecollide(szombie, bullet_group, True):
                szombie.slow(15)
                zombie_list.append(szombie.damage(1))
                pos = szombie.rect.center
                pos_list.append(pos)
            if szombie.rect.centery >= 720:
                fail = True
                lose = True
                running = False

        for tzombie in tzombie_group:
            if pygame.sprite.spritecollide(tzombie, bullet_group, True):
                tzombie.slow(10)
                zombie_list.append(tzombie.damage(1))
                pos = tzombie.rect.center
                pos_list.append(pos)
            if tzombie.rect.centery >= 720:
                fail = True
                lose = True
                running = False

        if pygame.sprite.spritecollide(player, szombie_group, True) or pygame.sprite.spritecollide(player, fzombie_group, True) or pygame.sprite.spritecollide(player, tzombie_group, True):
            lose = True
            running = False

        for i, pos in enumerate(pos_list):
            fade_timer = 0
            damage_image = random.choice(('blood_1.png','blood_5.png','blood_6.png','blood_7.png'))
            damage = Blood(damage_image, pos[0], pos[1] + 10)
            damage_blood.add(damage)
            del pos_list[i]

        screen.blit(grass_bg,(0,0))

        bullet_group.draw(screen)
        player_group.draw(screen)
        szombie_group.draw(screen)
        fzombie_group.draw(screen)
        tzombie_group.draw(screen)
        acid_group.draw(screen)
        damage_blood.draw(screen)

        bullet_group.update()
        player_group.update()
        szombie_group.update()
        fzombie_group.update()
        tzombie_group.update()
        acid_group.update()
        damage_blood.update()

        zombie_list = list(filter(None,zombie_list))
        print(zombie_list)

        win = progress_bar(len(zombie_list), 30, 1280, 30, 0, 700)
        if win:
            running = False

    elif win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    win = False
                    running = True

        game_over.fill(win_color)
        screen.blit(game_over,(0,0))
        text_surface = game_font2.render('You Survived!', True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(640, 360))
        screen.blit(text_surface, text_rect)

    elif lose:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    lose = False
                    fail = False
                    running = True

        game_over.fill(lose_color)
        screen.blit(game_over, (0, 0))
        if fail:
            text_surface = game_font.render('A Zombie Escaped...', True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(640, 360))
            screen.blit(text_surface, text_rect)
        else:
            text_surface = game_font.render('You Died...', True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(640, 360))
            screen.blit(text_surface, text_rect)

    timer += 1
    pygame.display.update()  # Draw frame
    clock.tick(120)  # Control the framerate