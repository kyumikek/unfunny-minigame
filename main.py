import pygame
import random
from gui_api import *
class Data:
    def loadImage(path,width=35,height=35,flipX = False, flipY = False):
        img = pygame.image.load(path)
        img = pygame.transform.scale(img,(width,height))
        img = pygame.transform.flip(img,flipX,flipY)
        return img.convert_alpha()
    def __init__(self):
        self.sprites = {
            "main_tile" : Data.loadImage("sprites/main_tile.png",32,32),
            "playerleft" : Data.loadImage("sprites/player.png",32,32,True),
            "playerright" : Data.loadImage("sprites/player.png",32,32),
            "enemyleft" : Data.loadImage("sprites/enemy.png",32,32,True),
            "enemyright" : Data.loadImage("sprites/enemy.png",32,32),
            "bomb1" : Data.loadImage("sprites/bomb.png",32,32),
            "bomb2" : Data.loadImage("sprites/bomb1.png",32,32),
            "bomb3" : Data.loadImage("sprites/bomb2.png",32,32),
            "bomb4" : Data.loadImage("sprites/bomb3.png",32,32),
            "bomb5" : Data.loadImage("sprites/bomb4.png",32,32),
            "key" : Data.loadImage("sprites/key.png",32,32),
            "heart" : Data.loadImage("sprites/heart.png",32,32),
            "play" :  Data.loadImage("sprites/play.png",150,150)
        }
class Bomb:
    def __init__(self,x,y,map,app):
        self.rect = pygame.Rect(x,y,32,32)
        self.app = app
        self.map = map
        self.map.bombs.append(self)
        self.death_timer = 0
        self.range_transparent = pygame.Surface((96,96),pygame.SRCALPHA)
        pygame.draw.circle(self.range_transparent,(255,255,255,100),(48,48),48)

        self.timer = 1
    def render(self):
        self.app.screen.blit(self.app.data.sprites[f"bomb{self.timer}"],self.rect)
        self.app.screen.blit(self.range_transparent,(self.rect.x-34,self.rect.y-34))
    def update(self):
        self.timer += 1
        if (self.timer==5):
            self.map.blocks[self.map.block_poses.index([self.rect.x,self.rect.y])].destroy()
            self.map.bombs.remove(self)

            for i in self.map.players:
                if pygame.Rect.colliderect(pygame.Rect(self.rect.x-34,self.rect.y-34,96,96),i.rect):
                    i.hp -= 1
            for i in self.map.enemies:
                if pygame.Rect.colliderect(pygame.Rect(self.rect.x-34,self.rect.y-34,96,96),i.rect):
                    i.alive = False
class Enemy:
    def __init__(self,x,y,map,app):
        self.rect = pygame.Rect(x,y,32,32)
        self.app = app
        self.map = map
        self.alive = True
        self.coll = {
            "left" : False,
            "right" : False,
            "down" : False,
            "up" : False,
        }
        self.map.enemies.append(self)
        self.map.enemy_poses.append([self.rect.x,self.rect.y])
        self.old_pos = [0,0]
    def destroy(self):
        id = self.map.enemies.index(self)
        self.map.enemy_poses.pop(id)
        self.map.enemies.remove(self)
    def update(self):
        if not self.alive:
            self.destroy()
        else:
            
            id = self.map.enemies.index(self)
            self.map.enemy_poses[id] = [self.rect.x,self.rect.y]
            for i in self.map.players:
                if (self.rect.y>i.rect.y and not [self.rect.x,self.rect.y-32] in self.map.holes and not [self.rect.x,self.rect.y-32] in self.map.enemy_poses):
                    self.old_pos = [self.rect.x,self.rect.y]
                    self.rect.y -= 32
                elif(self.rect.y<i.rect.y and not [self.rect.x,self.rect.y+32] in self.map.holes and not [self.rect.x,self.rect.y+32] in self.map.enemy_poses):
                    self.old_pos = [self.rect.x,self.rect.y]
                    self.rect.y += 32
                elif (self.rect.x>i.rect.x and not [self.rect.x-32,self.rect.y] in self.map.holes and not [self.rect.x-32,self.rect.y] in self.map.enemy_poses):
                    self.old_pos = [self.rect.x,self.rect.y]
                    self.rect.x -= 32
                elif(self.rect.x<i.rect.x and not [self.rect.x+32,self.rect.y] in self.map.holes and not [self.rect.x+32,self.rect.y] in self.map.enemy_poses):
                    self.old_pos = [self.rect.x,self.rect.y]
                    self.rect.x += 32
                if (self.rect.x==i.rect.x and self.rect.y==i.rect.y):
                    self.rect.x = self.old_pos[0]
                    self.rect.y = self.old_pos[1]
                    i.hp -= 1
        self.onBlock = False
        self.coll = {
            "left" : False,
            "right" : False,
            "down" : False,
            "up" : False,
        }
    def render(self):

        self.app.screen.blit(self.app.data.sprites["enemyright"],self.rect)
