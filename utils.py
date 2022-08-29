#!/bin/python
import datetime


def getUTCDayWWeekNumber(week, year):
    a = datetime.datetime.utcnow()
    b = datetime.datetime.now()
    return datetime.datetime.strptime(f'{year}-{week}-1-UTC', "%Y-%W-%w-%Z") - (a-b)

def getWeekPlus1(day):
    #Not 7 day, only 6 (aurion load ics for 6 days)
    return day + datetime.timedelta(days=6)

