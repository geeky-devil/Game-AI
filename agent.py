import gym
from gym import spaces
import pygame
import sys
import random
from pygame.locals import *
import numpy as np

class CustomEnv(gym.Env):
    def __init__(self):
        super(CustomEnv, self).__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.distance = 0
        self.spike_speed = 5
        self.delay = 200
        self.upper_bound = random.randint(0, self.delay)
        self.timer = 0
        self.num_evaded = 0
        self.run = True
        self.player_rect = pygame.rect.Rect(200, 400, 3, 30)
        self.spike = pygame.image.load("spike.png")
        self.spike = pygame.transform.scale(self.spike, (32, 32))
        self.spike_rect = self.spike.get_rect()
        self.spike_rect.center = (1000, 581)
        self.spike_group = pygame.sprite.Group()
        self.ground = pygame.rect.Rect(0, 598, 800, 5)
        self.action_space = spaces.Discrete(3)  # Jump, Jump Higher, Do Nothing
        self.observation_space = spaces.Box(low=0, high=800, shape=(6,), dtype=np.float32)
        self.jump=False
    def reset(self):
        self.jump_count = 0
        self.distance = 0
        self.spike_speed = 5
        self.delay = 200
        self.upper_bound = random.randint(0, self.delay)
        self.timer = 0
        self.num_evaded = 0
        self.jump=False
        self.player_rect.x = 200
        self.player_rect.y = 400
        self.spike_group.empty()
        return self.get_state()

    def step(self, action):
        done =False
        reward=0
        if action == 1 and self.player_rect.y==570:
            self.jump=True
        elif action==2:
            self.jump=False
                     
        if self.jump :
            if self.player_rect.y<300:
                self.player_rect.y=300
                self.jump=False
              
            self.player_rect.y-=10
            

        if (self.jump==False)and self.player_rect.y<568:
            self.player_rect.y+=10
        
        self.timer += 1

        if self.timer >= self.upper_bound:
            self.timer = 0
            self.upper_bound = random.randint(0, self.delay)
            if len(self.spike_group.sprites())<4:
                spk = pygame.sprite.Sprite()
                spk.image = self.spike
                spk.rect = self.spike_rect.copy()
                self.spike_group.add(spk)

        if self.player_rect.collidedictall(self.spike_group.spritedict):
            reward=0
            print("______________dead_____________")
            done=True
            
        
        for spike in self.spike_group.sprites():
            #self.screen.blit(self.spike, spike.rect)
            spike.rect.center=[spike.rect.center[0]-self.spike_speed,spike.rect.center[1]]
            if spike.rect.center[0]<self.player_rect.x-15:
                self.spike_group.remove(spike)
                self.num_evaded+=1
                reward=1
            

        if done: self.reset()
        return self.get_state(), reward, done, {}

    def render(self, mode='human'):
        if mode == 'human':
            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (0, 255, 0), self.ground)
            pygame.draw.rect(self.screen, (255, 0, 0), self.player_rect)
            for spike in self.spike_group.sprites():
                self.screen.blit(self.spike, spike.rect)
            pygame.display.update()
        elif mode == 'rgb_array':
            return pygame.surfarray.array3d(self.screen)
        else:
            super(CustomEnv, self).render(mode=mode)

    def get_state(self):
        base=[self.player_rect.x, self.player_rect.y]
        spike_list=list(sorted([x.rect.x for x in self.spike_group.sprites() ]))
        #print(spike_list)
        diff=4-len(spike_list)
        for i in range(diff):
            spike_list.append(1000)
        base.extend(spike_list)
        return base
    def close(self):
        pygame.quit()

