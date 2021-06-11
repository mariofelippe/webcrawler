import os

def menu_princial():
    
    # Limpa a tela do terminal.
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print('############################################')
    print('                WebCrawler                  ')
    print('############################################')

    print('1 - Obter informações da página.')
    print('99 - Sair.\n')
    op = input('Informe a opção: ')
    return op

def opcao_1():
    
    # Limpa a tela do terminal.
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print('############################################')
    print('                WebCrawler                  ')
    print('############################################')

    url = input('Informe a URL: ')
    return url