from game import new_game, make_move, possible_moves
import sys, pygame, math
from pygame.locals import *
pygame.init()


class GameView:
    def __init__(self):
        self.size = 600, 450
        self.myfont = pygame.font.SysFont("monospace", 35)
        self.window = pygame.display.set_mode(self.size)
        pygame.display.set_caption('2048')
        self.background = pygame.Surface(self.size)
        self.background.fill((255,255,255))
        self.window.blit(self.background, (0,0))
        pygame.display.flip()

        
    def color(self, n):
        """ Return RGB color for cell value n. """
        
        val = 255-20*math.log(n,2)
        if val < 0:
            val = 0
        return (255, val, val)


    def draw(self, board, score):
        """ Redraw board and score in the view. """

        size = len(board)        
        self.background.fill((20,20,20))
        
        # draw the cells
        for i in range(size):
            for j in range(size):
                val = board[i][j]
                if val: 
                    xpos, ypos = 10 + 110*j, 10 + 110*i
                    cell = pygame.Surface((100,100))
                    cell.fill(self.color(val))
                    text = self.myfont.render(str(val), 1, (0,0,0))
                    tx, ty = text.get_size()

                    cell.blit(text, (50-tx/2,50-ty/2))
                    self.background.blit(cell, (xpos,ypos))
                    
        # draw score text
        label = self.myfont.render("Score:", 1, (255,255,255))
        scoretxt = self.myfont.render(str(score), 1, (255,255,255))
        self.background.blit(label, (450,10))
        self.background.blit(scoretxt, (450,50))

        # update display
        self.window.blit(self.background, (0,0))
        pygame.display.flip()

        
def main():    
    view = GameView()    
    board, score = new_game(4)
    view.draw(board,score)
    clock = pygame.time.Clock()
    
    while True:
        clock.tick(20) # limit fps

        redraw = False

        for event in pygame.event.get():
            if event.type == QUIT: return

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    score += make_move(board, 'left')
                    redraw = True
                if event.key == K_RIGHT:
                    score += make_move(board, 'right')
                    redraw = True
                if event.key == K_UP:
                    score += make_move(board, 'up')
                    redraw = True
                if event.key == K_DOWN:
                    score += make_move(board, 'down')
                    redraw = True
    
        if redraw:            
            view.draw(board, score)
            print possible_moves(board)

if __name__ == "__main__":
    main()