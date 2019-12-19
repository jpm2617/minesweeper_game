import numpy as np 
import random
from termcolor import cprint
import os

def main():
  print()
  cprint('Welcome to MineSweeper', 'red')
  cprint('======================', 'red')
  cprint('MAIN MENU','red')
  cprint('-> For instructions on how to play, type \'I\'')
  cprint('-> To play, type \'P\'')
  cprint('-> To exit, type \'E\'')


  choise = input('').upper()

  if choise == 'I':
    os.system('clear')
    print(open('instructions.txt','r').read())
    input('Press any key when ready to play.')
    os.sytem('clear')
  elif choise == 'P':
     os.system('clear')
     n_bombs = 10
     # Solution board
     sol_board = solution_grid(10,10,n_bombs)
     # Interface for gameplay
     known_board = known_grid(10,10)
     # Playing function
     play(sol_board,known_board,n_bombs)
  elif choise == 'E':
     quit()
  else: 
    cprint('please select a valid options','red')
    main()

def play(s,k,n_bombs):

  print(np.array(s))
  print(np.array(k))
  while n_bombs>0:
    # Player choses a square 
    r, c = [int(r) for r in input("Enter row and col index: ").split()] 
    k[r][c]=s[r][c]
    v = k[r][c]
    if v=='*':
      print('================')
      print('You lost')
      print('================')
      print(np.array(k))
      main()
    elif v == 0:
      checkzeros(s,k,r,c)
    print(np.array(s))
    print(np.array(k))
  print('You win')


def checkzeros(s,k,r,c):
  neighbours_in=[[i,j] for i in (-1,0,1) for j in (-1,0,1) if not (i == j == 0)]
  for n in neighbours_in:
    r_n = r + n[0]
    c_n = c + n[1]
    if not (r_n < 0 or c_n < 0  or r_n > len(s[0])-1 or c_n > len(s) -1):
      sol_v = s[r_n][c_n]
      if sol_v != '*':
        k[r_n][c_n] = sol_v
      elif sol_v == 0:
        checkzeros(s,k,r_n,c_n)
        





    

  

def known_grid(row,col):
  board = [['-' for i in range(row)] for j in range(col)] 
  return board

def solution_grid(row,col,n_bombs):
  ## define bombs and place them on the board randomly shuffled
  size = row*col
  n_empty = size - n_bombs
  mines = ['*']*n_bombs + [0]*n_empty
  random.shuffle(mines)
  board = [[mines[j+i*col] for i in range(row)] for j in range(col)] 
 
  ## add padding to the board to avoid dealing with boundary (this is removed after)
  # top and bottom boundaries
  board.insert(0,[0]*(row+2))
  board+=[[0]*(row+2)]
  
  #left and right boundaries
  for i in range(1,row+1):
   # print(board[0])
    board[i].insert(0,0)
    board[i].append(0)

  ## update the number of bombs surrounding each square (ignore padding)
  neighbours_in=[[i,j] for i in (-1,0,1) for j in (-1,0,1) if not (i == j == 0)]
  for i in range(1,row+1):
    for j in range(1,col+1):
      # inside board
      if board[i][j] == '*':
        if i>0 or j>0 or i<row or j<col:
          for k in neighbours_in:
            if board[i+k[0]][j+k[1]] != '*':
              board[i+k[0]][j+k[1]] = board[i+k[0]][j+k[1]] + 1

  ## remove padding from the board
  #left and right boundaries
  for i in range(1,row+1):
    del board[i][0]
    del board[i][-1]
  #top and bottom boundaries
  del board[0], board[-1]
  
  return board

main()

