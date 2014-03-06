#! /usr/bin/env python
import pygame, gameObjects

def detectCollision(rect1, rect2):
    #rect (x,y,width,height)
    if rect1[0]+rect1[2] > rect2[0] and rect1[0] < rect2[0]+rect2[2] and rect1[1]+rect1[3] > rect2[1] and rect1[1] < rect2[1]+rect2[3]:
        return True
    else:
        return False

def updateObjectList(objectList, dt, window, imgLoader, player):
    for item in objectList:
        item.update(dt)
        if isinstance(item, gameObjects.playerLaser):
            #check if player laser hits an enemy
            for enemy in objectList:
                if isinstance(enemy, gameObjects.Enemy) and detectCollision(item.get_rect(), enemy.get_rect()):
                    enemy.reduceLife(1)
                    objectList.remove(item)
                    if enemy.getLife() <= 0:
                        player.addScore(100)
                        objectList.remove(enemy)
            #check if player laser is out of the picture
            if item.getPosition()[1] < 0 - item.getDimension()[1]:
                objectList.remove(item)
        elif isinstance(item, gameObjects.Enemy):
            #check if enemy is shooting and create shots if he is
            if item.getIsShooting():
                objectList.append(gameObjects.EnemyLaser(item.getPosition()[0], item.getPosition()[1], imgLoader))
                objectList.append(gameObjects.EnemyLaser(item.getPosition()[0]+item.getDimension()[0]-9, item.getPosition()[1], imgLoader))
            #check if enemy is out of the picture
            if item.getPosition()[1] > window.get_rect()[3]:
                objectList.remove(item)
        elif isinstance(item, gameObjects.EnemyLaser):
            #check collision between enemy laser and player
            if detectCollision(item.get_rect(), player.get_rect()):
                player.reduceLife(1)
                print "Leben: " ,player.life
                objectList.remove(item)
            #check if laser is out of the picture
            elif item.getPosition()[1] > window.get_rect()[3]:
                objectList.remove(item)
        elif isinstance(item, gameObjects.PowerUpLife):
            if detectCollision(item.get_rect(), player.get_rect()):
                player.addLife(1)
                objectList.remove(item)
            elif item.getPosition()[1] > window.get_rect()[3]:
                objectList.remove(item)
