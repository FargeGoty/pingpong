import pygame
from pygame import *
import random

font.init()
font = font.Font("font.ttf", 30)
winsfile = open("wins.txt","a")

win_width = 800
win_height = 450

window = display.set_mode((win_width, 500))
window.fill((0,3,11))
display.set_caption("Ping-Pong")
mixer.init()
mixer.pre_init(44100, 16, 2, 4096)
mixer.music.load("music.mp3")
mixer.music.set_volume(.5)
mixer.music.play()
winsound = mixer.Sound("win.wav")
winsound.set_volume(3)
defentsound = mixer.Sound("defent.wav")
defentsound.set_volume(10)
balltouchsound = mixer.Sound("balltouch.wav")
losesound = mixer.Sound("lose.wav")
winsound = mixer.Sound("win.wav")
FPS = 60
game = True
clock = time.Clock()
ball_speed_x = 5
ball_speed_y = 5
opponent_speed = 5
timer = 60

player_points = 0
opponent_points = 0

def win():
    global player_points,winsound
    player_points += 1
    winsound.play()

def defent():
    global opponent_points,defentsound
    opponent_points += 1
    defentsound.play()

def loadify(img):
    return image.load(img).convert_alpha()

class GameSprite(sprite.Sprite):
    def __init__(self, image:str, width:int, height:int):
        super().__init__()
        self.width = width
        self.height = height
        self.origimage = image
        self.image = transform.scale(loadify(image), (width,height))
        self.rect = self.image.get_rect()
        self.flipped = False
        self.mirrored = False
        self.speed = 0
    def render(self):
        window.blit(transform.flip(self.image, self.mirrored, self.flipped), self.rect)

class Player(GameSprite):
    def update(self,upkey,downkey,speed):
        if upkey and self.rect.y > 0+50:
            self.rect.y -= speed
        if downkey and self.rect.y < win_height-120+50:
            self.rect.y += speed

class Enemy(GameSprite):
    def update(self,ball):
        global opponent_speed
        if self.rect.top < ball.rect.y:
            self.rect.top += opponent_speed
        if self.rect.bottom > ball.rect.y:
            self.rect.bottom -= opponent_speed

class Sphere(GameSprite):
    def update(self,player,opponent):
        global ball_speed_x, ball_speed_y,win_width,win_height,balltouchsound,win,defent
        self.rect.x += ball_speed_x
        self.rect.y += ball_speed_y
        if self.rect.top <= 0+55 or self.rect.bottom >= win_height+50:
            ball_speed_y *= -1
            balltouchsound.play()
        if self.rect.right >= win_width:
            ball_speed_x *= -1
            defent()
            self.restart()
        if self.rect.left <= 0:
            ball_speed_x *= -1
            win()
            self.restart()

        if self.rect.colliderect(player.rect) or self.rect.colliderect(opponent.rect):
            ball_speed_x *= -1
            balltouchsound.play()
    def restart(self):
        global ball_speed_x,ball_speed_y
        self.rect.x = win_height/2
        self.rect.y = win_width/2
        ball_speed_y = 5
        ball_speed_x = 5

background = GameSprite("Background.png",win_width,win_height+50)
board = GameSprite("Board.png",win_width,win_height)
player = Player("Player.png",20,120)
opponent = Enemy("Computer.png",20,120)
ball = Sphere("Ball.png",30,30)
playercounterfake = GameSprite("ScoreBar.png",350,50)
opponentcounterfake = GameSprite("ScoreBar.png",350,50)

board.rect.y = 0+50
player.rect.x = win_width - 40
player.rect.y = 180+50
opponent.rect.x = 0 + 20
opponent.rect.y = 180+50
playercounterfake.rect.x = 0
playercounterfake.rect.y = 0
opponentcounterfake.rect.x = win_width-opponentcounterfake.width
opponentcounterfake.mirrored = True
opponentcounterfake.rect.y = 0

ball.restart()

gameend = False

start_ticks=time.get_ticks()
while game:
    key_pressed = key.get_pressed() 
    background.render()
    board.render()
    if not gameend:
        player.render()
        opponent.render()
        ball.render()
        player.update(key_pressed[K_UP],key_pressed[K_DOWN],5)
        opponent.update(ball)
        ball.update(player,opponent)
    playercounterfake.render()
    opponentcounterfake.render()
    seconds=(time.get_ticks()-start_ticks)/1000 #calculate how many seconds
    playerpointscounter = font.render(
    str(player_points), True, (236,211,228)
    )
    opponentpointscounter = font.render(
    str(opponent_points), True, (236,211,228)
    )
    faketimer = font.render(
    "Time", True, (84,55,78)
    )
    realtimer = font.render(
    str(timer-int(seconds)), True, (236,211,228)
    )
    enemytext = font.render(
    "Enemy", True, (84,55,78)
    )
    playertext = font.render(
    "You", True, (84,55,78)
    )
    if not gameend:
        window.blit(realtimer, (376,15))
        window.blit(faketimer, (376,-7))
    window.blit(playertext, (win_width-200,5))
    window.blit(enemytext, (0+50,5))
    window.blit(playerpointscounter, (win_width-150,5))
    window.blit(opponentpointscounter, (0+150,5))
    if timer-int(seconds) < 1:
        if player_points < opponent_points and not gameend:
            print("!Оппонент победил!")
            wintext = font.render(
            "Enemy win!", True, (236,211,228)
            )
            winsfile.write("Оппонент победил\n")
        if player_points > opponent_points and not gameend:
            print("!Игрок победил!")
            wintext = font.render(
            "Player win!", True, (236,211,228)
            )
            winsfile.write("Игрок победил\n")
        if player_points == opponent_points and not gameend:
            print("!Ничья!")
            wintext = font.render(
            "Tie!", True, (236,211,228)
            )
            winsfile.write("Ничья\n")
        if player_points < opponent_points:
            window.blit(wintext, (0+150,50))
            losesound.play()
        if player_points > opponent_points:
            window.blit(wintext, (win_height+150,50))
            winsound.play()
        if player_points == opponent_points:
            window.blit(wintext, (0+385,50))
        winsfile.close()
        gameend = True
        mixer.music.stop()
    for e in event.get():
        if e.type == QUIT:
            print("QUIT")
            game = False
    display.update()
    clock.tick(FPS)