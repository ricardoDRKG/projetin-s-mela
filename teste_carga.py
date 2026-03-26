"""
Teste automatizado — dispara N clientes simultâneos contra um servidor.
Uso: python teste_carga.py <porta> <num_clientes>
Exemplo (Q2/Q3): python teste_carga.py 65433 12
"""

import socket
import threading
import sys
import time

HOST = '127.0.0.1'
STRINGS = [
    "Python", "Sistemas Distribuídos", "Hello World",
    "Concorrência", "Semáforo", "Thread", "Socket TCP",
    "FAINOR", "Inversão", "BF2", "Computação", "Rede"
]

resultados = []
lock = threading.Lock()

def cliente_worker(porta, idx):
    msg = STRINGS[idx % len(STRINGS)]
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, porta))
            s.sendall(msg.encode('utf-8'))
            resposta = s.recv(1024).decode('utf-8')
            ok = resposta == msg[::-1]
            with lock:
                resultados.append((idx, msg, resposta, ok))
                status = "✓" if ok else "✗"
                print(f"  [{status}] Cliente {idx:02d}: '{msg}' → '{resposta}'")
    except Exception as e:
        with lock:
            resultados.append((idx, msg, str(e), False))
            print(f"  [!] Cliente {idx:02d} ERRO: {e}")

def main():
    if len(sys.argv) < 3:
        print("Uso: python teste_carga.py <porta> <num_clientes>")
        sys.exit(1)

    porta = int(sys.argv[1])
    n = int(sys.argv[2])

    print(f"\n=== Teste de carga: {n} clientes → porta {porta} ===\n")
    inicio = time.time()

    threads = [threading.Thread(target=cliente_worker, args=(porta, i)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    fim = time.time()
    corretos = sum(1 for r in resultados if r[3])
    print(f"\n=== Resultado: {corretos}/{n} corretos | Tempo: {fim-inicio:.2f}s ===\n")

if __name__ == '__main__':
    main()
