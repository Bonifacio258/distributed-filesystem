import socket
import threading

HOST = "localhost"
PORTA = 7000
WORKER_BASE_PORT = 9000
workers_disponiveis = [9000, 9001, 9002]
prox_worker = 0

class Master:
    def __init__(self, log_callback=None):
        self.log_callback = log_callback
        self.thread = threading.Thread(target=self.escutar_clientes, daemon=True)
        self.thread.start()
        self.log(f"🧠 Master iniciado na porta {PORTA}")

    def escutar_clientes(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORTA))
            s.listen()
            self.log(f"🎧 Aguardando clientes em {PORTA}...")
            while True:
                conn, addr = s.accept()
                self.log(f"📞 Conexão de {addr}")
                threading.Thread(target=self.tratar_cliente, args=(conn,), daemon=True).start()

    def tratar_cliente(self, conn):
        global prox_worker
        with conn:
            dados = conn.recv(1024).decode()
            self.log(f"📩 Requisição recebida: {dados}")

            partes = dados.split("|")
            if len(partes) < 2:
                conn.sendall("❌ Requisição malformada".encode())
                return

            operacao = partes[0]
            arquivo = partes[1]

            # AUTORIZAÇÃO AUTOMÁTICA PARA INTERFACE GRÁFICA
            autorizado = True  # você pode mudar isso se quiser autorizações manuais em outra interface

            if not autorizado:
                conn.sendall("⛔ Operação negada.".encode())
                return

            if not workers_disponiveis:
                conn.sendall("🚫 Nenhum worker disponível.".encode())
                return

            worker_port = workers_disponiveis[prox_worker % len(workers_disponiveis)]
            prox_worker += 1

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ws:
                    ws.settimeout(3)
                    ws.connect((HOST, worker_port))
                    ws.sendall(dados.encode())
                    resposta = ws.recv(2048).decode()
                    conn.sendall(f"✅ Operação realizada: {resposta}".encode())
                    self.log(f"📤 Resposta do worker {worker_port}: {resposta}")
            except Exception as e:
                erro_msg = f"💥 Erro ao contactar worker {worker_port}: {e}"
                self.log(erro_msg)
                conn.sendall(erro_msg.encode())

    def log(self, mensagem):
        print(mensagem)
        if self.log_callback:
            self.log_callback(mensagem)
