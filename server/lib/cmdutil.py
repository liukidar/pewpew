import os

def log(_str):
  print('\r' + _str + '\n> ', end='')

def clear():
  os.system("cls")