import os
import time

def header(url):
    limpar_tela()
    if not url:
        url = ''
    print(f'''
          ###########################################################################
                                           WebCrawler                    {url}
          ###########################################################################
          ''')
   
def lista_opcoes(opcoes):    
      
    for op in opcoes:
        print(f'                                {op}')
  
def mensagem(msg):
    os.system('cls' if os.name == 'nt' else 'clear')
    header('')
    print(f'''          
                                    {msg}
          
          ''')
    input_data('Aperte para continuar...')
    

def input_data(msg):
    
    entrada = input(f'\n                                {msg} ')
    return entrada

def menu_princial(url):
    
  
    header(url)
    opcoes = ['1 - Obter informações da URL.','2 - Listar todas os links.','99 - sair']    
    lista_opcoes(opcoes)
    
    op = input('''\n          Digite a opção: ''')
    return op


def opcao_1():
    
    header('')
    lista_opcoes(['99 - Sair.'])
    url = input_data('Informe a URL:')
    return url


def exibir_urls(urls):
    header('')
    for url in urls:
        print(f'            {url}')
    input_data('Aperte para continuar...')
    
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
    
