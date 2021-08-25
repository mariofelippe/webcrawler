# WebCrawler

Programa desenvolvido com objetivo de estudo.

## Objetivo

1. Aprimorar os conhecimento em pyhton.
2. Aplicar os conhecimentos adquiridos até o momento.
3. Desenvolver um código organizado.
4. Desenvolver o projeto com diretórios organizados.

## Implementação 

O projeto deve possuir alguns requisitos na implementação com o objeto de aplicar os conhecimentos adquiridos durante o estudos de algumas tecnologias, padrões e frameworks.

- [X] Utilizar o GIT e Github para controle do cógido.
- [X] Possuir um menu no terminal.
- [X] Possuir uma API.
- [X] Possuir um Front-End Web.
- [X] Utilizar Expressões regulares no projeto.
- [X] Trabalhar com manipulação de arquivo.

## Utilização

1. Instalando as bibliotecas utilizadas.

    `pip install -r requirements.txt`

2. Executando em modo terminal.

    `python run.py -t`

3. Execução sevidor web local.

    `python run.py`


## API

Uma API básica foi desenvolvida. E com as URLs abaixo é possível acessar algumas funções do sistema.

O parâmetro "URL" é informado pelo usuário e o sistema retorna algumas informações contidas na página como title, description, site_name, url e etc.

1. Consultar informações da URL.
```
GET http://localhost/api/info/(url)
```
2. Retornando as URLs da página.
```
GET http://localhost/api/links/(url)
```
3. Retornando as URLs da página com mais informações.
```
GET http://localhost/api/links/(url)/text
```
4. Retornando as imagens da página.
```
GET http://localhost/api/images/(url)