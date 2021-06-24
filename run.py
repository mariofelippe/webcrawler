from app import main
import sys

def star_app():
    
    # Pega os parametros do terminal.
    paramns = sys.argv
    
    if len(paramns) > 1:
        if paramns[1] != '-t':
            print('\nParametro informado inválido!')
            print('-t          Para iniciar o programa em modo terminal.\n')
        else:
            main.start_terminal()
    else:
        main.start_web()


if __name__ == '__main__':
    star_app()