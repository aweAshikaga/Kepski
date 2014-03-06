#! /usr/bin/env python
import pygame, math

class ImgLoad(object):
    def __init__(self):
        #LASERS
        self.imgLaserGreen = pygame.image.load("res/laserGreen.png").convert_alpha()
        self.imgLaserGreenShot = pygame.image.load("res/laserGreenShot.png").convert_alpha()
        self.imgLaserRed = pygame.image.load("res/laserRed.png").convert_alpha()
        self.imgLaserRedShot = pygame.image.load("res/laserRedShot.png").convert_alpha()
        
        #ENEMIES
        self.imgEnemyShip = pygame.image.load("res/enemyShip.png").convert_alpha()
        self.imgEnemyUFO = pygame.image.load("res/enemyUFO.png").convert_alpha()
        
        #OBJECTS
        self.imgLife = pygame.image.load("res/life.png").convert_alpha()
        self.imgMeteorBig = pygame.image.load("res/meteorBig.png").convert_alpha()
        self.imgMeteorSmall = pygame.image.load("res/meteorSmall.png").convert_alpha()
        self.imgBallPowerUp = pygame.image.load("res/ballPowerUp.png").convert_alpha()
    
    #GETTER-FUNCTIONS:
    def getLaserGreen(self):
        return self.imgLaserGreen
    def getLaserGreenShot(self):
        return self.imgLaserGreenShot
    def getLaserRed(self):
        return self.imgLaserRed
    def getLaserRedShot(self):
        return self.imgLaserRedShot
    def getEnemyShip(self):
        return self.imgEnemyShip
    def getEnemyUFO(self):
        return self.imgEnemyUFO
    def getLife(self):
        return self.imgLife
    def getMeteorBig(self):
        return self.imgMeteorBig
    def getMeteorSmall(self):
        return self.imgMeteorSmall
    def getBallPowerUp(self):
        return self.imgBallPowerUp

class MeteorBig(object):
    def __init__(self, posX, posY, imgLoader):
        self.posX = posX
        self.posY = posY
        self.img = imgLoader.getMeteorBig()
        self.rotation = 0
    
    def update(self, dt):
        pass
    
    def getBlit(self):
        return (self.img, (self.posX, self.posY))
        
class PowerUp(object):
    def __init__(self, posX, posY, velocity):
        self.posX = posX
        self.posY = posY
        self.velocity = velocity
    
    def __del__(self):
        print "PowerUp destroyed"

class PowerUpLife(PowerUp):
    def __init__(self, posX, posY, velocity, imgLoader):
        PowerUp.__init__(self, posX, posY, velocity)
        self.img = imgLoader.getLife()
    
    def getPosition(self):
        return (self.posX, self.posY)
    
    def getDimension(self):
        return (self.img.get_rect()[2], self.img.get_rect()[3])
    
    def get_rect(self):
        return (self.posX, self.posY, self.img.get_rect()[2], self.img.get_rect()[3])
    
    def update(self, dt):
        self.posY += self.velocity * dt
    
    def getBlit(self):
        return (self.img, (self.posX, self.posY))
        
class PowerUpBounceBall(PowerUp):
    def __init__(self, posX, posY, velocity, imgLoader):
        PowerUp.__init__(self, posX, posY, velocity)
        self.img = imgLoader.getBallPowerUp()
        

class Enemy(object):
    def __init__(self, posX, posY, velocity, behaviour="normal"):
        self.posX = posX
        self.posY = posY
        self.velocity = velocity
        self.behaviour = behaviour
        self.timePassed = 0.0
        self.isShooting = False
        self.shootingDelayTime = 1.0

