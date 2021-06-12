import requests
from bs4 import BeautifulSoup
import re

class Crawler():
    
    def __init__(self):
        
        self.__headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    
    def get_page(self,url):
                       
        self.__url = self.trata_url(url)
        
        try:
            self.__req = requests.get(self.__url,headers=self.__headers)
            self.__format_html()
        except Exception as erro:
            print(f'Erro ao tentar conectar \"{self.__url}\"! {erro}')
            

    def __format_html(self):
        try:
            self.html = self.__req.text
            self.html = BeautifulSoup(self.html, 'html.parser')
            return self.html
        except Exception as erro:
            print(f'Erro ao tentar criar o html! {erro}')
            
            
    def get_urls(self,text=False):
        
        try:
            self.__urls = self.html.find_all('a')
            lista_urls = []
            
            for url in self.__urls:
                self.__href = url.get('href')
                self.__text = url.get_text()
                
                # Verifica se a URL está completa (http://url.com/)
                if self.__href.split(':')[0] not in ['http','https']:
                    self.__href = f'{self.get_dominio()}{self.__href}'
                self.trata_url(self.__href)
                if text:
                    lista_urls.append({'text':self.__text,'href':self.__href})
                else:
                    lista_urls.append(self.__href)
            
            print(lista_urls)
        except Exception as erro:
            print(f'Erro ao obter as URLs! {erro}')
        
    def trata_url(self, url):
        
        # Verificar se url é completa.
        if '://' in url:
            return url
        
        return f'http://{url}'
    
    
    def get_dominio(self):
        
               
        # Pega o domínio da URL
        self.__protocolo = re.split(r'/', self.__url)[0]
        self.__dominio = re.split(r'/',  self.__url)[2]
        self.__dominio = f'{self.__protocolo}//{self.__dominio}'
        
        return self.__dominio