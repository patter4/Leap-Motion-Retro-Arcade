import math, pygame, sys
from pygame.locals import *


FPS = 200

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
LINE_THICKNESS = 10
PADDLE_SIZE = 50
PADDLE_OFFSET = 20

BLACK = (0,0,0)
WHITE = (255,255,255)

RIGHT = 1
LEFT = -1
UP = -1
DOWN = 1


def drawArena():
    DISPLAY_SURF.fill(BLACK)
    pygame.draw.rect(DISPLAY_SURF, WHITE, ((0,0),
                    (WINDOW_WIDTH, WINDOW_HEIGHT)), LINE_THICKNESS*2 )
    pygame.draw.line(DISPLAY_SURF, WHITE, ((WINDOW_WIDTH/2),0),((WINDOW_WIDTH/2),WINDOW_HEIGHT), (LINE_THICKNESS/4))


def drawPaddle(paddle):
    if paddle.bottom > WINDOW_HEIGHT - LINE_THICKNESS:
            paddle.bottom = WINDOW_HEIGHT - LINE_THICKNESS
    elif paddle.top < LINE_THICKNESS:
        paddle.top = LINE_THICKNESS
    pygame.draw.rect(DISPLAY_SURF, WHITE, paddle)


def drawBall(ball):
    pygame.draw.rect(DISPLAY_SURF, WHITE, ball)


def moveBall(ball, xDir, yDir, speed):
    ball.x += math.floor(speed*xDir)
    ball.y += math.floor(speed*yDir)
    return ball


def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == (LINE_THICKNESS) or ball.bottom == (WINDOW_HEIGHT - LINE_THICKNESS):
        ballDirY *= (-1)
    if ball.left == (LINE_THICKNESS) or ball.right == (WINDOW_WIDTH - LINE_THICKNESS):
        ballDirX *= (-1)
    return ballDirX, ballDirY


def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else: return 1


def checkPointScored(ball, score1, score2, ballDirX):
    if ball.left == LINE_THICKNESS:
        return 2
    elif ball.right == WINDOW_WIDTH - LINE_THICKNESS:
        return 1
    else:
        return 0


def displayScore(score1, score2):
    resultSurf1 = BASIC_FONT.render('Score = %s' %(score1), True, WHITE)
    resultRect1 = resultSurf1.get_rect()
    resultRect1.topleft = (20, 25)
    DISPLAY_SURF.blit(resultSurf1, resultRect1)

    resultSurf2 = BASIC_FONT.render('Score = %s' %(score2), True, WHITE)
    resultRect2 = resultSurf2.get_rect()
    resultRect2.topleft = (WINDOW_WIDTH - 120, 25)
    DISPLAY_SURF.blit(resultSurf2, resultRect2)


def main():
    pygame.init()
    global DISPLAY_SURF
    global BASIC_FONT, BASIC_FONT_SIZE
    BASIC_FONT_SIZE = 20
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption('Pong')

    score1=0
    score2=0

    ballx = WINDOW_WIDTH/2 - LINE_THICKNESS/2
    bally = WINDOW_HEIGHT/2 - LINE_THICKNESS/2

    playerOnePosition = (WINDOW_HEIGHT - PADDLE_SIZE) / 2
    playerTwoPosition = (WINDOW_HEIGHT - PADDLE_SIZE) / 2

    ballDirX = LEFT
    ballDirY = UP
    speed = 1

    playerOnePaddle = pygame.Rect(PADDLE_OFFSET, playerOnePosition,
                                  LINE_THICKNESS, PADDLE_SIZE)
    playerTwoPaddle = pygame.Rect(WINDOW_WIDTH - PADDLE_OFFSET - LINE_THICKNESS,
                                  playerTwoPosition, LINE_THICKNESS,
                                  PADDLE_SIZE)
    ball = pygame.Rect(ballx, bally, LINE_THICKNESS, LINE_THICKNESS)

    drawArena()
    drawPaddle(playerOnePaddle)
    drawPaddle(playerTwoPaddle)
    drawBall(ball)

    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        drawArena()
        drawPaddle(playerOnePaddle)
        drawPaddle(playerTwoPaddle)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY, speed)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)

        ballDirX = ballDirX * checkHitBall(ball, playerOnePaddle, playerTwoPaddle, ballDirX)

        score = checkPointScored(ball, score1, score2, ballDirX)
        if score == 1:
            score1+=1
        if score == 2:
            score2+=1
        displayScore(score1, score2)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

if __name__=='__main__':
    main()
