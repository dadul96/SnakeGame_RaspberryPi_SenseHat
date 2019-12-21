from sense_hat import SenseHat
import time
import random

s = SenseHat()
s.low_light = True

green = (0, 255, 0)
red = (255, 0, 0)
white = (255,255,255)
nothing = (0,0,0)

def five_logo():
    W = white
    O = nothing
    logo = [
    O, O, W, W, W, W, O, O,
    O, O, W, O, O, O, O, O,
    O, O, W, O, O, O, O, O,
    O, O, W, W, W, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, W, W, W, W, O, O,
    ]
    return logo

def four_logo():
    W = white
    O = nothing
    logo = [
    O, O, W, O, O, O, O, O,
    O, O, W, O, O, O, O, O,
    O, O, W, O, O, O, O, O,
    O, O, W, O, W, O, O, O,
    O, O, W, W, W, W, O, O,
    O, O, O, O, W, O, O, O,
    O, O, O, O, W, O, O, O,
    O, O, O, O, W, O, O, O,
    ]
    return logo

def three_logo():
    W = white
    O = nothing
    logo = [
    O, O, W, W, W, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, O, W, W, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, W, W, W, W, O, O,
    ]
    return logo

def two_logo():
    W = white
    O = nothing
    logo = [
    O, O, W, W, W, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, W, W, W, W, O, O,
    O, O, W, O, O, O, O, O,
    O, O, W, O, O, O, O, O,
    O, O, W, O, O, O, O, O,
    O, O, W, W, W, W, O, O,
    ]
    return logo

def one_logo():
    W = white
    O = nothing
    logo = [
    O, O, O, O, W, O, O, O,
    O, O, O, W, W, O, O, O,
    O, O, W, O, W, O, O, O,
    O, O, O, O, W, O, O, O,
    O, O, O, O, W, O, O, O,
    O, O, O, O, W, O, O, O,
    O, O, O, O, W, O, O, O,
    O, O, O, W, W, W, O, O,
    ]
    return logo

def clear_logo():
    W = white
    O = nothing
    logo = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    ]
    return logo
    
images = [five_logo, four_logo, three_logo, two_logo, one_logo, clear_logo]

while True:
  #variables:
  gameOverFlag = False
  speed = 0.5
  grow = False
  
  #start countdown:
  for image in images:
      s.set_pixels(image())
      time.sleep(.70)
  
  #set standard snake starting position:
  snakePosX = [3]
  snakePosY = [6]
  
  #generate random food position:
  foodPosX = 0
  foodPosY = 0
  while True:
    foodPosX = random.randint(0, 7)
    foodPosY = random.randint(0, 7)
    if foodPosX != snakePosX[0] or foodPosY != snakePosY[0]:
      break

  #set standard snake starting direction (move upwards):
  moveX = 0
  moveY = -1
  
  
  ###########
  ###########
  #game loop:
  while not gameOverFlag:
    #check food:
    if foodPosX == snakePosX[0] and foodPosY == snakePosY[0]:
      speed = speed - 0.02  #increase speed
      grow = True
      retryRandomFoodPos = True
      while retryRandomFoodPos:
        foodPosX = random.randint(0, 7)
        foodPosY = random.randint(0, 7)
        retryRandomFoodPos = False
        for i in range(len(snakePosX)):
          if foodPosX == snakePosX[i] and foodPosY == snakePosY[i]:
            retryRandomFoodPos = True
            break
    
    #check suicide:
    for i in range(1, len(snakePosX)):
      if snakePosX[0] == snakePosX[i] and snakePosY[0] == snakePosY[i]:
        gameOverFlag = True
    if gameOverFlag:
      break
    
    #check joystic:
    events = s.stick.get_events()
    for event in events:
      if event.direction == "left" and moveX != 1:
        moveX = -1
        moveY = 0
      elif event.direction == "right" and moveX != -1:
        moveX = 1
        moveY = 0
      elif event.direction == "up" and moveY != 1:
        moveY = -1
        moveX = 0
      elif event.direction == "down" and moveY != -1:
        moveY = 1
        moveX = 0
    
    #move direction:
    if grow:
      grow = False
      snakePosX.append(0)
      snakePosY.append(0)
      
    for i in range((len(snakePosX)-1), 0, -1):
      snakePosX[i] = snakePosX[i-1]
      snakePosY[i] = snakePosY[i-1]
    
    snakePosX[0] = snakePosX[0] + moveX
    snakePosY[0] = snakePosY[0] + moveY
    if snakePosX[0] > 7:
      snakePosX[0] = snakePosX[0] - 8
    if snakePosY[0] > 7:
      snakePosY[0] = snakePosY[0] - 8
    if snakePosX[0] < 0:
      snakePosX[0] = snakePosX[0] + 8
    if snakePosY[0] < 0:
      snakePosY[0] = snakePosY[0] + 8
      
    #update matrix:
    s.set_pixels(clear_logo())
    s.set_pixel(foodPosX, foodPosY, red) #set food pixel
    for i in range(len(snakePosX)):
      s.set_pixel(snakePosX[i], snakePosY[i], green) #set snake pixels
    
    #speed:
    time.sleep(speed)
  ###########
  ###########