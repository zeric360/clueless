from game_board import gameBoard
import pygame

class Gui:
     # attributes
     room = pygame.Rect(30, 30, 30, 30)
     hallway = pygame.Rect(15, 15, 40, 40)
     color = (255, 0, 0)

     #methods
     def __init__(self):
          pygame.init()     

     def draw_starting_board(self):
          print("Draw starting board")
     
     def draw_current_board(self, player_location_dict):
          #draw starting board everytime we update the board
          self.draw_starting_board()
          print("Draw board")
          for player, loc in player_location_dict.items():
               print(f"Drawing {player} in {loc}")

if __name__ == '__main__':
     gui = gui()    
     gb = gameBoard([1, 2, 3])

     gb.print_board()
     gui.draw_current_board(gb.player_location_dict)
