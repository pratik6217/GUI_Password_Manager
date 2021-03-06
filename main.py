import streamlit as st
import pymongo
from cryptography.fernet import Fernet
import random
import string
import smtplib, ssl
import SessionState
import pyperclip

PAGE_CONFIG = {"page_title" : "PassVault",'page_icon': './download.png', "layout" : "centered"}
st.set_page_config(**PAGE_CONFIG)

#from multiapp import Multiapp

# Global Variables for Dashboard
logged_in = False
logged_in_user = ""

#Dashboard Session state for user
#session_state_user = SessionState.get(name= "", button_sent = False)


#key = Fernet.generate_key()
#with open("key.key", "w") as file:
#	file.write(key.decode())

with open('key.key', 'r') as file:
	key = file.read()

f = Fernet(key.encode())

with open("MongoDb.key", 'r') as file:
	mongo_key = f.decrypt(file.read().encode()).decode()

# Creating a MongoDb Client

client = pymongo.MongoClient('mongodb+srv://admin:{mongo_key}@password-manager.bl1uj.mongodb.net/Password_manager?retryWrites=true&w=majority'.format(mongo_key = mongo_key))
db = client['Password_manager']
cursor = db['Login']


with open('password.key', 'w') as file:
	file.write(f.encrypt('givvpboplvahgqvs'.encode()).decode())

def send_mail(mail):
	context = ssl.create_default_context()
	port = 465
	email = "passvault6217@gmail.com"
	with open("password.key", "r") as file:
		password = f.decrypt(file.read().encode()).decode()
	
	message = """\
Subject: Registration Succesfull.

This message is to inform you that you have successfully registered with our services.

Thankyou for choosing us :)"""
	receiver = mail
	try:
		server = smtplib.SMTP_SSL("smtp.gmail.com", port, context = context)
		server.ehlo()
   		#server.starttls(context = context)
		
		server.login(email, password)
		server.ehlo()

		server.sendmail(email, receiver, message)
	except Exception as e:
		st.error(e)
	finally:
		server.quit()


def random_password_generator():
	# Session state for multi buttons inside Streamlit
	session_state = SessionState.get(name= '',user_name = '', button_sent1 = False, button_sent= False, insert = False, update = False, view = False, delete = False, new = False, logout =False, logout_count = 0, is_logged_in = False, home = True)

	st.title("Random Password Generator")
	st.subheader("Please select an option:")

	ch1 = st.beta_columns(2)
	choice1 = ch1[0].button("Mixed - Upper, Lower, Digits(Most Secure)")
	
	ch2 = st.beta_columns(2)
	choice2 = ch2[0].button("Lowercase") 
	
	ch3 = st.beta_columns(2)
	choice3 = ch3[0].button("Uppercase")
	

	if choice1:
		session_state.name = 'choice1'
		session_state.button_sent1 = True
	elif choice2:
		session_state.name = 'choice2'
		session_state.button_sent1 = True
	elif choice3:
		session_state.name = 'choice3'
		session_state.button_sent1 = True


	if session_state.name == 'choice1' and session_state.button_sent1:
		password = ''
		l = st.beta_columns(2)	
		length = l[0].number_input("Length of the password:")
		s = st.beta_columns(2)
		submit = s[0].button("submit")

		if submit:
			if length < 0:
				st.warning("Please enter a positive number !!")
			elif length < 5:
				st.warning("Please select the length to be >= 5 for a secure password !!")
			elif length >= 5:
				for i in range(int(length)):
					password += random.choice([random.choice(string.ascii_lowercase), random.choice(string.ascii_uppercase), random.choice(string.digits)])
 
				st.text("The generated password is {}".format(password))
				#pyperclip.copy(password)
				st.info("The Password has been copied to your clipboard !!")

	elif session_state.name == 'choice2' and session_state.button_sent1:
		password = ''
		l = st.beta_columns(2)	
		length = l[0].number_input("Length of the password:")
		s = st.beta_columns(2)
		submit = s[0].button("submit")

		if submit:
			if length < 0:
				st.warning("Please enter a positive number !!")
			elif length < 5:
				st.warning("Please select the length to be >= 5 for a secure password !!")
			elif length >= 5:
				for i in range(int(length)):
					password += random.choice([random.choice(string.ascii_lowercase)])
				st.text("The generated password is {}".format(password))
				#pyperclip.copy(password)
				st.info("The Password has been copied to your clipboard !!")


	elif session_state.name == 'choice3' and session_state.button_sent1:
		password = ''
		l = st.beta_columns(2)	
		length = l[0].number_input("Length of the password:")
		s = st.beta_columns(2)
		submit = s[0].button("submit")

		if submit:
			if length < 0:
				st.warning("Please enter a positive number !!")
			elif length < 5:
				st.warning("Please select the length to be >= 5 for a secure password !!")
			elif length >= 5:
				for i in range(int(length)):
					password += random.choice([random.choice(string.ascii_uppercase)])
				st.text("The generated password is {}".format(password))
				#pyperclip.copy(password)
				st.info("The Password has been copied to your clipboard !!")




