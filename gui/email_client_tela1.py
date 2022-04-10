#UNIVERSIDADE FEDERAL DO SUL E SULDESTE DO PARÁ
#ENGENHARIA DA COMPUTAÇÃO - TURMA 2019
#PROFESSOR: GLEISON DE OLIVEIRA MEDEIROS
#DISCIPLINA: REDE DE COMPUTADORES
#ALUNOS: CRISTINA VITORIA LEAL, SAMUEL PATRICK SILVA, THIAGO ELEUTERIO, ISAC GALVÃO, MANOEL MALON COSTA, HENRIQUE PEREIRA

#forçando imports para o pyinstaller construir o exe sem erros
import pygubu.builder.tkstdwidgets
import pygubu.builder.ttkstdwidgets

import pathlib
import sys
import os

import pygubu
import threading

import postman
import email_client_tela2
from postman import *
from tkinter import messagebox

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gui.ui"

#custom functions
def show_dest_error():
    messagebox.showerror(title="Atenção!", message="Preencha todos os campos")

def show_sucess():
    messagebox.showinfo(title="Sucesso!!", message="O email foi enviado com sucesso")

def show_error(mensagem):
    messagebox.showerror(title="Falha ao enviar email!!", message=str(mensagem))

class GuiApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('tela1', master)
        builder.connect_callbacks(self)

        if os.name == 'posix':
            _ = os.system('clear')
        else:
            _ = os.system('cls')

        self.destinatario = builder.get_object('entry4')
        self.assunto = builder.get_object('entry5')
        self.mensagem = builder.get_object('text1')
        self.botao_enviar = builder.get_object('button1')
        self.progress = builder.get_object('progressbar2')
        self.progress.place_forget()
        self.recuperar_dados()

    def recuperar_dados(self):
        try:
            dados = email_client_tela2.recuperar_dados()
            if dados != None:
                self.email = dados['email']
                self.senha = dados['senha']
                self.servidor = dados['servidor']
                self.porta = dados['porta']
            else:
                self.email = None
                self.senha = None
                self.servidor = None
                self.porta = None
        except:
            self.email = None
            self.senha = None
            self.servidor = None
            self.porta = None

    def on_alterar_email(self):
        alterar = email_client_tela2.GuiApp()
        alterar.run()
        pass

    def on_exit(self):
        sys.exit()
        pass

    def on_enviar(self):
        self.recuperar_dados()
        if self.email == None or self.senha == None or self.porta == None or self.servidor == None:
            messagebox.showerror(title="Atenção!", message="Insira todos os dados na opção \"Alterar Configurações\"!!")
            return

        self.refresh()
        self.botao_enviar['state'] = 'disabled'
        self.progress.place(relx=0.083, rely=0.79)
        self.progress.start(10)
        threading.Thread(target=self.enviar).start()

    def run(self):
        self.mainwindow.mainloop()

    def refresh(self):
        self.mainwindow.update()
        self.mainwindow.after(1000, self.refresh)

    def enviar(self):
        destinatario = self.destinatario.get()
        assunto = self.assunto.get()
        mensagem = self.mensagem.get('0.0', 'end')

        if not destinatario or str(destinatario).isspace() or not assunto or str(assunto).isspace() or not mensagem or str(mensagem).isspace():
            self.progress.place_forget()
            self.botao_enviar['state'] = 'normal'
            show_dest_error()
            return

        carteiro = Postman()
        server = ServerInfo(server_adress=self.servidor, port=self.porta)
        content = EmailContent(email_destinatario=destinatario, assunto=assunto, mensagem=mensagem)
        credenciais = Credentials(email=self.email, password=self.senha)
        carteiro.attachEmailContent(content)
        carteiro.attachServerInfo(server)
        carteiro.attachCredentials(credenciais)

        if carteiro.send_mail(postman.SSLSocket):
            show_sucess()
        else:
            show_error('\n'.join(carteiro.logs))
        self.progress.place_forget()
        self.botao_enviar['state'] = 'normal'



if __name__ == '__main__':
    app = GuiApp()
    app.run()

