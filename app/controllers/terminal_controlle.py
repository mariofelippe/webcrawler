from app.views import terminal

class TerminalController():
    
    def init(self):
        op = terminal.menu_princial()
        print(op)

        op = f'terminal.opcao_{op}()'
        exec(op)
