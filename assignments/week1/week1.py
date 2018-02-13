import datetime
import calendar

# name
name = raw_input("enter your name: ")

# date
date_string = datetime.datetime.now().strftime("%a %m/%d/%Y %H:%M:%S")

print('Hello, ' + str(name) + '!' + ' Today is ' + date_string)

