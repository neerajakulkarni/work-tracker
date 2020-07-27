# makes dictionary of apps and time, calculates time spent on each app

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
