#UNIVERSIDADE FEDERAL DO SUL E SULDESTE DO PARÁ
#ENGENHARIA DA COMPUTAÇÃO - TURMA 2019
#PROFESSOR: GLEISON DE OLIVEIRA MEDEIROS
#DISCIPLINA: REDE DE COMPUTADORES
#ALUNOS: CRISTINA VITORIA LEAL, SAMUEL PATRICK SILVA, THIAGO ELEUTERIO, ISAC GALVÃO, MANOEL MALON COSTA, HENRIQUE PEREIRA

from socket import *
import base64
import ssl


server_info = ("smtp.gmail.com", 465)
socket = socket(AF_INET, SOCK_STREAM)

#criando um socket seguro - SSL
secure_socket = ssl.wrap_socket(socket, ssl_version=ssl.PROTOCOL_SSLv23)
secure_socket.connect(server_info)

#credenciais da conta
mail_from = "et8873626@gmail.com"
password = "Et!.8873626"

#input dos dados
mail_to = input("Digite o email do destinatario: ")
mail_subject = input("Digite o título do email: ")
mail_message = input("Digite a mensagem: ")

#montando a mensagem
data = "Subject: "+mail_subject+"\n\n"+mail_message

#codificando as credenciais
base64_str = ("\x00" + mail_from + "\x00" + password).encode()
base64_str = base64.b64encode(base64_str)
auth = "AUTH PLAIN "+base64_str.decode()+"\r\n"

#conexões
secure_socket.send("HELO et8873626\r\n".encode())
print("\nEHLO Response: " + secure_socket.recv(1024).decode())

secure_socket.send(auth.encode())
print("AUTH Response: " + secure_socket.recv(1024).decode())

secure_socket.send(str("MAIL FROM: <" + mail_from + ">\r\n").encode())
print("MAIL FROM Response: " + secure_socket.recv(1024).decode())

secure_socket.send(str("RCPT TO: <" + mail_to + ">\r\n").encode())
print("RCPT TO Response: " + secure_socket.recv(1024).decode())

secure_socket.send("DATA\r\n".encode())
print("DATA Response: " + secure_socket.recv(1024).decode())

secure_socket.send(str(data + "\r\n.\r\n").encode())
print("RAW DATA Response: " + secure_socket.recv(1024).decode())

#encerrando a comuinicação
secure_socket.send("QUIT\r\n".encode())
print("QUIT Response: " + secure_socket.recv(1024).decode())
print("\033[1;92mEMAIL ENVIADO COM SUCESSO\033[0m")