import socket
import threading
import argparse

HOST = "localhost"
WORKER_BASE_PORT = 9000

class Worker:
    def __init__(self, id):
        self.porta = WORKER_BASE_PORT + id
        print(f"🔧 Worker {id} escutando na porta {self.porta}")
        threading.Thread(target=self.escutar_master, daemon=True).start()

    def escutar_master(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, self.porta))
            s.listen()
            while True:
                conn, _ = s.accept()
                threading.Thread(target=self.tratar_requisicao, args=(conn,), daemon=True).start()

    def tratar_requisicao(self, conn):
        with conn:
            dados = conn.recv(2048).decode()
            print(f"📥 Comando recebido: {dados}")
            partes = dados.split("|")
            operacao = partes[0]
            arquivo = partes[1]
            conteudo = partes[2] if len(partes) > 2 else ""

            if operacao == "1":
                resposta = f"Arquivo '{arquivo}' criado com conteúdo: {conteudo}"
            elif operacao == "2":
                resposta = f"Conteúdo do arquivo '{arquivo}' (simulado)"
            elif operacao == "3":
                resposta = f"Arquivo '{arquivo}' editado: {conteudo}"
            elif operacao == "4":
                resposta = f"Arquivo '{arquivo}' deletado"
            else:
                resposta = "⚠️ Operação desconhecida"

            conn.sendall(resposta.encode())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    args = parser.parse_args()
    Worker(args.id)
    input("Pressione Enter para sair...\n")
