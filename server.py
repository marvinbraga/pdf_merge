import json
import socket
import traceback
from datetime import datetime

from pdf_union import PdfUnion


class ServerMergePdf:

    len_buffer = 10 ** 9

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('127.0.0.1', 8777))
        self.server.listen(5)

    def execute(self):
        while True:
            try:
                print(self.server_date_time(), 'Aguardando conexão com cliente.')
                # Aguarda por uma conexão.
                (client, address) = self.server.accept()
                print(self.server_date_time(), f'Conectado por {client}.')
                # Passa o cliente conectado.
                self.worker(client)
            except Exception:
                traceback.print_exc()

    @staticmethod
    def server_date_time():
        """
        Recupera a data do servidor.
        """
        return datetime.strftime(datetime.now(), '%a, %d/%b/%y %H:%M:%S')

    def worker(self, client):
        try:
            while True:
                json_data = client.recv(self.len_buffer).decode('utf-8')
                if json_data:
                    # Recupera as informações enviadas pelo client.
                    pdfs, input_type = self.get_pdfs(json_data)
                    print(self.server_date_time(), f'Executando o comando: {input_type}...')
                    # Faz o merge nos Pdfs.
                    result = PdfUnion(input_type, 'None', *pdfs).execute().stream
                    print(self.server_date_time(), f'Comando executado: {input_type}...')
                    # Retorna o base64 do PDF mesclado.
                    client.sendall(result.encode('utf-8'))
                    print(self.server_date_time(), f'Valor retornado: [{len(result)}]...')
                else:
                    break
        except (EOFError, ConnectionResetError):
            print(self.server_date_time(), 'Conexão encerrada com o Cliente.')

        return self

    def get_pdfs(self, json_data):
        data = json.loads(json_data)
        # Recupera o tipo de input.
        input_type = 'input_base64'
        if data.get('from_file'):
            input_type = ''
        # Recupera os PDFs em base64.
        pdfs = data.get('pdfs')
        result = [doc for doc in pdfs]
        return result, input_type


if __name__ == '__main__':
    ServerMergePdf().execute()
