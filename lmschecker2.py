# this code checks due date of the assignments and prints those onto the file which have a due 
# after the date of execution of this program. If there are assignments which have a due date 
# after the date of the execution the program will store that there are no new updates

import requests, datetime, os, urllib3
from bs4 import BeautifulSoup

# this is to disable all the warnings during run time.
urllib3.disable_warnings()

f = open("/home/ayush/Coding/Zense/lmschecker.txt", "w")

with requests.Session() as session:
	url = "https://lms.iiitb.ac.in/moodle/login/index.php"
	final_url = "https://lms.iiitb.ac.in/moodle/my/"
	# change username and password for the program to work for you
	usr = {'username' : "imt2017009", "password" : "********"}
	log = session.get(url, verify = False)
	login = session.post(url, data = usr, verify = False)
	page = session.get(final_url, verify = False)
	html_content = page.content
	content = BeautifulSoup(html_content, "lxml")
	info_container =  (content.findAll("div", {"id" : "inst1900"}))[0].findAll("div", {"class" : "content"})
	containers = info_container[0].findAll("div", {"class" : "event"})
	
	for container in containers:
		desp = container.img["title"]
		assign = container.a.text
		course = (container.findAll("a"))[1].text
		sub_date = (container.findAll("div", {"class" : "date"}))[0].text
		f.write(course + '\n' + desp + " : " + assign + '\n' + "Due Date : " + sub_date + '\n' + "\n")
	f.close()
	f = open("lmschecker.txt", "a")
	# lmschecker.txt is written and if it is empty then it's size is 0 and thus will move in
	# the if statement.
	if (os.stat("/home/ayush/Coding/Zense/lmschecker.txt").st_size == 0):
		f.write("There are no new updates! \n")

	time = datetime.datetime.now()
	f.write("Date and Time : " + str(time))
	f.close()

# open crontab -e
# * */1 * * * /home/ayush/Coding/Zense/lmschecker2.py this will make the code run every hour

