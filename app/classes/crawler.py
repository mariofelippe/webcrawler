import requests
from bs4 import BeautifulSoup
import re

class Crawler():
    
    def __init__(self):
        
        self.__headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    
    def get_page(self,url):
        """
        Faz a requisição para a URL específica.

        Args:
            url ([str]): URL da página a ser verificada.
        """
                       
        self.__url = self.trata_url(url)
        
        try:
            self.__req = requests.get(self.__url,headers=self.__headers)
            self.__format_html()
        except Exception as erro:
            print(f'Erro ao tentar conectar \"{self.__url}\"! {erro}')
            
            

    def __format_html(self):
        """
        Instancia a classe BeautifulSoup e retorna o seu objeto.

        Returns:
            [obj]: Objeto da classe BeautifilSoup.
        """
        
        try:
            self.html = self.__req.text 
            self.html = BeautifulSoup(self.html, 'html.parser')
            return self.html
        except Exception as erro:
            print(f'Erro ao tentar criar o html! {erro}')
            
            
    def get_urls(self,text=False, limpa_parametros=False) -> list:
        """
        Busca todos as URLs de uma pagina WEB.

        Args:
            text (bool, optional): Retorna o text da tag <a>. Exemplo <a href="http://exemplo.com">Exemplo</a>
            Retorno [{'text': 'Exemplo', 'href': 'http://exemplo.com'}]
            
            limpa_parametros (bool, optional): Limpa os parametros contidos em ume URL. Defaults to False.

        Returns:
            [list]: Lista de URLs presentes na página.
        """
        
        try:
            self.__urls = self.html.find_all('a')
            lista_urls = []
            
            for url in self.__urls:
                
                # Pega a propriedade href e o texto da tag "a".
                self.__href = url.get('href')
                self.__text = url.get_text().strip()
                
                # Limpa os parametros passados pela url caso limpa_parametros=True.
                if limpa_parametros:
                    self.__href = self.__href.split('?')[0]
                
                # Verifica se a URL está completa (http://url.com/)
                if self.__href.split(':')[0] not in ['http','https']:
                    self.__href = f'{self.get_dominio()}{self.__href}'
                self.trata_url(self.__href)
                if text:
                    lista_urls.append({'text':self.__text,'href':self.__href})
                else:
                    lista_urls.append(self.__href)
            
            return lista_urls
        
        except Exception as erro:
            print(f'Erro ao obter as URLs! {erro}')
        
    def trata_url(self, url) -> str:
        """
        Verifica se a URL possui o padrão http e https.

        Args:
            url ([str]): URL a ser verificada.
            
        Returns:
            [str]: [description]
        """
        
        # Verificar se url é completa.
        if '://' in url:
            return url
        
        return f'http://{url}'
    
    
    def get_dominio(self) -> str:
        """
        Pega o domínio da URL verificada.

        Returns:
            [srt]: Domínio da URL verificada.
        """
                       
        # Pega protocolo e o domínio da URL.
        self.__protocolo = re.split(r'/', self.__url)[0]
        self.__dominio = re.split(r'/',  self.__url)[2]
        self.__dominio = f'{self.__protocolo}//{self.__dominio}'
        
        return self.__dominio