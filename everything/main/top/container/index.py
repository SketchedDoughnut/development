# the coding gods have screwed me over and I need to redesign this program

# import for initial
import os

# vars
wDir = os.path.dirname(os.path.abspath(__file__))
path_list = []
path_list.append([os.path.join(wDir, 'imports.py'), 'Imports agent'])
path_list.append([os.path.join(wDir, 'update.py'), 'Update agent'])
path_list.append([os.path.join(wDir, 'game_data/src/flappy/flappy.py'), 'Flappy bird'])
path_list.append([os.path.join(wDir, 'game_data/src/rhythm/rhythm.py'), 'Rhythm'])

# imports
def imports():
   #print('----------------------------')
   print(f'Running {path_list[0][1]}...')
   print('----------------------------')
   os.system(f'python {path_list[0][0]}')

imports()

print('----------------------------')
import pygame
from pygame.locals import *
import timeit
import time
import json

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 1920
HEIGHT = 1080

def update():
   print('----------------------------')
   print(f'Running {path_list[1][1]}...')
   os.system(f'python {path_list[1][0]}')

class Format:
  def __init__(self):
    self.x = None
    self.y = None
    self.width = None
    self.height = None

  def div(self):
    self.notes_pos = []
    self.num_cubes = 2
    cube_width = HEIGHT / self.num_cubes  # Adjust this as needed
    gap = (HEIGHT - (self.num_cubes * cube_width)) / (self.num_cubes + 1) # Calculate the gap between each cube
    for i in range(self.num_cubes): # Calculate the x-coordinate for each cube
        cube_y = round((i + 1) * gap + i * cube_width)
        self.notes_pos.append(cube_y)
 
  def build_rect(self):
    self.builds = []
    for i in self.notes_pos:
      assembly = pygame.Rect(0, i, WIDTH, round(HEIGHT / self.num_cubes))
      self.builds.append(assembly)
     
  def assemble(self):
    self.draw_queue = []
    for i in self.notes_pos:
      obj = Format()
      obj.x = 0
      obj.y = i
      obj.width = WIDTH
      obj.height = round(HEIGHT / self.num_cubes)
      self.draw_queue.append(obj)

  def handler(self):
    self.div()
    self.assemble()
    self.build_rect()





update()
f = open(f'{wDir}/state.json', 'r')
if bool(json.load(f)) == True:
   f.close()
   exit()
f.close()

setup = Format()
setup.handler()

setup_bool = False

while True:
  if setup_bool == False:
    start_1 = False
    start_2 = False

    import random
    color_list = []
    for i in setup.draw_queue:
      color_list.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    print('----------------------------')
    print('Colors:', color_list)
    print('S to export colors (game_data/ignore/colors.json)')
    print('R to refresh colors.')

    mouse_pressed = False
    s_pressed = False
    r_pressed = False

    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("thing!")

    setup_bool = True

  pygame.time.delay(1)

  for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
    
  # gathering input data
  keys = pygame.key.get_pressed()
  mouse_pos = pygame.mouse.get_pos()

  # exits if
  if keys[K_LCTRL]:
        if keys[K_c]:
            break
        elif keys[K_w]:
            break
  if keys[K_ESCAPE]:
      break
  
  if keys[K_s]:
     if s_pressed == False:
      f = open(os.path.join(wDir, 'game_data/ignore/colors.json'), 'r')
      color_load = list(json.load(f))
      f.close()
      color_load.append(color_list)
      f = open(os.path.join(wDir, 'game_data/ignore/colors.json'), 'w')
      json.dump(color_load, f)
      f.close()
      print('- dumped colors into game_data/ignore/colors.json')
      s_pressed = True
  elif not keys[K_s]:
     s_pressed = False

  if keys[K_r]:
     if r_pressed == False:
        import random
        color_list = []
        for i in setup.draw_queue:
          color_list.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        print('- refreshed colors')
        r_pressed = True
  elif not keys[K_r]:
     r_pressed = False
     

  
  for i, i2 in zip(setup.draw_queue, color_list):
    bound = pygame.draw.rect(window, i2, (i.x, i.y, i.width, i.height))
    mouse_pressed = pygame.mouse.get_pressed()
    if bound.collidepoint(mouse_pos):
      if mouse_pressed[0]:
        if setup.draw_queue.index(i) == 0:
          start_1 = True
        elif setup.draw_queue.index(i) == 1:
          start_2 = True
        else:
          start_1 = False
          start_2 = False

  font = pygame.font.Font('freesansbold.ttf', round(36 * 1.5))
  text1 = font.render(path_list[2][1], True, WHITE, None) # text, some bool(?), text color, bg color
  text1_rect = text1.get_rect(center=(WIDTH / 2, HEIGHT / 4))
  text2 = font.render(path_list[3][1], True, WHITE, None) # text, some bool(?), text color, bg color
  text2_rect = text1.get_rect(center=(WIDTH / 2, (3 * (HEIGHT / 4))))
  window.blit(text1, text1_rect)
  window.blit(text2, text2_rect)

  pygame.display.update()
  if start_1 or start_2:
    pygame.quit()
    if start_1:
      print('----------------------------')
      print('Redirecting into flappy bird...')
      os.system(f'python {path_list[2][0]}')
      setup_bool = False
    elif start_2:
      print('----------------------------')
      print('Redirecting into rhythm game...')
      os.system(f'python {path_list[3][0]}')
      setup_bool = False

print('----------------------------')
print('Exiting...')