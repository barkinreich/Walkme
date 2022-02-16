# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 10:24:24 2020

@author: shirl
"""

import db_handler
import logging 
#costumer finder
import dog_walker 
import dog_owner_new
from google.appengine.api import users


class Customer():
    def __init__(self):
        self.customer_first_name = ""
        self.customer_last_name = ""
        self.customer_dog_name = ""
        self.birth_date = ""
        
    def name(self):
        return self.O_First_name ,self.O_Last_name

class CustomerFinder():        
    def __init__(self):
        self.db_handler = db_handler.DbHandler()
        self.owner_city = ['Tel-Aviv', 'Haifa', 'Ramat Efal', 'Jerusalem', 'Yahud', 'Herzliya', 'Eilat']
		# walker_finder_results list
        self.customer_finder_results = []
                    
    def find_all(self, email):
        logging.info('find all')
        self.db_handler.connectToDb()
        cursor = self.db_handler.getCursor()
        query = """
                select O_First_Name, O_Last_Name, Dog_Name, O_Birth_Date
                from Trips inner join Dogs on Trips.Dog_Id= Dogs.Dog_Id inner join Dog_Owner on Dogs.Owner_Email_adress = Dog_Owner.Owner_Email_Adress
                where Trips.Walker_Email = %s;
                """
        cursor.execute(query,(email,))
        rows = cursor.fetchall()
        #mme
        cursor.close()
        all_his_customers = []
        
        for customer_record in rows:
            customer = Customer()
            customer.customer_first_name = customer_record[0]
            customer.customer_last_name = customer_record[1]
            customer.customer_dog_name = customer_record[2]
            all_his_customers.append(customer)
        
        self.db_handler.disconnectFromDb()
        return all_his_customers
    
    def MatchCustomer(self, Email, Age, City):
        logging.info('Matching A Customer')
        self.db_handler.connectToDb()
        cursor = self.db_handler.getCursor()
        query = """
				SELECT Dog_Owner.O_First_Name, Dog_Owner.O_Last_Name, Dog_Owner.O_Phone_Number, O_City, Dog_Owner.Owner_Email_Adress, FLOOR(TIMESTAMPDIFF(day, Dog_Owner.O_Birth_Date , now())/365.242199) as Age
                From Dog_Owner JOIN Dogs ON Dog_Owner.Owner_Email_Adress = Dogs.Owner_Email_Adress JOIN Trips On Dogs.Dog_Id = Trips.Dog_Id
                Where Walker_Email = %s and FLOOR(TIMESTAMPDIFF(day, Dog_Owner.O_Birth_Date , now())/365.242199) IN (Select FLOOR(TIMESTAMPDIFF(day, d1.O_Birth_Date , now())/365.242199) as NewAge From Dog_Owner as d1
                               Where FLOOR(TIMESTAMPDIFF(day, d1.O_Birth_Date , now())/365.242199) = %s and O_City In (SELECT O_City From Dog_Owner as d2 
                            Where d2.O_City = %s))
                Group By Owner_Email_Adress, O_City, Age;

                """
        cursor.execute(query, (Email, Age, City))
        NumberOfRows = int(cursor.rowcount)
        if NumberOfRows > 0:
            matching = cursor.fetchall()
            for m in matching:
                customer = dog_owner_new.Owner()
                customer.O_First_Name = m[0]
                customer.O_Last_Name = m[1]
                customer.O_Phone_Number = m[2]
                customer.O_City = m[3]
                self.customer_finder_results.append(customer)
		self.db_handler.disconnectFromDb()
		return self.customer_finder_results
        
        
    
    
