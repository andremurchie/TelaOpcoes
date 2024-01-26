# Andre Murchie 21/12/2023
import functions
import pandas as pd
import numpy as np

class Processing():
    def __init__(self, dic):
        self.dic = dic
           
    def grafico_premio_main(self):
        dic_premio = {}
        custos = []
        for i in range(0,4):
            flag, operacao, spot, strike, maturity, juros, volatilite = self.pega_parametros(i)
            if flag == "":
                pass
            else:
                mengo = spot
                custos.append(round(functions.BS(spot, strike, maturity, juros, volatilite, flag, operacao),4))
                lista_spots = self.retorna_lista_spot(spot)
                for s in lista_spots:
                    premio = functions.BS(s, strike, maturity, juros, volatilite, flag, operacao)
                    dic_premio[s] = dic_premio.get(s, 0) + premio 
        
        df_premio = pd.DataFrame(list(dic_premio.items()), columns=['x', 'y'])
        print(custos)
        df_premio["y"] = df_premio["y"] - (sum(custos))
        print(df_premio)
        return df_premio, custos, mengo

    def grafico_delta_main(self):
        dic_delta = {}
        deltas = []
        for i in range(0,4):
            flag, operacao, spot, strike, maturity, juros, volatilite = self.pega_parametros(i)
            if flag == "":
                pass
            else:
                deltas.append(round(functions.DELTA(spot, strike, maturity, juros, volatilite, flag, operacao),4))
                lista_spots = self.retorna_lista_spot(spot)
                for s in lista_spots:
                    delta = functions.DELTA(s, strike, maturity, juros, volatilite, flag, operacao)
                    dic_delta[s] = dic_delta.get(s, 0) + delta 
                    
        df_delta = pd.DataFrame(list(dic_delta.items()), columns=['x', 'y'])
        
        return df_delta, deltas
    
    def grafico_gamma_main(self):
        dic_gamma = {}
        gammas = []
        for i in range(0,4):
            flag, operacao, spot, strike, maturity, juros, volatilite = self.pega_parametros(i)
            if flag == "":
                pass
            else:
                gammas.append(functions.GAMMA(spot, strike, maturity, juros, volatilite, flag, operacao))
                lista_spots = self.retorna_lista_spot(spot)
                for s in lista_spots:
                    gamma = round(functions.GAMMA(s, strike, maturity, juros, volatilite, flag, operacao),4)
                    dic_gamma[s] = dic_gamma.get(s, 0) + gamma
        df_gamma = pd.DataFrame(list(dic_gamma.items()), columns=['x', 'y'])             
        return df_gamma, gammas
    
    def pega_parametros(self,n):
        flag = self.dic[f'opc{n}']
        operacao = self.dic[f'operacao{n}']
        spot =  self.dic[f'spot{n}']
        strike =  self.dic[f'strike{n}']
        maturity = self.dic[f'maturidade{n}']
        juros =  self.dic[f'juros{n}']
        volatilite =  self.dic[f'volatilidade{n}']

        return flag, operacao, spot, strike, maturity, juros, volatilite
    
    def retorna_lista_spot(self, spot):
        intervalo = 0.5
        lista_spot = np.linspace(spot*(1-intervalo), spot*(1+intervalo), 700)
        lista_spot = np.sort(np.append(lista_spot, spot))
        return lista_spot
    