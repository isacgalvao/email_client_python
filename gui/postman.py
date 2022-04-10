# Lib que envia emails utilizando o protocolo SMTP utilizando sockets
# FEITO COM CARINHO POR: ISAC <3

import socket
import base64
import ssl

#CONSTANTES
SSLSocket = 1
DefaultSocket = 2

#Informações do servidor
class ServerInfo:
    server_adress = str
    port = int
    recv_size: int
    def __init__(self, server_adress, port, recv_size = 1024):
        self.recv_size = recv_size
        self.server_adress = server_adress
        if isinstance(port, int):
            self.port = port
        else:
            self.port = int(port)


    def test(self):
        # needs to be implemented
        pass

#Credenciais
class Credentials:
    _email: str
    _senha: str

    def __init__(self, email, password):
        self._email = email
        self._senha = password

    def getEmail(self):
        return self._email

    def getSenha(self):
        return self._senha

#Conteudo do email
class EmailContent:
    def __init__(self, email_destinatario, assunto, mensagem):
        self.email_destinatario = email_destinatario
        self.assunto = assunto
        self.mensagem = mensagem

#Carteiro
class Postman:
    #Objetos
    _emailContent = None
    _serverInfo = None
    _credentials = None
    _socket = None
    logs = None

    _data = None
    _recv_size: int

    def __init__(self):
        pass

    def attachCredentials(self, credentials):
        if type(credentials) != Credentials:
            raise BaseException("Anexe uma instancia de Credentials")
        else:
            self._credentials = credentials

    def attachEmailContent(self, emailContet):
        if type(emailContet) != EmailContent:
            raise BaseException("Anexe uma instancia de EmailContent!!")
        else:
            self._emailContent = emailContet
            self._format_data()
        pass

    def attachServerInfo(self, serverInfo):
        if type(serverInfo) != ServerInfo:
            raise BaseException("[Error] Anexe uma instancia de ServerInfo")
        else:
            self._recv_size = serverInfo.recv_size
            self._serverInfo = serverInfo
        pass

    def _connectSSL(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv23)
        self._socket.connect((self._serverInfo.server_adress, self._serverInfo.port))
        server_response = self._socket.recv(self._recv_size).decode()
        if server_response[:3] != '220':
            raise Exception(f"O servidor não respondeu com 220.\nResposta do servidor: {server_response}")
        pass

    def _connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._serverInfo.server_adress, self._serverInfo.port))
        server_response = self._socket.recv(self._recv_size).decode()
        if server_response[:3] != '220':
            raise Exception(f"O servidor não respondeu com 220.\nResposta do servidor: {server_response}")
        pass

    def _format_data(self):
        self._data = "Subject: " + self._emailContent.assunto + "\n\n" + self._emailContent.mensagem
        pass

    def _auth_hash(self, email, senha):
        base64_str = ("\x00" + email + "\x00" + senha).encode()
        base64_str = base64.b64encode(base64_str)
        return "AUTH PLAIN " + base64_str.decode() + "\r\n"

    def _verify_objs(self):
        err = []
        if not isinstance(self._emailContent, EmailContent):
            err.append("EmailContent")
        if not isinstance(self._serverInfo, ServerInfo):
            err.append("ServerInfo")
        if not isinstance(self._credentials, Credentials):
            err.append("Credentials")
        if len(err) > 0:
            raise TypeError(f"Objetos obrigatórios não foram passados: {err}")

    def send_mail(self, socketType = SSLSocket):
        self._verify_objs()

        if socketType == SSLSocket:
            try:
                self._connectSSL()
            except:
                self.logs = ["Não foi possivel conectar com servidor informado!"]
                return False
        elif socketType == DefaultSocket:
            try:
                self._connect()
            except:
                self.logs = ["Não foi possivel conectar com servidor informado!"]
                return False

        auth = self._auth_hash(self._credentials.getEmail(), self._credentials.getSenha())

        logs = []

        self._socket.send("HELO cliente\r\n".encode())
        ehlo_response = self._socket.recv(self._recv_size)
        print(ehlo_response.decode())
        logs.append("HELO: "+ehlo_response.decode())

        self._socket.send(auth.encode())
        auth_response = self._socket.recv(self._recv_size)
        print("AUTH Response: "+auth_response.decode())
        logs.append("AUTH: "+auth_response.decode())
        if auth_response.decode()[:3] == '534':
            print("\033[1;31mVERIFIQUE SE A CONTA PODE RECEBER ACESSO DE APPS MENOS SEGUROS\033[0m\n")
        if auth_response.decode()[:3] == '535':
            print("\033[1;31mUSUARIO OU SENHA INCORRETOS\033[0m\n")

        self._socket.send(str("MAIL FROM: <" + self._credentials.getEmail() + ">\r\n").encode())
        mail_from_response = self._socket.recv(self._recv_size)
        print("MAIL FROM Response: " + mail_from_response.decode())
        logs.append("MAIL FROM: "+mail_from_response.decode())

        self._socket.send(str("RCPT TO: <" + self._emailContent.email_destinatario + ">\r\n").encode())
        rcp_response = self._socket.recv(self._recv_size)
        print("RCPT TO Response: " + rcp_response.decode())
        logs.append("RCPT TO: "+rcp_response.decode())

        self._socket.send("DATA\r\n".encode())
        data1_response = self._socket.recv(self._recv_size)
        print("DATA Response: " + data1_response.decode())
        logs.append("DATA: "+data1_response.decode())

        self._socket.send(str(self._data + "\r\n.\r\n").encode())
        data2_response = self._socket.recv(self._recv_size)
        print("RAW DATA Response: " + data2_response.decode())
        logs.append("RAW DATA: "+data2_response.decode())

        self._socket.send("QUIT\r\n".encode())
        quit_response = self._socket.recv(self._recv_size)
        print("QUIT Response: " + quit_response.decode())
        logs.append("QUIT: "+quit_response.decode())
        if quit_response.decode()[:3] == '502' or quit_response.decode()[:3] == '500':
            print("\033[1;31mFALHA AO ENVIAR O EMAIL\nVERIFIQUE AS RESPOSTAS DO SERVIDOR\033[0m")
            self.logs = logs
            return False
        else:
            print("\033[1;92mEMAIL ENVIADO COM SUCESSO\033[0m")
            return True

#postman = Postman()
#server = ServerInfo(server_adress="smtp.gmail.com", port=465)
#content = EmailContent(email_destinatario="teste@gmail.com", assunto="Isso é um teste", mensagem="aosdksadas")
#credenciais = Credentials(email="et8873626@gmail.com", password="Et!.88736264")
#postman.attachEmailContent(content)
#postman.attachServerInfo(server)
#postman.attachCredentials(credenciais)
#postman.send_mail()