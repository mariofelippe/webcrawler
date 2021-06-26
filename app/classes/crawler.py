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
            self.__html = ''
            
            

    def __format_html(self):
        """
        Instancia a classe BeautifulSoup e retorna o seu objeto.

        Returns:
            [obj]: Objeto da classe BeautifilSoup.
        """
        
        try:
            self.__html = self.__req.text 
            self.__html = BeautifulSoup(self.__html, 'html.parser')
            return self.__html
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
            self.__urls = self.__html.find_all('a')
            lista_urls = []
            
            
            
            for url in self.__urls:
                
                # Pega a propriedade href e o texto da tag "a".
                self.__href = url.get('href')
                self.__text = url.get_text().strip()
                self.__title = url.get('title')
                
                if self.__href == None:
                   continue
               
                if self.__text == '':
                    if self.__title:
                        self.__text = self.__title
                    else:
                        self.__text = ''
                # Limpa os parametros passados pela url caso limpa_parametros=True.
                if limpa_parametros:
                    self.__href = self.__href.split('?')[0]
                
                # Verifica se a URL está completa (http://url.com/)
                if self.__href.split(':')[0] not in ['http','https']:
                    self.__href = f'{self.get_dominio()}{self.__href}'
                self.trata_url(self.__href)
                
                if text:
                    if {'text':self.__text,'href':self.__href} not in lista_urls: # Trata possíveis duplicitadades
                        lista_urls.append({'text':self.__text,'href':self.__href})
                else:
                    if self.__href not in lista_urls:
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
    
    
    def get_meta(self):
        """ Pega as tag meta de uma página.
        Returns:
            [dic]: Dados das metas da página.
        """
        dados = dict()
        if self.__html:
            metas = self.__html.find_all('meta')
        else:
            return None     
        lista_nome = []
        lista_property = []
        http_equiv = []
        char = ''   
        
        for meta in metas:
            
            charset =  meta.get('charset')
            content = meta.get('content')
            name = meta.get('name')
            prop = meta.get('property')
            valor_id = meta.get('id')
            equival = meta.get('http-equiv')
            
            get = False
                     
            if charset:                
                char = charset
                get = True
            
            if name:
                lista_nome.append({name : content})
                get = True
            
            if prop:
                lista_property.append({prop : content})
                get = True
                
            if equival:
                http_equiv.append({equival : content})                
                get = True
                           
        dados['charset'] = char
        dados['name'] = lista_nome
        dados['property'] = lista_property
        dados['http-equiv'] = http_equiv
        
        return dados
            
           
    def get_info(self):
        
        """ Pega as info básicas da página.
        Returns:
            [dic]: Dados básicos de página. (nome, título, descrição)
        """       
        
        data = self.get_meta()
        info = dict() 
        
        if not data:
              return None
               
        for dado in data['name']:
            
            if 'title' in dado.keys():
                info['title'] = dado['title']
                       
            if 'description' in dado.keys():
                info['description'] = dado['description']
                    
        for dado in data['property']:
            
            if 'og:title' in dado.keys():
                info['title'] = dado['og:title']
                
            if 'og:site_name' in dado.keys():
                info['site_name'] = dado['og:site_name']
            
            if 'og:url' in dado.keys():
                info['url'] = dado['og:url']
                  
        return(info)
        
        
    def get_titles_page(self) -> list:
        """
        Pega as tags de título da página.
        Returns:
            [list]: Lista de títulos da página.
        """
        
        lista_titulo = []
        
        for i in range(1,7):                   
            self.__h = self.__html.find_all(f'h{i}')          
                    
            for tag in self.__h:                
                lista_titulo.append(tag.get_text().strip())
               
        return lista_titulo
    
    
    def get_images_page(self):
        """ Pega o text e a url das imagens da página.
        Returns:
            [list]: Lista informações referente as imagens encontradas.
        """
               
        lista_images = []
        controle = []
        self.__images = self.__html.find_all('img')
        
               
        for img in self.__images:
            url_img = self.ajusta_url(img.get('src'))
            
            alt_img = img.get('alt')
            if alt_img not in controle:
                if alt_img:
                    controle.append(alt_img)
                    lista_images.append({'text':alt_img,'url':url_img})
        
        self.__images = self.__html.find_all('amp-img')
        
        for img in self.__images:
            url_img = self.ajusta_url(img.get('src'))
            alt_img = img.get('title')
            if alt_img not in controle:
                if alt_img:
                    controle.append(alt_img)
                    lista_images.append({'text':alt_img,'url':url_img})
                
        return lista_images
    
    
    def ajusta_url(self,url) -> str:
                
        if url.split(':')[0] not in ['http','https']:
            print(f'{self.get_dominio()}{url}')
            return f'{self.get_dominio()}{url}'
        
        return url