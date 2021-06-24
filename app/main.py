from app.controllers.terminal_controlle import TerminalController
from app import app


def start_terminal():
    terminal = TerminalController()
    terminal.init()
    
    
def start_web():
    app.create_app()