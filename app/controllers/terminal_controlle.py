from app.views import terminal
from app.classes.crawler import Crawler

class TerminalController():
    
    def main(self):
        
        crawler = Crawler()
        url = None
        while True:
            
            
            
            op = terminal.menu_princial(url)
            if op == '99':
                terminal.mensagem('Fechando o programa...')
                terminal.limpar_tela()
                break
            
            if op == '1':
                urls = None
                retorno = terminal.adicionar_url()
                if not retorno:
                    terminal.mensagem('Informação inválida!')
                elif retorno == '99':
                    terminal.mensagem('Fechando o programa...')
                    terminal.limpar_tela()
                    break
                else:
                    try:
                        crawler.get_page(retorno)
                        #urls = crawler.get_urls(text=True, limpa_parametros=True)
                    except:
                        terminal.mensagem('Erro ao fazer a requisição!')
                    url = retorno
                    
                    dados = crawler.get_info()
                    terminal.exibir_info(dados)
                    
                    
            
            if op == '2':
                
                if not url:
                    retorno = terminal.adicionar_url()
                    url = retorno
                    if retorno == '99':
                        terminal.mensagem('Fechando o programa...')
                        terminal.limpar_tela()
                        break  
                    else:
                        crawler.get_page(retorno)
                        urls = crawler.get_urls(text=True, limpa_parametros=True)
                        terminal.exibir_urls(urls, url)
                        url = retorno
                        
                        
                        retorno = terminal.salvar_arquivo()
                        if retorno.lower() == 's':
                            self.exportar_dados(urls)
                                                                   
                else:
                     #crawler.get_page(url)
                     urls = crawler.get_urls(text=True, limpa_parametros=True)
                     
                     terminal.exibir_urls(urls, url)
                     retorno = terminal.salvar_arquivo()
                     if retorno.lower() == 's':
                         self.exportar_dados(urls)
                    
            
            if op not in ['1','2','99']:
                terminal.mensagem('Opção inválida!')        
           

    def exportar_dados(self, urls):
        
        
        nome_arquivo = terminal.input_data('Informe o nome do arquivo:').strip()
        
        try:
            arquivo = open('tmp\\{}.txt'.format(nome_arquivo),'w',encoding='utf')
            for linha in urls:
                arquivo.write('{}   ------>  {}\n'.format(str(linha['text'].replace(';',',')),linha['href']))
            arquivo.close()
        except Exception as erro:
            terminal.mensagem(f'Erro ao salvar arquivo. {erro}')    
    
    def init(self):
        self.main()