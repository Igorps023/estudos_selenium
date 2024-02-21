# %%
#Bibliotecas
# import pandas as pd
#from bs4 import BeautifulSoup
import pytz
from datetime import datetime 
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select


date_now = datetime.now(pytz.timezone('America/Sao_Paulo'))

date_yesterday = date_now - timedelta(days=1)
start_of_month = date_now.replace(day=1)

start_of_month = start_of_month.strftime('%d/%m/%y')
date_yesterday = date_yesterday.strftime('%d/%m/%y')


url = 'https://gigroup-c2c.involves.com/login/#/'
driver = Firefox()
driver.get(url)
sleep(1.2)

# %%
userlogin = 'igor.pereirasilva'
userpassword = '123456'

#Encontrar elementos
#Login e Senha
field_login = driver.find_elements(By.XPATH, '//input[@id="username"]')[0]
field_password = driver.find_elements(By.XPATH, '//input[@id="password"]')[0]
field_login.send_keys(userlogin)
field_password.send_keys(userpassword)
btn_login = driver.find_elements(By.XPATH, '//button[@class="inv-btn submit-button"]')[0].click()

driver.implicitly_wait(10)

procura = driver.find_elements(By.XPATH, \
                    '//*[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "danke")]')

procura[0].click()


#Menu esquerdo elemento
teste = driver.find_element(By.XPATH, \
                            '//div[@class="js-menu ng-scope"]//*[contains(text(), "Dashboard")]')

# Use ActionChains to perform a hover action
action = ActionChains(driver)
action.move_to_element(teste).perform()

# Wait for the body to have the class "isMenuOpen"
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, '//body[@class="isMenuOpen"]')))

#Categoria 1 Menu
Roteiros_e_visitas = driver.find_element(By.XPATH, \
                                    '//body[@class="isMenuOpen"]//div[@class="js-menu ng-scope"]//*[contains(text(), "Roteiros e visitas")]')

Roteiros_e_visitas.click()

#SubCategoria 1 Menu
Painel_de_visitas = driver.find_element(By.XPATH, \
                                         '//ap-menu-list-subitem//div[@class="ng-scope"]//*[@href="#!/app/~2F3Js8c5PAuuyjaQcA8HMKQ%3D%3D/paineldevisitas"]')

Painel_de_visitas.click()

# %%
#Retorna lista com os dois campos de input data, campos de placeholder separa em 'De' e 'Até'
date_filter_de = driver.find_element(By.XPATH, \
                                    '//div[@class="c-data-period ng-scope ng-isolate-scope"]//*[@class="c-input c-datepicker--filter ng-not-empty ng-valid-required ng-valid-date" and @placeholder="De"]')

date_filter_de.clear() #Limpar a data
date_filter_de.send_keys(start_of_month)


date_filter_ate = driver.find_element(By.XPATH, \
                                    '//div[@class="c-data-period ng-scope ng-isolate-scope"]//*[@class="c-input c-datepicker--filter ng-not-empty ng-valid-required ng-valid-date" and @placeholder="Até"]')

date_filter_ate.clear() #Limpar a data
date_filter_ate.send_keys(date_yesterday)

# %%
#Elemento Botao Pesquisar (DIVs Botoes Incluso)
btn = driver.find_elements(By.XPATH, 
                           '//div[@class="stg-filter-action ng-isolate-scope"]/ap-button[@class="ng-scope ng-isolate-scope"]//*[contains(text(), "Pesquisar")]')
btn[0].click()

# %%
#Botao inferior opcoes de exportacao
sleep(4)
btn_options_closed = driver.find_element(By.XPATH,
                                   '//div[@class="c-view__footer-options ng-scope dropdown"]')

btn_options_closed.click()

# %%
#Clicar em relatorio gerencial
sleep(3)
btn_options_opened = driver.find_elements(By.XPATH,
                                         '//div[@class="c-view__footer-options ng-scope dropdown open"]//ul[@class="dropdown-menu"]//*[contains(text(), "Relatório Gerencial")]')

btn_options_opened[0].click()

# %%
#Adicionar coluna de ID_DO_PDV
#Seletor Colunas Ocultas

#Elemento de texto arvore
sleep(2)
Texto_Colunas_Ocultas = driver.find_element(By.XPATH,
                                  '//h4/translate[contains(text(), "Colunas ocultas")]')

#Elemento da arvore que contem lista de itens ocultados do relatorio
item_avo = Texto_Colunas_Ocultas.find_element(By.XPATH, '../..') # 2 itens acima

botao_id_pdv = item_avo.find_element(By.XPATH, './div/div/button')
botao_id_pdv.click()

# %%
#Clicar no botao confirmar para baixar o relatorio
botao_confirmar = driver.find_element(By.XPATH,
                                       '//div[@class="c-view__footer-actions ng-scope ng-isolate-scope"]//*[contains(text(), "Confirmar")]')

botao_confirmar.click()


#Esperar fim do download e fechar Browser
sleep(3.5)
driver.close()