def login():
	global logged_in
	global logged_in_user
	

	st.title("Login")
	st.subheader("Please enter your details:")

	u_name = st.beta_columns(2)
	username = u_name[0].text_input("Username:")

	passs = st.beta_columns(2)
	password = passs[0].text_input("Password:",type = 'password')

	submit = st.beta_columns(2)
	choice = submit[0].button("Login")


	if choice:
		session_state_user.user_name = username
		session_state_user.sent_button = True
		session_state_user.logout_count = 0

		db_user = cursor.find_one({'username': username})
		if db_user == None:
			st.error('This user does not exists. Please register first !!')
		else:
			if f.decrypt(db_user['password']).decode() != password:
				st.error("Please enter the correct password !!")
			else:
				st.success("Logged in successfully.")
				logged_in = True
				logged_in_user = username
				session_state_user.user_name = username
				session_state_user.button_sent = True


	if session_state_user.button_sent:
		session_state_user.is_logged_in = True
		st.button('Go to My Dashboard -->')

	#Pointer for MongoDb for this user

def dashboard():
	menu = ['Password Vault', 'Random Password Generator']
	user_choice = st.sidebar.selectbox('Menu', menu)
	username = session_state_user.user_name
	st.sidebar.subheader('Tips to keep your accounts safe: ')
	st.sidebar.write('1. Never reveal your passwords to others.')
	st.sidebar.write('2. Use different passwords for different accounts.')
	st.sidebar.write('3. Use multi-factor authentication (MFA).')
	# st.sidebar.write('4. Length trumps complexity.')
	st.sidebar.write('5. Make passwords that are hard to guess but easy to remember.')
	st.sidebar.image('./dash.jpg')
	if user_choice == 'Password Vault':
	
		st.title("Welcome to your Dashboard, {}.".format(username))
		st.subheader("Please Choose one of the following:")

		ch1 = st.beta_columns(2)
		insert = ch1[0].button("Add a new Entry")

		ch1 = st.beta_columns(2)
		update = ch1[0].button("Update Existing Entry") 

		ch1 = st.beta_columns(2)
		view = ch1[0].button("View Saved Passwords") 

		ch1 = st.beta_columns(2)
		delete = ch1[0].button("Delete Entry")

		log = st.beta_columns(2)
		logout = log[0].button("Logout")

		if insert:
			session_state_user.button_sent = True
			session_state_user.insert = True
			session_state_user.view = False
			session_state_user.update = False
			session_state_user.delete = False

		if update:
			session_state_user.button_sent = True
			session_state_user.update = True
			session_state_user.insert = False
			session_state_user.view = False
			session_state_user.delete = False

		elif view:
			session_state_user.button_sent = True
			session_state_user.view = True
			session_state_user.insert = False
			session_state_user.update = False
			session_state_user.delete = False

		elif delete:
			session_state_user.button_sent = True
			session_state_user.delete = True
			session_state_user.insert = False
			session_state_user.update = False
			session_state_user.view = False

		elif logout:
			session_state_user.logout = True
			session_state_user.button_sent = False
			session_state_user.delete = False
			session_state_user.insert = False
			session_state_user.update = False
			session_state_user.view = False


		if session_state_user.insert:

			st.title("Insert")
			st.subheader("Enter the Details:")

			org = st.beta_columns(2)
			organization = org[0].text_input("Organizations Name:")
			password = org[1].text_input("Enter Password:", type = 'password')
			session_state_user.organization_name = organization

			s = st.beta_columns(2)
			i = s[0].button("Insert")

			if i:
				pointer = db[session_state_user.user_name]
				if pointer.find_one({'Organization': organization}):
					st.error("This Organization already exists !!")
				elif len(password) < 5:
					st.warning('Please create a stronger Password !!')
				else:
					try:
						pointer.insert_one({
						'Organization' : organization,
						'Password' : f.encrypt(password.encode())
						})

					except Exception as e:
						st.error(e)
					
					else:
						st.success("Records added Successfully !!")

		if session_state_user.update:
			pointer = db[session_state_user.user_name]
			st.title("Update Existing records")
			records = pointer.find({})
			leng = list(records)
		
			if len(leng) == 0:
				session_state_user.update = True
				st.info("It's Empty in here.\nPlease save records first !!")
			elif len(leng) > 0:
				for documents in leng:
					d = st.beta_columns(2)
					d[0].text_input('Organization: ', documents['Organization'], key= documents['Organization'])
					d[1].text_input('Password', f.decrypt(documents['Password']).decode(), type = 'password', key= documents['Password'])
					# st.text('Organization: {o} \nPassword: {p}'.format(o = documents['Organization'], p = f.decrypt(documents['Password']).decode()))
				
				st.write(' ')
				st.subheader('Enter New Credentials to update:')
				org = st.beta_columns(2)
				organization = org[0].text_input("Organizations Name:")
				password = org[1].text_input("Enter New Password:", type = 'password')
				session_state_user.organization_name = organization
				s = st.beta_columns(6)
				s[1].button('refresh')
				if s[0].button("update"):
					find = pointer.find_one({'Organization' : organization})
					if find:
						if len(password) < 5:
							st.warning('Please create a stronger Password !!')
						else:
							old = {'Organization' : find['Organization'],
								'Password' : find['Password']}
							if f.decrypt(old['Password']).decode() == password:
								st.warning('Old and New Passwords cannot be same !!')
							else:
								try:
									new = {'$set' : {'Organization' : organization, 'Password' : f.encrypt(password.encode())}}
									pointer.update_one(old, new)
								except Exception as e:
									st.error(e)
								else:
									st.success("Details Updated Succesfully !!")
					else:
						st.error("No such record exists !!")

		if session_state_user.view:
			pointer = db[session_state_user.user_name]
			st.title("View Saved Passwords")
			records = pointer.find({})
			leng = list(records)
			if len(leng) == 0:
				st.info("It's Empty in here.\nPlease save records first !!")
			elif len(leng) > 0:
				for documents in leng:
					d = st.beta_columns(2)
					d[0].text_input('Organization: ', documents['Organization'], key= documents['Organization'])
					d[1].text_input('Password', f.decrypt(documents['Password']).decode(), type = 'password', key= documents['Password'])
					# st.text('Organization: {o} \nPassword: {p}'.format(o = documents['Organization'], p = f.decrypt(documents['Password']).decode()))

		if session_state_user.delete:
			pointer = db[session_state_user.user_name]
			st.title("Delete Existing records")
			records = pointer.find({})
			leng = list(records)
			l = []
			if len(leng) == 0:
				st.info("It's Empty in here.\nPlease save records first !!")
			elif len(leng) > 0:
				for documents in leng:
					l.append(documents['Organization'])
				selection = st.radio('Organizations', l)
				# st.text('Organization: {o} \nPassword: {p}'.format(o = documents['Organization'], p = f.decrypt(documents['Password']).decode()))
				print(selection)
				org = st.beta_columns(2)
				organization = org[0].text_input("Organization Selected to delete:", selection)
				session_state_user.organization_name = organization
				s = st.beta_columns(6)
				s[1].button('refresh')
				if s[0].button("delete"):
					if pointer.find_one({'Organization' : selection}):
						pointer.delete_one({
							'Organization' : selection,
							})
						st.success("Details Deleted Succesfully !!")
					else:
						st.error("No Such Record Exists !!")

		if session_state_user.logout and session_state_user.button_sent == False:
			if session_state_user.logout_count == 0:
				session_state_user.option = ' '
				session_state_user.is_logged_in = False
				st.info("Please click logout once again to logout !!")
				session_state_user.logout_count += 1
			else:
				st.info("You have succsessfully logged out !!")

	elif user_choice == 'Random Password Generator':
		random_password_generator()

