README.md


#🗂️ Sistema de Arquivos Distribuído

Este projeto é um sistema de arquivos distribuído simples desenvolvido em Python com `sockets`, utilizando uma arquitetura com:

- Cliente (interface de terminal);
- Servidor Master com interface gráfica (Tkinter);
- Vários Workers responsáveis por armazenar e manipular os dados.

___🎯 Objetivo

Simular um sistema de arquivos distribuído no qual os clientes podem **criar, ler, editar e deletar arquivos**, com as requisições sendo encaminhadas por um servidor **master** para **workers**, que realizam as operações.

___🧱 Componentes

- `cliente.py` — Interface de linha de comando onde o usuário escolhe a operação (criar, ler, editar, deletar).
- `master_gui.py` — Interface gráfica do servidor Master (usando Tkinter).
- `master.py` — Lógica do servidor Master: recebe requisições dos clientes e repassa para os Workers disponíveis.
- `worker.py` — Código de cada Worker, que realiza as operações solicitadas.
- `servidor_simples.py` — Versão alternativa de servidor único (pode ser usada para testes sem workers).

-▶️ Como executar

1. Inicie os Workers** (cada um com um ID diferente):

python worker.py --id 0
python worker.py --id 1
python worker.py --id 2


2.__Inicie o Master com interface gráfica**:

python master_gui.py

3. Execute o Cliente para interagir com o sistema**:

python cliente.py

📦 Funcionalidades suportadas

* `1` - Criar Arquivo
* `2` - Ler Arquivo
* `3` - Editar Arquivo
* `4` - Deletar Arquivo

🛠️ Requisitos

* Python 3.x
* Bibliotecas padrão (`socket`, `threading`, `tkinter`, `argparse`)

📌 Observações

* A escolha do Worker é feita em round-robin.
* Os arquivos são mantidos em memória (não há persistência em disco).
* As mensagens seguem o formato: `operacao|nome_arquivo|conteudo`


📁 Exemplo de estrutura

distributed-filesystem/
├── cliente.py
├── master.py
├── master_gui.py
├── worker.py
├── servidor_simples.py
└── README.md

✨ Autor

Bonifácio ([@Bonifacio258](https://github.com/Bonifacio258))

📨 Whatsapp: +55 85 996184471
📨 Instagram: https://www.instagram.com/twocent_258?
