#! /usr/bin/env python
import pygame, random, os, gameObjects, gameLogic
pygame.init()



def menu(window):
    choice = 0
    isChoosing = True
    
    while isChoosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = 2
                isChoosing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    choice = 2
                    isChoosing = False
        
        window.fill((0,0,0))
        pygame.display.update()
        

def game(window):
    
    #VARIABLES
    FPS = 60
    gameIsRunning = True
    isShooting = False
    font = pygame.font.Font(None, 30)
    textScore = font.render("Score: ", 1, (255,255,255))
    directions = [] #this list keeps track of which arrow keys are pressed
    behaviourList = ["sinus", "normal"]
    player = gameObjects.Player(window.get_rect()[2]/2 - 50,window.get_rect()[3]-100, window) #create a new player object
    blitList =[]    #list of images and positions, that have to be blitted
    background = gameObjects.Background(window)
    imgLoader = gameObjects.ImgLoad()
    lifeBar = gameObjects.LifeBar(player, imgLoader)
    objectList = []
    #timer
    FpsClock = pygame.time.Clock()
    dtClock = pygame.time.Clock()
    timePassed = 0.0
    shootingDelayTime = 0.5
    shootingDelayTimeTracker = 0.0
    enemyDelayTime = 3.0
    enemyDelayTimeTracker = 0.0
    powerUpDelayTime = 2.0
    powerUpDelayTimeTracker = 0.0
    
    
    #GAME LOOP
    while gameIsRunning:
        
        #GET USER INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameIsRunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameIsRunning = False
                elif event.key == pygame.K_UP:
                    directions.append("Up")
                elif event.key == pygame.K_DOWN:
                    directions.append("Down")
                elif event.key == pygame.K_LEFT:
                    directions.append("Left")
                elif event.key == pygame.K_RIGHT:
                    directions.append("Right")
                elif event.key == pygame.K_SPACE:
                    isShooting = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    directions.remove("Up")
                elif event.key == pygame.K_DOWN:
                    directions.remove("Down")
                elif event.key == pygame.K_LEFT:
                    directions.remove("Left")
                elif event.key == pygame.K_RIGHT:
                    directions.remove("Right")
                elif event.key == pygame.K_SPACE:
                    isShooting = False
        
        #UPDATE GAME LOGIC
        FpsClock.tick(FPS)
        dt = dtClock.tick() / 1000.0
        timePassed += dt
        shootingDelayTimeTracker += dt
        enemyDelayTimeTracker += dt 
        powerUpDelayTimeTracker += dt
        
        if isShooting and shootingDelayTimeTracker >= shootingDelayTime:
            objectList.append(gameObjects.playerLaser(player.getPosition()[0], player.getPosition()[1], imgLoader))
            objectList.append(gameObjects.playerLaser(player.getPosition()[0] + player.getDimension()[0] - 9, player.getPosition()[1], imgLoader))
            shootingDelayTimeTracker = 0.0
        
        #manage the creation of enemies
        if enemyDelayTimeTracker >= enemyDelayTime:
            objectList.append(gameObjects.EnemyShip(random.randint(10, window.get_rect()[2]-imgLoader.getEnemyShip().get_rect()[2]),0,100,random.choice(behaviourList),imgLoader))
            enemyDelayTimeTracker = 0.0
        
        #manage the creation of powerUps:
        if powerUpDelayTimeTracker >= powerUpDelayTime:
            objectList.append(gameObjects.PowerUpLife(random.randint(0, window.get_rect()[2]-imgLoader.getLife().get_rect()[2]),0, 100, imgLoader))
            powerUpDelayTimeTracker = 0.0
        
        #update the state of the objects
        gameLogic.updateObjectList(objectList, dt, window, imgLoader, player)
        player.update(directions, dt)
        background.update(dt)
        lifeBar.update(window,player)
        textScoreAmount = font.render(str(player.getScore()), 0 , (255,255,255))
        
        
        #FILL blitList WITH SURFACES, THAT NEED TO BE DRAWN
        blitList=[]
        for item in background.getBlitList():
            blitList.append(item)
        for item in objectList:
            blitList.append(item.getBlit())
        for item in lifeBar.getBlitList():
            blitList.append(item)
        blitList.append((player.getImage(),(player.posX, player.posY)))
        blitList.append((textScore, (window.get_rect()[2]-textScoreAmount.get_rect()[2]-textScore.get_rect()[2],window.get_rect()[3]-textScore.get_rect()[3])))
        blitList.append((textScoreAmount, (window.get_rect()[2]-textScoreAmount.get_rect()[2], window.get_rect()[3]- textScoreAmount.get_rect()[3])))
        
        #DRAW TO THE SCREEN
        window.fill((0,0,0))
        for i in blitList:
            window.blit(i[0],i[1])
        
        
        pygame.display.update()

def main():
    windowSize = (1024,768)
    window = pygame.display.set_mode(windowSize)
    pygame.display.set_caption("KEPSKI FIGHTER")
    game(window)
    pygame.quit()

if __name__ == "__main__":
    main()
