"""
Cliente de teste — use para testar qualquer um dos servidores.
Uso: python cliente.py <porta> <string>
Exemplo: python cliente.py 65432 "Hello World"
"""

import socket
import sys

HOST = '127.0.0.1'

def main():
    if len(sys.argv) < 3:
        print("Uso: python cliente.py <porta> <string>")
        print("Exemplo: python cliente.py 65432 'Hello World'")
        sys.exit(1)

    porta = int(sys.argv[1])
    mensagem = sys.argv[2]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, porta))
        s.sendall(mensagem.encode('utf-8'))
        resposta = s.recv(1024).decode('utf-8')
        print(f"Enviado  : '{mensagem}'")
        print(f"Recebido : '{resposta}'")

if __name__ == '__main__':
    main()
