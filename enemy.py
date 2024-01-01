import pygame
from pygame import mixer
import random
import math

# ENEMY CLASS TO HAVE THEIR POSITIONS AND CHARACTERISTICS
class Enemy:
    def __init__(self, x, y, img, x_change):
        self.enemyX = x
        self.enemyY = y
        self.enemy_img = img
        self.enemyX_change = - x_change
        self.enemyY_change = 20 

    def enemy(self, screen):
        screen.blit(self.enemy_img, (self.enemyX, self.enemyY) )


# MANAGES THE ENEMY BASED ON THEIR LEVEL
class EnemyManager():

    def __init__(self):
        self.enemies = []
        self.score = 0
        self.level = 1
        self.enemy_types = [pygame.image.load('images/alien-1.png'), pygame.image.load('images/alien-2.png'), pygame.image.load('images/alien-3.png')]
        self.ufo = pygame.image.load('images/ufo.png')
        self.laser = pygame.image.load('images/laser.png')
        self.laserX = 0
        self.laserY = 0
        self.laserY_change = 1
        self.laser_state = 'ready'
        self.fireball = pygame.image.load('images/fireball.png')
        self.fireballX = 0
        self.fireballY = 0
        self.fireballY_change = 1
        self.fireball_state = 'ready'
        self.enemy_reached_spaceship = False
        self.enemy_ypos = [70, 140, 210]
        self.last_time = pygame.time.get_ticks()


    def distance_between_two_points(self,x1,y1, x2,y2):
        """calculates distance between two points"""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    

    def bullet_collided(self, bulletX, bulletY):
        """check if player's bullet attacked any of the enemies"""
        if self.level == 1:
            for row in self.enemies:
                if row == []:
                    self.enemies.remove(row)
                else:
                    for e in row:
                        if self.distance_between_two_points(e.enemyX, e.enemyY, bulletX, bulletY) < 20:
                            row.remove(e)
                            self.score += 1
                            e.enemyX=-100
                            e.enemyY=-100
                            return True
                        else:
                            False
        if self.level == 2:
            for e in self.enemies:
                if self.distance_between_two_points(e.enemyX+20, e.enemyY, bulletX, bulletY) < 45:
                    self.score += 5
                    self.enemies.remove(e)
                    e.enemyX = -100
                    e.enemyY = -100
                    return True
                else:
                    return False
        if self.level == 3:
            if self.distance_between_two_points(self.boss.enemyX +100, self.boss.enemyY+150, bulletX, bulletY ) <80:
                self.score += 10
                self.boss.energy -= 10
                self.boss.enemyY -= self.boss.enemyY_change
                return True
            

        
    def laser_collided(self, playerX, playerY):
        """checks if laser attacked the player"""
        if self.laser_state=='fire':
            if self.distance_between_two_points(self.laserX, self.laserY, playerX, playerY) < 20:
                self.laser_state='ready'
                self.laserX = random.choice(self.enemies).enemyX
                self.laserY = random.choice(self.enemies).enemyY
                return True


    def fireball_collided(self, playerX, playerY):
        """check if fireball attacked the player"""
        if self.fireball_state =='fire':
            if self.distance_between_two_points(self.fireballX+10, self.fireballY+10, playerX+15, playerY-20) < 50:
                self.fireball_state='ready'
                self.fireballX = self.boss.enemyX
                self.fireballY = self.boss.enemyY
                return True


    def create_enemies(self):
        """creating enemies based on the game level"""
        if self.level == 1:
            # deleting all the enemies if existed and from the game window
            if self.enemies != []:
                for row in self.enemies:
                    for e in row:
                        e.enemyX = -200
                        e.enemyY = -200
            self.enemies = []
            # creating enemies
            for i in range(3):
                row = []
                for j in range(1,7):
                    new_enemy = Enemy(90*j, self.enemy_ypos[i], self.enemy_types[i], 0.3)
                    row.append(new_enemy)
                self.enemies.append(row)
            
        if self.level == 2:
            # deleting all the enemies if existed and from the game window
            if self.enemies != []:
                for e in self.enemies:
                    e.enemyX = -200
                    e.enemyY = -200
            self.enemies = []
            # creating enemies
            for i in range(1, 6):
                new_enemy = Enemy(100*i, 50*i, self.ufo, 0.6)
                self.enemies.append(new_enemy)

        if self.level == 3:
            # deleting all the enemies if existed and from the game window
            if self.enemies != []:
                self.boss.enemyX = -600
                self.boss.enemyY = -600
            self.enemies = []
            # creating enemies
            kraken = pygame.image.load('images/kraken.png')
            self.boss = Enemy(300,50,kraken, 0.5)
            self.boss.enemyY_change = 20
            self.boss.energy = 150
            self.enemies.append(self.boss)
        


    def enemy_movement(self, screen, is_game_over, playerX, playerY, player_win, paused):
        """executing enemy movement based on the game level"""
        self.enemy_reached_spaceship = False
        if self.level == 1:
            self.level_1(screen, is_game_over, playerX, playerY, paused)
        elif self.level == 2:
            self.level_2(screen, is_game_over, playerX, playerY, paused)
        elif self.level == 3:
            self.level_3(screen, is_game_over, playerX, playerY, player_win, paused)
        return self.enemy_reached_spaceship
        


    def level_1(self, screen, is_over, playerX, playerY, paused):
        """enemy behavious in the level 1"""
        for row in self.enemies:
            if row != []:
                if row[-1].enemyX >= 840:
                    for item in row:
                        item.enemyX_change *= -1
                if row[0].enemyX <=0 :
                    for item in row:
                        item.enemyX_change *= -1
                for item in row:
                    if self.distance_between_two_points(item.enemyX, item.enemyY, playerX+15, playerY-35) < 20:
                        self.enemy_reached_spaceship = True
                    if not (is_over or paused):
                        item.enemyX += item.enemyX_change
                    item.enemy(screen) 
        current_time = pygame.time.get_ticks()
        if abs(self.last_time - current_time) >= 5000:
            for row in self.enemies:
                for item in row:
                    if not (is_over or paused):
                        item.enemyY += item.enemyY_change
            self.last_time = current_time
       
    
    def level_2(self, screen, is_over, playerX, playerY, paused):
        """enemy behavious in the level 2"""
        current_time = pygame.time.get_ticks()
        for e in self.enemies:
            if e.enemyX >=840:
                 e.enemyX_change *= -1
            if e.enemyX <= 0:
                e.enemyX_change *= -1
            if self.distance_between_two_points(e.enemyX, e.enemyY, playerX+15, playerY-35) < 20:
                        self.enemy_reached_spaceship = True
            if not (is_over or paused):
                 e.enemyX += e.enemyX_change
            e.enemy(screen)
            if random.randint(1,5) == 5 and self.laser_state == 'ready':
                sound = mixer.Sound('music/laser2.wav')
                sound.play()
                self.laser_state = 'fire'
                self.laserX = e.enemyX
                self.laserY = e.enemyY
        if self.laser_state == 'fire':
            if not (is_over or paused):
                self.laserY += self.laserY_change
            screen.blit(self.laser, (self.laserX+15, self.laserY+30))
            if self.laserY >= 700:
                self.laser_state = 'ready'
                self.laserX = random.choice(self.enemies).enemyX
                self.laserY = random.choice(self.enemies).enemyY
        if abs(self.last_time - current_time) >= 5000:
            for e in self.enemies:
                if not (is_over or paused):
                    e.enemyY += e.enemyY_change
            self.last_time = current_time



    def level_3(self, screen, is_over, playerX, playerY, player_win, paused):
        """enemy behavious in the level 3"""
        current_time = pygame.time.get_ticks()
        if self.boss.enemyX >=600:
            self.boss.enemyX_change *=-1
        if self.boss.enemyX <=0:
            self.boss.enemyX_change *= -1
        if self.boss.enemyY <=50:
            self.boss.enemyY = 50
        if self.distance_between_two_points(self.boss.enemyX + 150, self.boss.enemyY+230, playerX+15, playerY-35) < 20:
            self.enemy_reached_spaceship = True
        if not (is_over or player_win or paused):
            self.boss.enemyX += self.boss.enemyX_change
        self.boss.enemy(screen)
        if random.randint(1,5) == 5 and self.fireball_state == 'ready':
                sound = mixer.Sound('music/fireball.wav')
                sound.play()
                self.fireball_state = 'fire'
                self.fireballX = self.boss.enemyX
                self.fireballY = self.boss.enemyY
        if self.fireball_state == 'fire':
            if not (is_over or player_win or paused):
                self.fireballY += self.fireballY_change
            screen.blit(self.fireball, (self.fireballX+50, self.fireballY+150))
            if self.fireballY >= 700:
                self.fireball_state = 'ready'
                self.fireballX = self.boss.enemyX
                self.fireballY = self.boss.enemyY
        if abs(self.last_time - current_time) >= 1000:
            if not (is_over or player_win or paused):
                self.boss.enemyY += self.boss.enemyY_change
            self.last_time = current_time