class Player:
    def __init__(self,x,y,map,app):
        self.rect = pygame.Rect(x,y,32,32)
        self.app = app
        self.map = map
        self.map.players.append(self)
        self.direction = "left"
        self.alive = True
        self.hp = 3
        self.released = {
            "left" : False,
            "right" : False,
            "up" : False,
            "down" : False,
            "bomb" : False
        }
        self.onBlock = True
    def die(self):
        self.map.players.remove(self)
        self.app.manager.state = "main"
    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_r]:
            self.app.manager.state = "main"
        if not self.onBlock: self.alive = False
        if self.alive:
            if not key[pygame.K_a]:
                self.released["left"] = True
            elif(self.released["left"] and self.rect.x-32>-1 and not [self.rect.x-32,self.rect.y] in self.map.holes):
                self.rect.x -= 32
                self.direction = "left"
                self.released["left"] = False
                self.app.update()
            if not key[pygame.K_d]:
                self.released["right"] = True
            elif(self.released["right"] and self.rect.x+32<513 and not [self.rect.x+32,self.rect.y] in self.map.holes):
                self.rect.x += 32
                self.direction = "right"
                self.released["right"] = False
                self.app.update()
            if not key[pygame.K_s]:
                self.released["down"] = True
            elif(self.released["down"] and self.rect.y+32<513 and not [self.rect.x,self.rect.y+32] in self.map.holes):
                self.rect.y += 32
                self.released["down"] = False
                self.app.update()
            if not key[pygame.K_w]:
                self.released["up"] = True
            elif(self.released["up"]  and self.rect.y-32>-1 and not [self.rect.x,self.rect.y-32] in self.map.holes):
                self.rect.y -= 32
                self.released["up"] = False
                self.app.update()
            if not key[pygame.K_SPACE]:
                self.released["bomb"] = True
            elif(self.released["bomb"]):
                Bomb(self.rect.x,self.rect.y,self.map,self.app)
                self.app.update()
                self.released["bomb"] = False
        self.onBlock = False
        self.app.screen.blit(self.app.data.sprites[f"player{self.direction}"],self.rect)
        r = 0
        for i in range(self.hp):
            self.app.ui_surface.blit(self.app.data.sprites["heart"],pygame.Rect(r*34,0,32,32))
            r+=1
        if self.hp < 1:
            self.die()
class Block:
    def __init__(self,x,y,map,app):
        self.app = app
        self.map = map
        self.rect = pygame.Rect(x,y,32,32)
        self.map.block_poses.append([x,y])
        self.map.blocks.append(self)
    def destroy(self):
        self.map.blocks.remove(self)
        self.map.block_poses.remove([self.rect.x,self.rect.y])
    def update(self):
        for i in self.map.players:
            if pygame.Rect.colliderect(i.rect,self.rect):
                i.onBlock = True

        self.app.background.blit(self.app.data.sprites["main_tile"],self.rect)
