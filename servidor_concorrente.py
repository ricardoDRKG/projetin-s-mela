"""
Questão 2 – Servidor Concorrente com Threads
Uma thread por conexão — múltiplos clientes simultâneos.
"""

import socket
import threading

HOST = '127.0.0.1'
PORT = 65433

def inverter_string(s: str) -> str:
    return s[::-1]

def handle_client(conn, addr):
    with conn:
        print(f"[THREAD] Cliente conectado: {addr} | Thread: {threading.current_thread().name}")
        dados = conn.recv(1024).decode('utf-8').strip()
        if dados:
            invertido = inverter_string(dados)
            print(f"[THREAD] '{dados}' → '{invertido}' | {addr}")
            conn.sendall(invertido.encode('utf-8'))
    print(f"[THREAD] Conexão encerrada: {addr}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()
        print(f"[CONCORRENTE] Servidor ouvindo em {HOST}:{PORT}")

        while True:
            conn, addr = servidor.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
            print(f"[CONCORRENTE] Threads ativas: {threading.active_count() - 1}")

if __name__ == '__main__':
    main()
