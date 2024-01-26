# Andre Murchie 21/12/2023
import tkinter as tk
from tkinter import ttk
from tkinter import font

class TelaConfig:
    def __init__(self, root):
        self.root = root
        self.entries = {}

    def configure_window(self):
        self.root.state('zoomed')

    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)

        self.tab_main = ttk.Frame(tab_control)
        tab_premio = ttk.Frame(tab_control)
        tab_delta = ttk.Frame(tab_control)
        tab_gamma = ttk.Frame(tab_control)

        self.setup_main_tab(self.tab_main)

        tab_control.add(self.tab_main, text='Main')
        tab_control.pack(expand=1, fill='both')

    def setup_main_tab(self, tab):
        # Rótulos de Input
        labels = ["Tipo", "Operação", "Spot", "Strike", "Volatilidade", "Maturidade", "Juros"]
        tipo_options = ["","CALL", "PUT"]
        operacao_options = ["","C", "V"]
        
        for i, label in enumerate(labels):
            ttk.Label(tab, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            self.entries[label] = []
            for j in range(4):
                if label == "Tipo":
                    combo = ttk.Combobox(tab, values=tipo_options, width=7)
                    combo.grid(row=i, column=j+1, padx=0, pady=0)
                    combo.set(tipo_options[0])  # default value
                    self.entries[label].append(combo)    
                elif label == "Operação":
                    combo = ttk.Combobox(tab, values=operacao_options, width=7)
                    combo.grid(row=i, column=j+1, padx=0, pady=0)
                    combo.set(operacao_options[0])  # default value
                    self.entries[label].append(combo)                
                else:
                    entry = ttk.Entry(tab, width=10)
                    entry.grid(row=i, column=j+1, padx=0, pady=0)
                    self.entries[label].append(entry)


                if label in ["Volatilidade", "Maturidade", "Juros", "Spot"]:
                    chk_var = tk.BooleanVar()
                    chk = ttk.Checkbutton(tab, variable=chk_var, command=lambda l=label, var=chk_var: self.sync_entries(l, var))
                    chk.grid(row=i, column=j+2, padx=0, pady=0)
                
                if label in ["Volatilidade", "Juros"]:
                    entry.insert(tk.END, '%')
        
        # Rótulos de Output
        labels = ["Prêmio", "Delta", "Gamma"]
        for i, label in enumerate(labels):
            ttk.Label(tab, text=label).grid(row=i+12, column=0, padx=5, pady=5, sticky="w")
            self.entries[label] = []
            for j in range(5):
                if j != 4:
                    entry = ttk.Entry(tab, width=10)
                    entry.grid(row=i+12, column=j+1, padx=5, pady=5)
                    self.entries[label].append(entry)
                else:
                    design_fonte = font.Font(family="Helvetica", size=10, weight="bold")
                    entry = ttk.Entry(tab, width=10, font=design_fonte)
                    entry.grid(row=i+12, column=j+1, padx=5, pady=5)
                    self.entries[label].append(entry)

        # DataFrame de Output
        self.treeview_frame = ttk.Frame(tab)
        self.treeview_frame.grid(row=0, column=15, rowspan=100, sticky="nsew")
        self.dataframe_treeview = ttk.Treeview(self.treeview_frame)
        self.dataframe_treeview.pack(expand=True, fill='both')

    def sync_entries(self, label, var):
        if var.get():
            value = self.entries[label][0].get()
            for entry in self.entries[label][1:]:
                entry.delete(0, tk.END)
                entry.insert(0, value)


    def update_dataframe_treeview(self, df):
        self.dataframe_treeview.delete(*self.dataframe_treeview.get_children())
        self.dataframe_treeview['columns'] = list(df.columns)
        self.dataframe_treeview['show'] = 'headings'
        for col in df.columns:
            self.dataframe_treeview.heading(col, text=col)
        for index, row in df.iterrows():
            self.dataframe_treeview.insert("", "end", values=list(row))
        self.adjust_column_widths(df)

    def adjust_column_widths(self, df):
        for col in df.columns:
            col_len = tk.font.Font().measure(col)
            for val in df[col]:
                val_len = tk.font.Font().measure(str(val))
                col_len = max(col_len, val_len)
            self.dataframe_treeview.column(col, width=col_len + 5, stretch=False, anchor="c")  # Ajuste com alguma margem

    def save_properties(self):
        #Busca os valores das entradas e chama suas funções de cálculo
        dic = {}
        for i in range(0,4):
            dic_ = {f'opc{i}'         : self.entries["Tipo"][i].get(),
                    f'operacao{i}'    : self.entries["Operação"][i].get(),
                    f'spot{i}'        : "" if self.entries["Spot"][i].get() == "" else float(self.entries["Spot"][i].get()),
                    f'strike{i}'      : "" if self.entries["Strike"][i].get() == "" else float(self.entries["Strike"][i].get()),
                    f'volatilidade{i}': "" if self.entries["Volatilidade"][i].get().rstrip('%') == "" else float(self.entries["Volatilidade"][i].get().rstrip('%')) / 100,
                    f'maturidade{i}'  : "" if self.entries["Maturidade"][i].get() == "" else float(self.entries["Maturidade"][i].get()),
                    f'juros{i}'       : "" if self.entries["Juros"][i].get().rstrip('%') == "" else float(self.entries["Juros"][i].get().rstrip('%')) / 100}
            dic.update(dic_)
        return dic