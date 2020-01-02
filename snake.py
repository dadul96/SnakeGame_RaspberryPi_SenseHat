from sense_hat import SenseHat
import time
import random

senseHat = SenseHat()
senseHat.low_light = True

GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
NO_LED = (0, 0, 0)


def five_img():
    W = WHITE
    O = NO_LED
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
    W = WHITE
    O = NO_LED
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
    W = WHITE
    O = NO_LED
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
    W = WHITE
    O = NO_LED
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
    W = WHITE
    O = NO_LED
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

COUNTDOWN_DELAY = 0.70
MATRIX_MIN_VALUE = 0
MATRIX_MAX_VALUE = 7
MATRIX_SIZE = 8

while True:
    # variables:
    gameOverFlag = False
    growSnakeFlag = False
    generateRandomFoodFlag = False
    snakeMovementDelay = 0.5
    snakeMovementDelayDecrease = -0.02

    # start countdown:
    for img in images:
        senseHat.set_pixels(img())
        time.sleep(COUNTDOWN_DELAY)

    # set default snake starting position (values are just chosen by preference):
    snakePosX = [3]
    snakePosY = [6]

    # generate random food position:
    while True:
        foodPosX = random.randint(0, 7)
        foodPosY = random.randint(0, 7)
        if foodPosX != snakePosX[0] or foodPosY != snakePosY[0]:
            break

    # set default snake starting direction (values are just chosen by preference):
    movementX = 0
    movementY = -1

    # -----------------------------------
    #             game loop
    # -----------------------------------
    while not gameOverFlag:
        # check if snake eats food:
        if foodPosX == snakePosX[0] and foodPosY == snakePosY[0]:
            growSnakeFlag = True
            generateRandomFoodFlag = True
            snakeMovementDelay += snakeMovementDelayDecrease

        # check if snake bites itself:
        for i in range(1, len(snakePosX)):
            if snakePosX[i] == snakePosX[0] and snakePosY[i] == snakePosY[0]:
                gameOverFlag = True

        # check if game-over:
        if gameOverFlag:
            break

        # check joystick events:
        events = senseHat.stick.get_events()
        for event in events:
            if event.direction == "left" and movementX != 1:
                movementX = -1
                movementY = 0
            elif event.direction == "right" and movementX != -1:
                movementX = 1
                movementY = 0
            elif event.direction == "up" and movementY != 1:
                movementY = -1
                movementX = 0
            elif event.direction == "down" and movementY != -1:
                movementY = 1
                movementX = 0

        # grow snake:
        if growSnakeFlag:
            growSnakeFlag = False
            snakePosX.append(0)
            snakePosY.append(0)

        # move snake:
        for i in range((len(snakePosX)-1), 0, -1):
            snakePosX[i] = snakePosX[i-1]
            snakePosY[i] = snakePosY[i-1]

        snakePosX[0] += movementX
        snakePosY[0] += movementY

        # check game borders:
        if snakePosX[0] > MATRIX_MAX_VALUE:
            snakePosX[0] -= MATRIX_SIZE
        elif snakePosX[0] < MATRIX_MIN_VALUE:
            snakePosX[0] += MATRIX_SIZE
        if snakePosY[0] > MATRIX_MAX_VALUE:
            snakePosY[0] -= MATRIX_SIZE
        elif snakePosY[0] < MATRIX_MIN_VALUE:
            snakePosY[0] += MATRIX_SIZE

        # spawn random food:
        if generateRandomFoodFlag:
            generateRandomFoodFlag = False
            retryFlag = True
            while retryFlag:
                foodPosX = random.randint(0, 7)
                foodPosY = random.randint(0, 7)
                retryFlag = False
                for x, y in zip(snakePosX, snakePosY):
                    if x == foodPosX and y == foodPosY:
                        retryFlag = True
                        break

        # update matrix:
        senseHat.clear()
        senseHat.set_pixel(foodPosX, foodPosY, RED)
        for x, y in zip(snakePosX, snakePosY):
            senseHat.set_pixel(x, y, GREEN)

        # snake speed (game loop delay):
        time.sleep(snakeMovementDelay)
