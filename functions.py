import numpy as np
from scipy.stats import norm


N = norm.cdf
Nm = norm.pdf

def BS(spot, strike, maturity, juros, volatilite, flag, operacao):
    flag = flag.upper()
    operacao = operacao.upper()

    if flag == "CALL":
        flag = 1
    else:
        flag = -1
    
    maturity = maturity/252

    vp_k = strike/(1+juros)**maturity
    d1 = np.log(spot/vp_k) / (volatilite * np.sqrt(maturity)) + (volatilite * np.sqrt(maturity))/2
    d2 = np.log(spot/vp_k) / (volatilite * np.sqrt(maturity)) - (volatilite * np.sqrt(maturity))/2
    premio = flag * spot * N(flag * d1) - flag * vp_k * N(flag * d2) 
    
    return premio if operacao == "C" else -premio

def DELTA(spot, strike, maturity, juros, volatilite, flag, operacao):
    flag = flag.upper()
    operacao = operacao.upper()

    if flag == "CALL":
        flag = 1
    else:
        flag = -1

    maturity = maturity/252
    vp_k = strike/(1+juros)**maturity
    d = np.log(spot/strike) / (volatilite * np.sqrt(maturity)) + (volatilite * np.sqrt(maturity)/2)

    if flag == 1:
        delta = N(d) * np.exp(-juros * maturity)
    else:
        delta = N(d - 1) * np.exp(-juros * maturity)
    
    return delta if operacao == "C" else -delta

def GAMMA(spot, strike, maturity, juros, volatilite, flag, operacao):
    operacao = operacao.upper()

    maturity = maturity/252
    vp_k = strike / (1+juros)**maturity
    d = np.log(spot/vp_k) / (volatilite * np.sqrt(maturity)) + (volatilite * np.sqrt(maturity)/2)
    gamma = Nm(d) / spot / volatilite / np.sqrt(maturity)
    
    return gamma if operacao == "C" else -gamma

def VEGA(spot, strike, maturity, juros, volatilite, flag):
    maturity = maturity/252
    vp_k = strike/(1+juros)**maturity
    d = np.log(spot/vp_k) / (volatilite * np.sqrt(maturity)) + (volatilite * np.sqrt(maturity)/2)
    vega = N(d) * spot * np.sqrt(maturity)
    return vega