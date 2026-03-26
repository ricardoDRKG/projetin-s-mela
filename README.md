# 🔄 Servidor de Inversão de String com Concorrência Controlada

**Projeto BF2 – Sistemas Concorrentes e Distribuídos**  
**Prof. Sâmela Rocha | FAINOR**

---

## 📋 Descrição

Implementação de um servidor TCP de inversão de strings em três versões progressivas, demonstrando a evolução de um servidor sequencial até um servidor concorrente com controle de recursos por semáforo.

---

## 📁 Estrutura dos Arquivos

```
projeto-bf2/
├── servidor_sequencial.py   # Q1 – Servidor TCP sequencial (1 cliente por vez)
├── servidor_concorrente.py  # Q2 – Servidor com threads (múltiplos clientes)
├── servidor_semaforo.py     # Q3 – Servidor com Semaphore (máx. 8 threads)
├── cliente.py               # Cliente TCP para testes manuais
├── teste_carga.py           # Script de carga com múltiplos clientes simultâneos
└── README.md
```

---

## ⚙️ Pré-requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa — apenas módulos da biblioteca padrão (`socket`, `threading`, `sys`, `time`)
- Funciona em Windows, Linux e macOS

Verifique sua versão do Python:
```bash
python --version
```

---

## 🚀 Como Executar

> Em todos os casos: abra **dois terminais** separados na pasta do projeto.

---

### Questão 1 — Servidor Sequencial (porta 65432)

Atende **um cliente por vez**.

**Terminal 1 – iniciar o servidor:**
```bash
python servidor_sequencial.py
```

**Terminal 2 – enviar uma string:**
```bash
python cliente.py 65432 "Hello World"
```

**Saída esperada:**
```
Enviado  : 'Hello World'
Recebido : 'dlroW olleH'
```

---

### Questão 2 — Servidor Concorrente com Threads (porta 65433)

Atende **múltiplos clientes simultaneamente**, criando uma thread por conexão.

**Terminal 1 – iniciar o servidor:**
```bash
python servidor_concorrente.py
```

**Terminal 2 – teste com cliente único:**
```bash
python cliente.py 65433 "Sistemas Distribuídos"
```

**Terminal 2 – teste de carga com 10 clientes simultâneos:**
```bash
python teste_carga.py 65433 10
```

---

### Questão 3 — Servidor com Semáforo / máx. 8 threads (porta 65434)

Igual à Q2, mas **limita a 8 threads simultâneas** usando `threading.Semaphore(8)`.

**Terminal 1 – iniciar o servidor:**
```bash
python servidor_semaforo.py
```

**Terminal 2 – teste com 12 clientes (ultrapassa o limite):**
```bash
python teste_carga.py 65434 12
```

O servidor exibirá os slots ocupados em tempo real, nunca ultrapassando 8/8:
```
[SEMÁFORO] Slots ocupados: 8/8
```

---

## 🛠️ Uso do Cliente Manual

```bash
python cliente.py <porta> "<string>"
```

| Exemplo | Comando |
|---|---|
| Testar Q1 | `python cliente.py 65432 "Python"` |
| Testar Q2 | `python cliente.py 65433 "Concorrência"` |
| Testar Q3 | `python cliente.py 65434 "Semáforo"` |

---

## 📊 Uso do Script de Carga

```bash
python teste_carga.py <porta> <numero_de_clientes>
```

| Exemplo | Comando |
|---|---|
| 10 clientes na Q2 | `python teste_carga.py 65433 10` |
| 12 clientes na Q3 | `python teste_carga.py 65434 12` |

---

## 📌 Resumo Comparativo

| Característica | Q1 – Sequencial | Q2 – Threads | Q3 – Semáforo |
|---|---|---|---|
| Clientes simultâneos | 1 | Ilimitado | Máx. 8 |
| Modelo de concorrência | Nenhum | Thread por conexão | Thread + Semaphore |
| Controle de recursos | Não | Não | Sim |
| Porta padrão | 65432 | 65433 | 65434 |

---

## 💡 Como funciona o Semáforo

O `threading.Semaphore(8)` mantém um contador interno iniciado em 8:

- **`semaforo.acquire()`** → decrementa o contador. Se já estiver em 0, a thread **bloqueia** até um slot ser liberado.
- **`semaforo.release()`** → incrementa o contador, **acordando** uma thread em espera.

Isso garante que nunca mais de 8 conexões sejam processadas ao mesmo tempo.

---

*Projeto desenvolvido para a disciplina de Sistemas Concorrentes e Distribuídos – FAINOR.*