def register():
# Page Title
	st.title("Register")
	st.subheader("Please enter your details:")

#Creating Containers for First and last names.
	first_name, last_name = st.beta_columns(2)
	name = first_name.text_input("First Name:")
	surname = last_name.text_input("Last Name:")

	e = st.beta_columns(1)
	email = e[0].text_input("Email:")

	u, ph = st.beta_columns(2)
	username = u.text_input("Username:")
	phone = ph.text_input("Phone:")
  

	p1, p2 = st.beta_columns(2)
	password1 = p1.text_input("Password:", type = 'password')
	password2 = p2.text_input("Re-enter Password:", type = 'password')

	space = st.beta_columns(3)
	agree = space[0].checkbox("I agree")
	submit = space[2].button("submit")

	if submit:
		if name == '':
			st.warning('Name cannot be blank !!')
		elif password1 == '':
			st.error('Passwords cannot be empty !!')
		elif email == '':
			st.warning('Email cannot be empty !!')
		elif username == '':
			st.warning('Username cannot be blank !!') 
		elif phone == '':
			st.warning('Phone field cannot be blank !!')
		elif agree:
			if len(password1) < 5:
				st.warning('Please enter a stronger Password !!')
			elif password1 == password2:
				exists = cursor.find_one({'username': username})
				if exists:
					st.error("This username already exists !!")
				else:
					db_insert = cursor.insert_one({
					'name': name + ' ' + surname,
					'username': username,
					'password': f.encrypt(password1.encode()),
					'email': email,
					'phone': int(phone),
					})

					if db_insert:
						try:
							send_mail(email)
						except Exception as e:
							st.error(e)

						st.success("Succesfully Registered.")
					else:
						st.error('Something went wrong !!')

			else:
				st.error("The two passwords did not match !!")
		else:
			st.warning("Please select the 'agree' checkbox !!")



