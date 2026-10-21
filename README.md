\# 🛰️ Transportador CLI



Uma ferramenta de linha de comandos (CLI) leve, interativa e eficiente em Python para transferência de ficheiros e dados via sockets TCP de ponto a ponto (P2P).



\## 🚀 Funcionalidades



\- \*\*Menu Interativo:\*\* Interface amigável no terminal para fácil navegação e operação.

\- \*\*Transferência via Sockets TCP:\*\* Conexão direta e rápida entre máquinas na mesma rede ou via túnel.

\- \*\*Tratamento por Chunks:\*\* Leitura e envio de ficheiros otimizados em blocos de memória para suportar ficheiros grandes sem consumo excessivo de RAM.

\- \*\*Suporte a Argumentos de Terminal:\*\* Pode ser executado diretamente via argumentos da CLI para automações e scripts.

\- \*\*Modo Servidor e Cliente:\*\* Capacidade de aguardar conexões de entrada ou iniciar o envio/receção para um nó remoto.



\---



\## 🛠️ Requisitos



\- Python 3.8+

\- Nenhuma biblioteca externa necessária (utiliza apenas bibliotecas nativas como `socket`, `sys`, `os`, `argparse`).



\---



\## 📦 Como Usar



\### 1. Clonar o Repositório

```bash

git clone git@github.com:joeangelo21/transportador.git

cd transportador



2\. Modo Interativo



Para abrir o menu interativo, basta executar o script sem argumentos adicionais:

Bash



python transportador.py



3\. Modo Linha de Comandos (CLI)



Também podes passar parâmetros diretamente para automatizar tarefas:



&#x20;   Modo Escuta (Receber Ficheiro):

&#x20;   Bash



&#x20;   python transportador.py --listen --port 5000 --output ./ficheiro\_recebido.zip



&#x20;   Modo Envio (Enviar Ficheiro):

&#x20;   Bash



&#x20;   python transportador.py --send --host 192.168.1.10 --port 5000 --file ./meu\_ficheiro.zip



🔒 Segurança e Privacidade



O Transportador foi projetado para operações diretas P2P sem dependência de servidores de terceiros ou serviços na nuvem. Toda a transferência ocorre diretamente entre a origem e o destino configurados.

👨‍💻 Autor



Desenvolvido por Joelson Angelo (@joeangelo21).

