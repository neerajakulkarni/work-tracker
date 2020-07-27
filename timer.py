import time
import datetime
import re
import sys
import schedule
import sqlite3
from sectoday import Convert
from findidle import idletime
from makedict import totalcalc

if sys.platform in ['Windows', 'win32', 'cygwin']:
    import win32api
    import win32gui
    import uiautomation as auto
elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    from AppKit import NSWorkspace
    from Foundation import *

def job():
    activewindow = ""
    initialpos = "" #initial mouse position
    count = 0 # flag for apps
    i = 0 #flag variable while calculating idle time
    list = dict()
    timespent = 0 # on an individual app
    total = 0 # total time spent on device
    mouse = Controller() #mouse controller to detect position
    t=0 #stores idle value returned
    idlesum=0 #sum of idle time for 1 app
    idle = 0 #stores idle time

    while True:
    	if sys.platform in ['Windows', 'win32', 'cygwin']:
    		window = win32gui.GetForegroundWindow()
    		newactive = win32gui.GetWindowText(window)
    	elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    		newactive = (NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'])
    	if newactive != activewindow:
    		start=time.time()
    		if count==1:
    			timespent = (start-end)-int(idlesum)
    			totalcalc(activewindow, timespent, list)
    			total = total + int(timespent)
    		activewindow = newactive
    		count=1
    		idlesum = 0
    		end=time.time()
    	if str(datetime.datetime.now().time()).startswith('23:59:50'):
    		if start != 0:
    			timespent = (time.time()-start)-int(idlesum)
    			totalcalc(activewindow, timespent, list)
    			total = total + int(timespent)
    		break
    	t = idletime(initialpos, i, idle, t)
    	if t >= 300:
    		idlesum = idlesum + t

    finalist = dict()
    for i in list.keys():
        finalist[i] = re.sub(r"[^a-zA-Z0-9]+", ' ', str(Convert(list[i]))) # converting the time in sec into hrs, mins, sec

    strtotal = re.sub(r"[^a-zA-Z0-9]+", ' ', str(Convert(total))) # converting total time on device to hrs, mins, sec

    today = datetime.date.today() #getting current date

    # define connection and cursor to insert into database

    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    timetracker_sql = '''CREATE TABLE IF NOT EXISTS "TimeTracker" (
                day_id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                day TEXT,
                timespenttotal TEXT)'''

    cursor.execute(timetracker_sql)

    # creating app tracker table
    app_sql = '''CREATE TABLE IF NOT EXISTS "AppTracker" (
                id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                appname TEXT,
                FOREIGN KEY (day_id) REFERENCES TimeTracker(day_id),
                timespentapp TEXT)'''

    cursor.execute(app_sql)

    cursor.execute('''INSERT INTO TimeTracker (day, timespenttotal) VALUES(?, ?)''', (today, strtotal)

    for k, v in finalist.items():
        cursor.execute("INSERT INTO AppTracker (appname, timespentapp) VALUES(?, ?)", (k, v))

    conn.commit()

schedule.every().day.at("00:00:00").do(job)
while True:
    schedule.run_pending() #running the program daily at 12 am
