import pygame

pygame.init()

WIDTH, HEIGHT = 700, 500
FPS = 90

PADDLE_WIDTH, PADDLE_HEIGHT = 20 , 100
PADDLE_VEL = 9
#COLORES
ROJO = (255,0,0)
BLANCO = (255,255,255)
NEGRO = (0,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)

BALL_SIZE = 7
MAX_VEL = 6
WINNING_SCORE = 10

SCORE_FONT = pygame.font.SysFont("comicsans",50)

WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")

class Ball:
    def __init__(self,x,y):
        self.size = BALL_SIZE
        self.x = x
        self.y = y
        self.x_vel = MAX_VEL
        self.y_vel = 0
    
    def draw(self,win):
        pygame.draw.circle(win,center=(self.x,self.y),color=BLANCO,radius=BALL_SIZE)

    def move(self):
        self.x+=self.x_vel
        self.y+=self.y_vel

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.x_vel *= -1
        self.y_vel = 0

class Paddle:
    VEL = PADDLE_VEL
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT

    def reset(self):
        self.y = HEIGHT // 2 - PADDLE_HEIGHT//2


    def draw(self,win):
        #pygame.draw.rect(surface=win,color=self.color,rect=(self.x,self.y,self.width,self.height),border_radius=12,width=3)   #activa color
        pygame.draw.rect(surface=win,color=BLANCO,rect=(self.x,self.y,self.width,self.height))

    def move(self,up = True):
        if up:
            self.y-= self.VEL
        else:
            self.y += self.VEL

def draw(win,paddles,ball,left_score,right_score):
    win.fill(NEGRO)

    left_score_text = SCORE_FONT.render(f"{left_score}",1,BLANCO) #el 1 es para antialiasing
    right_score_text = SCORE_FONT.render(f"{right_score}",1,BLANCO)
    win.blit(left_score_text,(WIDTH//4 - left_score_text.get_width()//2,20))
    win.blit(right_score_text,(3*WIDTH//4 - right_score_text.get_width()//2,20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10,HEIGHT,HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win,BLANCO,(WIDTH//2-5,i,10,HEIGHT//20))

    ball.draw(win)

    pygame.display.update()

def handle_paddle_movement(keys,left_paddle,right_paddle):
    if keys[pygame.K_UP] and right_paddle.y>0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y+PADDLE_HEIGHT<HEIGHT:
        right_paddle.move(up=False)
    
    if keys[pygame.K_w] and left_paddle.y>0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y+PADDLE_HEIGHT<HEIGHT:
        left_paddle.move(up=False)

def handle_colission(ball,left_paddle,right_paddle):
    if ball.y - BALL_SIZE <= 0 or ball.y + BALL_SIZE >= HEIGHT:
        ball.y_vel *= -1
    
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + PADDLE_HEIGHT:
            if ball.x - BALL_SIZE <= left_paddle.x + PADDLE_WIDTH:
                ball.x_vel *= -1
                half_paddle_y=left_paddle.y+PADDLE_HEIGHT//2
                ball.y_vel = (ball.y-half_paddle_y)*MAX_VEL*2/PADDLE_HEIGHT
    
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + PADDLE_HEIGHT:
            if ball.x + BALL_SIZE >= right_paddle.x:
                ball.x_vel *= -1
                half_paddle_y=right_paddle.y+PADDLE_HEIGHT//2
                ball.y_vel = (ball.y-half_paddle_y)*MAX_VEL*2/PADDLE_HEIGHT

def reset_position(l_paddle,r_paddle,ball):
    ball.reset()
    l_paddle.reset()
    r_paddle.reset()

def main():
    jugando = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10,HEIGHT//2-PADDLE_HEIGHT//2,ROJO)
    right_paddle = Paddle(WIDTH-PADDLE_WIDTH-10,HEIGHT//2-PADDLE_HEIGHT//2,AZUL)
    ball = Ball(WIDTH//2,HEIGHT//2)

    left_score = 0
    right_score = 0

    while jugando:
        won = False
        clock.tick(FPS)
        draw(WINDOW,[left_paddle,right_paddle],ball,left_score,right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False
                break
    
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys,left_paddle,right_paddle)
        handle_colission(ball,left_paddle,right_paddle)
        ball.move()

        if ball.x <= 0:
            right_score += 1
            reset_position(left_paddle,right_paddle,ball)

        elif ball.x >= WIDTH:
            left_score += 1
            reset_position(left_paddle,right_paddle,ball)
        
        if left_score >= WINNING_SCORE:
            win_text = "Left Player Won!"
            won = True
        elif right_score >= WINNING_SCORE:
            win_text = "Right Player Won!"
            won = True
        
        if won:
            text = SCORE_FONT.render(win_text,1,BLANCO)
            WINDOW.blit(text, (WIDTH//2 -  text.get_width()//2,HEIGHT//2- text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            reset_position(left_paddle,right_paddle,ball)
            left_score, right_score = 0 , 0

    pygame.quit()

if __name__ == "__main__":
    main()