import socket

HOST = "localhost"
PORTA = 7000  # Porta do servidor master

print("🎯 Cliente do Sistema de Arquivos Distribuídos")
print("1 - Criar Arquivo\n2 - Ler Arquivo\n3 - Editar Arquivo\n4 - Deletar Arquivo\nDigite 'sair' para encerrar.")

while True:
    operacao = input("\nEscolha a operação (1-4) ou 'sair': ").strip()
    if operacao.lower() == 'sair':
        print("👋 Encerrando cliente.")
        break

    if operacao not in ["1", "2", "3", "4"]:
        print("⚠️ Operação inválida. Escolha entre 1 e 4.")
        continue

    arquivo = input("📄 Nome do arquivo: ").strip()
    conteudo = ""
    if operacao in ["1", "3"]:
        conteudo = input("📝 Conteúdo: ").strip()

    mensagem = f"{operacao}|{arquivo}|{conteudo}"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORTA))
            s.sendall(mensagem.encode())
            resposta = s.recv(2048).decode()
            print(f"\n✅ Resposta do servidor: {resposta}")
    except ConnectionRefusedError:
        print(f"\n❌ Erro: não foi possível conectar ao servidor master em {HOST}:{PORTA}.")
        print("💡 Verifique se o servidor master está em execução.")
    except Exception as e:
        print(f"\n⚠️ Erro inesperado: {e}")
