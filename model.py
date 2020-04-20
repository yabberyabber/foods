#!/usr/bin/env python3

import json
from pprint import pprint
import sys
from collections import defaultdict

def train_model( dataset ):
   recipe_count = len( dataset )
   ingredient_count = defaultdict( lambda: 0 )
   cuisine_count = defaultdict( lambda: 0 )
   ingredient_by_cuisine = defaultdict( lambda: defaultdict( lambda: 0 ) )


   for recipe in dataset:
      cuisine = recipe[ 'cuisine' ]
      cuisine_count[ cuisine ] += 1
      for ingredient in recipe[ 'ingredients' ]:
         ingredient_count[ ingredient ] += 1
         ingredient_by_cuisine[ cuisine ][ ingredient ] += 1

   P_cuisine = {
         cuisine: count / recipe_count
         for cuisine, count
         in cuisine_count.items()
   }

   P_ingredient = {
         ingredient: count / recipe_count
         for ingredient, count
         in ingredient_count.items()
   }

   P_ingredient_given_cuisine = {
         cuisine: {
            ingredient: count / cuisine_count[ cuisine ]
            for ingredient, count
            in ingredient_count.items()
         }
         for cuisine, ingredient_count
         in ingredient_by_cuisine.items()
   }

   def P_cuisine_given_ingredient( ingredient, cuisine ):
      # P( cuisine | ingredient ) = P( ingredient | cuisine ) * P( cuisine ) / P( ingredient )
      probability = (
            P_ingredient_given_cuisine[ cuisine ].get( ingredient, 0 ) * P_cuisine[ cuisine ]
            / P_ingredient.get( ingredient, 1 )
      )
      # print( 'looking up {} in {}... {}'.format(
      #          ingredient, P_ingredient.get( ingredient ), probability ) )
      return probability

   def P_cuisine_distribution( ingredients ):
      # P( cuisine | ingredients ) = 
      return {
         cuisine: product( [
            P_cuisine_given_ingredient( ingredient, cuisine )
            for ingredient
            in ingredients
         ] ) * P_cuisine[ cuisine ]
         for cuisine
         in cuisine_count.keys()
      }

   return P_cuisine_distribution

def product( lst ):
   result = 1.0
   for l in lst:
      result *= l
   return result

def renderize( probability_distribution, percent=True ):
   items = probability_distribution.items()
   items = sorted( items, key=lambda x: x[ 1 ] )

   for thing, probability in items:
      if percent:
         print( "{0: <16}: {1:02.2f}%".format( thing, probability * 100 ) )
      else:
         print( "{0: <16}: {1}".format( thing, probability ) )

def main( recipe ):
   with open( 'dataset/train.json' ) as f:
      dataset = json.load( f )
   
   model = train_model( dataset )

   renderize( model( recipe ) )

if __name__ == '__main__':
   main( sys.argv[ 1: ] )