class Key:
    def __init__(self,x,y,map,app):
        self.app = app
        self.map = map
        self.rect = pygame.Rect(x,y,32,32)
        self.map.blocks.append(self)
    def destroy(self):
        self.app.blocks.remove(self)
    def update(self):
        for i in self.map.players:
            if pygame.Rect.colliderect(i.rect,self.rect):
                i.app.manager.state = "win"

        self.app.background.blit(self.app.data.sprites["key"],self.rect)

class StateManager:
    def main_button(app):
        print("balls")
        app.manager.state = "game"
        app.map.gen_map()
    def __init__(self,app):
        self.app = app
        self.state = "main"
        self.states = {
            "game": self.update_game,
            "win" : self.win_screen,
            "main" : self.main_screen
        }    
        self.main_button = Button(181,181,150,150,"#404949",StateManager.main_button,self.app,self.app.data.sprites["play"])
    def main_screen(self):
        self.app.background.fill("black")
        self.main_button.update()
    def win_screen(self):
        self.state = "main"
        self.app.background.fill("black")
        pass
    def update_game(self):
        
        self.app.background.fill("black")
        for i in self.app.map.blocks:
            i.update()
        self.app.screen.blit(self.app.background,(0,0))
        for i in self.app.map.players:
            i.update()
        for i in self.app.map.enemies:
            i.render()
        for i in self.app.map.bombs:
            i.render()
    def add_state(self,state_name,function):
        self.states[state_name] = function
    def update_states(self):
        self.states[self.state]()
class Map:
    def __init__(self,width,height,app):

        self.scale = [width,height]
        self.players = []
        self.blocks = []
        self.block_poses = []
        self.enemy_poses = []
        self.holes = []
        self.enemies = []
        self.bombs = []
        self.app = app
    def gen_map(self):
        self.blocks = []
        self.block_poses = []
        self.enemies = []
        self.bombs = []
        self.holes = []
        self.players = []
        for i in range(random.randint(18,36)):
            self.holes.append([random.randint(0,int(self.scale[0]/32))*32,random.randint(0,int(self.scale[1]/32))*32])
        for x in range(int(self.scale[0]/32)):
            for y in range(int(self.scale[1]/32)):
                if not [x*32,y*32] in self.holes:
                    Block(x*32,y*32,self,self.app)
        for i in range(random.randint(9,18)):
            pos = [random.randint(0,int(self.scale[0]/32))*32,random.randint(0,int(self.scale[1]/32))*32]
            if not pos in self.holes:
                Enemy(pos[0],pos[1],self,self.app)
        gened_key = False
        while not gened_key:
            pos = [random.randint(0,int(self.scale[0]/32))*32,random.randint(0,int(self.scale[1]/32))*32]
            if not pos in self.holes:
                gened_key = True
                Key(pos[0],pos[1],self,self.app)
        gened_player = False
        while not gened_player:
            pos = [random.randint(0,int(self.scale[0]/32))*32,random.randint(0,int(self.scale[1]/32))*32]
            if not pos in self.holes:
                gened_player = True
                Player(0,0,self,self.app)
class App:
    def __init__(self,width=512,height=512):
        self.scale = [width,height]
        self.screen = pygame.display.set_mode((width,height))
        self.background = pygame.Surface((width,height))
        self.clock = pygame.time.Clock()
        self.data = Data()
        self.manager = StateManager(self)
        self.map = Map(width,height,self)
        self.ui_surface = pygame.Surface((width,height),pygame.SRCALPHA)
        
        self.delta = 0
        self.running = True
    def update(self):
        for i in self.map.bombs:
            i.update()
        for i in self.map.enemies:
            i.update()
    def run(self):
        self.map.gen_map()
        while self.running:
            self.ui_surface.fill((0,0,0,0))
            self.delta = self.clock.tick(60)/1000
            pygame.display.set_caption(str(self.clock.get_fps()))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.manager.update_states()
            self.screen.blit(self.ui_surface,(0,0))
            pygame.display.flip()
if __name__ == "__main__":
    _app = App(512,512)
    _app.run()