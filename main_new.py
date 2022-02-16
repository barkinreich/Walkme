# import webapp2  - Python web framework compatible with Google App Engine
import webapp2
# import the users library from google
import jinja2
import os
# import the users library from google
from google.appengine.api import users
# import logging so we can write messages to the log
import logging
import dog_owner_new
import dog_walker
from dog_breed import DogBreedFinder
import Customer_finder
import dog_trip


# import the class DogOwner

jinja_environment =jinja2.Environment(loader=
 jinja2.FileSystemLoader
(os.path.dirname(__file__)))

#####

class Home(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_environment.get_template('home.html')
        self.response.write(home_template.render().encode("utf-8"))
        logging.info('Currently in Home')
        
class dogowner(webapp2.RequestHandler):
    def get(self):
        logging.info('hello1')
        user = users.get_current_user()
        if not user:
            #if the user does not exist, redirect him to login to google 
            self.redirect(users.create_login_url('/dogowner'))
        else:
            logging.info('hello2')
            owner_user = dog_owner_new.Owner()
            owner_user.Owner_Email_Adress = users.get_current_user().email()
            if owner_user.IsExist():
                logging.info('The user exists')
                    #Display user_exist.html
                template = jinja_environment.get_template('user_exist.html')
                self.response.write(template.render())
                logging.info('the user exists')
            else:
                logging.info('Im here!!!!!')
				# the user dowsn't exist#
				# Display Dog owner registration form
                template = jinja_environment.get_template('dog_owner_input.html')
                self.response.write(template.render())
                logging.info('In dog_owner_input.html')
                

class dogwalker(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            logging.info('The user is not logged in.')
            # Redirectedirect the user to the login window
            self.redirect(users.create_login_url('/dogwalker'))
        else:
            # the user is logged in and check if the user already exists
            user_id = users.get_current_user().email()
            is_walker= dog_walker.Walker()
            is_walker.Walker_Email = user_id
            if is_walker.IsExist():
                # the user exists 
                logging.info('The walker already exists')
            else:
                # the user doesn't exist
                # Display Dog owner registration form
                template = jinja_environment.get_template('dog_walker_input.html')
                all_dog_breeds = DogBreedFinder().find_all()
                
                data = {'dog_breeds': all_dog_breeds,
                        'hello': user}
                
                self.response.write(template.render(data).encode("utf-8"))
                logging.info('Input Dog Walker Info')
                
                
class customers(webapp2.RequestHandler):
    def get(self):
        logging.info('In Customers Before Template')
        user = users.get_current_user()
        email = user.email()
        template = jinja_environment.get_template('customers.html')
        #if not working drop the things in find all and drop the thing in customer finder 
        all_his_customers = Customer_finder.CustomerFinder().find_all(email)
        data = {'customers' : all_his_customers }
        logging.info('collapsed here')
        self.response.write(template.render(data).encode("utf-8"))

class customerfinder(webapp2.RequestHandler):
    def post(self):
        customer_finder = Customer_finder.CustomerFinder()
        Owner_Email_Adress = users.get_current_user().email()
        Owner_Age = self.request.get('DogOwnerAge')
        owner_city = str(self.request.get('Filter_City'))
        match_results = customer_finder.MatchCustomer(Owner_Email_Adress, Owner_Age, owner_city)
        if len(match_results) > 0:
			# there are results
			template = jinja_environment.get_template('customer_filter_results.html')
			parameters_for_template = {	'new_customer_results': match_results}
			self.response.write(template.render(parameters_for_template))
            
        else:
            # there are no results
            # redirect to the no_walker_results.html
            template = jinja_environment.get_template('no_walker_results.html')
            self.response.write(template.render())
		
        
class NewTrip(webapp2.RequestHandler):
	def get(self):
		# When we receive an HTTP GET request - display the new trip the user chose 
		logging.info('NewTrip.get()')
		new_trip = dog_trip.Trip()
		# get parameters from query string
		new_trip.Dog_Id=self.request.get('dog_id')
		new_trip.Walker_Email=self.request.get('walker_choise')
		new_trip.Name_Of_Day=self.request.get('walker_day')
		# get owner mail
		new_trip.Owner_Email_Adress = users.get_current_user().email()		
		# check if the user exists
		Exist = new_trip.IsExist()
		if Exist:
			logging.info('Trip.Exist()')
		else:
			# insert trip to db
			new_trip.insertToDb()
			# get the new trip from db
			show_trips= new_trip.getNewTrip()
			logging.info('getNewTrip')
			# the template will use a show_trip.html file
			template = jinja_environment.get_template('show_trip.html')
			# define the parameters and their name
			# that we will send to the template
			parameters_for_template = {	'new_show_trips': show_trips }
			self.response.write(template.render(parameters_for_template)) 

class MyTrips(webapp2.RequestHandler):			
    # When we receive an HTTP GET request - display all the owner's trips 
	def get(self):
		logging.info('In MyTrips class')
		#Check if the user is logged in
		user = users.get_current_user()
		if not user:
			logging.info('The user object does not exist.')
			logging.info('The user is logged out.')
			# Redirectedirect the user to the login window
			# after login rediredt the user back to /mytrips
			self.redirect(users.create_login_url('/mytrips'))
		else:
			user_id = users.get_current_user().email()
			is_owner= dog_owner_new.Owner()
			is_owner.Owner_Email_Adress = user_id
			if is_owner.IsExist():
				logging.info('The user is a dog owner')
				trip_lst = is_owner.AllTrips()
				if len(trip_lst) > 0:
					#Displat trip results
					template = jinja_environment.get_template('all_trips.html')
					# define the parameters that we will send to the template
					parameters_for_template = {	'new_trips_lst': trip_lst }
					self.response.write(template.render(parameters_for_template))
					logging.info('all_trips.html')
				else:
					# the user has no trips
					template = jinja_environment.get_template('no_trips.html')
					self.response.write(template.render())
					logging.info('no_trips.html')				
			else:
				# The user is not a dog owner
				template = jinja_environment.get_template('not_dog_owner.html')
				self.response.write(template.render())
				logging.info('In not_dog_owner.html')
    
    
class Logout(webapp2.RequestHandler):
    def get(self):
		logging.info('In Logout.get()')
		# if the user is logged in - we will perform log out
		user = users.get_current_user()

		if user:
			logging.info('The user is logged in - performing logout ')

			# force the user to logout and redirect him afterward to 
			# show_status page, to display the status afterwards
			self.redirect(users.create_logout_url('/logout'))

		else:
			template = jinja_environment.get_template('logout.html')
			self.response.write(template.render())
			logging.info('user is now not logged in ')
			logging.info('The user is logged out. There is nothing to do')
			logging.info('Redirecting to /') 
        
app = webapp2.WSGIApplication([('/', Home),
                               ('/dogwalker', dogwalker),
                               ('/customers' , customers),
                               ('/customersfilter', customerfinder),
                               ('/show_trips', NewTrip),
                               ('/mytrips', MyTrips),
                               ('/logout', Logout)
                               ],debug=True)
				

            
            
            
            
            
            
            
        
    