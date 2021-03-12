import streamlit as st
import pymongo
from cryptography.fernet import Fernet
import random
import string
import smtplib, ssl
import SessionState
import pyperclip

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

# Creating a MongoDb Client

client = pymongo.MongoClient('mongodb+srv://admin:admin@password-manager.bl1uj.mongodb.net/Password_manager?retryWrites=true&w=majority')
db = client['Password_manager']
cursor = db['Login']



def send_mail(mail):
	context = ssl.create_default_context()
	port = 465
	email = "passvault6217@gmail.com"
	with open("password.key", "r") as file:
		password = file.read()
	
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
	session_state = SessionState.get(name='', button_sent = False)

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
		session_state.button1 = True
	elif choice2:
		session_state.name = 'choice2'
		session_state.button2 = True
	elif choice3:
		session_state.name = 'choice3'
		session_state.button_sent = True


	if session_state.name == 'choice1' and session_state.button_sent:
		password = ''

		l = st.beta_columns(2)	
		length = l[0].number_input("Length of the password:")

		s = st.beta_columns(2)
		submit = s[0].button("submit")

		if submit:
			for i in range(int(length)):
				password += random.choice([random.choice(string.ascii_lowercase), random.choice(string.ascii_uppercase), random.choice(string.digits)])
 
			st.text("The generated password is {}".format(password))
			pyperclip.copy(password)
			st.info("The Password has been copied to your clipboard !!")

	elif session_state.name == 'choice2' and session_state.button_sent:
		password = ''
		l = st.beta_columns(2)	
		length = l[0].number_input("Length of the password:")
		for i in range(int(length)):
			password += random.choice([random.choice(string.ascii_lowercase)])

		s = st.beta_columns(2)
		submit = s[0].button("submit")

		if submit:
			st.text("The generated password is {}".format(password))
			pyperclip.copy(password)
			st.info("The Password has been copied to your clipboard !!")


	elif session_state.name == 'choice3' and session_state.button_sent:
		password = ''
		l = st.beta_columns(2)	
		length = l[0].number_input("Length of the password:")
		for i in range(int(length)):
			password += random.choice([random.choice(string.ascii_uppercase)])

		s = st.beta_columns(2)
		submit = s[0].button("submit")

		if submit:
			st.text("The generated password is {}".format(password))
			pyperclip.copy(password)
			st.info("The Password has been copied to your clipboard !!")




def login():
	global logged_in
	global logged_in_user

	session_state_user = SessionState.get(user_name = '', button_sent = False, insert = False, update = False, view = False, delete = False, new = False)

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
				session_state_user.name = username
				session_state_user.button_sent = True


	if session_state_user.button_sent:

	#Pointer for MongoDb for this user

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
		for documents in records:
			st.text('Organization: {o} \nPassword: {p}'.format(o = documents['Organization'], p = f.decrypt(documents['Password']).decode()))
		
		org = st.beta_columns(2)
		organization = org[0].text_input("Organizations Name:")
		password = org[1].text_input("Enter Password:", type = 'password')
		session_state_user.organization_name = organization
		s = st.beta_columns(2)
		if s[0].button("update"):
			find = pointer.find_one({'Organization' : organization})
			if find:
				try:
					old = {'Organization' : find['Organization'],
					'Password' : find['Password']}
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
		for documents in records:
			st.text('Organization: {o} \nPassword: {p}'.format(o = documents['Organization'], p = f.decrypt(documents['Password']).decode()))

	if session_state_user.delete:
		pointer = db[session_state_user.user_name]
		st.title("Delete Existing records")
		records = pointer.find({})
		for documents in records:
			st.text('Organization: {o} \nPassword: {p}'.format(o = documents['Organization'], p = f.decrypt(documents['Password']).decode()))
		
		org = st.beta_columns(2)
		organization = org[0].text_input("Organizations Name:")
		session_state_user.organization_name = organization
		s = st.beta_columns(2)
		if s[0].button("delete"):
			if pointer.find_one({'Organization' : organization}):
				pointer.delete_one({
					'Organization' : organization,
					})
				st.success("Details Deleted Succesfully !!")
			else:
				st.error("No Such Record Exists !!")


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
		if password1 == password2:
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


def home():
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
	st.write("For any Problem or Queries You can contact us at: passvault6217@gmail.com")

#app = Multiapp()

#app.add("Home", home)
#app.add("Login", login)
#app.add("Register", register)
#app.add("Random Password Generator", random_password_generator)

#app.run()


menu = ['Home','Login', 'Register', 'Random Password Generator']
option = st.sidebar.selectbox("Menu", menu)

if option == "Home":
	home()
elif option == "Login":
	login()
elif option == "Register":
	register()
elif option == "Random Password Generator":
	random_password_generator()
