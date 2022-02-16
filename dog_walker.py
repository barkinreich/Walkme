# -------------------------------------------------------------------------------
# Registration for new dog walker
# -------------------------------------------------------------------------------
# this file contains one class objects: Dog walker, which helps us to manage the info to DB
# -------------------------------------------------------------------------
# Author:       Group 19
# Last updated: 13.1.2020
# -------------------------------------------------------------------------

# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
from dog_breed import DogBreed, DogBreedFinder

class Walker():
    def __init__(self):
        logging.info('Initializing Dog Walker')
        self.o_DbHandler = db_handler.DbHandler()
		# create data members of the class DogWalker
        self.registration_date = ""
        self.w_first_name = ""
        self.w_last_name = ""
        self.Walker_Email = ""
        self.w_phone = ""
        self.w_city = ""
        self.w_street = "" 
        self.w_house_number = ""
        self.w_daily_price = ""
        self.w_max_dogs = ""
        self.w_breed = ""
        self.w_days = ""
		# days_lst contains tuples of (day,owner mail)
        self.w_days_lst = []
		# breeds_lst contains tuples of (breed name,owner mail)
        self.w_breeds_lst = []
    
    def get_email(self) : 
        return self.Walker_Email
       
        
	# the method insert all the info after registration to DB
	def insertToDb(self):
		logging.info('In Walker.insertToDb')
		self.o_DbHandler.connectToDb()
		cursor = self.o_DbHandler.getCursor()

		query = """
				INSERT INTO Dog_Walker(Registration_date, First_Name, Last_Name, Walker_Email, Walker_Phone_Number, Street, City, House_Number)
				VALUES(sysdate(),%s,%s,%s,%s,%s,%s)
				"""
		cursor.execute(query,
						(self.w_first_name, self.w_last_name, self.w_mail, self.w_phone, self.w_street, self.w_city, self.w_house_number ))
		self.o_DbHandler.commit()	

		# change the format of breeds that given in form
		self.getBreedsInHtmlFormat()
				
		query1 = """
				INSERT INTO willing_to_take(Name_Of_Breed, Walker_Email)
				VALUES(%s,%s)
				"""
		for breed in self.w_breeds_lst:
			cursor.execute(query1,
							(breed))
		self.o_DbHandler.commit()

		# change the format of days that given in form
		self.getDaysInHtmlFormat()
				
		query2 = """
				INSERT INTO Avaibiliy(Name_Of_Day, Walker_Email)
				VALUES(%s,%s)
				"""
		for day in self.w_days_lst:
			cursor.execute(query2,
							(day))
		self.o_DbHandler.commit()		
		
		self.o_DbHandler.disconnectFromDb()
		return
		
	# the method checks if the dog owner exist in db
    def IsExist(self):
        logging.info('In DogWalker.IsExist')
        self.o_DbHandler.connectToDb()
        cursor = self.o_DbHandler.getCursor()
        query = """
        		SELECT *
				FROM Dog_Walker
				WHERE Walker_Email = %s
				"""
        cursor.execute(query,
					(self.Walker_Email,))
        NumberOfRows = int(cursor.rowcount)
        logging.info("Number of records " + str(NumberOfRows))
        self.o_DbHandler.disconnectFromDb()
        return NumberOfRows > 0		
	
	# the method changes the format of days that given in form
    def getDaysInHtmlFormat(self):
        new_days = ''
        temp = self.w_days
        for day in temp:
            new_days += str(day)
            new_days += ', '
            self.w_days_lst.append((str(day),str(self.w_mail)))
        self.w_days = new_days[:-2]
        return self.w_days
	
	# the method changes the format of breeds that given in form
    def getBreedsInHtmlFormat(self):
        new_breed = ''
        temp = self.w_breed
        for breed in temp:
            new_breed += str(breed)
            new_breed += ', '
            self.w_breeds_lst.append((str(breed),str(self.walker_Email)))
        self.w_breed = new_breed[:-2] #deleting the comma and space
        return self.w_breed