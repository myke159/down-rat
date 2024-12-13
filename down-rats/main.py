
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def pasta(nome_pasta):
    texto = nome_pasta

    path = os.getcwdb()
    path = str(path).replace(
        '\\\\', '\\').replace(
            'b', '').replace(
                "'", ''
            )
    return path+texto

def ler_rats(name):
    with open(f'{name}', 'r') as arq:
        rats = arq.readlines()
        return rats
    
download_dir = pasta('\\baixados')
# print(download_dir)

# sys.exit()

# todas as XPATHS
enderecos = {
    'pesquisa_todas_O.S': '//*[@id="pesq_os"]',
    'busca_por_chamado': '//*[@id="pesq_os"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input', #Press enter dps
    'lupa': '/html/body/table[3]/tbody/tr/td[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[8]/span/a', #Contem o ID do chamado (LUPA)
    'reimprimir_comprovante': '/html/body/table[3]/tbody/tr/td[2]/table[2]/tbody/tr/td/table[2]/tbody/tr[1]/td[2]/a', #ID do chamado
    'link_chamados': 'https://assist.positivotecnologia.com.br/bin/at/pesq_os.php',
    'link_down': 'https://assist.positivotecnologia.com.br/bin/at/comprovantes/gerarRatPdf.php?os_id={ID}'
    } 



options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

chrome_prefs = {
    "download.default_directory": download_dir,  # Define o diretório de download
    "download.prompt_for_download": False,  # Desativa a janela de prompt de download
    "plugins.always_open_pdf_externally": True,  # Força o Chrome a abrir PDFs externamente (sem abrir o visualizador)
    "download.directory_upgrade": True
}
options.add_experimental_option("prefs", chrome_prefs)

# Inicia o navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Acessa a página dos chamados no Assist
driver.get('https://assist.positivotecnologia.com.br/bin/at/pesq_os.php')
os.system('cls')
print("\n !!! LOGUE EM SUA CONTA !!! \n")
sleep(1)
#
input("Depois que conectar pressione ENTER para seguir!\n\n")

# print(chamados)
while True:
    chamados = ler_rats("rats.txt")
    for chamado in chamados:
        chamado = chamado.replace("\n", '')
        driver.get('https://assist.positivotecnologia.com.br/bin/at/pesq_os.php')
        try:
            campo_chamado = driver.find_element(By.XPATH, enderecos['busca_por_chamado'])
            campo_chamado.send_keys(chamado, Keys.RETURN)
        except:
            continue

        # input('Teste se foi: press enter')

        sleep(0.5)
        #Pegar o ID
        try:
            lupa_id = driver.find_element(By.XPATH, enderecos['lupa'])
        except:
            continue
        os.system('cls')
        href = lupa_id.get_attribute('href')
        novo_id = href.split('=')[1]

        # print(href)
        # input('Teste se foi: press enter')

        #Baixar o PDF
        driver.get(f'https://assist.positivotecnologia.com.br/bin/at/comprovantes/gerarRatPdf.php?os_id={novo_id}')

        # input('Teste se foi: press enter')
    status = str(input("Rodar novamente? \n SIM = [ENTER]\n NAO = [NAO]:    "))
    if status.upper() == 'NAO':
        break

# Para encerrar o programa
os.system('cls')
input("!! ENCERRANDO PROGRAMA !!")
sleep(2)

# Fecha o navegador
driver.quit()
