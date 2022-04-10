import pathlib
import tkinter.messagebox
import webbrowser
import pygubu
import json

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gui.ui"
CONFIG_FILE = "config.cfg"

#custom functions
def show_file_error():
    tkinter.messagebox.showerror(title="Atenção!", message="Ocorreu um erro ao tentar salvar os dados :(")

def show_port_error():
    tkinter.messagebox.showerror(title="Atenção!", message="A porta precisa ser um número")

def show_error():
    tkinter.messagebox.showerror(title="Atenção!", message="Preencha todos os campos")

def show_sucess():
    tkinter.messagebox.showinfo(title="Aviso!",message="Dados salvos com sucesso!!")

def recuperar_dados():
    try:
        f = open(CONFIG_FILE, "r")
        dados = json.loads(f.read())
        return dados
    except:
        return None

def salvar_dados(email, senha, servidor, porta):
    try:
        f = open(CONFIG_FILE, "w")
        try:
            f.write(json.dumps(dict(email=email, senha=senha, servidor=servidor, porta=porta)))
        except:
            show_file_error()
        finally:
            f.close()
    except:
        show_file_error()
    pass

class GuiApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('tela2', master)

        self.email_ = builder.get_object('entry7')
        self.senha = builder.get_object('entry8')
        self.servidor_smtp = builder.get_object('entry9')
        self.porta = builder.get_object('entry10')
        builder.import_variables(self, ['email_', 'senha', 'servidor_smtp', 'porta'])

        builder.connect_callbacks(self)
    
    def run(self):
        dados = recuperar_dados()
        if dados:
            self.email_.set(dados["email"])
            self.senha.set(dados["senha"])
            self.servidor_smtp.set(dados["servidor"])
            self.porta.set(dados["porta"])

        self.mainwindow.mainloop()

    def on_alterar(self):
        email = self.email_.get()
        senha = self.senha.get()
        porta = self.porta.get()
        servidor_smtp = self.servidor_smtp.get()

        if not email or str(email).isspace():
            show_error()
        elif not senha or str(senha).isspace():
            show_error()
        elif not porta or str(porta).isspace() or not str(porta).isdigit():
            if not str(self.porta.get()).isdigit():
                show_port_error()
            else:
                show_error()
        elif not servidor_smtp or str(servidor_smtp).isspace():
            show_error()
        else:
            salvar_dados(email, senha, servidor_smtp, porta)
            show_sucess()
            self.mainwindow.destroy()


    def on_tutorial(self):
        webbrowser.open_new_tab("https://support.google.com/accounts/answer/6010255?hl=pt")
        pass


if __name__ == '__main__':
    app = GuiApp()
    app.run()

