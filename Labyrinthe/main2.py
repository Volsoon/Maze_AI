# -*- coding: utf-8 -*-

import pygame
import sys
import time
import math
from ia import Dqn
import matplotlib.pyplot as plt

pygame.init()

# define const
SIZE = WIDTH, HEIGHT = 640*1.5+30, 480*1.5+30
BLACK = 0, 0, 0

# define the map
map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1], 
[1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 
[1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1], 
[1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1], 
[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1], 
[1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1], 
[1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], 
[1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], 
[1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1], 
[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1], 
[1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1], 
[1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1], 
[1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1], 
[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1], 
[1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1], 
[1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1], 
[1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1], 
[1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 3, 1], 
[1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1], 
[1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 
[1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

class Player():
    def __init__(self, spawn:tuple) -> None:
        self.x = spawn[0]+10
        self.y = spawn[1]+10
        self.body = pygame.Rect(self.x, self.y, 5, 5)
        self.center = list(self.body.center)
        self.player_angle = 0
        self.dirX = math.cos(self.player_angle);
        self.dirY = math.sin(self.player_angle);
        self.list_rays_dist_to_wall = []
        self.nb_rays = 120
        for i in range(self.nb_rays):
            self.list_rays_dist_to_wall.append(0)
        self.last_reward = 0
        self.brain = Dqn(5+self.nb_rays, 4, 0.9)
        self.actions = ["up", "right", "left", "down"]
        self.scores = []

    def check_collision(self, x:int, y:int, rect_list) -> bool:
        """Checks if the agent collides a wall

        Args:
            x (int): x coordinate
            y (int) : y coordinate
            rect_list (list): list of the walls

        Returns:
            bool: return True if there is a collision otherwise return False
        """
        for rect in rect_list:
            if self.body.move(x, y).colliderect(rect):
                return True
        return False

    def move_up(self, speed, rect_list) -> bool:
        """Move the agent to the top if there is no collision

        Args:
            speed : travel speed
            rect_list : list of walls (it is for checking collisions)

        Returns:
            bool : True if there is no collisions and False if there is a collision
        """
        self.player_angle = (math.pi/2)
        new_x = int(speed*math.cos(self.player_angle))
        new_y = int(speed*math.sin(self.player_angle))
        self.center = self.body.center
        self.dirX = int(math.cos(self.player_angle));
        self.dirY = int(math.sin(self.player_angle));
        if self.check_collision(new_x, new_y, rect_list) == False:
            self.body.x += new_x
            self.body.y += new_y
            return True
        else:
            return False

    def move_down(self, speed, rect_list) -> bool:
        """Move the agent to the bottom if there is no collision

        Args:
            speed : travel speed
            rect_list : list of walls (it is for checking collisions)

        Returns:
            bool : True if there is no collisions and False if there is a collision
        """
        self.player_angle = (math.pi/2)*3 # Changes the player angle

        new_x = int(speed*math.cos(self.player_angle))
        new_y = int(speed*math.sin(self.player_angle))

        self.center = self.body.center

        self.dirX = int(math.cos(self.player_angle)); # Changes the player X direction
        self.dirY = int(math.sin(self.player_angle)); # Changes the player Y direction

        if self.check_collision(new_x, new_y, rect_list) == False:
            self.body.x += new_x
            self.body.y += new_y
            return True
        else:
            return False

    def move_left(self, speed, rect_list) -> bool:
        """Move the agent to the left if there is no collision

        Args:
            speed : travel speed
            rect_list : list of walls (it is for checking collisions)

        Returns:
            bool : True if there is no collisions and False if there is a collision
        """
        self.player_angle = (math.pi/2)*2
        new_x = int(speed*math.cos(self.player_angle))
        new_y = int(speed*math.sin(self.player_angle))
        self.center = self.body.center
        self.dirX = int(math.cos(self.player_angle));
        self.dirY = int(math.sin(self.player_angle));
        if self.check_collision(new_x, new_y, rect_list) == False:
            self.body.x += new_x
            self.body.y += new_y
            return True
        else:
            return False

    def move_right(self, speed, rect_list) -> bool:
        """Move the agent to the right if there is no collision

        Args:
            speed : travel speed
            rect_list : list of walls (it is for checking collisions)

        Returns:
            bool : True if there is no collisions and False if there is a collision
        """
        self.player_angle = (math.pi/2)*4
        new_x = int(speed*math.cos(self.player_angle))
        new_y = int(speed*math.sin(self.player_angle))
        self.center = self.body.center
        self.dirX = int(math.cos(self.player_angle));
        self.dirY = int(math.sin(self.player_angle));
        if self.check_collision(new_x, new_y, rect_list) == False:
            self.body.x += new_x
            self.body.y += new_y
            return True
        else:
            return False

    def move_to_spawn(self) -> None:
        """Teleports the agent to the spawn
        """
        self.body.x = self.x
        self.body.y = self.y
        
    
    def draw_direction_vector(self, surface):
        """Draw the direction vector of the agent and the angle of vue

        Args:
            surface : surface where the vectors are drawn  
        """
        start_pos = self.center
        end_pos = (self.center[0]+self.dirX*50,
                self.center[1]+self.dirY*50)
        end_pos_right = (self.center[0]+math.cos(self.player_angle-math.pi/6)*50,
                self.center[1]+math.sin(self.player_angle-math.pi/6)*50)
        end_pos_left = (self.center[0]+math.cos(self.player_angle+math.pi/6)*50,
                self.center[1]+math.sin(self.player_angle+math.pi/6)*50)
        pygame.draw.line(surface, (255, 0, 0), start_pos, end_pos)
        pygame.draw.line(surface, (255, 0, 0), start_pos, end_pos_right)
        pygame.draw.line(surface, (255, 0, 0), start_pos, end_pos_left)

    # Thanks to ---- for the algorithm and --- to help me understand it
    def DDA_algorithm(self, surface):
        for i in range(1, self.nb_rays):
            rayStart: tuple = (self.center[0]/30, self.center[1]/30)
            start_angle = self.player_angle+math.pi/6
            FOV = math.pi/3
            ray_angle = start_angle-(FOV/self.nb_rays)*i
            rayDirX:int = math.cos(ray_angle)
            rayDirY:int = math.sin(ray_angle)
            mapX:int = int(self.center[0]/30)
            mapY:int = int(self.center[1]/30)
            
            ray_lenght_X:float = 0.0
            ray_lenght_Y:float = 0.0
                

            if rayDirX == 0: rayDirX = 0.00001
            if rayDirY == 0: rayDirY = 0.00001

            # length of ray from one x or y-side to next x or y-side
            unit_ray_step_size_X : float = math.sqrt(1 + (rayDirY * rayDirY) / (rayDirX * rayDirX))
            unit_ray_step_size_Y : float = math.sqrt(1 + (rayDirX * rayDirX) / (rayDirY * rayDirY))
            wall_dist:float = 0.0
            
            # what direction to step in x or y-direction (either +1 or -1)
            stepX : int = 0
            stepY : int = 0
                
            # was there a wall hit?
            hit : bool = False 
            side :int = 0 # was a NS or a EW wall hit?
                
            # calculate step and initial sideDist
            if rayDirX < 0:
                stepX = -1
                ray_lenght_X = (rayStart[0] - float(mapX)) * unit_ray_step_size_X
            else:
                stepX = 1
                ray_lenght_X = (float(mapX + 1.0) - rayStart[0]) * unit_ray_step_size_X
            if rayDirY < 0:
                stepY = -1
                ray_lenght_Y = (rayStart[1] - float(mapY)) * unit_ray_step_size_Y
            else:
                stepY = 1
                ray_lenght_Y = (float(mapY) + 1.0 - rayStart[1]) * unit_ray_step_size_Y
                
            # perform DDA
            f_max_distance:float = 960.0
            f_distance:float = 0.0
            while not hit and f_distance < f_max_distance:
                # jump to next map square, OR in x-direction, OR in y-direction
                if ray_lenght_X < ray_lenght_Y:
                    f_distance = ray_lenght_X
                    ray_lenght_X += unit_ray_step_size_X
                    mapX += stepX
                else:
                    f_distance = ray_lenght_Y
                    ray_lenght_Y += unit_ray_step_size_Y
                    mapY += stepY
                
                
                # Check if ray has hit a wall
                if mapY <= len(map)-1 and mapX <= len(map[0])-1:
                    if map[mapY][mapX] == 1:
                        end_pos = (self.center[0]+math.cos(ray_angle)*f_distance*30, self.center[1]+math.sin(ray_angle)*f_distance*30)
                        self.list_rays_dist_to_wall.append(f_distance*30)
                        if len(self.list_rays_dist_to_wall) > self.nb_rays:
                            del self.list_rays_dist_to_wall[0]
                        pygame.draw.rect(surface, (255, 0, 0), (mapX*30, mapY*30, 30, 30))
                        pygame.draw.line(surface, (255, 255, 0), self.center, end_pos)
                        hit = True
                


class Game():
    def __init__(self) -> None:
    # initialises the game
        self.screen = pygame.display.set_mode(SIZE)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.convert()
        self.list_rect = []
        self.goals = []
        self.last_distance2goal = 0
        self.last_distance2spawn = 0
        self.player_last_pos = (0, 0)
        self.state_count = 0
        self.current_goal = 0
        self.goals_coords = []
        # create a list of rect and player
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == True:
                    self.list_rect.append(
                        pygame.Rect(j*20*1.5, i*20*1.5, 20*1.5, 20*1.5)
                    )
                if map[i][j] == 2:
                    self.player = Player((j*20*1.5, i*20*1.5))
                    self.spawn = pygame.Rect(j*20*1.5, i*20*1.5, 30, 30)
                if map[i][j] == 3:
                    goal = pygame.Rect(j*20*1.5, i*20*1.5, 30, 30)
                    self.goals.append(goal)
                    self.goals_coords.append(goal.center)
    

    def Draw(self):
        # Clears the screen
        self.screen.fill(BLACK)
        self.background.fill(BLACK)

        # Draws the walls
        for wall in self.list_rect:
            pygame.draw.rect(self.background, (255, 255, 255), wall)
        
        # Draws the spawn
        pygame.draw.rect(self.background, (0, 0, 255), self.spawn)

        # Draws the agent, the direction vector and the rays
        pygame.draw.rect(self.background, (255, 0, 255), self.player.body)
        self.player.draw_direction_vector(self.background)
        self.player.DDA_algorithm(self.background)

        # Draws the goal
        pygame.draw.rect(self.background, (0, 255, 0), self.goals[self.current_goal])

        # Updates the screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def update(self):
        # Saves the last signal
        last_signal = self.player.list_rays_dist_to_wall + list(self.player.center)
        last_signal.append(self.player.player_angle)
        last_signal.append(self.player.dirX)
        last_signal.append(self.player.dirY)

        # Chooses an action and send the last reward and the last signal to the neural network
        action = self.player.brain.update(self.player.last_reward, last_signal)

        # Saves the score
        self.player.scores.append(self.player.brain.score())


        if self.player.actions[action] == "up":
            if self.player.move_up(1, self.list_rect) == False: # Gives a bad reward if the agent touches a wall 
                    self.player.last_reward = -1
                    print("collision") 
            else:
                print("down")
                self.player.last_reward = -0.4


        elif self.player.actions[action] == "down":
            if self.player.move_down(1, self.list_rect) == False: # Gives a bad reward if the agent touches a wall 
                    self.player.last_reward = -1
                    print("collision") 
            else:
                print("up")
                self.player.last_reward = -0.4


        elif self.player.actions[action] == "right":
            if self.player.move_right(1, self.list_rect) == False: # Gives a bad reward if the agent touches a wall 
                    self.player.last_reward = -1
                    print("collision") 
            else:
                print("right")
                self.player.last_reward = -0.4


        elif self.player.actions[action] == "left":
            if self.player.move_left(1, self.list_rect) == False: # Gives a bad reward if the agent touches a wall 
                    self.player.last_reward = -1 
                    print("collision")
            else:
                print("left")
                self.player.last_reward = -0.4
                
        # Calculates the distance between the agent and the goal and the agent and the spawn
        distance2goal = math.sqrt((self.player.center[0] - self.goals_coords[self.current_goal][0])**2 + (self.player.center[1] - self.goals_coords[self.current_goal][1])**2)
        distance2spawn = math.sqrt((self.player.center[0] - self.spawn.centerx)**2 + (self.player.center[1] - self.spawn.centery)**2)

        # Gives a good reward if the agent get close to the goal or if the agent get far to the spawn
        if distance2goal < self.last_distance2goal or distance2spawn > self.last_distance2spawn:
            self.player.last_reward += 0.1
        
        
        # Gives a good reward 
        
        
        # Gives a bad reward if the agent is far to the goal
        if distance2goal > 300:
            self.player.last_reward -= 0.1
            
        if distance2spawn < 20:
            self.player.last_reward = -2
        
        # Changes goal if the agent is to the goal
        if distance2goal < 20:
            #self.player.last_reward = 1
            print("win")
            if len(self.goals) > 1 and (self.current_goal+1) < len(self.goals):
                self.current_goal += 1
            else:
                self.current_goal = 0
        print(self.player.last_reward)
        # Updates last distances
        self.last_distance2goal = distance2goal
        self.last_distance2spawn = distance2spawn
        self.state_count += 1
        if self.state_count == 30:
            self.player_last_pos = self.player.center
            sel.state_count = 0
    

    def run(self):
        # Game loop
        while True:
            # Get event from keyboard
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        print("=> saving brain...")
                        self.player.brain.save()
                        plt.plot(self.player.scores)
                        plt.show()
                        print("done!")
                    if event.key == pygame.K_l:
                        self.player.brain.load()

            self.Draw() 
            self.update()


if __name__ == "__main__":
    game = Game()
    game.run()