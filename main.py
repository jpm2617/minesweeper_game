import numpy as np 
import random
#from termcolor import cprint
import os

def main():
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
    input('Press any key to come back to the menu')
    os.sytem('clear')
    main()
  elif choise == 'P':
     os.system('clear')
     n_bombs = 9
     row = 6 #16
     col = 6  #16
     # Solution board
     sol_board = solution_grid(row,col,n_bombs)
     # Interface for gameplay
     known_board = known_grid(row,col)
     # Playing function
     play(sol_board,known_board)
  elif choise == 'E':
     quit()
  else: 
    cprint('please select a valid options','red')
    main()

# Playing function 
def play(s,k):
  debug = 0

  endgame = False
  while endgame == False:
    printboard(s,k,debug)
    win = checkwin(s,k)
    print('Number of spaces to cover: %s' %win)
    if win == 0:
      print('================')
      print('You win')
      print('================')
      endgame = True

    r, c , m= choise_play(k)
    if m == 'm':
      marker(r,c,s,k)
    else:
      k[r][c]=s[r][c]
      v = k[r][c]
      if v == 0:
        checkzeros(s,k,r,c)       
      elif v=='*':
        print('================')
        print('You lost')
        print('================')
        endgame = True

  printboard(s,k,debug)
  main()

# Check if win and return how many spaces are left. 
def checkwin(s,k):
  vec_k =  [i for j in k for i in j] 
  sol_k =  [i for j in k for i in j] 
  #count how many spaces left
  count_k = 0 
  for i in range(len(sol_k)):
    v1 = vec_k[i]
    v2 = sol_k[i]
    if (v1 == '-' or v1 == '⚐') and v2 !='*':
      count_k=count_k+1
  return count_k
    
#Input for gameplay
def choise_play(k):
  outside = True
  while outside == True:
    r, tmp = [i for i in input("Enter row and col index ['i j' or 'i jm' if marker (add or remove)]: ").split()] 
    r = int(r)
    try:
      int(tmp)
      m=0
    except:
      m='m'  
    if m != 0:
      c=int(tmp[:(len(tmp)-1)])
    else:
      c =int(tmp)
    if r>len(k) or r<0 or c>len(k[0]) or c<0:
      print("Outside of board")
    else:
      outside = False
  print(r,c,m)
  return r, c, m
         
#Place or removes a marker in the given location.
def marker(r, c, s, k):
    if k[r][c] == '⚐':
      k[r][c] ='-'
    elif k[r][c] == '-':
      k[r][c] = '⚐'

#Function to print board 
def printboard(s,k,debug):
  if debug == 1:
    print(np.array(s))
    print(np.array(k))
  else:
    print(np.array(k))

#Function to open surrounding zeros if required
def checkzeros(s,k,r,c):
  rc_n = [[r,c]]
  neighbours_in=[[i,j] for i in (-1,0,1) for j in (-1,0,1) if not (i == j == 0)]
  jj = 0
  while jj < len(rc_n):
    for n in neighbours_in:
      r_n = rc_n[jj][0] + n[0]
      c_n = rc_n[jj][1] + n[1]
      if not (r_n < 0 or c_n < 0  or r_n > len(s[0])-1 or c_n > len(s) -1):
        sol_v = s[r_n][c_n]
        if sol_v != '*':
          k[r_n][c_n] = sol_v
        if not any(i == [r_n,c_n] for i in rc_n) and sol_v==0:
          rc_n += [[r_n, c_n]]
    jj = jj +1
    
#User interface initialization
def known_grid(row,col):
  board = [['-' for i in range(row)] for j in range(col)] 
  return board

#Solution initialization
def solution_grid(row,col,n_bombs):
  ## define bombs and place them on the board randomly shuffled
  size = row*col
  n_empty = size - n_bombs
  mines = ['*']*n_bombs + [0]*n_empty
  random.shuffle(mines)
  board = [[mines[j+i*col] for i in range(row)] for j in range(col)] 
 
  ## update the number of bombs surrounding each square 
  neighbours_in=[[i,j] for i in (-1,0,1) for j in (-1,0,1) if not (i == j == 0)]
  for i in range(0,row):
    for j in range(0,col):
      if board[i][j] == '*':
        for k in neighbours_in:
          r_n = i + k[0]
          c_n = j + k[1]
          if not (r_n < 0 or c_n < 0  or r_n > row-1 or c_n > col-1):
            if board[r_n][c_n] != '*':
              board[r_n][c_n] = board[r_n][c_n] + 1
  return board

main()
