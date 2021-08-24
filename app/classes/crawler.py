import requests
from bs4 import BeautifulSoup
import re

class Crawler():
    
    def __init__(self):
        
        self.__headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
  
    def get_page(self,url) -> bool:
        """ Faz a requisição para a URL específica.

        Args:
            url ([str]): URL da página a ser verificada.

        Returns:
            [bool]: True se a requisição for com sucesso e False se houve erro.
        """
                       
        self.__url = self.trata_url(url)
        
        try:
            self.__req = requests.get(self.__url,headers=self.__headers,timeout=20)
            self.__format_html()
            return True
        except Exception as erro:
            print(f'Erro ao tentar conectar \"{self.__url}\"! {erro}')
            self.__html = ''
            return False
            
            

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
            controle = []
            
            
            for url in self.__urls:
                
                # Pega a propriedade href e o texto da tag "a".
                self.__href = url.get('href')
                self.__text = url.get_text().strip()
                self.__title = url.get('title')
                self.__span = url.span
                self.__amp_img = url.find('amp-img')
                self.__img = url.find('img')
                
                # Inicializa as variavies img
                
                self.__url_image = ''
                self.__alt_image = ''
                
                if self.__amp_img:
                    self.__url_image = self.__amp_img.get('src')
                    self.__alt_image = self.__amp_img.get('alt')
                
                if self.__img:
                    self.__url_image = self.__img.get('src')
                    self.__alt_image = self.__img.get('alt')
                
                if self.__alt_image == None:
                    self.__alt_image = ''
                                
                if self.__href == None:
                   continue
               
                if self.__text == '':
                    if self.__title:
                        self.__text = self.__title
                    else:
                        self.__text = ''
                
                if self.__span != None:
                    if self.__text != self.__span.get_text().strip():
                        self.__span = self.__span.get_text().strip()
                    else:
                        self.__span = ''
                else:
                    self.__span = ''
                
                # Remove espaços
                self.__text = self.remove_espacos(self.__text)
                
                # Limpa os parametros passados pela url caso limpa_parametros=True.
                if limpa_parametros:
                    self.__href = self.__href.split('?')[0]
                
                # Verifica se a URL está completa (http://url.com/)
                if self.__href.split(':')[0] not in ['http','https']:
                    self.__href = f'{self.get_dominio()}{self.__href}'
                self.trata_url(self.__href)
                
                if text:
                    if self.__text not in controle: # Trata possíveis duplicitadades
                        lista_urls.append({'text': self.__text,
                                           'span': self.__span,
                                           'href': self.__href,
                                           'url_image': self.__url_image,
                                           'alt_image': self.__alt_image                                           
                                           })
                        controle.append(self.__text)
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
                
            if 'viewport' in dado.keys():
                info['viewport'] = dado['viewport']
                
            if 'theme-color' in dado.keys():
                info['theme-color'] = dado['theme-color']    
                   
        for dado in data['property']:
            
            if 'og:title' in dado.keys():
                info['title'] = dado['og:title']
                
            if 'og:site_name' in dado.keys():
                info['site_name'] = dado['og:site_name']
            
            if 'og:url' in dado.keys():
                info['url'] = dado['og:url']
                
            if 'og:locale' in dado.keys():
                info['locale'] = dado['og:locale']
                
            if 'og:type' in dado.keys():
                info['type'] = dado['og:type']
                
            if 'og:image' in dado.keys():
                info['image'] = dado['og:image']
        
        if data['charset']:
            info['charset'] = data['charset']
        
        return(info)
        
        
    def get_titles_page(self) -> list:
        """
        Pega as tags de título da página.
        Returns:
            [list]: Lista de títulos da página.
        """
        
        # Verifica se o html foi retornado e caso não não faça nada.
        if not self.__html:
            return
        
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
        
        if url == None:
            return ''
                
        if url.split(':')[0] not in ['http','https']:
            print(f'{self.get_dominio()}{url}')
            return f'{self.get_dominio()}{url}'
        
        return url
    
    def get_nav_page(self, url=False):
        
        if not self.__html:
            return
                
        self.__lista_nav = []
        self.__controle = []
        self.__nav = self.__html.nav
      
        if self.__nav == None or self.__nav == '':
            self.__nav = self.__html.header
        
        if not self.__nav:
            return 
        
        self.__urls = self.__nav.find_all('a')
        
      
       
        for url in self.__urls:
            
            self.__url = url.get('href')
            self.__text = url.get_text().strip()
            self.__title = url.get('title')
            
            if self.__text in self.__controle:
                continue
            
            if self.__text == None or self.__text == '':
                
                self.__text = self.__title
                
                if self.__text == None or self.__text == '':
                    continue
            
            self.__controle.append(self.__text) 
            if url == True:          
                self.__lista_nav.append({'title':self.__text, 'url':self.__url})
            else:
                 self.__lista_nav.append(self.__text)
        # Realiza o processo para a tag header.
            
        self.__nav = self.__html.header
        self.__urls = self.__nav.find_all('a')
        
       
        for url in self.__urls:
            
            self.__url = url.get('href')
            self.__text = url.get_text().strip()
            self.__title = url.get('title')
            
            if self.__text in self.__controle:
                continue
            
            if self.__text == None or self.__text == '':
                
                self.__text = self.__title
                
                if self.__text == None or self.__text == '':
                    continue
            
            self.__controle.append(self.__text)           
            if url == True:          
                self.__lista_nav.append({'title':self.__text, 'url':self.__url})
            else:
                 self.__lista_nav.append(self.__text)
        
        return self.__lista_nav
            
    def get_img_urls(self):
        
        self.__lista_images = []
        self.__controle = []
        self.__a = self.__html.find_all('a')
        
        for item in self.__a:
            href = item.get('href')
            tag_amp_img = item.find('amp-img')
            tag_img = item.find('img')
            text = item.get_text().strip()            
            
                  
            if tag_amp_img:                              
                url_image = tag_amp_img.get('src')
                alt = tag_amp_img.get('alt')
                text = self.remove_espacos(text)
                
                self.__lista_images.append({'href':href, 
                                            'url_image':url_image,
                                            'text': text,
                                            'alt':alt})

            if tag_img:                              
                url_image = tag_img.get('src')
                alt = tag_img.get('alt')
                text = self.remove_espacos(text)
                
                self.__lista_images.append({'href':href, 
                                            'url_image':url_image,
                                            'text': text,
                                            'alt':alt})
        return self.__lista_images
             
    def remove_espacos(self,text) -> str:
        """
        Remove os excessos de espacos em textos dentro de tags.
        """
        regra = '\s{2,}'
        if text:
            espaco = re.search(regra, str(text))
            if espaco:
                espaco = espaco.group()
                text = text.replace(espaco, ' | ')
        
        return text