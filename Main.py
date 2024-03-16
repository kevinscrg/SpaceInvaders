import sys

import pygame
import random
import math
from pygame import mixer
import io

from Class.Button import Button
from Entitys.Bullet import Bullet
from Entitys.Enemy import Enemy
from Entitys.Player import Player



def Read_Font(fuente):
    with open(fuente,'rb') as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)


def Display_Score(score,font,screen,Score_x,Score_y):
    text = font.render(f"Score: {score}",True, (255, 255, 255))
    screen.blit(text, (Score_x, Score_y))


def colision(ent1,ent2):
    if math.sqrt(math.pow(ent2.x - ent1.x,2) + math.pow(ent2.y - ent1.y,2)) < 75:
        return True
    else:
        return False


def Final_Text(f_final,screen):
    FinalFont = f_final.render("YOU LOSE",True,(255,0,0))
    screen.blit(FinalFont,(670,400))

def DisplayEntity(entity,screen):
    screen.blit(entity.image,(entity.x,entity.y))

def EnemySpawn(enemies, nr_rows, cuantity):
    l = []
    for i in range(nr_rows):
        for j in range(cuantity):
            l.append(Enemy(1, 1, 128 * j + 115, i * 128 + 100, i * 0.5 + 0.5, pygame.image.load("assets/enemigo1.png")))
        enemies.append(l)
        l =[]


def Win(screen, f_final,Bytes_Font):
    final_text1 = f_final.render("YOU WIN!", True, (255, 255, 255))
    execution = True
    rep_bttn = Button(image=None, pos=(900,450), text_input="Replay", font=pygame.font.Font(Bytes_Font, 60),
                      base_color="#d7fcd4", hover_color="white")
    Quit_bttn = Button(image=None, pos=(900, 650), text_input="Main Menu", font=pygame.font.Font(Bytes_Font, 60),
                       base_color="#d7fcd4", hover_color="white")
    screen.blit(final_text1,(760,200))
    while execution:
        Mouse = pygame.mouse.get_pos()
        for button in [rep_bttn, Quit_bttn]:
            button.Mouse_On(Mouse)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rep_bttn.check_event(Mouse):
                    Game(screen,Bytes_Font)
                elif Quit_bttn.check_event(Mouse):
                    execution = False
        pygame.display.update()


def Lose(screen, f_final, Bytes_Font):
    final_text1 = f_final.render("YOU LOSE!", True, (255, 0, 0))
    execution = True
    rep_bttn = Button(image=None, pos=(900, 450), text_input="Replay", font=pygame.font.Font(Bytes_Font, 60),
                      base_color="#d7fcd4", hover_color="white")
    Quit_bttn = Button(image=None, pos=(900, 650), text_input="Main Menu", font=pygame.font.Font(Bytes_Font, 60),
                       base_color="#d7fcd4", hover_color="white")
    screen.blit(final_text1, (760, 200))
    while execution:
        Mouse = pygame.mouse.get_pos()
        for button in [rep_bttn, Quit_bttn]:
            button.Mouse_On(Mouse)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rep_bttn.check_event(Mouse):
                    Game(screen, Bytes_Font)
                elif Quit_bttn.check_event(Mouse):
                    execution = False
        pygame.display.update()


