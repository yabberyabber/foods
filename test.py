#!/usr/bin/env python3

import json
from pprint import pprint
from model import train_model
from collections import namedtuple

def split_dataset( dataset, i, mod ):
   test = []
   train = []

   for idx, value in enumerate( dataset ):
      if idx % mod == i:
         train.append( value )
      else:
         test.append( value )

   return test, train

def highest_P( distribution ):
   return sorted( distribution.items(), key=lambda x: -x[ 1 ] )[ 0 ][ 0 ]

def validate( tests, model ):
   right, wrong = 0, 0

   for test in tests:
      cuisine = highest_P( model( test[ 'ingredients' ] ) )
      if cuisine == test[ 'cuisine' ]:
         right += 1
      else:
         wrong += 1

   return ModelStats( right, wrong )
ModelStats = namedtuple( 'ModelStats', [ 'right', 'wrong' ] )

def main():
   with open( 'dataset/train.json' ) as f:
      dataset = json.load( f )

   for i in range( 10 ):
      test_dataset, train_dataset = split_dataset( dataset, i, 10 )

      model = train_model( train_dataset )

      stats = validate( test_dataset, model )

      print( '\nValidatoin cross {}:'.format( i ) )
      pprint( stats )
      print( 'Percentage: {}'.format( stats.right * 100.0 / ( stats.right + stats.wrong ) ) )

if __name__ == '__main__':
   main()
