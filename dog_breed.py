# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 18:16:10 2020

@author: shirl
"""

import db_handler
import logging

class DogBreed():
    def __init__(self):
        self.Name_Of_Breed = ""
        self.Avg_Height = 0.0
        self.Avg_Weight = 0.0
    
    def name(self):
        return self.Name_Of_Breed

class DogBreedFinder():        
    def __init__(self):
        self.db_handler = db_handler.DbHandler()
                    
    def find_all(self):
        self.db_handler.connectToDb()
        cursor = self.db_handler.getCursor()
        query = "SELECT Name_Of_Breed, Avg_Height, Avg_Weight FROM Dog_Breed"
        cursor.execute(query)
        rows = cursor.fetchall()
        ##me
        cursor.close()
        all_dog_breeds = []
        
        for breed_record in rows:
            breed = DogBreed()
            breed.Name_Of_Breed = breed_record[0]
            breed.Avg_Height = breed_record[1]
            breed.Avg_Weight = breed_record[2]
            all_dog_breeds.append(breed)
        
        self.db_handler.disconnectFromDb()
        return all_dog_breeds