def Game(screen,Bytes_Font):
    execution = True

    pygame.display.set_caption("Space Invaders")
    icon = pygame.image.load("assets/alien.png")
    pygame.display.set_icon(icon)


    BackGround = pygame.image.load("assets/fondo.png")


    mixer.music.load("assets/MusicaFondo.mp3")
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)


    font = pygame.font.Font(Bytes_Font, 32)

    f_final = pygame.font.Font(Bytes_Font, 60)
    final_text2 = f_final.render("YOU LOSE",True,(255,255,255))

    player = Player(3, 836, 836, 0, pygame.image.load("assets/nave-espacial.png"), 0)
    Heart_img = pygame.image.load("assets/corazon.png")
    bullets = []
    ebullets = []
    enemies = []
    EnemySpawn(enemies,3,4)



    while execution:
        screen.blit(BackGround, (0,0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.setVelocity(-1.5)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.setVelocity(1.5)
                elif event.key == pygame.K_SPACE:
                    if len(bullets) < 5:
                        bullet_sound = mixer.Sound("assets/disparo.mp3")
                        bullet_sound.set_volume(0.3)
                        bullet_sound.play()
                        bullets.append(Bullet(player.x + 30, player.y, -1.5, pygame.image.load("assets/bala.png"),0))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    player.setVelocity(0)
        player.move()
        if player.x < 0:
            player.SetX(0)
        elif player.x >1666:
            player.SetX(1666)

        DisplayEntity(player,screen)



        for bullet in bullets:
            bullet.move()
            DisplayEntity(bullet,screen)
        for bullet in bullets:
            bullet.exit_screen_area()
            if not bullet.is_visible:
                bullets.remove(bullet)
                del bullet

        for row in enemies:
            for enemy in row:
                enemy.move()
                DisplayEntity(enemy, screen)
                if enemy.x < 0:
                    for e in row:
                        e.setVelocity(e.velocity * -1)

                elif enemy.x > 1666:
                    for e in row:
                        e.setVelocity(e.velocity * -1)
                shoot_random = random.randint(1,1000)
                if shoot_random >999:
                    if len(ebullets) < 4:
                        ebullets.append(Bullet(enemy.x + 30, enemy.y, 1.5, pygame.image.load("assets/Disparo_alien.png"),1))

        for bullet in ebullets:
            bullet.move()
            DisplayEntity(bullet, screen)
            ebullet_col = colision(bullet,player)
            if ebullet_col:
                player.TakeDamage(1)
                ebullets.remove(bullet)
                del bullet

        for bullet in ebullets:
            bullet.exit_screen_area()
            if not bullet.is_visible:
                ebullets.remove(bullet)
                del bullet

        for bullet in bullets:
            for row in enemies:
                for enemy in row:
                    bullet_collision =colision(bullet,enemy)
                    if bullet_collision:
                        enemy_DSound = mixer.Sound("assets/Golpe.mp3")
                        enemy_DSound.play()
                        player.updateScore()
                        bullets.remove(bullet)
                        row.remove(enemy)

        for i in range(player.health):
            screen.blit(Heart_img,(i*40 + 0, 940))




        Display_Score(player.score,font,screen,10,10)
        pygame.display.update()

        if player.health <= 0:
            Lose(screen,f_final,Bytes_Font)
            execution = False

        for row in enemies:
            if len(row) == 0:
                enemies.remove(row)
        if len(enemies) == 0:
            for bullet in bullets:
                bullets.remove(bullet)
            pygame.display.update()
            Win(screen,f_final,Bytes_Font)
            execution = False

def Start_Menu(screen):
    BackGround = pygame.image.load("assets/fondo.png")
    Bytes_Font = Read_Font("assets/freesansbold.ttf")
    play_bttn = Button(image=None, pos=(900,350), text_input="Play", font=pygame.font.Font(Bytes_Font, 60),
                       base_color="#d7fcd4", hover_color="white")
    Quit_bttn = Button(image=None, pos=(900,550), text_input="Quit", font=pygame.font.Font(Bytes_Font, 60),
                       base_color="#d7fcd4", hover_color="white")
    execution = True


    while execution:
        Mouse = pygame.mouse.get_pos()
        screen.blit(BackGround, (0, 0))
        for button in [play_bttn, Quit_bttn]:
            button.Mouse_On(Mouse)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_bttn.check_event(Mouse):
                    Game(screen,Bytes_Font)
                elif Quit_bttn.check_event(Mouse):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()



def main():
    pygame.init()
    screen = pygame.display.set_mode((1794, 996))
    Start_Menu(screen)




main()

