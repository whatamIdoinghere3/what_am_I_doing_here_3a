from pygame import *
from random import randint
from time import \
    time as timer  # import the timing function so that the interpreter doesn’t need to look for this function in the pygame module time, give it a different name ourselves

# background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# fonts and labels
font.init()
font2 = font.Font(None, 36)

font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

# image
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"  # enemy
img_bullet = "bullet.png"
img_ast = "asteroid.png"  # asteroid

score = 0
lost = 0
max_lost = 3

goal = 10  # how many ships need to be hit to win

life = 3  # Life Point


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    # method to control the sprite with arrow keys
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()


# create a window
win_width = 700
win_height = 500
display.set_caption("Shooter Games - Nadia Maharani")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    print('monster ke ', i, 'kecepatan = ', randint(1, 7))
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

bullets = sprite.Group()
finish = False

# Main loop
run = True

rel_time = False  # flag in charge of reload
num_fire = 0  # variable to count shots

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # fire_sound.play()
                # ship.fire()

                # check how many shots have been fired and whether reload is in progress
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:  # if the player fired 5 shots
                    last_time = timer()  # record time when this happened
                    rel_time = True  # set the reload flag

    if not finish:
        window.blit(background, (0, 0))

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()  # read time

            if now_time - last_time < 3:  # before 3 seconds are over, display reload message
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0  # set the bullets counter to zero
                rel_time = False  # reset the reload flag

        # bullet-monster collision check (both monster and bullet disappear upon touching)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # this loop will be repeated as many times as monsters are killed
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # possible loss: missed too many or the character collided with the enemy
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True  # lost, set the background and no more sprite control.
            window.blit(lose, (200, 200))

        # win check: how many points did you score?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    time.delay(50)


