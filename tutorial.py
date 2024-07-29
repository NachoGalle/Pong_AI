import pygame
from pong_classes import Game #esto lo puedo hacer porque pong_AI contiene  __init__.py
import neat
import os
import pickle #para guardar objetos (en este caso genomas) 

FPS = 60
WIDHT, HEIGHT = 700, 500
window = pygame.display.set_mode((WIDHT,HEIGHT))

class PongGame:
    def __init__(self,win,width,height):
        self.game = Game(window,WIDHT,HEIGHT)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball
    
    def test_ai(self,genome, config):
        run = True
        reloj = pygame.time.Clock()

        net = neat.nn.FeedForwardNetwork.create(genome,config)


        while run:
            reloj.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            
            output= net.activate((self.right_paddle.y,self.ball.y,abs(self.right_paddle.x-self.ball.x)))
            decision = output.index(max(output))
            if decision == 0:
                pass
            elif decision == 1:
                self.game.move_paddle(left=False,up=True)
            else:
                self.game.move_paddle(left=False,up=False)

            keys =pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle()
            if keys[pygame.K_s]:
                self.game.move_paddle(up=False)

            gameinfo=self.game.loop()
            
            self.game.draw(draw_score=True)
            pygame.display.update()
        
        pygame.quit
    
    def train_ai(self,genome1,genome2,config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1,config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2,config)

        
        
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()         

            output1= net1.activate((self.left_paddle.y,self.ball.y,abs(self.left_paddle.x-self.ball.x)))
            decision1 = output1.index(max(output1))
            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.move_paddle(left=True,up=True)
            else:
                self.game.move_paddle(left=True,up=False)

            output2= net2.activate((self.right_paddle.y,self.ball.y,abs(self.right_paddle.x-self.ball.x)))
            decision2 = output2.index(max(output2))
            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.move_paddle(left=False,up=True)
            else:
                self.game.move_paddle(left=False,up=False)

            game_info = self.game.loop()
            self.game.draw(draw_hits=True)
            pygame.display.update()

            #if game_info.left_score >=1 or game_info.right_score >=1 or game_info.left_hits > 30:
            #    self.calculate_fitness(genome1,genome2,game_info)
            #    break

            if game_info.left_score + game_info.right_score >=3 or game_info.left_hits > 25:
                self.calculate_fitness(genome1,genome2,game_info)
                break
    
    def calculate_fitness(self,genome1,genome2,game_info):
        #genome1.fitness+= game_info.left_hits
        #genome2.fitness += game_info.right_hits

        genome1.fitness+= game_info.left_hits
        genome2.fitness += game_info.right_hits
            
def eval_genomes(genomes,config):
    widht, height = 700,500
    window = pygame.display.set_mode((widht,height))
    for i, (genome_id1,genome1) in enumerate(genomes):
        if i == len(genomes)-1:
            break
        genome1.fitness = 0
        #genome1.fitness = 0 if genome1.fitness == None else genome1.fitness
        for genome_id2 , genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness  #los genomas que no hayan jugado tienen fitness = 0
            game = PongGame(window,widht,height)
            game.train_ai(genome1,genome2,config)

def run_neat(config):
    # Create the population, which is the top-level object for a NEAT run.
    pop = neat.Population(config)
    
    #pop = neat.Checkpointer.restore_checkpoint("neat-checkpoint-")      #para cargar desde un checkpoint 
    pop.add_reporter(neat.StdOutReporter(True))                          # Add a stdout reporter to show progress in the terminal.
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(1))       #Cada cuanto se guarda un checkpoint
    
    winner = pop.run(eval_genomes, 15)  #corre NEAT por n generaciones (eval_genomes es la fitness_function)
    with open("best.pickle","wb") as f:   #wb=write bites
        pickle.dump(winner,f)
    
def test_ai(config):
    widht, height = 700,500
    window = pygame.display.set_mode((widht,height))
    with open("best.pickle","rb") as f:   #rb=read bites
        winner = pickle.load(f)
    game = PongGame(window,widht,height)
    game.test_ai(winner,config)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config.txt")

    config = neat.Config(neat.DefaultGenome,neat.DefaultReproduction,
                         neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)

    run_neat(config)
    #input("test neural network")
    #test_ai(config)