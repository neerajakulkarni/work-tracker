import time
import datetime
import re
import sys
import schedule

if sys.platform in ['Windows', 'win32', 'cygwin']:
    import win32api
    import win32gui
    import uiautomation as auto
elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    from AppKit import NSWorkspace
    from Foundation import *
elif sys.platform in ['linux', 'linux2']:
        import linux as l

def job():
    activewindow = ""
    count = 0
    list = dict()
    timespent = 0
    total = 0

    def SectoDay(t):
        hour = t // 3600
        t %= 3600
        minutes = t // 60
        t %= 60
        seconds = t
        if hour == 0 and minutes == 0:
            return(seconds, "seconds")
        elif hour == 0:
            return(minutes, "minutes", seconds, "seconds")
        else:
            return(hour, "hours", minutes, "minutes", seconds, "seconds")

    def totalcalc(actwin, timesp, list2):
        if sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
            if actwin not in list2 and actwin != 'loginwindow':
                list2[actwin] = int(timesp)
            elif actwin in list2 and actwin != 'loginwindow':
                list2[actwin] = list2[actwin] + int(timesp)
        elif sys.platform in ['Windows', 'win32', 'cygwin']:
            if actwin not in list2 and actwin != "" and actwin.startswith('http')==False:
                list2[actwin] = int(timesp)
            elif actwin in list2 and actwin != "" and actwin.startswith('http')==False:
                list2[actwin] = list2[actwin] + int(timesp)

    while True:
        if sys.platform in ['Windows', 'win32', 'cygwin']:
            window = win32gui.GetForegroundWindow()
            newactive = win32gui.GetWindowText(window)
        elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
            newactive = (NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'])
        if newactive != activewindow:
            start=time.time()
            if count==1:
                timespent = start-end
                totalcalc(activewindow, timespent, list)
                total = total + int(timespent)
            activewindow = newactive
            #print("Current window:", activewindow)
            count=1
            end=time.time()

        if str(datetime.datetime.now().time()).startswith('23:59:50'):
            timespent = time.time()-start
            totalcalc(activewindow, timespent, list)
            total = total + int(timespent)
            break

    finalist = dict()
    for i in list.keys():
        finalist[i] = re.sub(r"[^a-zA-Z0-9]+", ' ', str(SectoDay(list[i])))
    print('\n'.join("{}: {}".format(k, v) for k, v in finalist.items()))

    strtotal = str(SectoDay(total))
    print("Total time spent on device:", re.sub(r"[^a-zA-Z0-9]+", ' ', strtotal))

schedule.every().day.at("00:00:00").do(job)
while True:
    schedule.run_pending()
