# Andre Murchie 21/12/2023

import functions
from config_tela import TelaConfig
from processing import Processing


import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)

class AppWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Janela com Abas")
        #Cria as Entradas
        self.tela_config = TelaConfig(self)
        self.tela_config.configure_window()
        self.tela_config.create_tabs()

        #Botão de Calcular
        calc_button = tk.Button(self.tela_config.tab_main, text="Calcular", command=self.calcula_main)
        calc_button.grid(row=8, column=0, columnspan=3, pady=0)


    def plot_graph(self, df, metrica, column, row):
        fig, ax = plt.subplots(figsize=(6, 2.5))
        df.plot(kind='line', x='x', y='y', ax=ax, color='blue')
        df.plot(kind='scatter', x='x', y='y', ax=ax, color='red', marker='o', s = 5)

        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
        
        ax.set_title(f"{metrica} x Spot")
        ax.set_ylabel("Spot")
        ax.grid(True)

        chart = FigureCanvasTkAgg(fig, self.tela_config.tab_main)
        chart.get_tk_widget().grid(row=row, column=column, padx=0, pady=10, rowspan=8)

    def calcula_main(self):
        dic = self.tela_config.save_properties()
        self.processing = Processing(dic)
        
        df_premio, custos, spot = self.processing.grafico_premio_main()
        df_delta, deltas = self.processing.grafico_delta_main()
        df_gamma, gammas = self.processing.grafico_gamma_main()

        self.plot_graph(df_premio, metrica = 'Prêmio', column=9, row=0)
        self.plot_graph(df_delta, metrica = 'Delta', column=9, row=8)
        self.plot_graph(df_gamma, metrica = 'Gamma', column=9, row=40)

        # Outputs
        outputs = {"Prêmio": custos, "Delta":deltas, "Gamma":gammas}
        for k,v in outputs.items():
            for i, entry in enumerate(self.tela_config.entries[k]):
                entry.delete(0, tk.END)
                try:
                    entry.insert(0, v[i]) if i != 4 else entry.insert(0, round(sum(v),4)) 
                except: 
                    entry.insert(0, "")
        # Tabela
        df_premio.rename(columns={"y":"Prêmio"}, inplace=True)
        df_delta.rename(columns={"y":"Delta"}, inplace=True)
        df_gamma.rename(columns={"y":"Gamma"}, inplace=True)
        df_merged = pd.merge(df_premio, df_delta, on='x')
        df_merged = pd.merge(df_merged, df_gamma, on='x')
        df_merged.rename(columns={"x":"Spot"}, inplace=True)
        df_merged["% Spot"] = (df_merged["Spot"] / spot) -1 
        df_merged["% Prêmio"] = np.maximum(df_merged["Prêmio"] / sum(custos) -1, -1.0)  
        
        df_merged['% Spot'] = df_merged['% Spot'].map(lambda x: '{:.4f}%'.format(x * 100))
        df_merged['% Prêmio'] = df_merged['% Prêmio'].map(lambda x: '{:.2f}%'.format(x * 100))
        df_merged['Spot'] = df_merged['Spot'].map(lambda x: '{:.4f}'.format(x))
        df_merged['Prêmio'] = df_merged['Prêmio'].map(lambda x: '{:.4f}'.format(x))
        df_merged['Delta'] = df_merged['Delta'].map(lambda x: '{:.4f}'.format(x))
        df_merged['Gamma'] = df_merged['Gamma'].map(lambda x: '{:.4f}'.format(x))
        
        df_merged = df_merged[["% Spot", "Spot", "Prêmio", "% Prêmio", "Delta", "Gamma"]]
        df_final = df_merged.iloc[(len(df_merged)//2)-30 : (len(df_merged)//2)+30]
        self.tela_config.update_dataframe_treeview(df_final)
        print(df_final)

# Executando a aplicação
if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()