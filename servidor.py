import socket
import threading
import os

HOST = "localhost"  # Endereço do servidor
PORT = 7000  # Porta do servidor

# Função para verificar se a porta está disponível
def porta_disponivel(porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((HOST, porta)) != 0

# Classe Servidor
class Servidor:
    def __init__(self):
        self.files = {}  # Dicionário para armazenar os arquivos na memória
        self.lock = threading.Lock()  # Para garantir a consistência das operações

    def escutar_clientes(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Servidor escutando em {HOST}:{PORT}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.tratar_conexao_cliente, args=(conn,)).start()

    def tratar_conexao_cliente(self, conn):
        with conn:
            dados = conn.recv(1024).decode()
            print(f"Requisição do cliente: {dados}")
            resposta = self.processar_requisicao(dados)
            conn.sendall(resposta.encode())

    def processar_requisicao(self, dados):
        try:
            partes = dados.split("|")
            operacao = partes[0]
            nome_arquivo = partes[1]
            conteudo = partes[2] if len(partes) > 2 else ""

            with self.lock:  # Bloquear as operações para garantir consistência
                if operacao == "1":  # Criar arquivo
                    if nome_arquivo in self.files:
                        return "Erro: Arquivo já existe."
                    self.files[nome_arquivo] = conteudo
                    return f"Arquivo '{nome_arquivo}' criado com sucesso!"

                elif operacao == "2":  # Ler arquivo
                    if nome_arquivo not in self.files:
                        return "Erro: Arquivo não encontrado."
                    return f"Conteúdo de '{nome_arquivo}': {self.files[nome_arquivo]}"

                elif operacao == "3":  # Editar arquivo
                    if nome_arquivo not in self.files:
                        return "Erro: Arquivo não encontrado."
                    self.files[nome_arquivo] = conteudo
                    return f"Arquivo '{nome_arquivo}' editado com sucesso!"

                elif operacao == "4":  # Excluir arquivo
                    if nome_arquivo not in self.files:
                        return "Erro: Arquivo não encontrado."
                    del self.files[nome_arquivo]
                    return f"Arquivo '{nome_arquivo}' excluído com sucesso!"

                else:
                    return "Erro: Operação desconhecida."
        except Exception as e:
            return f"Erro ao processar requisição: {str(e)}"


if __name__ == "__main__":
    servidor = Servidor()
    servidor.escutar_clientes()