class EnemyShip(Enemy):
    
    def __init__(self, posX, posY, velocity, behaviour, imgLoader):
        Enemy.__init__(self, posX, posY, velocity, behaviour)
        self.img = imgLoader.getEnemyShip()
        self.life = 2
    
    def update(self, dt):
        self.timePassed += dt
        self.shootingDelayTime += dt
        
        #movement
        if self.behaviour == "sinus":
            vector = [1, math.sin(5*self.timePassed)*5]
            #vector = [vector[0] / math.sqrt(vector[0]**2 + vector[1]**2), vector[1] / math.sqrt(vector[0]**2 + vector[1]**2)]
            self.posY += vector[0] * self.velocity * dt
            self.posX += vector[1] * self.velocity * dt
        elif self.behaviour == "normal":
            self.posY += self.velocity * dt
        else:
            self.posY += self.velocity * dt
        
        #shooting
        if self.shootingDelayTime >= 1.0: 
            self.isShooting = True
            self.shootingDelayTime = 0.0
            
    def reduceLife(self, amount):
        self.life -= amount
    
    def getLife(self):
        return self.life
    
    def getIsShooting(self):
        if self.isShooting:
            self.isShooting = False
            return True
        else:
            return False
        
        
        
    def getImage(self, imgLoader):
        return self.img
    
    def get_rect(self):
        return (self.posX, self.posY, self.img.get_rect()[2], self.img.get_rect()[3])
    
    def getPosition(self):
        return (self.posX, self.posY)
    
    def getBlit(self):
        return (self.img , (self.posX, self.posY))
    
    def getDimension(self):
        return (self.img.get_rect()[2], self.img.get_rect()[3])
        
        

class playerLaser(object):
    def __init__(self,posX,posY, imgLoader):
        self.posX = posX
        self.posY = posY
        self.img = imgLoader.getLaserGreen()
        self.velocity = 400 #in pixels per second
        self.direction = [0 , -1]
        #next line normalizes the direction vector to a magnitude of 1
        self.direction = [self.direction[0] / math.sqrt(self.direction[0]**2 + self.direction[1]**2), self.direction[1] / math.sqrt(self.direction[0]**2 + self.direction[1]**2)]
    
    def update(self,dt):
        self.posX = self.posX + self.direction[0] * self.velocity * dt
        self.posY = self.posY + self.direction[1] * self.velocity * dt
    
    def getBlit(self):
        return (self.img , (self.posX, self.posY))
        
    def getDimension(self):
        return (self.img.get_rect()[2], self.img.get_rect()[3])
    
    def getPosition(self):
        pos = (self.posX, self.posY)
        return pos
    
    def get_rect(self):
        return (self.posX, self.posY, self.img.get_rect()[2], self.img.get_rect()[3])

class EnemyLaser(object):
    def __init__(self, posX, posY, imgLoader):
        self.posX = posX
        self.posY = posY
        self.img = imgLoader.getLaserRed()
        self.velocity = 400 #in pixels per second
        self.direction = [0, 1]
        #next line normalizes the direction vector to a magnitude of 1
        self.direction = [self.direction[0] / math.sqrt(self.direction[0]**2 + self.direction[1]**2), self.direction[1] / math.sqrt(self.direction[0]**2 + self.direction[1]**2)]
    
    def update(self,dt):
        self.posX = self.posX + self.direction[0] * self.velocity * dt
        self.posY = self.posY + self.direction[1] * self.velocity * dt
    
    def getBlit(self):
        return (self.img , (self.posX, self.posY))
        
    def getDimension(self):
        return (self.img.get_rect()[2], self.img.get_rect()[3])
    
    def getPosition(self):
        pos = (self.posX, self.posY)
        return pos
    
    def get_rect(self):
        return (self.posX, self.posY, self.img.get_rect()[2], self.img.get_rect()[3])

