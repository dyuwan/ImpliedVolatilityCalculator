# -*- coding: utf-8 -*-
from Core import Newton
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
from math import exp
from numpy import sqrt,mean
import datetime
import calendar

nifty_data=pd.read_csv("Nifty.csv")
real_data=pd.read_csv("Real Data1.csv")
real_data['IV']=0
real_data['HV']=0
expiry=date
opendate=date
      
def parameters():
    global expiry
    global opendate
    uS=0.0
    uK=[]
    ur=0.0
    
    #with open("C:/Users/DyuwanS/Desktop/Project1/Nifty.txt", "r") as f:  
        #uS=float(f.read())
    #f.close()
    uS=11916.75
    #count=0
    
    #a=int(0.923*12000)
    #b=int(1.09*12000)
    
    #for nifty in range(a,b,50):
        #uK.append(nifty)
        #count+=1
    
    uTr=time_eval()
    uT=float((uTr)/365)
    ucallV=[]
    for row in range (0,len(real_data)):
        uK.append(real_data.iloc[row]["Strike Price"])
        ucallV.append(real_data.iloc[row]["Settle Price"])
        real_data.iloc[row,real_data.columns.get_loc('Symbol')]="NIFTY"
        real_data.iloc[row,real_data.columns.get_loc('Date')]=opendate
        real_data.iloc[row,real_data.columns.get_loc('Expiry')]=expiry
        real_data.iloc[row,real_data.columns.get_loc('Spot Price')]=uS
        real_data.iloc[row,real_data.columns.get_loc('Time')]=uTr
        
        p=ucallV[row]
        q=uK[row]
        result=Newton(p, uS, q, ur, uT)
        real_data.iloc[row,real_data.columns.get_loc('IV')]=result
    
    #print(real_data)
        
def historical():
    global expiry
    global opendate
    close=[]
    start=[]
    r=[]
    hvol=[]
    ctr1=0
    ctr2=22
    for j in range(opendate.day,expiry.day):
        
        for row in range (ctr1,ctr2):      
            close.append(nifty_data.iloc[row]["Close"])
            start.append(nifty_data.iloc[row]["Open"])
            r.append((close[row]-start[row])/start[row])
        r_mean = mean(r)
        diff_square=0.0
        for i in range(0,len(r)):
            diff_square =diff_square+(r[i]-r_mean)**2
        std = sqrt(diff_square*(1.0/(len(r)-1)))
        hvol.append(std*sqrt(252))
        ctr1 +=1
        ctr2 +=1

    for x in range(0,len(hvol)):
        real_data.iloc[x,real_data.columns.get_loc('HV')]=hvol[x]
    for x in range(len(hvol),len(real_data)):
        k=0.140*exp((x-20)/1000)
        real_data.iloc[x,real_data.columns.get_loc('HV')]=k
    #print(real_data['HV'])
    
def LastThInMonth(year, month):
    global expiry
    daysInMonth = calendar.monthrange(year, month)[1] 
    dt = datetime.date(year, month, daysInMonth)

    offset = 4 - dt.isoweekday()
    if offset > 0: 
        offset =offset-7                          
    
    dt =dt+datetime.timedelta(offset)
    expiry=dt
    day=dt.day
    return day
 
def time_eval():
    global opendate
    day=int(input("Enter day of purchase: "))
    print("1.January 2.February 3.March 4.April 5.May 6.June 7.July")
    print("8.August 9.September 10.October 11.November  12.December")
    month=int(input("Select month of purchase: "))
    duration=int(input("Select duration of option: "))
    duration=duration-1
    yn=input("Is the Year 2019[Y/N] ?")   
    if yn=='Y' or 'y':
        year=2019
    else:
        year=int(input("Enter year: "))
    #date_format = "%d/%m/%y"
    opendate=datetime.date(year, month, day)
    #print(opendate)
    
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
    
def plot_skew(date):
    option_data=real_data[real_data['Date'] == date]
    plt.plot(option_data['Strike Price'],option_data['IV'])
    plt.legend(option_data['Date'])  
    plt.plot(option_data['Strike Price'],option_data['HV'])
    plt.legend(option_data['Symbol'])
    plt.ylabel("Implied Volatility")
    plt.xlabel("Strike Price")
    plt.show()
    
def plot_skew_HV(date):
    option_data=real_data[real_data['Date'] == date]
    plt.plot(option_data['Strike Price'],option_data['HV'])
    plt.legend(option_data['Symbol'])
    plt.ylabel("Historical Volatility")
    plt.xlabel("Strike Price")
    plt.show()

def input_data():
    parameters()
    historical()
    print("\n")
    print("Provide details for smile plotting ")
    day=int(input("Enter day of purchase: "))
    month=int(input("Select month of purchase: "))
    year=2019
    date_smile=datetime.date(year, month, day)
    
    for dated in real_data['Date']:
        if dated==date_smile:
            plot_skew(date_smile)
            #plot_skew_HV(date_smile)
            break;
        else:
            print("Date does not correspond to Data")
            break;

def main():
    input_data()

if __name__ == "__main__":
    main()
