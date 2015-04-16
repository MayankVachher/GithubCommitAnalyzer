import operator
from datetime import datetime, timedelta
import os
import numpy
import matplotlib.pyplot as plt
#..................................................................................................................................
def write2new(): #Getting to Read the file into different sections and writes to new file
    file = open("data.txt","r") #Open Original File
    new = open("Temp.txt","w") #Open New Temp File to write to
    count = 0 #Keep track of line number
    readline1 = 0 #Checks whether first line has been read or not
    d1 = ""; d2 = ""; d3 = ""; d4 = ""
    for line in file:
        if count%4 == 1: d1 = line
        elif count%4 == 2: d2 = line
        elif count%4 == 3: d3 = line
        else:
            if readline1:
                d4 = line
                new.write(d1.strip()+"$"+d2.strip()+"$"+d3.strip()+"$"+d4)
            else:
                readline1 = 1
        count += 1
    new.close()
    file.close()
    return (count-1)/4
#..................................................................................................................................   
def mostactivemem(): # Finds most active member in the whole log based on maximum number of commits
    file = open("Temp.txt","r")
    memdict = {} # Counts number of commits per member
    for line in file:
        username = line.split("$")[0] # Extract Username
        if username not in memdict: memdict[username] = 1
        else: memdict[username] += 1
    file.close()
    temp = sorted(memdict.iteritems(), key=operator.itemgetter(1)) # List of Tuples of key-value pairs sorted on the basis of number of commits
    maxval = temp[len(temp)-1][1]
    print "Most Active Member(s) is/are:",
    for i in temp:
        if i[1] == maxval: print i[0],
    print "\n"
#..................................................................................................................................
def regularitycalc():
    file = open("Temp.txt","r")
    memdict = {} # Stores days of commits per member
    for line in file:
        username,dates = line.split("$")[0],(line.split("$")[3]).strip() # Extracts Username and Date
        if username not in memdict: memdict[username] = [dates]
        else:
            if dates not in memdict[username]: memdict[username].append(dates) #Collects all dates for every member
    file.close()
    temp = []
    for x,y in memdict.items():
        temp.append((x,len(y)))
    temp.sort(key=operator.itemgetter(1)) # List of Tuples of key-value pairs sorted on the basis of number of commit days
    return temp
#..................................................................................................................................
def mostregularmem(): # Finds most regular member in the whole log based on maximum number of days committed on
    temp = regularitycalc()
    maxval = temp[len(temp)-1][1]
    print "Most Regular Member(s) is/are:",
    for i in temp:
        if i[1] == maxval: print i[0],
    print "\n"
#..................................................................................................................................
def regularofeverymem(): # Prints the number of days worked of all the the members
    temp = regularitycalc()
    width_col1 = max([len(x[0]) for x in temp])
    width_col2 = max([len(str(x[1])) for x in temp])
    print "{0:<{col1}}\t{1:<{col2}}".format("Member Name","Commit Duration",col1=width_col1,col2=width_col2)
    print "." * (width_col1 + width_col2 + 8 + len("Commit Duration"))
    for x in temp:
        print "{0:<{col1}}\t{1:<{col2}} day(s)".format(x[0],x[1],col1=width_col1,col2=width_col2)
#..................................................................................................................................
def regularofteam(): # Prints how regular the team was
    file = open("Temp.txt","r")
    datelist = [] # Stores days of commits
    for line in file:
        dates = (line.split("$")[3]).strip() # Extracts Date as a string
        dates = [int(var) for var in dates.split("-")]
        if dates not in datelist: datelist.append(dates)
    file.close()
    datelist.sort()
    x,y,z = datelist[-1]
    final = date(x,y,z)
    x,y,z = datelist[0]
    initial = date(x,y,z)
    print "The Team worked for %d days out of a total %d days!\n" % (len(datelist),(final - initial).days)
#..................................................................................................................................
def periodofinactivity(): # Prints the number of days the team didn't work at all
    file = open("Temp.txt","r")
    datelist = [] # Stores days of commits
    for line in file:
        dates = (line.split("$")[3]).strip() # Extracts Date as a string
        dates = [int(var) for var in dates.split("-")]
        if dates not in datelist: datelist.append(dates)
    file.close()
    datelist.sort()
    x,y,z = datelist[-1]
    final = date(x,y,z)
    x,y,z = datelist[0]
    initial = date(x,y,z)
    print "The Team was inactive for %d days out of a total %d days!\n" % ((final - initial).days - len(datelist),(final - initial).days)
