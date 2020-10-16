import json
import socket

HOST = '127.0.0.1'
PORT = 8777

with open('pdf_base64.txt', 'r') as f:
    lines = f.readlines()
    f.close()

pdfs = {'pdfs': [lines[0], lines[0]]}
pdfs_json = json.dumps(pdfs)

len_buffer = 10 ** 9

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(pdfs_json.encode('utf-8'))
    data = s.recv(len_buffer).decode('utf-8')

print('Recebido', len(data))
