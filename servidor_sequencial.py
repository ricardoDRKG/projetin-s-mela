"""
Questão 1 – Servidor Socket Sequencial
Servidor TCP que recebe uma string e devolve invertida.
Atende um cliente por vez.
"""

import socket

HOST = '127.0.0.1'
PORT = 65432

def inverter_string(s: str) -> str:
    return s[::-1]

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()
        print(f"[SEQUENCIAL] Servidor ouvindo em {HOST}:{PORT}")

        while True:
            conn, addr = servidor.accept()
            with conn:
                print(f"[SEQUENCIAL] Cliente conectado: {addr}")
                dados = conn.recv(1024).decode('utf-8').strip()
                if dados:
                    invertido = inverter_string(dados)
                    print(f"[SEQUENCIAL] Recebido: '{dados}' → Enviando: '{invertido}'")
                    conn.sendall(invertido.encode('utf-8'))

if __name__ == '__main__':
    main()
