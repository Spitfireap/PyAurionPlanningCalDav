from datetime import datetime
import caldav
from getpass import getpass
import api
from icalendar import Calendar
import utils

AURION_VEVENT_FIELDS = (
        'SUMMARY', 'DTSTART', 'DTEND', 'DTSTAMP',
        'SEQUENCE', 'LOCATION', 'DESCRIPTION'
    )
    
def getEventsFromFile(file):
    with open(file, "r") as ics_file:
        calendar = Calendar.from_ical(ics_file.read())
    eventsDict = {}
    for event in calendar.walk("VEVENT"):
        eventsDict[event["uid"]] = event
    return eventsDict

class AurionNotInit(Exception):
    pass

class Caldav():

    def __init__(self, ) -> None:
        username = input("Nom d'utilisateur CalDav")
        password_calDav = getpass("Mot de passe CalDav: ")
        
        url = input("URL des calendriers caldav (~~ https://host.domain.tld/dav/calendars):\n")
        self.calendarUrl = input("URL du calendrier cible:\n")
        self.client = caldav.DAVClient(url=url, username=username, password=password_calDav)
        self.targetCalendar = self.client.calendar(url=self.calendarUrl)

        host_aurion = input("le host aurion (aurion-prod.domain.tld en general):\n")
        url_aurion = input("l'url d'aurion (https://aurion-prod.domain.tld en général):\n")
        self.aurion_api = api.API(host_aurion, url_aurion)
        self.is_aurion_init = False

    def update(self, week, year, icsMaster):
        monday = utils.getUTCDayWWeekNumber(week, year)
        targetEvents = self.targetCalendar.date_search(start=monday, end=utils.getWeekPlus1(monday))
        masterEvents = getEventsFromFile(icsMaster)
        existingEvent = []
        for event in targetEvents:
            #Delete event not existent in master, modify those who changed
            icalEvent = event.icalendar_instance.subcomponents[0]
            uid = icalEvent["UID"]
            if uid not in masterEvents:
                #Lesson deleted
                now = datetime.utcnow()
                print(icalEvent["summary"], "is deleted")
                timeNow = now.strftime("%Y%m%d%H%M%S%f")
                icalEvent["uid"] = f"{timeNow}-deleted" #For nextcloud keeping a trash bin for events
                event.delete()
                continue
            existingEvent.append(uid)
            curMasterEvent = masterEvents[uid]
            for properties in curMasterEvent.property_items():
                if properties[0] in AURION_VEVENT_FIELDS and icalEvent[properties[0]] != properties[1]:
                    icalEvent[properties[0]] = properties[1]
                    #Updates everything but at least it's up to date
        
        for masterEvent in masterEvents:
            if masterEvent not in existingEvent:
                ical = masterEvents[masterEvent].to_ical()
                #Event not on ical
                self.targetCalendar.save_event(ical)

    def initAurion(self):
        username_aurion = input("Nom d'utilisateur Aurion:\n")
        password_aurion = getpass("Mot de passe aurion: ")

        self.aurion_api.login(username_aurion, password_aurion)
        self.aurion_api.navigate()
        self.is_aurion_init = True
        
    def updateCalendars(self, weeks, year):
        if not self.is_aurion_init:
            raise(AurionNotInit)
        for week in weeks:
            self.aurion_api.selectCal(week, year)
            file_name = f"ics/ics-{week}-{year}.ics"
            with open(file_name, "w") as ics_file:
                ics_file.write(self.aurion_api.getCal())
            self.update(week, year, file_name)



if __name__ == "__main__":
    #Changer les semaines à upload sur calDav
    weeks = [36,37,38,39]
    cal = Caldav()
    cal.initAurion()
    cal.updateCalendars(weeks, 2022) #Changer l'année si jamais... 