#..................................................................................................................................    
def whoworkedonwhat(): # Prints the change logs of person whose name is input
    file = open("Temp.txt","r")
    memlist = [] # Stores names of members
    for line in file:
        mem = (line.split("$")[0]) # Extracts Usernames
        if mem not in memlist: memlist.append(mem)
    file.close()
    memlist.sort()
    print "Choose Member from the following list... "
    for x,y in enumerate(memlist):
        print str(x+1)+".",y
    index = input("Choice Number: ")
    file = open("Temp.txt","r")
    print "\nHistory of commits of",memlist[index-1]
    print "................................................................................."
    for line in file:
        if line.split("$")[0] == memlist[index-1]:
            print line.split("$")[2]
#..................................................................................................................................    
def mostactivefile_forplot():
    file = open("Temp.txt","r")
    memdict = {} # Counts number of commits per member
    for line in file:
        username = line.split("$")[0]# Extract Username
        if username not in memdict: memdict[username] = 1
        else: memdict[username] += 1
    file.close()
    temp = sorted(memdict.iteritems(), key=operator.itemgetter(1)) # List of Tuples of key-value pairs sorted on the basis of number of commits
    labels = []
    commits = []
    for x in temp:
        labels.append(x[0])
        commits.append(x[1])
    fig=plt.figure()
    axis=fig.add_subplot(111)
    axis.set_xlim(0,150)
    plt.yticks(numpy.arange(len(commits)),labels)
    axis.set_title("Most Active Member")
    axis.set_ylabel("Names")
    axis.set_xlabel("Number of Commits Made")
    plt.barh(range(len(commits)),commits,color='#4682B4')
    plt.subplots_adjust(left=0.20)
    plt.show()
#..................................................................................................................................    
def mostregular_forplot():
    days=[]
    names=[]
    temp=regularitycalc()
    for i in temp:
        days.append(i[1])
        names.append(i[0])
    fig=plt.figure()
    axis=fig.add_subplot(111)
    axis.set_xlim(0,20)
    plt.yticks(numpy.arange(len(days))+0.5,names)
    axis.set_title("Commits Duration in Days")
    axis.set_ylabel("Names")
    axis.set_xlabel("Number of Days commits made")
    plt.barh(range(len(days)),days,color='Green')
    plt.subplots_adjust(left=0.20)
    plt.show()    
#..................................................................................................................................
def commitsondays():
    file = open("Temp.txt","r")
    datedict = {} # Counts number of commits per date
    datelist = []
    for line in file:
        dates = (line.split("$")[3]).strip() # Extracts Date as string
        dates = datetime.strptime(dates,'%Y-%m-%d')
        if dates not in datedict: datedict[dates] = 1; datelist.append(dates)
        else: datedict[dates] += 1
    file.close()
    datelist.sort()
    final = datelist[-1]
    initial = datelist[0]
    duration = (final - initial).days
    labels = []
    commits = []
    for x in range(duration):
        labels.append((initial+timedelta(days=x)).strftime('%Y-%m-%d'))
        if (initial+timedelta(days=x)) not in datedict: commits.append(0)
        else: commits.append(datedict[initial+timedelta(days=x)])
    plt.plot(range(duration+1)[1:], commits, 'r-o')
    plt.xlim(0,duration)
    plt.ylim(0,max(commits)+3)
    plt.xticks(range(duration+1)[1:], labels, rotation='vertical')
    plt.subplots_adjust(bottom=0.17)
    #plt.set_title("Number of Commits made by Team per day")
    plt.xlabel("Dates")
    plt.ylabel("Number of Commits")
    plt.show()
#..................................................................................................................................
def plot():
    print "1. Graph for number of commits made by members"
    print "2. Graph for regularity of members"
    print "3. Graph for commits made by team"
    n=input("\nEnter Choice Number: ")
    if n==1: mostactivefile_forplot()
    elif n==2: mostregular_forplot()
    elif n==3: commitsondays()
    else: print "Invalid Choice!"
write2new()
#........ User Interface ..........................................................................................................
choice = True
while(choice):
    print "\n {0:^{col1}}".format("Main Menu",col1 = 75)
    print "." * 75
    print "What would you like to do..."
    print "1. Find the Most Active Member of the Team"
    print "2. Find the Most Regular Member in the Team"
    print "3. Find the Number of Commits made per Member of the Team"
    print "4. Find the Number of Days of Inactivity of the Team"
    print "5. Find the Log Details by Member Name"
    print "6. Plot the data as graphs"
    print "0. Exit"
    valinput = input("\nEnter Choice Number: ")
    print "\n"
    if valinput == 1: mostactivemem()
    elif valinput == 2: mostregularmem()
    elif valinput == 3: regularofeverymem()
    elif valinput == 4: periodofinactivity()
    elif valinput == 5: whoworkedonwhat()
    elif valinput == 6: plot()
    elif valinput == 0: choice = False
    else: print "Invalid Choice!"
os.remove("Temp.txt")    
