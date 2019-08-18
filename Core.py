# -*- coding: utf-8 -*-
from math import exp, log, sqrt, pi
from Stats import cdistf, pdistf
da=0.0
db=0.0
flag=0

def dval(S, K, r, v, T):
    global da
    global db
    da=(log(S/K)+(r+(v*v)/2)*T)/(v*sqrt(T))
    db=da - v*sqrt(T)

def call_price(S, K, r, v, T):
    global da
    global db
    dval(S, K, r, v, T)
    call=S*cdistf(da)-K*exp(-r*T)*cdistf(db)
    return call

def put_price(S, K, r, v, T):
    global da
    global db
    dval(S, K, r, v, T)
    put=K*exp((-r*T))*cdistf(-db)-S*cdistf(-da)
    return put

def Black_Scholes_Greeks_Call(S, K, r, v, T):
    global da
    global db
    Delta = cdistf(da)
    Gamma = pdistf(da)/(S*v*sqrt(T))
    Theta = -(S*v*pdistf(da))/(2*sqrt(T)) - r*K*exp(-r*T)*cdistf(db)
    Vega = S *sqrt(T)*pdistf(da)
    Rho = K*T*exp(-r*T)*cdistf(db)
    print ("Option Greeks for Call")
    print("Delta= ")
    print(Delta)
    print("Gamma= ")
    print(Gamma)
    print("Theta= ")
    print(Theta)
    print("Vega= ")
    print(Vega)
    print("Rho= ")
    print(Rho)

def Black_Scholes_Greeks_Vega(S, K, r, v, T):
    dval(S, K, r, v, T)
    Vega = S *sqrt(T)*pdistf(da)
    return Vega

def Black_Scholes_Greeks_Put(S, K, r, v, T):
    global da
    global db
    Delta = -cdistf(-da)
    Gamma = pdistf(da)/(S*v*sqrt(T))
    Theta = -(S*v*pdistf(da))/(2*sqrt(T)) + r*K*exp(-r*T)*cdistf(-db)
    Vega = S *sqrt(T)*pdistf(da)
    Rho = -K*T*exp(-r*T)*cdistf(-db)
    print ("Option Greeks for Put")
    print("Delta= ")
    print(Delta)
    print("Gamma= ")
    print(Gamma)
    print("Theta= ")
    print(Theta)
    print("Vega= ")
    print(Vega)
    print("Rho= ")
    print(Rho)

def interval(callV, S, K, r, T):
    IV=sqrt(2*pi/T)*callV/S
    upper_limit=IV+0.2
    lower_limit=IV-0.2
    formcall=float(0.0)
    formcall=float(call_price(S, K, r, IV, T))

    while abs(formcall - callV) > 0.01:
        if formcall <= callV:
            lower_limit=IV
        elif formcall > callV:
            upper_limit=IV
                  
        IV=0.5*(upper_limit + lower_limit)
        formcall=float(call_price(S, K, r, IV, T))
        
    return IV

def intervalP(callV, S, K, r, T):
    IV=sqrt(2*pi/T)*callV/S
    upper_limit=IV+0.2
    lower_limit=IV-0.2
    formcall=float(0.0)
    formcall=float(put_price(S, K, r, IV, T))

    while abs(formcall - callV) > 0.01:
        if formcall <= callV:
            lower_limit=IV
        elif formcall > callV:
            upper_limit=IV
                  
        IV=0.5*(upper_limit + lower_limit)
        formcall=float(put_price(S, K, r, IV, T))
        
    return IV

def Newton(Market_Value, S, K, r, T):
    iterations = 100
    precision = 1.0e-3
    sigma = 0.5
    for i in range(0, iterations):
        price = call_price(S, K, r, sigma, T)
        vega = Black_Scholes_Greeks_Vega(S, K, r, sigma, T)

        price = price
        diff = Market_Value - price

        if (abs(diff) < precision):
            return sigma

        sigma = sigma + diff/vega
    return sigma

def NewtonP(Market_Value, S, K, r, T):
    iterations = 100
    precision = 1.0e-3
    sigma = 0.5
    for i in range(0, iterations):
        price = put_price(S, K, r, sigma, T)
        vega = Black_Scholes_Greeks_Vega(S, K, r, sigma, T)

        price = price
        diff = Market_Value - price

        if (abs(diff) < precision):
            return sigma

        sigma = sigma + diff/vega
    return sigma

def approx(callV, S, K, T):
    a=sqrt(2*pi/T)
    b=(callV-(S-K)/2)/(S-(S-K)/2)
    v=a*b
    return abs(v)
    
def result(S, K, r, v, T):
    print("Underlying Price:    ")
    print(S)
    print("\nStrike Price:    ")
    print(K)
    print("\nRisk-free Interest Rate:    ")
    print(r)
    print("\nVolatility:    ")
    print(v)
    print("\nTime Duration:    ") 
    print(T)
    print("\n")

def main():
    S=float(input("Enter Spot Price   ="))
    K=float(input("Enter Strike Price ="))
    r=float(input("Enter Interest rate="))
    v=float(input("Enter Volatility   ="))
    T=float(input("Enter Maturity     ="))
    dval(S, K, r, v, T)
    result(S, K, r, v, T)
    print ("\nCall Price:    ")
    print(call_price(S, K, r, v, T))
    print ("\nPut Price:    ")
    print(put_price(S, K, r, v, T))
    
    print("\n")
    flag=int(input("Select Call(0) or Put(1) Option: "))
    callV=float(input("Enter Value of option "))
    print ("1.Interval Limits:    ")
    print ("2.Newton Rhapson:    ")
    print ("3.At-the-Money Approximation:    ")
    method=float(input("Select Method "))
    
    if method==1:
        if flag==0:
            catch = interval(callV, S, K, r, T)
        elif flag==1:
            catch = intervalP(callV, S, K, r, T)
        print("Implied volatility ")
        print(catch)
    elif method==2:
        if flag==0:
            catch = Newton(callV, S, K, r, T)
        elif flag==1:
            catch=NewtonP(callV, S, K, r, T)
        print("Implied volatility ")
        print(catch)
    elif method==3:
        v=approx(callV, S, K, T)
        print("Approximated Volatility is ")
        print(v)
        
if __name__ == "__main__":
    main()