session_state_user = SessionState.get(option = '', name = '', user_name = '', button_sent1 = False, button_sent = False, insert = False, update = False, view = False, delete = False, new = False, logout =False, logout_count = 0, home = True, is_logged_in = False)

if session_state_user.is_logged_in == False:
	menu = ['Home', 'Login', 'Register']
	session_state_user.option = st.sidebar.selectbox("Menu", menu)
	st.sidebar.subheader('Tips to keep your accounts safe: ')
	st.sidebar.write('1. Never reveal your passwords to others.')
	st.sidebar.write('2. Use different passwords for different accounts.')
	st.sidebar.write('3. Use multi-factor authentication (MFA).')
	# st.sidebar.write('4. Length trumps complexity.')
	st.sidebar.write('5. Make passwords that are hard to guess but easy to remember.')
	st.sidebar.image('./dash.jpg')
	
if session_state_user.option == 'Home':
	st.title("Welcome to our Password Manager.")
	st.subheader('''
	PUT PASSWORDS IN THEIR PLACE
	We'll Take Care Of Them For You ! ''')
	st.write(" ")
	st.write(" ")
	st.write('''THE PASSWORD MANAGER, PERFECTED
	Keep track of all your passwords, whether you use them once a day or once a year.

	Have them ready when you need them and instantly typed for you.''')

	st.write(" ")
	st.write(" ")
	st.subheader('What is a password manager?')
	st.write("A password manager securely keeps track of all your passwords.")	
	st.write("It's the only way to create unique passwords for all your accounts, remember them, and have them typed for you online.")
	st.write(" ")
	st.write(" ")
	st.subheader('Have your passwords, wherever you go.')
	st.write('Dashlane backs up your passwords and keeps them up to date across your phone, computer or tablet.')
	st.write("")
	st.write("")
	st.image('download.svg', width = None)
	st.write("")
	st.write("")
	st.title("Don't wait. Get started today.")
	st.write("")
	place = st.beta_columns(2)
	st.write("For any Problem or Queries You can contact us at: passvault6217@gmail.com")


if session_state_user.is_logged_in:
	dashboard()

if session_state_user.option == "Login" and session_state_user.is_logged_in == False:
	session_state_user.home = False
	login()
elif session_state_user.option == "Register" and session_state_user.is_logged_in == False:
	session_state_user.home = False
	register()
# elif session_state_user.option == "Random Password Generator":
	# random_password_generator()
#app = Multiapp()

#app.add("Home", home)
#app.add("Login", login)
#app.add("Register", register)
#app.add("Random Password Generator", random_password_generator)

#app.run()


