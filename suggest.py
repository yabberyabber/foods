#!/usr/bin/env python3

import json
import sys
from pprint import pprint
from collections import defaultdict
from model import renderize

def train_model( dataset ):
   ingredient_by_ingredient = defaultdict( lambda: defaultdict( lambda: 0 ) )
   ingredient_count = defaultdict( lambda: 0 )

   for recipe in dataset:
      for ingredientA in recipe[ 'ingredients' ]:
         ingredient_count[ ingredientA ] += 1
         for ingredientB in recipe[ 'ingredients' ]:
            ingredient_by_ingredient[ ingredientA ][ ingredientB ] += 1

   P_ingredient = {
      ingredient: count / len( dataset )
      for ingredient, count
      in ingredient_count.items()
   }

   P_ingredient_co_occurance = {
      ingredientA: {
         ingredientB: count / ingredient_count[ ingredientA ]
         for ingredientB, count
         in co_occurances.items()
      }
      for ingredientA, co_occurances
      in ingredient_by_ingredient.items()
   }

   def what_else( ingredients ):
      # P( co_ing | ing ) = P( ing | co_ing )
      scores = defaultdict( lambda: 0 )

      for ingredient in ingredients:
         for co_ingredient, co_occurance_chance in P_ingredient_co_occurance.get( ingredient, {} ).items():
            scores[ co_ingredient ] += co_occurance_chance * P_ingredient[ ingredient ]

      return scores

   return what_else



def main( ingredients ):
   with open( 'dataset/train.json' ) as f:
      dataset = json.load( f )
   with open( 'dataset/test.json' ) as f:
      dataset += json.load( f )

   model = train_model( dataset )

   renderize( model( ingredients ), percent=False )

if __name__ == '__main__':
   if len( sys.argv ) < 2:
      print( 'Usage: {} INGREDIENT [INGREDIENT... ]'.format( sys.argv[ 0 ] ) )
      print( 'Suggests ingredients that commonly co-occur with the ingredients provided. Ingredients are ranked based on the number of times they co-occur with the given ingredients.' )
      print( 'Provided ingredients will occur in the suggestions. If a provided ingredient scores low, that probably means it has no business being in your meal :)' )
      sys.exit( 2 )
   main( sys.argv[ 1: ] )
