from app.views import terminal
from app.classes.crawler import Crawler

class TerminalController():
    
    def init(self):
        
        crawler = Crawler()
        url = None
        while True:
            
            op = terminal.menu_princial(url)
            if op == '99':
                terminal.mensagem('Fechando o programa...')
                terminal.limpar_tela()
                break
            
            if op == '1':
                retorno = terminal.opcao_1()
                if retorno == '99':
                    terminal.mensagem('Fechando o programa...')
                    terminal.limpar_tela()
                    break
                else:
                    crawler.get_page(retorno)
                    urls = crawler.get_urls(text=True, limpa_parametros=True)
                    url = retorno
            
            if op == '2':
                if not url:
                    retorno = terminal.opcao_1()
                    if retorno == '99':
                        terminal.mensagem('Fechando o programa...')
                        terminal.limpar_tela()
                        break  
                    else:
                        crawler.get_page(retorno)
                        urls = crawler.get_urls(text=True, limpa_parametros=True)
                        terminal.exibir_urls(urls)
                        url = retorno  
                                         
                else:
                     terminal.exibir_urls(urls)
                    
           

