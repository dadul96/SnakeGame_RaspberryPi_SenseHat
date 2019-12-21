from sense_hat import SenseHat
import time
import random

senseHat = SenseHat()
senseHat.low_light = True

green = (0, 255, 0)
red = (255, 0, 0)
white = (255,255,255)
nothing = (0,0,0)

def five_img():
    W = white
    O = nothing
    img = [
    O, O, W, W, W, W, O, O,
    O, O, W, O, O, O, O, O,
    O, O, W, O, O, O, O, O,
    O, O, W, W, W, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, W, W, W, W, O, O,
    ]
    return img

def four_img():
    W = white
    O = nothing
    img = [
    O, O, W, O, O, O, O, O,
    O, O, W, O, O, O, O, O,
    O, O, W, O, O, O, O, O,
    O, O, W, O, W, O, O, O,
    O, O, W, W, W, W, O, O,
    O, O, O, O, W, O, O, O,
    O, O, O, O, W, O, O, O,
    O, O, O, O, W, O, O, O,
    ]
    return img

def three_img():
    W = white
    O = nothing
    img = [
    O, O, W, W, W, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, O, W, W, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, W, W, W, W, O, O,
    ]
    return img

def two_img():
    W = white
    O = nothing
    img = [
    O, O, W, W, W, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, O, O, O, W, O, O,
    O, O, W, W, W, W, O, O,
    O, O, W, O, O, O, O, O,
    O, O, W, O, O, O, O, O,
    O, O, W, O, O, O, O, O,
    O, O, W, W, W, W, O, O,
    ]
    return img

def one_img():
    W = white
    O = nothing
    img = [
    O, O, O, O, W, O, O, O,
    O, O, O, W, W, O, O, O,
    O, O, W, O, W, O, O, O,
    O, O, O, O, W, O, O, O,
    O, O, O, O, W, O, O, O,
    O, O, O, O, W, O, O, O,
    O, O, O, O, W, O, O, O,
    O, O, O, W, W, W, O, O,
    ]
    return img

images = [five_img, four_img, three_img, two_img, one_img]

while True:
  #variables:
  gameOverFlag = False
  growFlag = False
  randomFoodFlag = False
  speed = 0.5
  speedIncrease = 0.02

  #start countdown:
  for img in images:
      senseHat.set_pixels(img())
      time.sleep(.70)
  
  #set standard snake starting position:
  snakePosX = [3]
  snakePosY = [6]
  
  #generate random food position:
  while True:
    foodPosX = random.randint(0, 7)
    foodPosY = random.randint(0, 7)
    if foodPosX != snakePosX[0] or foodPosY != snakePosY[0]:
      break

  #set standard snake starting direction:
  moveX = 0
  moveY = -1
  
  
  #-----------------------------------
  #             game loop
  #-----------------------------------
  while not gameOverFlag:
    #check food:
    if foodPosX == snakePosX[0] and foodPosY == snakePosY[0]:
      growFlag = True
      randomFoodFlag = True
      speed = speed - speedIncrease
    
    #check suicide:
    for i in range(1, len(snakePosX)):
      if snakePosX[i] == snakePosX[0] and snakePosY[i] == snakePosY[0]:
        gameOverFlag = True
    
    #check gameover:
    if gameOverFlag:
      break
    
    #check joystic:
    events = senseHat.stick.get_events()
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
    
    #grow snake:
    if growFlag:
      growFlag = False
      snakePosX.append(0)
      snakePosY.append(0)
    
    #move direction:
    for i in range((len(snakePosX)-1), 0, -1):
      snakePosX[i] = snakePosX[i-1]
      snakePosY[i] = snakePosY[i-1]
      
    snakePosX[0] = snakePosX[0] + moveX
    snakePosY[0] = snakePosY[0] + moveY
    
    #check game borders:
    if snakePosX[0] > 7:
      snakePosX[0] = snakePosX[0] - 8
    elif snakePosX[0] < 0:
      snakePosX[0] = snakePosX[0] + 8
    if snakePosY[0] > 7:
      snakePosY[0] = snakePosY[0] - 8
    elif snakePosY[0] < 0:
      snakePosY[0] = snakePosY[0] + 8
    
    #spawn random food:
    if randomFoodFlag:
      randomFoodFlag = False
      retryFlag = True
      while retryFlag:
        foodPosX = random.randint(0, 7)
        foodPosY = random.randint(0, 7)
        retryFlag = False
        for x, y in zip(snakePosX, snakePosY):
          if x == foodPosX and y == foodPosY:
            retryFlag = True
            break
    
    #update matrix:
    senseHat.clear()
    senseHat.set_pixel(foodPosX, foodPosY, red)
    for x, y in zip(snakePosX, snakePosY):
      senseHat.set_pixel(x, y, green)
    
    #speed:
    time.sleep(speed)