class Player(object):
    def __init__(self,posX,posY, window):
        self.posX = posX
        self.posY = posY
        self.life = 3
        self.score = 0
        self.screenHeight = window.get_rect()[3]
        self.screenWidth = window.get_rect()[2]
        self.velocity = 300 #in pixels per second
        self.imgMiddle = pygame.image.load("res/player.png").convert_alpha()
        self.imgLeft = pygame.image.load("res/playerLeft.png").convert_alpha()
        self.imgRight = pygame.image.load("res/playerRight.png").convert_alpha()
        self.imgDamaged = pygame.image.load("res/playerDamaged.png").convert_alpha()
        self.imgShield = pygame.image.load("res/shield.png").convert_alpha()
        self.image = self.imgMiddle
        self.width = self.imgMiddle.get_rect()[2]
        self.height = self.imgMiddle.get_rect()[3]
    
    def getPosition(self):
        return (self.posX, self.posY)
    
    def update(self, directions, dt):
        #UPDATE POSITION OF THE PLAYER
        if "Up" in directions:
            if self.posY - self.velocity * dt < 0:
                self.posY = 0
            else:
                self.posY = self.posY - self.velocity * dt
        if "Down" in directions:
            if self.posY + self.velocity * dt > self.screenHeight - self.height:
                self.posY = self.screenHeight - self.height
            else:
                self.posY = self.posY + self.velocity * dt
        if "Left" in directions:
            if self.posX - self.velocity * dt < 0:
                self.posX = 0
            else:
                self.posX = self.posX - self.velocity * dt
        if "Right" in directions:
            if self.posX + self.velocity * dt > self.screenWidth - self.width: 
                self.posX = self.screenWidth - self.width
            else:
                self.posX = self.posX + self.velocity * dt 
        
        #UPDATE THE CURRENT IMAGE
        if "Right" in directions and "Left" in directions:
            self.image = self.imgMiddle
        elif "Left" in directions:
            self.image = self.imgLeft
        elif "Right" in directions:
            self.image = self.imgRight
        else:
            self.image = self.imgMiddle
    
    def getScore(self):
        return self.score
    
    def reduceScore(self, amount):
        self.score -= amount
    
    def addScore(self, amount):
        self.score += amount
    
    def reduceLife(self, amount):
        self.life -= amount
    
    def addLife(self, amount):
        self.life += amount
    
    def getLife(self):
        return self.life
    
    def getImage(self):
        return self.image
    
    def getDimension(self):
        return (self.image.get_rect()[2], self.image.get_rect()[3])
    
    def get_rect(self):
        return (self.posX, self.posY, self.image.get_rect()[2], self.image.get_rect()[3])

class LifeBar(object):
    def __init__(self, player, imgLoader):
        self.hitpoints = player.getLife()
        self.img = imgLoader.getLife()
        self.blitList = []
    
    def update(self, window, player):
        self.hitpoints = player.getLife()
        self.blitList = []
        if self.hitpoints > 5:
            for i in xrange(5):
                self.blitList.append((self.img, (i*(self.img.get_rect()[2]+5), window.get_rect()[3]-self.img.get_rect()[3])))
        elif self.hitpoints <= 0:
            pass
        else:
            for i in xrange(self.hitpoints):
                self.blitList.append((self.img, (i*(self.img.get_rect()[2]+5), window.get_rect()[3]-self.img.get_rect()[3])))
    
    def getBlitList(self):
        return self.blitList

class Background(object):
    def __init__(self, window):
        self.velocity = 150 #in Pixels per second
        self.screenWidth = window.get_rect()[2]
        self.screenHeight = window.get_rect()[3]
        self.imgBackground = pygame.image.load("res/Background/starBackground.png").convert()
        self.imgBackgroundWidth = self.imgBackground.get_rect()[2]
        self.imgBackgroundHeight = self.imgBackground.get_rect()[3]
        self.columns = (self.screenWidth / self.imgBackgroundWidth) + 1
        self.rows = (self.screenHeight / self.imgBackgroundWidth) + 2
        
        self.bgList = [[("",(0,0)) for i in xrange(self.rows)] for j in xrange(self.columns)]
        
        for i in xrange(self.rows):
            for j in xrange(self.columns):
                self.bgList[i][j] = (self.imgBackground, (self.imgBackgroundWidth * j, self.imgBackgroundHeight * i))
                print self.bgList[i][j]
        
    def update(self, dt):
        #BACKGROUND SCROLLS DOWN AND IF TOO FAR BOTTOM IT REPOSITIONS ITSELF AT THE TOP
        for i in xrange(self.rows):
            for j in xrange(self.columns):
                if self.bgList[i][j][1][1] >= self.screenHeight:
                    self.bgList[i][j] = (self.imgBackground, (self.bgList[i][j][1][0], self.bgList[i][j][1][1] - self.imgBackgroundHeight * self.columns + self.velocity * dt))
                else:
                    self.bgList[i][j] = (self.imgBackground, (self.bgList[i][j][1][0], self.bgList[i][j][1][1] + self.velocity * dt))
        
    def getBlitList(self):
        #FUNCTION TO RETURN THE BACKGROUND IN A COMPATIBLE FORMAT FOR THE BLIT-LIST IN THE MAIN-MODULE
        self.blitList = []
        
        for i in xrange(self.rows):
            for j in xrange(self.columns):
                self.blitList.append(self.bgList[i][j])
        
        return self.blitList
        
