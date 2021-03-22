from firebase import firebase
from pyfcm import FCMNotification
from calendarObject import calendar
import json
import datetime

"""
This Class manage the Firebase API
"""
class firebaseManagment():

    """
    Construct of Fibrebase Class

    :param url: URL to the Firebase host
    :param api_key: API key for the Authentication 
    """
    def __init__ (self,url,api_key):
        self.db = firebase.FirebaseApplication(url,None)
        fcm = FCMNotification(api_key=api_key)
        self.id =""
        self.days = []

    # Check if the user's email exists in the DBs
    def check_email_exists(self, email):
        users = self.db.get('/users',None)
        for user in users:
            user_info = self.db.get('/users',user)
            if (user_info["email"] == email):
                self.id = user_info["id"]
                return True
        print ("This email adress is not registered \n")
        return False
    
    # Get from DB the pills
    def get_pills_calendar(self):
        iteration = 0
        pills = 0
        days = self.db.get('/Calendar',self.id)
        path = '/Calendar/'+self.id
        self.calendar_path = path
        for day in days:
            aux_day=calendar.Day(day["day"])
            if ("pills" in day):
                for pill in day["pills"]:
                    aux_day.add_pill(pill["name"],pill["date"],pill["pillSelection"],pill["pillTaken"],pill["src"])
            iteration+=1
            self.days.append(aux_day)
    
    def print_planned_pills(self,day):
        print("Today is : ",self.days[day].day)
        if (len(self.days[day].pills) > 0):
            print ("Your planned pills for today are:")
            for pill in self.days[day].pills:
                print (pill.pillName)
            return True
        else:
            print ("There are no pills planned for today")
            return False
    
    # Get a data of day and pills for that day and print it
    def print_calendar(self):
        print("Week Calendar:")
        for i in range(7):
            print (self.days[i].day,":")
            if (len(self.days[i].pills) > 0):
                print ("Your planned pills for", self.days[i].day + " are :")
            for pill in self.days[i].pills:
                print (pill.pillName)
            else:
                print ("There are no pills planned for ", self.days[i].day)
   
    """
    Check if the predicted pill is in current_day

    :param pill_predicted: pill predicted
    :param current_day: day selected
    :return: boolean
    """
    def is_pill_planned(self,pill_predicted,current_day):
        for pill in self.days[current_day].pills:
            if( pill.pillName == pill_predicted ):
                return True
        return False
    
    # Pass to next day of the week
    def next_day(self,day):
        if (day < 6):
            day +=1
        else:
            day =0
        return day
    
    # Set on the Firebase DB that the pill predicted has been taken
    def post_pill_taken(self, day,pill_predicted):
        i =0
        for pill in self.days[day].pills:
            if( pill.pillName == pill_predicted ):
                now = datetime.datetime.now()
                self.days[day].pills[i].pillTaken=True
                self.days[day].pills[i].date = str(now.hour)+":"+str(now.minute)
                write_path = self.calendar_path+"/"+str(day)+"/pills/"+str(i)+"/"
                self.db.put(write_path, "date",self.days[day].pills[i].date)
                self.db.put(write_path, "pillTaken",True)