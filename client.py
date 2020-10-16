import json
import socket

HOST = '127.0.0.1'
PORT = 8777

with open('pdf_base64.txt', 'r') as f:
    lines = f.readlines()
    f.close()

# prepara para enviar 5 vezes o pdf de teste.
pdfs = {'pdfs': [lines[0] for x in range(5)]}
# cria o jason de envio.
pdfs_json = json.dumps(pdfs)

# informa o tamanho do buffer.
len_buffer = 10 ** 9

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # Envia os pdfs.
    s.sendall(pdfs_json.encode('utf-8'))
    # Aguarda retorno da mesclagem.
    data = s.recv(len_buffer).decode('utf-8')

# Imprime o tamanho do pdf mesclado.
print('Recebido', len(data))
