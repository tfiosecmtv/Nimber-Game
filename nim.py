
import random
import time

class CantMove( Exception ) :

   def __init__( self, reason ) : 
      self. __reason = reason

   def __repr__( self ) :
      return "unable to find a move: {}". format( self.__reason )


class Nim :
   def __init__( self, startstate ) :
      self. state = startstate


   # Goal is to be unambiguous : 

   def __repr__( self ) :
      s = ""
      for i in range(1, len(self.state)+1, 1):
          s += str(i)
          s += '   :'
          for x in range(0, self.state[i-1], 1):
             s += ' 1'
          s += '\n'
      return s


   # Return sum of all rows:

   def sum( self ) :
       a = 0
       for st in self.state:
           a += st
       return a


   # Return nimber (xor of all rows): 

   def nimber( self ) :
      size = len(self.state)
      i = 0
      while self.state[i] == 0:
         i += 1
      a = self.state[i]
      for j in range(i+1, size, 1):
          if(self.state[j] == 0):
             continue
          a = a ^ self.state[j] #ignore 0s
      return a


   # Make a random move, raise a CantMove if
   # there is nothing left to remove. 

   def randommove( self ) :
       a = 0
       for i in self.state:
           if i == 0:
               a += 1
       if a == len(self.state):
           raise CantMove( "no sticks left" ) #check all the rows
       while True:
           row = random.randrange(0, len(self.state), 1 )
           if self.state[row] == 0:
                continue
           remove = random.randrange(1, self.state[row] + 1, 1 )
           break
       self.state[row] = self.state[row] - remove

   # Try to force a win with misere strategy.
   # This functions make a move, if there is exactly
   # one row that contains more than one stick.
   # In that case, it makes a move that will leave
   # an odd number of rows containing 1 stick.
   # This will eventually force the opponent to take the
   # last stick.
   # If it cannot obtain this state, it should raise
   # CantMove( "more than one row has more than one stick" )

   def removelastmorethantwo( self ) :
       j = 0
       i = 0
       for n in range(0, len(self.state), 1):
           if self.state[n] > 1:
              index = n
              i += 1
           if self.state[n] == 1:
              j += 1   # number of rows containing only one stick
       if(i == 1):
           if(j % 2 == 0):
              self.state[index] = 1
           else:
              self.state[index] = 0
       else :
           raise CantMove( "more than one row has more than one stick" )

   # Try to find a move that makes the nimber zero.
   # Raise CantMove( "nimber is already zero" ), if the
   # nimber is zero already.

   def makenimberzero( self ) :
      i = True
      if self.nimber() == 0 :
         raise CantMove( "nimber is already zero" )
      while i:
           row = random.randrange(0, len(self.state), 1 )
           r = self.state[row]
           if (r ^ self.nimber()) < r:
                self.state[row] = r ^ self.nimber()
                i = False
  
 
   def optimalmove( self ) :
      try:
         self.removelastmorethantwo()
      except CantMove:
          try:
             self.makenimberzero()
          except CantMove:
             self.randommove()

   # Let the user make a move. Make sure that the move
   # is correct. This function never crashes, not
   # even with the dumbest user in the world. 
           
   def usermove( self ) :
      print("Choose a row")
      i = True
      while i:
          try:
             a = int ( input() )
             if a < 1 or a > len(self.state):
                print("Write a correct input")
                continue
             if self.state[a-1] == 0:
                print ("Write a correct input" )
                continue
              
             i = False
          except ValueError:
             print("Write a correct input")
    
      print("Choose a number of sticks to leave")
      i = True
      while i:
         try:
            b = int(input())
            if b < 0 or b >= self.state[a-1]:
               print("Write a correct input")
               continue
            i = False
         except ValueError:
            print("Write a correct input")

      self.state[a-1] = b


def play( ) :
   st = Nim( [ 1, 2, 3, 4, 5, 6 ] )
   turn = 'user'
   while st. sum( ) > 1 :
      if turn == 'user' :
         print( "\n" )
         print( st )
         print( "hello, user, please make a move" )
         st. usermove( )
         turn = 'computer'
      else :
         print( "\n" )
         print( st )
         print( "now i will make a move\n" )
         print( "thinking" )
         for r in range( 15 ) :
            print( ".", end = "", flush = True )
            time. sleep( 0.1 )
         print( "\n" )
         st. optimalmove( )
         turn = 'user'
   print( "\n" )
   if turn == 'user' :
      print( "you lost\n" )
   else :
      print( "you won\n" )

#play()
