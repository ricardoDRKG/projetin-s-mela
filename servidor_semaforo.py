"""
Questão 3 – Servidor Concorrente com Semáforo (máx. 8 threads)
Igual ao servidor da Q2, mas usa threading.Semaphore(8) para limitar
o número de threads executando simultaneamente a no máximo 8.
"""

import socket
import threading

HOST = '127.0.0.1'
PORT = 65434
MAX_THREADS = 8

semaforo = threading.Semaphore(MAX_THREADS)

def inverter_string(s: str) -> str:
    return s[::-1]

def handle_client(conn, addr):
    semaforo.acquire()
    try:
        with conn:
            ativas = MAX_THREADS - semaforo._value
            print(f"[SEMÁFORO] Cliente: {addr} | Thread: {threading.current_thread().name} "
                  f"| Slots ocupados: {ativas}/{MAX_THREADS}")
            dados = conn.recv(1024).decode('utf-8').strip()
            if dados:
                invertido = inverter_string(dados)
                print(f"[SEMÁFORO] '{dados}' → '{invertido}' | {addr}")
                conn.sendall(invertido.encode('utf-8'))
        print(f"[SEMÁFORO] Conexão encerrada: {addr}")
    finally:
        semaforo.release()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()
        print(f"[SEMÁFORO] Servidor ouvindo em {HOST}:{PORT} | Limite: {MAX_THREADS} threads")

        while True:
            conn, addr = servidor.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

if __name__ == '__main__':
    main()
