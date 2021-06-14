import os
import time

def header(url):
    limpar_tela()
    if not url:
        url = ''
    print(f'''
          ################################################################################################
                                                    WebCrawler                        {url}
          ################################################################################################
          ''')
   
def lista_opcoes(opcoes):    
      
    for op in opcoes:
        print(f'                                        {op}')
  
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
    opcoes = ['1 - Adicionar URL.','2 - Listar todos os links.','99 - sair']    
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
    quantidade = len(urls)
           
    # Controle de paginação.
    inicial = 0
    final = 20
    
    op = input_data(f' {quantidade} de links encontrados. Exibir na tela? (S - Sim)')
    
    if op.lower() == 's':
        exibir = True
    else:
        exibir = False
        
    while exibir:
        
        header('')
       
        for i in range(inicial, final):
            
            if i >= quantidade:
                continue
            
            print('                 {} - {} -> {}'.format(i+1,urls[i]['text'], urls[i]['href']))
        
        print(f'''
                                {quantidade} links localizados.
              ''')
        
        op = input_data('Aperte Enter para próxima página ou 99 para sair.')
        if op == '99':
            break
        else:
            inicial = final
            final = inicial + 20
            if final > quantidade:
                mensagem('Todos os dados já foram exibidos!')
                break
    
        
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    
