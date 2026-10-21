#!/usr/bin/env python3
"""
Transportador CLI - Ferramenta de Transferência de Arquivos Ponto a Ponto
Autor: Joelson Angelo (joeangelo21)
"""

import os
import socket
import tarfile
import io
import sys
import argparse

CHUNK_SIZE = 65536  # 64 KB

def modo_servidor(porta, pasta_destino="."):
    """Modo receptor: escuta conexões e recebe o pacote tar.gz."""
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', porta))
            s.listen(1)
            print(f"\n[*] Servidor aguardando conexão em 0.0.0.0:{porta}...")

            conn, addr = s.accept()
            print(f"[+] Conexão estabelecida com {addr[0]}:{addr[1]}")

            buffer = io.BytesIO()
            with conn:
                bytes_recebidos = 0
                while True:
                    dados = conn.recv(CHUNK_SIZE)
                    if not dados:
                        break
                    buffer.write(dados)
                    bytes_recebidos += len(dados)
                    print(f"\r[*] Recebendo: {bytes_recebidos / (1024*1024):.2f} MB", end="")

                print("\n[+] Transferência concluída. Extraindo arquivos...")
                buffer.seek(0)
                try:
                    with tarfile.open(fileobj=buffer, mode="r:gz") as tar:
                        tar.extractall(path=pasta_destino)
                    print(f"[+] Arquivo(s) extraído(s) com sucesso em '{os.path.abspath(pasta_destino)}'!")
                except Exception as e:
                    print(f"\n[!] Erro ao extrair pacote: {e}")

    except KeyboardInterrupt:
        print("\n[!] Servidor interrompido pelo usuário.")
    except Exception as e:
        print(f"\n[!] Erro no servidor: {e}")

def modo_cliente(arquivo_alvo, ip_destino, porta):
    """Modo emissor: compacta o alvo em memória e envia via socket."""
    if not os.path.exists(arquivo_alvo):
        print(f"\n[!] Erro: O arquivo ou pasta '{arquivo_alvo}' não existe.")
        return

    print(f"\n[*] Compactando '{arquivo_alvo}' em memória...")
    buffer = io.BytesIO()
    try:
        with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
            tar.add(arquivo_alvo, arcname=os.path.basename(arquivo_alvo))
    except Exception as e:
        print(f"[!] Erro ao compactar: {e}")
        return

    tamanho_total = buffer.tell()
    buffer.seek(0)
    print(f"[+] Pacote gerado: {tamanho_total / (1024*1024):.2f} MB")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"[*] Conectando ao destino {ip_destino}:{porta}...")
            s.connect((ip_destino, porta))
            
            bytes_enviados = 0
            while chunk := buffer.read(CHUNK_SIZE):
                s.sendall(chunk)
                bytes_enviados += len(chunk)
                progresso = (bytes_enviados / tamanho_total) * 100
                print(f"\r[*] Transportando: {progresso:.1f}% ({bytes_enviados / (1024*1024):.2f} MB)", end="")
            
            print(f"\n[+] '{arquivo_alvo}' enviado com sucesso!")

    except ConnectionRefusedError:
        print("\n[!] Erro: Conexão recusada. O servidor no IP destino está rodando e com a porta aberta?")
    except Exception as e:
        print(f"\n[!] Erro na transferência: {e}")

def menu_interativo():
    """Menu amigável via terminal quando o script é executado sem argumentos."""
    print("=" * 50)
    print("        TRANSPORTADOR DE ARQUIVOS P2P")
    print("=" * 50)
    print("[ 1 ] Enviar arquivo/pasta (Modo Cliente)")
    print("[ 2 ] Aguardar/Receber arquivo (Modo Servidor)")
    print("=" * 50)
    
    opcao = input("Escolha uma opção (1 ou 2): ").strip()

    if opcao == '1':
        alvo = input("\n[?] Qual o arquivo ou pasta para enviar?: ").strip('"\' ')
        ip = input("[?] Para qual IP você quer transportar?: ").strip()
        porta_str = input("[?] Porta de destino (Padrão 4444): ").strip()
        porta = int(porta_str) if porta_str else 4444

        if alvo and ip:
            modo_cliente(alvo, ip, porta)
        else:
            print("[!] Erro: O arquivo e o IP do destino são obrigatórios.")

    elif opcao == '2':
        porta_str = input("\n[?] Em qual porta deseja escutar? (Padrão 4444): ").strip()
        porta = int(porta_str) if porta_str else 4444
        destino = input("[?] Pasta para salvar o arquivo recebido (Padrão '.'): ").strip()
        destino = destino if destino else "."

        modo_servidor(porta, destino)
    else:
        print("[!] Opção inválida. Encerrando.")

def main():
    parser = argparse.ArgumentParser(description="Transportador CLI - Transferência de arquivos via Socket TCP")
    parser.add_argument("-l", "--listen", action="store_true", help="Ativa o modo servidor (receber)")
    parser.add_argument("-t", "--target", type=str, help="Arquivo ou pasta a ser enviada")
    parser.add_argument("-i", "--ip", type=str, help="IP do servidor de destino")
    parser.add_argument("-p", "--port", type=int, default=4444, help="Porta TCP (padrão: 4444)")
    parser.add_argument("-o", "--output", type=str, default=".", help="Pasta de saída para arquivos recebidos")

    args = parser.parse_args()

    # Se a pessoa passou argumentos via terminal (ex: -t arquivo -i 192.168.1.5)
    if args.listen:
        modo_servidor(args.port, args.output)
    elif args.target and args.ip:
        modo_cliente(args.target, args.ip, args.port)
    else:
        # Se rodou só 'python transportador.py', entra no modo interativo
        menu_interativo()

if __name__ == "__main__":
    main()