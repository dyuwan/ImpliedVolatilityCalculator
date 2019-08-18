import pandas as pd
import matplotlib.pyplot as plt
from Core import Newton
nifty_data=pd.read_csv("Data.csv")
nifty_data['IV']=0

def fetch():
    for row in range(0,len(nifty_data)):
        S=nifty_data.iloc[row]["Spot Price"]
        K=nifty_data.iloc[row]["Strike Price"]
        r=0.0
        Tr=nifty_data.iloc[row]["Time"]
        T=float(Tr/365)
        callV=nifty_data.iloc[row]["LTP"]
        result=Newton(callV, S,K ,r, T)
        nifty_data.iloc[row,nifty_data.columns.get_loc('IV')]=result
    
def plot_skew(date):
    option_data=nifty_data[nifty_data['Date'] == date]
    plt.plot(option_data['Strike Price'],option_data['IV'])
    plt.legend(option_data['Date'])
    plt.ylabel("Implied Volatility")
    plt.xlabel("Strike Price")
    plt.show()
    
def input_data():
    fetch()
    date_smile=input("Please enter date for Smile Plotting(dd-mm-yyyy): ")
    for date in nifty_data['Date']:
        if date==date_smile:
            plot_skew(date_smile)
            break;
        else:
            print("Date does not correspond to Data")

input_data()
         