# -*- coding: utf-8 -*-
from Core import Newton
from datetime import date
import datetime
import calendar
import pandas as pd
nifty_data=pd.read_csv("Data.csv")
nifty_data['IV']=0

def parameters():
    uS=0.0
    #with open("C:/Users/DyuwanS/Desktop/Project1/Nifty.txt", "r") as f:  
        #uS=f.read()
    #f.close()
    uS=10321.75
    #count=0
    uK=[]
    #a=int(0.75*12000)
    #b=int(1.25*12000)
    #for nifty in range(a,b,50):
        #uK.append(nifty)
        #count+=1
    
    ur=0.0
    uT=float((time_eval())/365)
    ucallV=[]
    for row in range (0,len(nifty_data)):
        uK.append(nifty_data.iloc[row]["Strike Price"])
        ucallV.append(nifty_data.iloc[row]["LTP"])

    for i in range (0,len(nifty_data)):
        print(Newton(ucallV[i], uS, uK[i], ur, uT))
    
    
def LastThInMonth(year, month):
    daysInMonth = calendar.monthrange(year, month)[1] 
    dt = datetime.date(year, month, daysInMonth)

    offset = 4 - dt.isoweekday()
    if offset > 0: 
        offset =offset-7                          
    
    dt =dt+datetime.timedelta(offset)
    day=dt.day
    return day
 
def time_eval():
    day=int(input("Enter day of purchase: "))
    print("1.January 2.February 3.March 4.April 5.May 6.June 7.July")
    print("8.August 9.September 10.October 11.November  12. December")
    month=int(input("Select month of purchase: "))
    duration=int(input("Select duration of option: "))
    yn=input("Is the Year 2019[Y/N] ?")   
    if yn=='Y' or 'y':
        year=2019
    else:
        year=int(input("Enter year: "))
    #date_format = "%d/%m/%y"
    
    if month==1 or 3 or 5 or 7 or 8 or 10 or 12:
        d0 = date(year, month, day)
        thday=LastThInMonth(year, month+duration)
        d1 = date(year, month+duration, thday)
        delta = d1 - d0
        return delta.days
            
    elif month==4 or 6 or 9 or 11:
        d0 = date(year, month, day)
        thday=LastThInMonth(year, month+duration)
        d1 = date(year, month+duration, thday)
        delta = d1 - d0
        return delta.days
        
    else:
        d0 = date(year, month, day)
        thday=LastThInMonth(year, month+duration)
        d1 = date(year, month+duration, thday)
        delta = d1 - d0
        return delta.days

def main():
    parameters()

if __name__ == "__main__":
    main()
