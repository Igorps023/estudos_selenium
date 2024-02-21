# %%
import pandas as pd
import numpy as np
import os
from pathlib import Path
import glob

import logging
logging.basicConfig(filename='myProgramLog.txt', level=logging.DEBUG, format='%(asctime)s -  %(levelname)s -  %(message)s')

logging.debug('Start of program')

# %%
arquivos = ['teste.csv', 'janela.csv', 'item.csv']
caminho = Path(r'C:\Users\stree\OneDrive\Desktop\XLSX')

for j in arquivos:
    print(Path( caminho.joinpath(j) ).as_posix() )

# %% [markdown]
# 

# %%
Path.cwd()

# %%
Path.home()

# %%
os.listdir(caminho)

# %%
list(caminho.glob('*EstadoSP*') )

# %%
#Gera uma lista com pastas, arquivos, etc.
arquivos_excel = os.listdir(caminho)
arquivos_excel

# %%
caminho = Path(r'C:\Users\stree\OneDrive\Desktop\XLSX')

filtro = list(
    filter(lambda x: os.path.isfile(os.path.join(caminho, x)), arquivos_excel)
)

#Printa cada item da lista que nao e um arquivo
print("List of files:")
for file_name in filtro:
    print(file_name)

# %%


# %%



