# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 21:44:21 2020

@author: user
"""

# -------------------------------------------------------------------------------
# A class to find a dog walker according to the user input
# -------------------------------------------------------------------------
# Author:       Bar Kinreich, Shirli Motro, Katrina 
# Last updated: 13.01.2020
# -------------------------------------------------------------------------

# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
# import dog_walker class
import dog_walker


class DogWalkerFinder():
	def __init__(self):
		logging.info('Initializing DogWalkerFinder')
		self.dw_DbHandler = db_handler.DbHandler()

		# create data members of the class DogWalkerFinder
		self.dw_DogWalkersList = []
		# the user's choises
		self.dog_name = ""
		self.dog_breed = ""
		self.owner_mail = ""
		self.dog_id = ""
		self.dw_days =  ""
		# insert defult values to filters
		self.max_rate = 9999
		self.owner_city = ['Tel-Aviv', 'Haifa', 'Ramat Efal', 'Jerusalem', 'Yahud', 'Herzliya', 'Eilat']
		# days_lst gets days in html format
		self.dw_days_lst = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
		# walker_finder_results list
		self.walker_finder_results = []

# -------------------------------------------------------------
# The method uses sql query to get all availble walkers
# -------------------------------------------------------------
	def getAllDogWalkers(self):
		logging.info('In DogWalkerFinder.getAllDogWalkers')
		self.dw_DbHandler.connectToDb()
		cursor = self.dw_DbHandler.getCursor()
		sql = """
				select dw_first_name, dw_last_name, dw.dw_email, dw_phone_number, dw_city_of_residence, dw_daily_price, b_name, day
				from work_days as wds join dog_walker as dw on wds.dw_email=dw.dw_email join  willing_to_take as wtt on dw.dw_email = wtt.dw_email
				where max_dogs > (select count(d_id)
				from walking_days as wd join dog_walker as dw1 on wd.dw_email=dw1.dw_email
				where dw1.dw_email=dw.dw_email and wds.day=wd.day)
				"""
		cursor.execute(sql)
		walkers_lst = cursor.fetchall()
		# insert the results to a walker list consist of walker objects
		for walker in walkers_lst: 
			walker_record = dog_walker.Walker()
			walker_record.w_first_name = walker[0]
			walker_record.w_last_name = walker[1]
			walker_record.w_mail = walker[2]
			walker_record.w_phone = walker[3]
			walker_record.w_city = walker[4]
			walker_record.w_daily_price = walker[5]
			walker_record.w_breed = walker[6]
			walker_record.w_days = walker[7]
			self.dw_DogWalkersList.append(walker_record)

		self.dw_DbHandler.commit()
		cursor.close()
		self.dw_DbHandler.disconnectFromDb()
		return self.dw_DogWalkersList

	# change the days from html format 
	def getDaysInHtmlFormat(self):
		self.dw_days_lst = []
		new_days = ''
		temp = self.dw_days
		for day in temp:
			new_days += str(day)
			new_days += ', '
			self.dw_days_lst.append(str(day))
		self.dw_days = new_days[:-2]
		return self.dw_days

# -------------------------------------------------------------
# The method uses sql query to get the walkers according to the user filters
# -------------------------------------------------------------
	def WalkerMatch(self):
		logging.info('In DogWalkerFinder.WalkerMatch')
		self.dw_DbHandler.connectToDb()
		cursor = self.dw_DbHandler.getCursor()
		query = """
				select dw.dw_email, dw_first_name, dw_last_name, dw_phone_number, dw_city_of_residence, dw_daily_price, day, b_name
				from work_days as wds join dog_walker as dw on wds.dw_email=dw.dw_email join  willing_to_take as wtt on dw.dw_email = wtt.dw_email
				where max_dogs > (select count(d_id)
									from walking_days as wd join dog_walker as dw1 on wd.dw_email=dw1.dw_email
									where dw1.dw_email=dw.dw_email and wds.day=wd.day) and wds.day=%s and dw.dw_daily_price<=%s and dw.dw_city_of_residence=%s
				"""
		# run on all the days the user chose
		for day in self.dw_days_lst:
			# run on all the citys the user chose
			for city in self.owner_city:
				cursor.execute(query,
							(day, self.max_rate, city))
				# check if there are results 
				# if there are results- insert into a walker object list 
				NumberOfRows = int(cursor.rowcount)
				if NumberOfRows > 0:
					matching = cursor.fetchall()
					for m in matching:
						walker = dog_walker.Walker()
						walker.w_mail = m[0]
						walker.w_first_name = m[1]
						walker.w_last_name = m[2]
						walker.w_phone = m[3]
						walker.w_city = m[4]
						walker.w_daily_price = m[5]
						walker.w_days = m[6]
						walker.w_breed = m[7]
						self.walker_finder_results.append(walker)
		self.dw_DbHandler.disconnectFromDb()
		return self.walker_finder_results
		
	# get owner city according to the owner mail
	def getOwnerCity(self):
		logging.info('In DogWalkerFinder.getOwnerCity')
		self.dw_DbHandler.connectToDb()
		cursor = self.dw_DbHandler.getCursor()
		query = """
				select  o_city_of_residence
				from dog_owner_regular
				where or_email = %s
				"""
		cursor.execute(query,
						(self.owner_mail,))
		city = cursor.fetchone()
		self.owner_city = [city[0]]
		self.dw_DbHandler.commit()
		self.dw_DbHandler.disconnectFromDb()
		return
	
	# get dog id according to dog name and owner mail
	def getDogId(self):
		logging.info('In DogWalkerFinder.getOwnerCity')
		self.dw_DbHandler.connectToDb()
		cursor = self.dw_DbHandler.getCursor()
		query = """
				select d_id
				from dogs
				where d_name = %s and or_email = %s
				"""
		cursor.execute(query,
						(self.dog_name, self.owner_mail))
		id = cursor.fetchone()
		self.dog_id = id[0]
		self.dw_DbHandler.commit()
		self.dw_DbHandler.disconnectFromDb()
		return
	